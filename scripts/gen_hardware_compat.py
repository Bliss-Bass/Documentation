#!/usr/bin/env python3
"""Generate public x86 hardware compatibility docs from Mesa PCI IDs + linuxhw/DMI.

Outputs:
  data/hardware/linuxhw_paths.txt   (cached path inventory)
  data/hardware/oem_devices.json    (per-brand / industrial model inventory)
  data/hardware/oem_summary.json    (pie + totals for charts)
  data/hardware/pos_brands.json     (POS/panel catalog vs linuxhw presence)
  data/hardware/compat.json         (Mesa + catalog + summary refs)
  Installation/x86_64-v2/hardware-compatibility.md
  Installation/x86_64-v2/_generated_hardware_compat.md

Usage:
  python3 scripts/gen_hardware_compat.py
  python3 scripts/gen_hardware_compat.py --refresh-linuxhw
  python3 scripts/gen_hardware_compat.py --mesa /path/to/mesa3d
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    sys.stderr.write("PyYAML required: pip install pyyaml\n")
    raise SystemExit(1) from exc

DOC_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MESA = Path(
    "/bbd016/los-23.2-tablet-x86-20260702/aosp-workspace/external/mesa3d"
)
PCI_IDS_SUBDIR = Path("include/pci_ids")
DEFAULT_LINUXHW_CLONE = Path("/tmp/linuxhw-dmi")
LINUXHW_REPO = "https://github.com/linuxhw/DMI.git"
LINUXHW_CACHE_MAX_AGE_DAYS = 14

# CHIPSET(id, enum, "family", "name")  — iris / crocus style
CHIPSET_4 = re.compile(
    r'CHIPSET\s*\(\s*(0x[0-9a-fA-F]+)\s*,\s*([^,\)]+)\s*,\s*"([^"]*)"\s*,\s*"([^"]*)"\s*\)'
)
# CHIPSET(id, enum, "name")  — i915 style
CHIPSET_3 = re.compile(
    r'CHIPSET\s*\(\s*(0x[0-9a-fA-F]+)\s*,\s*([^,\)]+)\s*,\s*"([^"]*)"\s*\)'
)
# CHIPSET(id, FAMILY)  — radeonsi style
CHIPSET_2 = re.compile(
    r'CHIPSET\s*\(\s*(0x[0-9a-fA-F]+)\s*,\s*([A-Za-z0-9_]+)\s*\)'
)

DRIVER_META = {
    "iris": {
        "vendor": "Intel",
        "driver": "iris",
        "status": "supported",
        "gpu_class": "intel_igpu",
        "source": "iris_pci_ids.h",
    },
    "i915": {
        "vendor": "Intel",
        "driver": "i915",
        "status": "supported_caveat",
        "gpu_class": "intel_igpu",
        "source": "i915_pci_ids.h",
    },
    "crocus": {
        "vendor": "Intel",
        "driver": "crocus",
        "status": "supported_caveat",
        "gpu_class": "intel_igpu",
        "source": "crocus_pci_ids.h",
    },
    "radeonsi": {
        "vendor": "AMD",
        "driver": "radeonsi",
        "status": "supported_caveat",
        "gpu_class": "amd_igpu",
        "source": "radeonsi_pci_ids.h",
    },
}

STATUS_LABEL = {
    "supported": "Supported",
    "caveat": "Caveat",
    "supported_caveat": "Supported with caveats",
    "unsupported": "Unsupported",
    "supported_likely": "Likely supported",
    "avoid": "Avoid (gaming / NVIDIA lines)",
}

# Canonical brand -> DMI vendor name aliases (matched case-insensitively)
NAME_BRAND_ALIASES: dict[str, list[str]] = {
    "HP": ["hewlett-packard", "hp", "hewlett packard"],
    "Dell": ["dell", "dell inc.", "dell inc", "dellinc.", "dell system", "dell emc"],
    "Asus": ["asustek computer", "asustek", "asus", "asusTek computer"],
    "Acer": ["acer", "acer inc.", "acer incorporated"],
    "Lenovo": ["lenovo", "lenovo product"],
    "Framework": ["framework"],
    "Star Labs": ["star labs", "starlabs", "starlabsystems"],
}

# Vendors that appear in linuxhw/DMI and fit Industrial / POS / Panel / white-label mini-PC ODM.
# Matched as case-insensitive equality OR substring of the DMI vendor field.
# Board OEMs (MSI/Gigabyte/ASRock) and bare "Intel" motherboards live in OTHER_X86 instead.
# Short tokens (iei, elo, partner, …) use word-boundary / equality — see _SHORT_VENDOR_EXACT.
INDUSTRIAL_VENDOR_NEEDLES: list[str] = [
    "advantech",
    "axiomtek",
    "aaeon",
    "adlink",
    "adlinktech",
    "posiflex",
    "elo touch solutions",
    "elo touch",
    "faytech",
    "panasonic connect",
    "panasonic",
    "siemens",  # exact/starts only; never Fujitsu Siemens — see is_industrial_vendor
    "touch dynamic",
    "touch dynamics",
    "partner",  # exact/starts only (Partner Tech POS) — short-exact
    "flytech",
    "senor",
    "sam4s",
    "kontron",
    "shuttle",
    "minisforum",
    "nexcom",
    "onlogic",
    "cincoze",
    "neousys",
    "vecow",
    "portwell",
    "dfi",
    "seco",
    "congatec",
    "winmate",
    "jetway",
    "aopen",
    "asrock industrial",
    "ruggedpc",
    "wyse",
    "igel technology",
    "beckhoff",
    "lanner",
    "rtd embedded",
    "chuwi",
    "beelink",
    "minix",
    "lattepanda",
    "icp-iei",
    "iei",
    "tangent computer",
    "wearnes",
    "cake",  # POS tablet path
    # White-label / mini-PC ODMs commonly rebadged under many retail names
    "azw",
    "zotac",
    "gmktec",
    "trigkey",
    "besstar",
    "intel client systems",
    "getac",
    "teclast",
    "compulab",
    "atopnuc",
    "awow",
    "xplore",
    "hampoo",
    "arbor",
    "reachingtech",
    "fanless mini pc",
]

# Keyword match on type/prefix/model (not vendor alone). Avoid "Positivo" false POS hits.
INDUSTRIAL_NAME_KEYWORDS = (
    "panel pc",
    "panelpc",
    "panel-pc",
    "industrial",
    "kiosk",
    "embedded",
    "digital signage",
    "signage player",
    "thin client",
    "thinclient",
    "rugged",
    "box pc",
    "boxpc",
    "fanless",
    "pos terminal",
    "pos system",
    "poslab",
    "toughbook",
    "toughpad",
)

# Notable board / chassis ODMs, Linux OEMs, and white-label DMI strings that are
# not Industrial/POS but still useful for x86 inventory (long tail of the tree).
# Do not dump every unknown vendor here — curated needles only.
OTHER_X86_VENDOR_NEEDLES: list[str] = [
    "gigabyte",
    "msi",
    "micro-star",
    "asrock",  # plain ASRock boards; "ASRock Industrial" already industrial
    "asrockrack",
    "biostar",
    "ecs",
    "foxconn",
    "pegatron",
    "clevo",
    "quanta",
    "compal",
    "wistron",
    "inventec",
    "system76",
    "tuxedo",
    "supermicro",
    "huanan",
    "machinist",
    "maxsun",
    "colorful",
    "evga",
    "abit",
    "tyan",
    "wortmann",
    "pc specialist",
    "mechrevo",
    "tongfang",
    "american megatrends",
    "ami",
    "micro computer (hk)",
    "intel",  # bare Intel boards / remaining NUCs after Intel Client Systems
    "oem",
]

_OTHER_X86_SHORT_EXACT = {
    "msi",
    "ecs",
    "ami",
    "oem",
    "abit",
    "tyan",
    "evga",
}

# Gaming / discrete-NVIDIA naming heuristics (case-insensitive substring).
AVOID_PATTERNS = (
    "alienware",
    "legion",
    " loq",
    "loq ",
    "loq-",
    "/loq",
    "rog ",
    "rog-",
    "/rog",
    "strix",
    "tuf gaming",
    "tuf-",
    "omen",
    "victus",
    "nitro",
    "predator",
    "geforce",
    " rtx",
    "rtx ",
    "gtx ",
    "g15",
    "g16",
    "g14",
    "g17",
    "g18",
    "zephyrus",
    "helios",
    "triton",
    "aurora",
    "stealth",
    "katana",
    "scar ",
    "flow x",
    "flow z",
    "razer blade",
    "quadro",  # often discrete workstation NVIDIA
)

FORM_FACTOR_ORDER = [
    "Notebook",
    "Desktop",
    "Convertible",
    "Mini PC",
    "All-in-One",
    "Tablet",
    "Server",
    "Stick PC",
    "System On Chip",
    "Firewall",
]


def parse_chipsets(path: Path, driver_key: str) -> list[dict]:
    """Parse CHIPSET macros from a Mesa pci_ids header."""
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    meta = DRIVER_META[driver_key]
    chips: list[dict] = []
    seen: set[str] = set()

    for m in CHIPSET_4.finditer(text):
        chip_id = m.group(1).lower()
        if chip_id in seen:
            continue
        seen.add(chip_id)
        family = m.group(3).strip() or m.group(2).strip()
        chips.append(
            {
                "id": chip_id,
                "enum": m.group(2).strip(),
                "family": family,
                "name": m.group(4).strip(),
                **meta,
            }
        )

    remainder = CHIPSET_4.sub("", text)
    for m in CHIPSET_3.finditer(remainder):
        chip_id = m.group(1).lower()
        if chip_id in seen:
            continue
        seen.add(chip_id)
        enum = m.group(2).strip()
        name = m.group(3).strip()
        chips.append(
            {
                "id": chip_id,
                "enum": enum,
                "family": enum,
                "name": name,
                **meta,
            }
        )

    remainder2 = CHIPSET_3.sub("", remainder)
    for m in CHIPSET_2.finditer(remainder2):
        chip_id = m.group(1).lower()
        if chip_id in seen:
            continue
        seen.add(chip_id)
        family = m.group(2).strip()
        chips.append(
            {
                "id": chip_id,
                "enum": family,
                "family": family,
                "name": family,
                **meta,
            }
        )

    return chips


def collect_mesa(mesa_root: Path) -> dict:
    pci_dir = mesa_root / PCI_IDS_SUBDIR
    drivers = {}
    all_chips: list[dict] = []
    family_counts: dict[str, Counter] = defaultdict(Counter)

    for key, filename in (
        ("iris", "iris_pci_ids.h"),
        ("i915", "i915_pci_ids.h"),
        ("crocus", "crocus_pci_ids.h"),
        ("radeonsi", "radeonsi_pci_ids.h"),
    ):
        path = pci_dir / filename
        chips = parse_chipsets(path, key)
        drivers[key] = {
            "file": filename,
            "present": path.is_file(),
            "chip_count": len(chips),
            "status": DRIVER_META[key]["status"],
            "families": sorted({c["family"] for c in chips if c.get("family")}),
        }
        for c in chips:
            family_counts[key][c["family"]] += 1
        all_chips.extend(chips)

    nvidia = {
        "status": "unsupported",
        "policy": (
            "Discrete NVIDIA GPUs are not classified as supported. "
            "Bass ships Nouveau only; there is no proprietary NVIDIA driver. "
            "Treat GeForce / RTX dGPU systems as unsupported for production."
        ),
        "parsed_as_supported": False,
    }

    return {
        "mesa_root": str(mesa_root),
        "pci_ids_dir": str(pci_dir),
        "drivers": drivers,
        "family_counts": {k: dict(v) for k, v in family_counts.items()},
        "chips": all_chips,
        "nvidia": nvidia,
        "summary": {
            "intel_iris_chips": drivers["iris"]["chip_count"],
            "intel_iris_families": len(drivers["iris"]["families"]),
            "intel_i915_chips": drivers["i915"]["chip_count"],
            "intel_crocus_chips": drivers["crocus"]["chip_count"],
            "amd_radeonsi_chips": drivers["radeonsi"]["chip_count"],
            "amd_radeonsi_families": len(drivers["radeonsi"]["families"]),
            "total_open_chips_parsed": len(all_chips),
        },
    }


def load_oem_catalog(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def brand_best_avoid(brand_block: dict) -> tuple[str, str, str]:
    """Return (best_fit, avoid, overall_status_label) for curated guidance."""
    best: list[str] = []
    avoid: list[str] = []
    statuses: set[str] = set()
    for e in brand_block.get("entries", []):
        statuses.add(e["status"])
        if e["status"] in ("supported", "caveat"):
            best.append(e["series"])
        else:
            avoid.append(e["series"])
    if statuses == {"supported"}:
        overall = "Usually fine"
    elif "unsupported" in statuses and (statuses & {"supported", "caveat"}):
        overall = "Mixed: prefer Intel or AMD built-in graphics"
    elif statuses <= {"caveat", "supported"} and "caveat" in statuses:
        overall = "Usually fine; double-check the model"
    else:
        overall = "See brand notes"
    return (
        "; ".join(best) if best else "(none listed)",
        "; ".join(avoid) if avoid else "(none listed)",
        overall,
    )


def plain(text: str) -> str:
    """Normalize copy for docs: no em/en dashes, ellipses, arrows, or math signs."""
    if not text:
        return ""
    out = str(text)
    for old, new in (
        ("\u2014", " - "),  # em dash
        ("\u2013", "-"),  # en dash
        ("\u2212", "-"),  # minus
        ("\u2026", "..."),
        ("\u2192", " -> "),
        ("\u2190", " <- "),
        ("\u2260", " is not "),
        ("\u00a0", " "),
        ("—", " - "),
        ("–", "-"),
        ("…", "..."),
        ("→", " -> "),
        ("←", " <- "),
        ("≠", " is not "),
    ):
        out = out.replace(old, new)
    out = re.sub(r"[ \t]+", " ", out)
    return out.strip()


def md_escape(text: str) -> str:
    return plain(text).replace("|", "\\|")


def _empty_cell(text: str | None) -> str:
    t = plain(text or "")
    return t if t else "-"


def normalize_form_factor(raw: str) -> str | None:
    """Normalize DMI top-level type; drop junk / README paths."""
    t = raw.strip().strip('"')
    if not t or t in ("README.md", "LICENSE"):
        return None
    mapping = {
        "All In One": "All-in-One",
        "Mini Pc": "Mini PC",
        "Stick Pc": "Stick PC",
        "System On Chip": "System On Chip",
        "Notebook": "Notebook",
        "Desktop": "Desktop",
        "Convertible": "Convertible",
        "Tablet": "Tablet",
        "Server": "Server",
        "Firewall": "Firewall",
    }
    return mapping.get(t, t)


def build_vendor_alias_map() -> dict[str, str]:
    out: dict[str, str] = {}
    for brand, aliases in NAME_BRAND_ALIASES.items():
        for a in aliases:
            out[a.lower()] = brand
    return out


def classify_support(prefix: str, model: str) -> str:
    blob = f" {prefix} {model} ".lower()
    for pat in AVOID_PATTERNS:
        if pat in blob:
            return "avoid"
    return "supported_likely"


# Short tokens that must not match as bare substrings
# (e.g. "seco" in MouseComputer, "ocom" in computer, "elo" inside longer words).
_SHORT_VENDOR_EXACT = {
    "iei",
    "elo",
    "ocom",
    "partner",
    "senor",
    "licon",
    "icp-iei",
    "dfi",
    "seco",
    "wyse",
    "cake",
    "aopen",
    "jetway",
    "kontron",
    "nexcom",
    "onlogic",
    "cincoze",
    "vecow",
    "portwell",
    "winmate",
    "lanner",
    "adlink",
    "adlinktech",
    "aaeon",
    "posiflex",
    "advantech",
    "axiomtek",
    "chuwi",
    "beelink",
    "minix",
    "shuttle",
    "ruggedpc",
    "lattepanda",
    "minisforum",
    "congatec",
    "azw",
    "gmk",
    "awow",
    "arbor",
    "flytech",
    "sam4s",
    "faytech",
}


def _needle_word_boundary(vendor: str, needle: str) -> bool:
    """True if needle equals vendor, or matches a whole token (space/./-/_ bound)."""
    vl = vendor.lower().strip()
    n = needle.lower().strip()
    if not n:
        return False
    if vl == n:
        return True
    if vl.startswith(n + " ") or vl.startswith(n + ".") or vl.startswith(n + "-"):
        return True
    if vl.startswith(n + "_"):
        return True
    # starts with needle then non-alpha (e.g. "iei,", "elo/")
    if vl.startswith(n) and len(vl) > len(n) and not vl[len(n)].isalpha():
        return True
    tokens = re.split(r"[\s.\-_/]+", vl)
    return n in tokens


def _vendor_needle_match(vendor: str, needles: list[str], short_exact: set[str]) -> bool:
    vl = vendor.lower().strip()
    if not vl:
        return False
    for needle in needles:
        n = needle.lower().strip()
        if not n:
            continue
        # Short tokens or listed shorts: word-boundary / equality only
        if len(n) < 5 or n in short_exact:
            if _needle_word_boundary(vl, n):
                return True
            continue
        if n in vl:
            return True
    return False


def is_industrial_vendor(vendor: str) -> bool:
    vl = vendor.lower().strip()
    # Siemens: exact / starts with Siemens — never Fujitsu Siemens
    if "siemens" in vl:
        if "fujitsu" in vl:
            return False
        if vl == "siemens" or vl.startswith("siemens ") or vl.startswith("siemens."):
            return True
        return False
    # Partner Tech POS: vendor must start with Partner (not "IT Partner" / "PC Partner")
    if vl == "partner" or vl.startswith("partner ") or vl.startswith("partner-"):
        return True
    if vl.startswith("partner tech"):
        return True
    # Skip "partner" in the general needle list (handled above)
    needles = [n for n in INDUSTRIAL_VENDOR_NEEDLES if n != "partner"]
    shorts = _SHORT_VENDOR_EXACT - {"partner"}
    return _vendor_needle_match(vendor, needles, shorts)


def is_industrial_by_name(typ: str, prefix: str, model: str, vendor: str) -> bool:
    if vendor.lower().startswith("positivo"):
        return False
    blob = f"{typ} {prefix} {model}".lower()
    return any(k in blob for k in INDUSTRIAL_NAME_KEYWORDS)


def is_toshiba_industrial(vendor: str, typ: str, prefix: str, model: str) -> bool:
    """Toshiba only when industrial keyword OR Toughbook/Toughpad in name."""
    vl = vendor.lower().strip()
    if not (vl == "toshiba" or vl.startswith("toshiba ")):
        return False
    blob = f"{typ} {prefix} {model}".lower()
    if "toughbook" in blob or "toughpad" in blob:
        return True
    return any(k in blob for k in INDUSTRIAL_NAME_KEYWORDS)


def is_intel_nuc_line(vendor: str, prefix: str, model: str) -> bool:
    """Bare 'Intel' DMI often mixes NUCs with motherboards — pull NUC-named lines into industrial."""
    vl = vendor.lower().strip()
    if not (vl == "intel" or vl.startswith("intel ")):
        return False
    if "client systems" in vl:
        return False  # handled as industrial vendor needle
    blob = f"{prefix} {model}".lower()
    return "nuc" in blob


def is_other_x86_vendor(vendor: str) -> bool:
    vl = vendor.lower().strip()
    # Prefer industrial classification for ASRock Industrial / Intel Client Systems.
    if is_industrial_vendor(vendor):
        return False
    # Plain ASRock (not Industrial) stays in OTHER_X86
    shorts = _OTHER_X86_SHORT_EXACT | {"msi", "ecs", "oem", "ami"}
    return _vendor_needle_match(vendor, OTHER_X86_VENDOR_NEEDLES, shorts)


def cache_is_fresh(path: Path, max_age_days: int = LINUXHW_CACHE_MAX_AGE_DAYS) -> bool:
    if not path.is_file() or path.stat().st_size < 1000:
        return False
    age = datetime.now(timezone.utc).timestamp() - path.stat().st_mtime
    return age < max_age_days * 86400


def fetch_linuxhw_paths(
    cache_path: Path,
    clone_dir: Path,
    refresh: bool,
) -> Path:
    """Ensure linuxhw path list exists; refresh via sparse blobless clone if needed."""
    if not refresh and cache_is_fresh(cache_path):
        print(f"Reusing cached linuxhw paths: {cache_path}")
        return cache_path

    clone_dir = clone_dir.resolve()
    need_clone = refresh or not (clone_dir / ".git").is_dir()
    if need_clone:
        if clone_dir.exists():
            subprocess.run(["rm", "-rf", str(clone_dir)], check=True)
        print(f"Sparse-cloning {LINUXHW_REPO} -> {clone_dir}")
        subprocess.run(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--sparse",
                "--depth",
                "1",
                LINUXHW_REPO,
                str(clone_dir),
            ],
            check=True,
        )
    else:
        print(f"Reusing existing clone: {clone_dir}")

    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD"],
        cwd=clone_dir,
        check=True,
        capture_output=True,
        text=True,
    )
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(result.stdout, encoding="utf-8")
    print(f"Wrote {cache_path} ({len(result.stdout.splitlines())} paths)")
    return cache_path


def _summarize_vendor_segment(
    models: dict[tuple, dict],
    segment_tag: str,
) -> dict:
    """Aggregate unique models into totals + per-vendor ranking for a segment."""
    status_counts: Counter = Counter()
    form_unique: dict[str, set] = defaultdict(set)
    prefix_counts: Counter = Counter()
    by_vendor_models: dict[str, dict[tuple, dict]] = defaultdict(dict)
    for key, meta in models.items():
        status_counts[meta["status"]] += 1
        form_unique[meta["type"]].add((meta["prefix"], meta["model"]))
        prefix_counts[meta["prefix"]] += 1
        by_vendor_models[meta["vendor"]][key] = meta

    vendors_ranked = []
    for vendor, vmodels in sorted(
        by_vendor_models.items(), key=lambda x: -len(x[1])
    ):
        vs = Counter(m["status"] for m in vmodels.values())
        vf: dict[str, set] = defaultdict(set)
        for m in vmodels.values():
            vf[m["type"]].add((m["prefix"], m["model"]))
        vendors_ranked.append(
            {
                "vendor": vendor,
                "models": len(vmodels),
                "supported_likely": vs.get("supported_likely", 0),
                "avoid": vs.get("avoid", 0),
                "form_factors": {
                    t: len(s)
                    for t, s in sorted(vf.items(), key=lambda x: -len(x[1]))
                },
            }
        )

    return {
        "models": len(models),
        "supported_likely": status_counts.get("supported_likely", 0),
        "avoid": status_counts.get("avoid", 0),
        "form_factors": {
            t: len(s)
            for t, s in sorted(form_unique.items(), key=lambda x: -len(x[1]))
        },
        "top_prefixes": [
            {"prefix": p, "models": c}
            for p, c in prefix_counts.most_common(12)
        ],
        "top_vendors": vendors_ranked[:40],
        "vendors": vendors_ranked,
        "devices": [
            models[k]
            for k in sorted(models, key=lambda x: (x[0], x[1], x[2], x[3]))
        ],
        "segment": segment_tag,
    }


def ingest_linuxhw(paths_file: Path) -> dict:
    """Parse DMI paths into unique models for name brands + industrial + other ODMs."""
    alias_map = build_vendor_alias_map()
    # key: (type, vendor, prefix, model) -> meta
    name_models: dict[str, dict[tuple, dict]] = {b: {} for b in NAME_BRAND_ALIASES}
    industrial_models: dict[tuple, dict] = {}
    other_x86_models: dict[tuple, dict] = {}
    all_form_factors: Counter = Counter()
    path_rows = 0
    skipped = 0

    for line in paths_file.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("/")
        if len(parts) != 5:
            skipped += 1
            continue
        raw_type, vendor, prefix, model, _hwid = parts
        typ = normalize_form_factor(raw_type)
        if typ is None:
            skipped += 1
            continue
        path_rows += 1
        all_form_factors[typ] += 1  # path-level; unique counts computed later

        key = (typ, vendor, prefix, model)
        status = classify_support(prefix, model)
        brand = alias_map.get(vendor.lower())
        if brand:
            if key not in name_models[brand]:
                name_models[brand][key] = {
                    "type": typ,
                    "vendor": vendor,
                    "prefix": prefix,
                    "model": model,
                    "status": status,
                    "segment": "name_brand",
                    "brand": brand,
                }
            continue

        if (
            is_industrial_vendor(vendor)
            or is_toshiba_industrial(vendor, typ, prefix, model)
            or is_industrial_by_name(typ, prefix, model, vendor)
            or is_intel_nuc_line(vendor, prefix, model)
        ):
            if key not in industrial_models:
                industrial_models[key] = {
                    "type": typ,
                    "vendor": vendor,
                    "prefix": prefix,
                    "model": model,
                    "status": status,
                    "segment": "industrial_pos_odm",
                }
            continue

        if is_other_x86_vendor(vendor):
            if key not in other_x86_models:
                other_x86_models[key] = {
                    "type": typ,
                    "vendor": vendor,
                    "prefix": prefix,
                    "model": model,
                    "status": status,
                    "segment": "other_x86_odm",
                }

    def summarize_brand(brand: str, models: dict[tuple, dict]) -> dict:
        status_counts: Counter = Counter()
        form_unique: dict[str, set] = defaultdict(set)
        prefix_counts: Counter = Counter()
        devices = []
        for key, meta in sorted(models.items(), key=lambda x: (x[0][0], x[0][2], x[0][3])):
            status_counts[meta["status"]] += 1
            form_unique[meta["type"]].add((meta["prefix"], meta["model"]))
            prefix_counts[meta["prefix"]] += 1
            devices.append(meta)
        form_factors = {
            t: len(s)
            for t, s in sorted(form_unique.items(), key=lambda x: (-len(x[1]), x[0]))
        }
        top_prefixes = [
            {"prefix": p, "models": c}
            for p, c in prefix_counts.most_common(12)
        ]
        top_forms = [
            f"{t} ({n})"
            for t, n in list(form_factors.items())[:4]
        ]
        return {
            "brand": brand,
            "models": len(models),
            "supported_likely": status_counts.get("supported_likely", 0),
            "avoid": status_counts.get("avoid", 0),
            "form_factors": form_factors,
            "top_form_factors": top_forms,
            "top_prefixes": top_prefixes,
            "devices": devices,
        }

    brands_out = {}
    for brand in NAME_BRAND_ALIASES:
        brands_out[brand] = summarize_brand(brand, name_models[brand])

    industrial_out = _summarize_vendor_segment(
        industrial_models, "industrial_pos_odm"
    )
    other_x86_out = _summarize_vendor_segment(other_x86_models, "other_x86_odm")

    # Unique form-factor counts across inventoried segments only
    invent_form: dict[str, set] = defaultdict(set)
    for brand, block in brands_out.items():
        for d in block["devices"]:
            invent_form[d["type"]].add((brand, d["prefix"], d["model"]))
    for d in industrial_models.values():
        invent_form[d["type"]].add(("industrial", d["vendor"], d["prefix"], d["model"]))
    for d in other_x86_models.values():
        invent_form[d["type"]].add(("other_x86", d["vendor"], d["prefix"], d["model"]))

    form_factor_unique = {
        t: len(s)
        for t, s in sorted(
            invent_form.items(),
            key=lambda x: (
                FORM_FACTOR_ORDER.index(x[0])
                if x[0] in FORM_FACTOR_ORDER
                else 99,
                -len(x[1]),
                x[0],
            ),
        )
    }

    # Also report all form factors seen in the full tree (path rows / unique)
    tree_form_unique: dict[str, set] = defaultdict(set)
    tree_form_paths: Counter = Counter()
    for line in paths_file.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.strip().split("/")
        if len(parts) != 5:
            continue
        typ = normalize_form_factor(parts[0])
        if typ is None:
            continue
        tree_form_paths[typ] += 1
        tree_form_unique[typ].add((parts[1], parts[2], parts[3]))

    tree_form_factors = {
        "by_unique_model": {
            t: len(tree_form_unique[t])
            for t in sorted(
                tree_form_unique,
                key=lambda x: (
                    FORM_FACTOR_ORDER.index(x) if x in FORM_FACTOR_ORDER else 99,
                    -len(tree_form_unique[x]),
                    x,
                ),
            )
        },
        "by_hwid_path": dict(tree_form_paths.most_common()),
    }

    name_total = sum(b["models"] for b in brands_out.values())
    ind_total = industrial_out["models"]
    other_total = other_x86_out["models"]
    supported = (
        sum(b["supported_likely"] for b in brands_out.values())
        + industrial_out["supported_likely"]
        + other_x86_out["supported_likely"]
    )
    avoid = (
        sum(b["avoid"] for b in brands_out.values())
        + industrial_out["avoid"]
        + other_x86_out["avoid"]
    )

    return {
        "source": "https://github.com/linuxhw/DMI",
        "attribution": "linux-hardware.org / linuxhw/DMI path inventory",
        "paths_file": str(paths_file),
        "path_rows_parsed": path_rows,
        "paths_skipped": skipped,
        "unique_models_name_brands": name_total,
        "unique_models_industrial_pos_odm": ind_total,
        "unique_models_other_x86_odm": other_total,
        "unique_models_inventoried": name_total + ind_total + other_total,
        "tree_unique_models_all_vendors": sum(
            len(s) for s in tree_form_unique.values()
        ),
        "form_factors_tree": tree_form_factors,
        "form_factors_inventoried": form_factor_unique,
        "name_brands": brands_out,
        "industrial_pos_odm": industrial_out,
        "other_x86_odm": other_x86_out,
        "support_totals": {
            "supported_likely": supported,
            "avoid": avoid,
        },
    }


def build_oem_summary(inventory: dict, catalog: dict, generated: str) -> dict:
    pie_support = {
        "Likely supported": inventory["support_totals"]["supported_likely"],
        "Avoid gaming NVIDIA lines": inventory["support_totals"]["avoid"],
    }
    pie_brand = {
        brand: block["models"]
        for brand, block in inventory["name_brands"].items()
        if block["models"] > 0
    }
    if inventory["industrial_pos_odm"]["models"] > 0:
        pie_brand["Industrial POS ODM"] = inventory["industrial_pos_odm"]["models"]
    if inventory.get("other_x86_odm", {}).get("models", 0) > 0:
        pie_brand["Other x86 ODMs"] = inventory["other_x86_odm"]["models"]

    by_brand = {}
    for brand, block in inventory["name_brands"].items():
        cat_block = next(
            (b for b in catalog.get("brands", []) if b["brand"] == brand),
            {},
        )
        by_brand[brand] = {
            "optional": bool(cat_block.get("optional", False)),
            "models": block["models"],
            "supported_likely": block["supported_likely"],
            "avoid": block["avoid"],
            "form_factors": block["form_factors"],
            "top_form_factors": block["top_form_factors"],
        }

    other = inventory.get("other_x86_odm") or {
        "models": 0,
        "supported_likely": 0,
        "avoid": 0,
        "form_factors": {},
        "top_vendors": [],
    }

    return {
        "generated": generated,
        "source": inventory["source"],
        "unique_models_inventoried": inventory["unique_models_inventoried"],
        "unique_models_name_brands": inventory["unique_models_name_brands"],
        "unique_models_industrial_pos_odm": inventory[
            "unique_models_industrial_pos_odm"
        ],
        "unique_models_other_x86_odm": inventory.get(
            "unique_models_other_x86_odm", other["models"]
        ),
        "tree_unique_models_all_vendors": inventory["tree_unique_models_all_vendors"],
        "form_factors_tree": inventory["form_factors_tree"],
        "by_brand": by_brand,
        "industrial_pos_odm": {
            "models": inventory["industrial_pos_odm"]["models"],
            "supported_likely": inventory["industrial_pos_odm"]["supported_likely"],
            "avoid": inventory["industrial_pos_odm"]["avoid"],
            "form_factors": inventory["industrial_pos_odm"]["form_factors"],
            "top_vendors": inventory["industrial_pos_odm"]["top_vendors"][:15],
        },
        "other_x86_odm": {
            "models": other["models"],
            "supported_likely": other["supported_likely"],
            "avoid": other["avoid"],
            "form_factors": other.get("form_factors", {}),
            "top_vendors": (other.get("top_vendors") or [])[:15],
        },
        "status_totals": inventory["support_totals"],
        "pie": pie_support,
        "pie_by_brand": pie_brand,
    }


def _top_prefixes_line(prefixes: list[dict], limit: int = 8) -> str:
    parts = [f"`{p['prefix']}` ({p['models']})" for p in prefixes[:limit]]
    return ", ".join(parts) if parts else "—"


def load_pos_catalog(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _pos_needle_hits_vendor(vendor: str, needle: str) -> bool:
    """Strict-ish match for POS catalog needles (avoid ocom⊂computer)."""
    vl = vendor.lower().strip()
    n = needle.lower().strip()
    if not n or not vl:
        return False
    if len(n) < 5 or n in _SHORT_VENDOR_EXACT or n in {
        "ocom",
        "iei",
        "elo",
        "partner",
        "senor",
        "licon",
        "toshiba",
    }:
        return _needle_word_boundary(vl, n)
    return n in vl


def match_pos_brands(paths_file: Path, pos_catalog: dict) -> dict:
    """Search linuxhw paths for curated POS/panel brands (presence ≠ support proof)."""
    default_guidance = (
        pos_catalog.get("default_guidance")
        or (
            "Intel/AMD built-in graphics expected OK; "
            "test USB/serial/CAN devices in your app; "
            "skip separate NVIDIA graphics"
        )
    ).strip().replace("\n", " ")

    all_models: list[tuple[str, str, str, str]] = []
    for line in paths_file.read_text(encoding="utf-8", errors="replace").splitlines():
        parts = line.strip().split("/")
        if len(parts) != 5:
            continue
        typ = normalize_form_factor(parts[0])
        if typ is None:
            continue
        all_models.append((typ, parts[1], parts[2], parts[3]))

    brands_out = []
    found = 0
    missing = 0
    for entry in pos_catalog.get("brands") or []:
        name = entry["name"]
        needles = [str(n).lower() for n in (entry.get("needles") or [name.lower()])]
        notes = (entry.get("notes") or "").strip()
        matched: set[tuple[str, str, str, str]] = set()
        toshiba_mode = name.lower().startswith("toshiba") or any(
            n == "toshiba" for n in needles
        )
        for typ, vendor, prefix, model in all_models:
            blob = f"{vendor} {prefix} {model}".lower()
            hit = False
            if toshiba_mode:
                if not _pos_needle_hits_vendor(vendor, "toshiba"):
                    continue
                if (
                    "toughbook" in blob
                    or "toughpad" in blob
                    or any(k in blob for k in INDUSTRIAL_NAME_KEYWORDS)
                ):
                    hit = True
            else:
                for n in needles:
                    # Vendor match (word-boundary for short needles)
                    if _pos_needle_hits_vendor(vendor, n):
                        hit = True
                        break
                    # Longer needles may appear only in prefix/model (never short-substrings)
                    if len(n) >= 6 and _needle_word_boundary(blob, n):
                        hit = True
                        break
            if hit:
                matched.add((typ, vendor, prefix, model))

        in_hw = len(matched) > 0
        if in_hw:
            found += 1
        else:
            missing += 1
        brands_out.append(
            {
                "name": name,
                "in_linuxhw": in_hw,
                "models": len(matched),
                "needles": needles,
                "notes": notes,
                "guidance": default_guidance,
            }
        )

    return {
        "source": "scripts/pos_manufacturers.yaml",
        "default_guidance": default_guidance,
        "brands": brands_out,
        "found": found,
        "missing": missing,
        "total": len(brands_out),
    }


def render_markdown(
    mesa: dict,
    catalog: dict,
    inventory: dict,
    summary: dict,
    generated: str,
    pos_report: dict | None = None,
) -> str:
    s = mesa["summary"]
    pie = summary["pie"]
    pie_brand = summary["pie_by_brand"]
    total = summary["unique_models_inventoried"]
    tree_ff = summary["form_factors_tree"]["by_unique_model"]
    other_n = summary.get("other_x86_odm", {}).get("models", 0)
    ind = summary["industrial_pos_odm"]
    status = summary.get("status_totals") or {}
    likely = int(status.get("supported_likely", pie.get("Likely supported", 0)))
    avoid = int(status.get("avoid", pie.get("Avoid gaming NVIDIA lines", 0)))

    lines: list[str] = []
    lines.append("---")
    lines.append(
        "description: Which PCs can run Bass x86, in plain language"
    )
    lines.append("---")
    lines.append("")
    lines.append("# Hardware compatibility (x86)")
    lines.append("")
    lines.append(
        "This page answers a simple question: **will Bass:Lineout run on this PC?**"
    )
    lines.append("")
    lines.append("## The short answer")
    lines.append("")
    lines.append(
        "1. **Yes**, for most **Intel** or **AMD** PCs from about the last ten years "
        "(and many older ones too)."
    )
    lines.append(
        "2. **No** for machines that need a **separate NVIDIA graphics card** "
        "(gaming laptops and many workstations). Bass does not ship NVIDIA's "
        "closed-source driver."
    )
    lines.append(
        "3. The PC itself is usually fine. Extra screens (including many "
        "customer-facing displays) are largely handled by Bass "
        "[Display Mapper](../../UserGuides/display-mapper.md) and "
        "[Input Mapper](../../UserGuides/touch-mapper.md), plus related "
        "stack work. What still needs project-level care is **store or "
        "factory devices that talk over USB, serial, or CAN**: card readers, "
        "cash drawers, receipt printers, barcode scanners, and similar. "
        "Bass can expose those buses (including Config Overrides for common "
        "wiring cases), but the **Android app** still has to speak the "
        "device protocol."
    )
    lines.append("")
    lines.append(
        "Numbers on this page come from a public list of PCs that people have "
        "reported to [linux-hardware.org](https://linux-hardware.org) "
        "([linuxhw/DMI on GitHub](https://github.com/linuxhw/DMI)). "
        "A brand missing from that list is **not** the same as unsupported. "
        "See the [appendix](#appendix-a-word-list) for short definitions."
    )
    lines.append("")
    lines.append("## Check your graphics chip")
    lines.append("")
    lines.append("On a running Bass system (or any Linux live session):")
    lines.append("")
    lines.append("```bash")
    lines.append("lspci -nn | grep -iE 'vga|3d|display'")
    lines.append("```")
    lines.append("")
    lines.append("| If you see | What it means |")
    lines.append("|------------|---------------|")
    lines.append(
        "| Intel vendor id `8086:` | Expected to work "
        "(built-in Intel graphics). |"
    )
    lines.append(
        "| AMD vendor id `1002:` | Expected to work "
        "(built-in AMD graphics). Confirm the screen comes up. |"
    )
    lines.append(
        "| NVIDIA vendor id `10de:` | Treat as out of scope for production "
        "unless you already tested that exact chip with our build. |"
    )
    lines.append("")
    lines.append(
        "If this is a point-of-sale or industrial box, test card readers, "
        "cash drawers, printers, and other USB/serial/CAN devices with your "
        "Android app on that exact model. Extra monitors and customer-facing "
        "displays are usually covered by Display Mapper and Input Mapper."
    )
    lines.append("")
    lines.append("## Buying tips by brand")
    lines.append("")
    lines.append(
        "Quick \"buy this / skip that\" notes. Model counts later on this page "
        "come from linuxhw. This table is shopping guidance only."
    )
    lines.append("")
    lines.append("| Brand | Prefer | Skip | Notes |")
    lines.append("|-------|--------|------|-------|")
    for brand_block in catalog.get("brands", []):
        brand = brand_block["brand"]
        opt = " (optional)" if brand_block.get("optional") else ""
        best, avoid_s, overall = brand_best_avoid(brand_block)
        lines.append(
            f"| {md_escape(brand)}{opt} | {md_escape(best)} | "
            f"{md_escape(avoid_s)} | {md_escape(overall)} |"
        )
    lines.append("")
    lines.append(
        "Full series notes for each brand are in "
        "[Appendix D](#appendix-d-series-notes-by-brand)."
    )
    lines.append("")
    lines.append("## Picture of the inventory")
    lines.append("")
    lines.append(
        f"We track **{total:,}** distinct PC models across the brands and "
        f"segments below (out of **{summary['tree_unique_models_all_vendors']:,}** "
        "models in the full linuxhw tree)."
    )
    lines.append("")
    lines.append("| Outcome (name-matched sample) | Models |")
    lines.append("|--------------------------------|-------:|")
    lines.append(f"| Expected OK (Intel/AMD open graphics path) | {likely:,} |")
    lines.append(f"| Likely gaming / discrete NVIDIA naming | {avoid:,} |")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart LR")
    lines.append("  HW[Intel or AMD PC] --> OK[Expected to work]")
    lines.append("  HW --> Periph[Test USB serial CAN devices]")
    lines.append("  HW --> Disp[Display Mapper for extra screens]")
    lines.append("  AvoidN[Separate NVIDIA card] --> No[Out of scope]")
    lines.append("```")
    lines.append("")
    lines.append("| Where the models sit | Count |")
    lines.append("|----------------------|------:|")
    for label, count in sorted(pie_brand.items(), key=lambda x: -x[1]):
        if int(count) <= 0:
            continue
        lines.append(f"| {md_escape(label)} | {int(count):,} |")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart TB")
    lines.append(f"  Total[Tracked models {total}]")
    for brand, block in summary["by_brand"].items():
        if block["models"] <= 0:
            continue
        nid = re.sub(r"[^A-Za-z0-9]", "", brand) or "Brand"
        lines.append(f"  Total --> {nid}[{brand} {block['models']}]")
    ind_n = ind["models"]
    if ind_n:
        lines.append(f"  Total --> Ind[Industrial POS ODM {ind_n}]")
    if other_n:
        lines.append(f"  Total --> Oth[Other x86 makers {other_n}]")
    lines.append("```")
    lines.append("")
    lines.append("## Common PC brands")
    lines.append("")
    lines.append(
        "| Brand | Models in sample | Expected OK | Skip (gaming/NVIDIA naming) |"
    )
    lines.append(
        "|-------|-----------------:|------------:|----------------------------:|"
    )
    for brand, block in summary["by_brand"].items():
        if block["models"] <= 0:
            continue
        opt = " (optional)" if block.get("optional") else ""
        lines.append(
            f"| {md_escape(brand)}{opt} | {block['models']:,} | "
            f"{block['supported_likely']:,} | {block['avoid']:,} |"
        )
    lines.append(
        f"| Industrial / POS / ODM | {ind['models']:,} | "
        f"{ind['supported_likely']:,} | {ind['avoid']:,} |"
    )
    other = summary.get("other_x86_odm") or {}
    if other.get("models", 0):
        lines.append(
            f"| Other x86 makers / boards | {other['models']:,} | "
            f"{other['supported_likely']:,} | {other['avoid']:,} |"
        )
    lines.append("")
    lines.append("### Popular name lines (examples)")
    lines.append("")
    for brand, block in inventory["name_brands"].items():
        if block["models"] <= 0:
            continue
        lines.append(f"**{brand}** ({block['models']:,} models)")
        lines.append("")
        lines.append(
            f"- Common name prefixes: {_top_prefixes_line(block['top_prefixes'])}"
        )
        lines.append("")
    lines.append("## Industrial, POS, and panel PCs")
    lines.append("")
    lines.append(
        "This group covers factory PCs, point-of-sale terminals, panel PCs, "
        "rugged notebooks, thin clients, and many mini-PC makers "
        "(examples: Advantech, AAEON, Shuttle, Panasonic Toughbook, "
        "Intel NUC-class, OnLogic, Elo Touch)."
    )
    lines.append("")
    lines.append(
        "The same physical machine can show up under more than one maker name "
        "in the database (retail brand vs board maker vs a generic `OEM` label). "
        "Treat the counts as a sample, not a perfect product catalog."
    )
    lines.append("")
    lines.append(
        f"**{ind['models']:,}** models in this group "
        f"({ind['supported_likely']:,} expected OK, {ind['avoid']:,} skip)."
    )
    lines.append("")
    lines.append("| Maker | Models | Expected OK | Skip | Common shapes |")
    lines.append("|-------|-------:|------------:|-----:|---------------|")
    for v in ind.get("top_vendors", [])[:20]:
        tops = ", ".join(
            f"{t} ({n})"
            for t, n in list(v.get("form_factors", {}).items())[:3]
        ) or "-"
        lines.append(
            f"| {md_escape(v['vendor'])} | {v['models']:,} | "
            f"{v['supported_likely']:,} | {v['avoid']:,} | {md_escape(tops)} |"
        )
    more = len(inventory["industrial_pos_odm"].get("vendors", [])) - 20
    if more > 0:
        lines.append("")
        lines.append(
            f"Plus {more} more makers in "
            f"[`oem_devices.json`](../../data/hardware/oem_devices.json) "
            f"(field `industrial_pos_odm.vendors`)."
        )
    lines.append("")
    lines.append(
        f"- Common name prefixes: "
        f"{_top_prefixes_line(inventory['industrial_pos_odm']['top_prefixes'])}"
    )
    lines.append("")

    oth_inv = inventory.get("other_x86_odm") or {}
    if oth_inv.get("models", 0):
        lines.append("## Other PC makers and motherboard brands")
        lines.append("")
        lines.append(
            "Board makers (MSI, Gigabyte, ASRock, and similar), notebook "
            "factories (Clevo and peers), Linux PC brands (System76, TUXEDO), "
            "and common generic labels. This is a curated slice, not every "
            "remaining name in linuxhw."
        )
        lines.append("")
        lines.append(
            f"**{oth_inv['models']:,}** models in this group "
            f"({oth_inv['supported_likely']:,} expected OK, "
            f"{oth_inv['avoid']:,} skip)."
        )
        lines.append("")
        lines.append("| Maker | Models | Expected OK | Skip | Common shapes |")
        lines.append("|-------|-------:|------------:|-----:|---------------|")
        for v in (oth_inv.get("top_vendors") or [])[:20]:
            tops = ", ".join(
                f"{t} ({n})"
                for t, n in list(v.get("form_factors", {}).items())[:3]
            ) or "-"
            lines.append(
                f"| {md_escape(v['vendor'])} | {v['models']:,} | "
                f"{v['supported_likely']:,} | {v['avoid']:,} | {md_escape(tops)} |"
            )
        more_o = len(oth_inv.get("vendors", [])) - 20
        if more_o > 0:
            lines.append("")
            lines.append(
                f"Plus {more_o} more makers in "
                f"[`oem_devices.json`](../../data/hardware/oem_devices.json) "
                f"(field `other_x86_odm.vendors`)."
            )
        lines.append("")
        lines.append(
            f"- Common name prefixes: "
            f"{_top_prefixes_line(oth_inv.get('top_prefixes') or [])}"
        )
        lines.append("")

    if pos_report and pos_report.get("brands"):
        lines.append("## Retail POS and kiosk brands")
        lines.append("")
        lines.append(
            "Many store and kiosk brands ship Windows-only images, so they "
            "rarely show up in linuxhw. **Missing from the list does not mean "
            "Bass will not run.** If the unit uses Intel or AMD built-in "
            "graphics, treat it as expected to work. Use Display Mapper / "
            "Input Mapper for extra screens; test USB, serial, and CAN devices "
            "with your Android app on that model."
        )
        lines.append("")
        lines.append(
            f"Our curated list: **{pos_report['found']}** of "
            f"**{pos_report['total']}** brands appear at least once in this "
            f"linuxhw snapshot ({pos_report['missing']} do not)."
        )
        lines.append("")
        lines.append("| Brand | Seen in linuxhw? | Models seen | Notes |")
        lines.append("|-------|:----------------:|------------:|-------|")
        for b in pos_report["brands"]:
            in_hw = "yes" if b["in_linuxhw"] else "no"
            models = f"{b['models']:,}" if b["in_linuxhw"] else "-"
            note = plain(b.get("notes") or "") or (
                "Intel/AMD built-in graphics expected OK; "
                "test USB/serial devices in your app"
            )
            lines.append(
                f"| {md_escape(b['name'])} | {in_hw} | {models} | "
                f"{md_escape(note)} |"
            )
        lines.append("")
        lines.append(
            "Source list: "
            f"[`pos_manufacturers.yaml`](../../scripts/pos_manufacturers.yaml); "
            f"machine-readable: "
            f"[`pos_brands.json`](../../data/hardware/pos_brands.json)."
        )
        lines.append("")

    # --- Appendix ---
    lines.append("## Appendix A: Word list")
    lines.append("")
    lines.append("| Term | Plain meaning |")
    lines.append("|------|---------------|")
    lines.append(
        "| Bass:Lineout | Our Android-on-PC product: Android is the main OS. |"
    )
    lines.append(
        "| Built-in graphics (iGPU) | Graphics chip on the same package as the "
        "CPU (typical Intel or AMD laptops and office PCs). |"
    )
    lines.append(
        "| Separate / discrete GPU (dGPU) | A dedicated graphics card or module, "
        "often NVIDIA in gaming PCs. |"
    )
    lines.append(
        "| Mesa | The open-source graphics library Bass uses to drive the display. |"
    )
    lines.append(
        "| DRM | Direct Rendering Manager: the Linux kernel side of display "
        "and GPU access. |"
    )
    lines.append(
        "| DMI | Desktop Management Interface: the firmware strings that name "
        "the PC maker and model. |"
    )
    lines.append(
        "| linuxhw / linux-hardware.org | Public database of PCs people probed "
        "while running Linux. |"
    )
    lines.append(
        "| Unique model | One maker + product name line in that database "
        "(not one physical serial number). |"
    )
    lines.append(
        "| ODM / white-label | A factory builds the chassis; several retail "
        "brands may sell the same box under different names. |"
    )
    lines.append(
        "| POS | Point of sale: store terminals, cash drawers, receipt printers. |"
    )
    lines.append(
        "| Panel PC | A computer built into a touchscreen for factory or kiosk use. |"
    )
    lines.append(
        "| Display Mapper | Bass Settings tool for resolution, density, and "
        "rotation on built-in and extra screens (including many customer "
        "displays). |"
    )
    lines.append(
        "| Input Mapper (Touch Mapper) | Bass Settings tool for mapping touch "
        "and related input across screens. |"
    )
    lines.append(
        "| Config Overrides | Bass settings/files that can help wire common "
        "serial, USB, and CAN cases; the Android app still owns the device "
        "protocol. |"
    )
    lines.append(
        "| SKU | A specific sellable configuration (CPU, graphics, memory). |"
    )
    lines.append(
        "| PCI vendor id | A short code for the chip maker "
        "(`8086` Intel, `1002` AMD, `10de` NVIDIA). |"
    )
    lines.append("")
    lines.append("## Appendix B: How we count models")
    lines.append("")
    lines.append(
        "Each unique model is one combination of "
        "`(shape, maker, name prefix, model)` from linuxhw. "
        "We do not count every individual machine by serial number."
    )
    lines.append("")
    lines.append(
        "\"Expected OK\" vs \"Skip\" in the tables is a simple name heuristic: "
        "gaming or discrete-NVIDIA style names are marked skip. "
        "It is not a lab certification."
    )
    lines.append("")
    lines.append("| PC shape in the full linuxhw tree | Unique models |")
    lines.append("|------------------------------------|--------------:|")
    for ff, n in tree_ff.items():
        lines.append(f"| {md_escape(ff)} | {n:,} |")
    lines.append("")
    lines.append(
        "JSON dumps: "
        f"[`oem_devices.json`](../../data/hardware/oem_devices.json), "
        f"[`oem_summary.json`](../../data/hardware/oem_summary.json)."
    )
    lines.append("")
    lines.append("## Appendix C: Graphics drivers in this build")
    lines.append("")
    lines.append(
        "Chip id tables come from Mesa `include/pci_ids/` in our source tree."
    )
    lines.append("")
    lines.append("| Driver | Chip ids | Families | Policy |")
    lines.append("|--------|----------|----------|--------|")
    lines.append(
        f"| Intel Iris | {s['intel_iris_chips']} | "
        f"{s['intel_iris_families']} | Fully supported |"
    )
    lines.append(
        f"| Intel i915 (older) | {s['intel_i915_chips']} | - | "
        "Supported; older chips may need extra care |"
    )
    lines.append(
        f"| Intel crocus | {s['intel_crocus_chips']} | "
        f"{len(mesa['drivers']['crocus']['families'])} | "
        "Supported; older chips may need extra care |"
    )
    lines.append(
        f"| AMD radeonsi | {s['amd_radeonsi_chips']} | "
        f"{s['amd_radeonsi_families']} | "
        "Supported; confirm display on your build |"
    )
    lines.append(
        "| NVIDIA discrete | - | - | **Not supported** for production "
        "(Nouveau only) |"
    )
    lines.append("")
    lines.append(
        f"**{s['total_open_chips_parsed']}** open-driver chip ids parsed "
        "(Iris + i915 + crocus + radeonsi)."
    )
    lines.append("")
    iris_families = mesa["drivers"]["iris"]["families"]
    show = iris_families[:12]
    more_f = len(iris_families) - len(show)
    bullet = ", ".join(f"`{f}`" for f in show)
    if more_f > 0:
        bullet += f", ... (+{more_f} more)"
    lines.append(f"Sample Intel Iris family names: {bullet}")
    lines.append("")
    np = catalog.get("nvidia_policy") or {}
    policy_text = plain(np.get("summary") or mesa["nvidia"]["policy"] or "")
    if policy_text:
        lines.append("### NVIDIA policy (detail)")
        lines.append("")
        lines.append(policy_text)
        lines.append("")
    lines.append("## Appendix D: Series notes by brand")
    lines.append("")
    for brand_block in catalog.get("brands", []):
        brand = brand_block["brand"]
        opt = " (optional)" if brand_block.get("optional") else ""
        lines.append(f"### {brand}{opt}")
        lines.append("")
        for e in brand_block.get("entries", []):
            label = STATUS_LABEL.get(e["status"], e["status"])
            examples = ", ".join(e.get("examples") or []) or "-"
            lines.append(f"#### {plain(e['series'])}")
            lines.append("")
            lines.append(f"- **Status:** {plain(label)}")
            lines.append(f"- **Graphics class:** `{e['gpu_class']}`")
            lines.append(f"- **Examples:** {md_escape(examples)}")
            if e.get("notes"):
                lines.append(f"- **Notes:** {md_escape(e['notes'])}")
            lines.append("")
    lines.append("## Appendix E: Data files")
    lines.append("")
    lines.append("| File | Contents |")
    lines.append("|------|----------|")
    lines.append(
        "| [`oem_devices.json`](../../data/hardware/oem_devices.json) | "
        "Per-model inventory rows |"
    )
    lines.append(
        "| [`oem_summary.json`](../../data/hardware/oem_summary.json) | "
        "Roll-up counts |"
    )
    lines.append(
        "| [`pos_brands.json`](../../data/hardware/pos_brands.json) | "
        "POS / panel / kiosk brand checklist |"
    )
    lines.append(
        "| [`compat.json`](../../data/hardware/compat.json) | "
        "Mesa chip id summary |"
    )
    lines.append(
        "| [`oem_catalog.yaml`](../../scripts/oem_catalog.yaml) | "
        "Curated prefer / skip series |"
    )
    lines.append(
        "| [`pos_manufacturers.yaml`](../../scripts/pos_manufacturers.yaml) | "
        "Curated POS brand list |"
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(
        f"*Generated by `scripts/gen_hardware_compat.py` on {generated}. "
        "Inventory from [linuxhw/DMI](https://github.com/linuxhw/DMI). "
        "Graphics id tables from Mesa. Prefer/skip tips are guidance only.*"
    )
    lines.append("")
    return "\n".join(lines)


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mesa",
        type=Path,
        default=Path(os.environ.get("MESA", str(DEFAULT_MESA))),
        help="Path to mesa3d source tree",
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=DOC_ROOT / "scripts" / "oem_catalog.yaml",
        help="OEM catalog YAML (curated prefer/avoid tips)",
    )
    parser.add_argument(
        "--doc-root",
        type=Path,
        default=DOC_ROOT,
        help="Documentation repository root",
    )
    parser.add_argument(
        "--linuxhw-clone",
        type=Path,
        default=Path(os.environ.get("LINUXHW_DMI", str(DEFAULT_LINUXHW_CLONE))),
        help="Sparse clone directory for linuxhw/DMI",
    )
    parser.add_argument(
        "--refresh-linuxhw",
        action="store_true",
        help="Re-fetch linuxhw/DMI path list even if cache is fresh",
    )
    parser.add_argument(
        "--pos-catalog",
        type=Path,
        default=DOC_ROOT / "scripts" / "pos_manufacturers.yaml",
        help="POS / panel / kiosk manufacturer YAML (not derived from linuxhw)",
    )
    parser.add_argument(
        "--skip-devices-list",
        action="store_true",
        help="Omit per-model devices arrays from oem_devices.json (smaller file)",
    )
    args = parser.parse_args()

    mesa_root = args.mesa.resolve()
    doc_root = args.doc_root.resolve()
    catalog_path = args.catalog.resolve()
    pos_catalog_path = args.pos_catalog.resolve()
    data_dir = doc_root / "data" / "hardware"
    paths_cache = data_dir / "linuxhw_paths.txt"

    if not (mesa_root / PCI_IDS_SUBDIR).is_dir():
        sys.stderr.write(f"Mesa pci_ids not found under {mesa_root}\n")
        return 1
    if not catalog_path.is_file():
        sys.stderr.write(f"OEM catalog missing: {catalog_path}\n")
        return 1
    if not pos_catalog_path.is_file():
        sys.stderr.write(f"POS catalog missing: {pos_catalog_path}\n")
        return 1

    generated = date.today().isoformat()
    fetch_linuxhw_paths(paths_cache, args.linuxhw_clone, args.refresh_linuxhw)

    mesa = collect_mesa(mesa_root)
    catalog = load_oem_catalog(catalog_path)
    pos_catalog = load_pos_catalog(pos_catalog_path)
    inventory = ingest_linuxhw(paths_cache)
    summary = build_oem_summary(inventory, catalog, generated)
    pos_report = match_pos_brands(paths_cache, pos_catalog)

    # Slim devices file option
    devices_doc = {
        "generated": generated,
        "generator": "scripts/gen_hardware_compat.py",
        "source": inventory["source"],
        "attribution": inventory["attribution"],
        "unique_models_inventoried": inventory["unique_models_inventoried"],
        "unique_models_name_brands": inventory["unique_models_name_brands"],
        "unique_models_industrial_pos_odm": inventory[
            "unique_models_industrial_pos_odm"
        ],
        "unique_models_other_x86_odm": inventory.get(
            "unique_models_other_x86_odm", 0
        ),
        "tree_unique_models_all_vendors": inventory["tree_unique_models_all_vendors"],
        "form_factors_tree": inventory["form_factors_tree"],
        "form_factors_inventoried": inventory["form_factors_inventoried"],
        "support_totals": inventory["support_totals"],
        "name_brands": {},
        "industrial_pos_odm": {},
        "other_x86_odm": {},
    }
    for brand, block in inventory["name_brands"].items():
        entry = {k: v for k, v in block.items() if k != "devices"}
        if not args.skip_devices_list:
            entry["devices"] = block["devices"]
        devices_doc["name_brands"][brand] = entry

    ind = inventory["industrial_pos_odm"]
    ind_out = {k: v for k, v in ind.items() if k != "devices"}
    if not args.skip_devices_list:
        ind_out["devices"] = ind["devices"]
    devices_doc["industrial_pos_odm"] = ind_out

    oth = inventory.get("other_x86_odm") or {}
    oth_out = {k: v for k, v in oth.items() if k != "devices"}
    if not args.skip_devices_list and oth.get("devices") is not None:
        oth_out["devices"] = oth["devices"]
    devices_doc["other_x86_odm"] = oth_out

    compat = {
        "generated": generated,
        "generator": "scripts/gen_hardware_compat.py",
        "mesa": {
            "root": mesa["mesa_root"],
            "summary": mesa["summary"],
            "drivers": mesa["drivers"],
            "nvidia": mesa["nvidia"],
            "family_counts": mesa["family_counts"],
        },
        "oem_catalog_source": str(catalog_path.relative_to(doc_root)),
        "linuxhw_source": inventory["source"],
        "oem_summary_ref": "data/hardware/oem_summary.json",
        "oem_devices_ref": "data/hardware/oem_devices.json",
        "oem": catalog,
        "chips": mesa["chips"],
    }

    write_json(data_dir / "compat.json", compat)
    write_json(data_dir / "oem_summary.json", summary)
    write_json(data_dir / "oem_devices.json", devices_doc)
    write_json(
        data_dir / "pos_brands.json",
        {
            "generated": generated,
            "generator": "scripts/gen_hardware_compat.py",
            **pos_report,
        },
    )

    md = render_markdown(
        mesa, catalog, inventory, summary, generated, pos_report=pos_report
    )
    page = doc_root / "Installation" / "x86_64-v2" / "hardware-compatibility.md"
    frag = doc_root / "Installation" / "x86_64-v2" / "_generated_hardware_compat.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(md, encoding="utf-8")
    body = md.split("---\n", 2)[-1] if md.startswith("---") else md
    frag.write_text(
        f"<!-- Generated by scripts/gen_hardware_compat.py on {generated} -->\n{body}",
        encoding="utf-8",
    )

    print("Wrote:")
    print(f"  {paths_cache}")
    print(f"  {data_dir / 'compat.json'}")
    print(f"  {data_dir / 'oem_summary.json'}")
    print(f"  {data_dir / 'oem_devices.json'}")
    print(f"  {data_dir / 'pos_brands.json'}")
    print(f"  {page}")
    print(f"  {frag}")
    print("Mesa chips:")
    print(json.dumps(mesa["summary"], indent=2))
    print("Inventory totals:")
    print(
        json.dumps(
            {
                "unique_models_inventoried": summary["unique_models_inventoried"],
                "name_brands": summary["unique_models_name_brands"],
                "industrial_pos_odm": summary["unique_models_industrial_pos_odm"],
                "other_x86_odm": summary.get("unique_models_other_x86_odm", 0),
                "tree_all_vendors": summary["tree_unique_models_all_vendors"],
                "pie": summary["pie"],
                "pie_by_brand": summary["pie_by_brand"],
                "by_brand_models": {
                    b: summary["by_brand"][b]["models"] for b in summary["by_brand"]
                },
                "pos_brands_found": pos_report["found"],
                "pos_brands_missing": pos_report["missing"],
                "pos_brands_total": pos_report["total"],
            },
            indent=2,
        )
    )
    if summary["unique_models_inventoried"] < 1000:
        sys.stderr.write(
            "WARNING: inventoried unique models < 1000; expected thousands.\n"
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
