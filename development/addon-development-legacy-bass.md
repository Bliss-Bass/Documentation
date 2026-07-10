# Addon Development: Legacy Bass OS

**This page is for classic Bass OS** projects that use `private/addons/`, `vendor/bass/patches/`, and unfold scripts such as `unfold_bliss.sh` / `build_bass.sh`.

If you are on **Bass: Lineout** (`vendor/ax86-lite`), stop here and use:

→ **[Addon Development: Bass Lineout](addon-development.md)**

Lineout build packages and Lineout runtime `addon_init` overrides are documented only on that page. This legacy guide does **not** apply to `vendor/ax86-lite/tools/build.sh`.

---

## What a legacy Bass addon is

On classic Bass OS, an addon is something dropped into `private/addons/` so the unfold process can sync manifests and apply patches (and optionally bring private APKs or sources).

A legacy addon can include one or more of:

* **Patchsets** applied on top of the tree during unfold
* **Prebuilt APKs** (for example Restricted Launcher Pro)
* **Private package sources** (for example Kiosk Launcher)
* **Script addons** that run during unfold or build

---

## Patchset addon layout

### Where things go

Place the patchset addon folder (`patchsets-addon_name`) in `private/addons/`. Unfold searches that location, syncs any manifest it finds, then applies the addon's patches.

### Manifest

* Point the manifest path at `vendor/bass/patches/patchsets-addon_name`
* Name the manifest file after the addon
* Use a git remote name unique to that addon

### Folder shape

```text
patchsets_addon_name/
  README.md
  manifest/
    private-addon_name.xml
  addon_name/
    device/generic/common/0001-change_name-1-of-3.patch
    bootable/newinstaller/0001-change_name-2-of-3.patch
    bootable/recovery/0001-change_name-3-of-3.patch
```

Older internal template examples lived under build-host paths such as `assets/examples/addon_templates/patchsets-network_options`. Use those only on classic Bass trees that still ship them.

---

## Licensed private addons

If you hold a license for private Bass addons or features, place the files you were given into `private/addons` or `private/manifests` before unfold. Vendor-specific patches for those products often go in `patches-vendor/`. Check your organization's Bass-OS project folder; some deliveries already include those pieces.

See also the licensed-addons notice in [Building Bass OS](building-bass.md) (classic Bass sections).

---

## Do not confuse with Lineout

| | Legacy Bass OS (this page) | Bass Lineout |
|--|----------------------------|--------------|
| Vendor tree | `vendor/bass` (typical) | `vendor/ax86-lite` |
| Drop new features in | `private/addons/` | `vendor_packages/` |
| Build entry | `build_bass.sh` / unfold | `tools/build.sh` |
| Runtime `/data/misc` + `addon_init` | May exist on some images | Documented on the [Lineout addon page](addon-development.md) |

If you maintain both products, keep legacy addons in the Bass private tree and Lineout features in `vendor/ax86-lite/vendor_packages/`.

---

## Related

* [Addon Development: Bass Lineout](addon-development.md)
* [Building Bass OS](building-bass.md)
* [Contributing](contributing-documentation.md)
