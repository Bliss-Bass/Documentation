# Addon Development: Bass Lineout

**This page is for Bass: Lineout** (`vendor/ax86-lite`, `tools/build.sh`).

If you are on classic Bass OS with `private/addons/` and `unfold_bliss.sh`, use the separate guide instead:

→ **[Addon Development: Legacy Bass OS](addon-development-legacy-bass.md)**

Do not mix the two. Lineout does **not** scan `private/addons/` the way older Bass unfold did. Legacy Bass does **not** use `vendor/ax86-lite/vendor_packages/` the same way.

---

## Lineout overview

On Lineout, "addon" work falls into two buckets that both belong to this product line:

| Bucket | Where it lives | How you enable it |
|--------|----------------|-------------------|
| **Build packages** | `vendor/ax86-lite/vendor_packages/` | `build.sh` flags (`--extras`, `--btnmgr`, …) |
| **Runtime overrides** | `/data/misc/`, GRUB flags, `addon_init` | Push files + cmdline / `setprop` |

Both are documented below. Neither is the old `private/addons/` patchset model.

---

## Build packages

Features ship as product packages in the vendor tree.

```text
vendor/ax86-lite/vendor_packages/<Name>/
  Android.bp / *.mk
  README.md          # picked up by Ax86Docs when present
  init .rc / .sh     # optional; keep package-local when possible
```

Enable them from `vendor/ax86-lite/tools/build.sh` (see [Building Bass OS](building-bass.md)):

| Flag | Packages / behavior |
|------|---------------------|
| `--extras` | Touch Mapper, Display Mapper, Config Overrides, Tweaks, Ax86Docs |
| `--btnmgr` | Button Manager |
| `--logger` / `--logging-enabled` | Ax86 Logger |
| `--bootsight` | BootSight (+ `ro.bass.fleet_mgmt=bootsight`) |
| `--smartdock` | SmartDock DFC |
| `--ethernetconfig` | Ethernet Config |

### Adding a new Lineout package

1. Create `vendor_packages/YourFeature/` with a product `.mk` and (for apps) `Android.bp`.
2. Wire it in `ax86_lite.mk` behind a flag (or always-on if that is intentional).
3. Add the flag to `tools/build.sh` help and export defaults.
4. Drop a `README.md` in the package so [Ax86Docs](../applications/Ax86Docs/Ax86Docs.md) picks it up on the next `--extras` build.
5. Prefer package-local `init.rc` / scripts. Avoid editing core `addon_init.rc` unless the feature is shared early-boot plumbing.

App docs on this site:

* [Touch Mapper](../applications/BlissTouchMapper/BlissTouchMapper.md)
* [Display Mapper](../applications/BlissDisplayMapper/BlissDisplayMapper.md)
* [Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md)
* [Bliss Tweaks](../applications/BlissTweaks/BlissTweaks.md)
* [Button Manager](../applications/Ax86ButtonManager/Ax86ButtonManager.md)
* [Ax86 Logger](../applications/Ax86Logger/Ax86Logger.md)
* [BootSight](../applications/BootSight/BootSight.md)

### Newer Lineout branches (`addons/<id>/`)

Some newer ax86-lite branches move packages under `addons/<id>/` with `addon.cfg` and a compat symlink from `vendor_packages/<Pkg>`. See `vendor_packages/Ax86ButtonManager/docs/PORTING-23.2.md` in the vendor tree.

On current Lineage 21 / A14 Lineout trees, packages still live directly under `vendor_packages/` and are gated by `ax86_lite.mk` + `tools/build.sh`. Use that layout unless your branch already has the `addons/` integrator.

---

## Runtime overrides (`addon_init`)

Lineout also supports **on-device** overrides without rebuilding the ISO. Scripts under `/vendor/bin/addon_*.sh` run from `addon_init.rc` after `/data` is available. They can bind-mount files from `/data/misc/` over vendor/system paths, apply settings, and react to property triggers.

This is still the **Lineout** product path (same vendor tree). It is not the legacy Bass private-addon unfold flow.

| Path | Role |
|------|------|
| `/vendor/etc/init/addon_init.rc` | Triggers early and late init, mapper props |
| `/vendor/bin/addon_init.sh` | Orchestrator (DMI props, bind mounts, late boot) |
| `addon_hardware.sh` / `addon_peripherals.sh` / `addon_packages.sh` / `addon_mappers.sh` | Helpers used by `addon_init` |
| `/data/misc/` | Fleet- or tech-provided override files |

### GRUB / cmdline toggles (Lineout)

| Flag | Effect |
|------|--------|
| `ADDON_IDC=1` | Custom `.idc` files from `/data/system/devices/idc` |
| `BLISS_INPUT_PORTS_ADDON=1` | `/data/misc/input-port-addon.xml` for input↔display ports |
| `ADDON_BOOTANIMATION=1` | `/data/misc/bootanimation.zip` |
| `ADDON_BASSINIT=1` | Custom vendor init under `/data/vendor/etc/init/` |

How-tos:

* [Using IDC Addon](../setup_and_configuration/addon_idc.md)
* [Creating an input-port-addon.xml file](../setup_and_configuration/input-port-associations.md)

On `--extras` builds, [Touch Mapper](../applications/BlissTouchMapper/BlissTouchMapper.md) can generate the input-port file from Settings. Prefer that UI when available; GRUB flags still matter for headless imaging.

### Config files and property triggers (Lineout)

| Mechanism | Docs |
|-----------|------|
| `settings_*.conf`, `runtime_props.conf`, `device_config.conf` | [Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md) |
| `custom_device.prop` (early `ro.*`) | Same page; applied by `addon_init` before framework |
| Master apply | `setprop persist.ax86.update_configs 1` |
| Per-mapper apply | `sys.ax86.display.update`, `sys.ax86.touch.update`, `sys.ax86.radio.update`, `sys.ax86.location.update` |

Vendor reference (also in Ax86Docs): `OVERRIDES.md` and `VENDOR_DEPLOYMENT.md` in `vendor/ax86-lite`.

### Good uses for runtime overrides

* Field fixes (digitizer axes, DPI) without a new ISO
* Fleet imaging: push `/data/misc` files, set GRUB flags, reboot
* Config Override examples under `vendor/ax86-lite/docs/examples/`

Runtime overrides are **not** how you ship a new privileged app. New apps go under `vendor_packages/` with a build flag.

---

## Related (Lineout)

* [Building Bass OS](building-bass.md)
* [Ax86Docs](../applications/Ax86Docs/Ax86Docs.md)
* [Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md)
* [Fleet Management](../features/fleet-management.md)
* [Addon Development: Legacy Bass OS](addon-development-legacy-bass.md) (different product tree)
