# Feature Flags (aconfig) on Bass: Lineout

Android turns many features on and off with **aconfig flags** (for example
`com.android.window.flags.enable_stepped_cascading`). A Bass image is meant to serve many
different devices and use cases, so Bass keeps as many of these flags as possible
**switchable on the running device**: from [Bliss Tweaks](../applications/BlissTweaks/BlissTweaks.md),
from [Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md)
(`device_config.conf`), or over ADB. This page explains how that works and how to maintain it.

## Read-only and read-write flags

Every flag has a state (`ENABLED` / `DISABLED`) and a permission:

| Permission | What it means |
|------------|---------------|
| `READ_WRITE` | The value can be changed at runtime (`device_config`, `aflags`, Bliss Tweaks). Takes effect after a reboot, or after restarting the app for Launcher3 and SystemUI flags. |
| `READ_ONLY` | The value is fixed when the image is built. Runtime changes are ignored. |
| fixed read-only (`is_fixed_read_only` in the flag's declaration) | Always read-only. Can only be changed by building with a different value. |

Android 17 (LineageOS 24.0, release `cp2a`) builds every flag read-only by default
(`RELEASE_ACONFIG_REQUIRE_ALL_READ_ONLY=true`), and Google's release values also mark many
flags `READ_ONLY` one by one. Bass undoes both.

## How Bass keeps flags switchable

Every Bass Android 17 build reads `device/generic/x86_64_tablet/release/`, a release config
map in the device tree:

| File | What it does |
|------|--------------|
| `flag_values/cp2a/RELEASE_ACONFIG_REQUIRE_ALL_READ_ONLY.textproto` | Allows read-write flags again. |
| `flag_values/cp2a/RELEASE_ACONFIG_FLAG_DEFAULT_PERMISSION.textproto` | Makes `READ_WRITE` the default for flags no release sets. |
| `aconfig/cp2a/` | A generated pack that turns Google's explicit `READ_ONLY` values `READ_WRITE`, keeping each flag's state, for the namespaces in `rw_namespaces.conf`. |
| `rw_namespaces.conf` | The namespaces the pack covers (desktop, windowing, multitasking, display, launcher, SystemUI, input, ...). |

The build loads this map after Google's values (`build/release`) and before Lineage's
(`vendor/lineage/release`) and the addons' (for example dual-shade). So a value an addon sets on
purpose still wins, and an addon can keep a flag read-only when it must not change at runtime.

On Android 16 (LineageOS 23.2) the same settings came from the `desktop-aconfig` addon.

## Checking a device

```bash
adb shell aflags list | grep -c read-write                 # how many flags can be switched
adb shell aflags list | grep enable_stepped_cascading      # one flag: state and permission
adb shell device_config put lse_desktop_experience \
    com.android.window.flags.enable_stepped_cascading true # then reboot
```

## The inventory tool

`device/generic/x86_64_tablet/scripts/aconfig_inventory.py` reads the source tree, so none of
these commands need a build. Run them from the AOSP workspace root.

| Command | What it does |
|---------|--------------|
| `scan . cp2a -o flags.csv` | Every flag in the tree with its declaration and its value for a release (CSV). |
| `diff old.csv new.csv [--namespaces a,b]` | Flags added, removed or changed between two scans, for example Android 16 against Android 17. |
| `rw-pack flags.csv cp2a <dir> --namespaces-file conf` | Writes the read-write pack (above). |
| `caches . cp2a <dir> --namespaces-file conf [--maps-file f]` | Builds the same flag caches the build ships (`aconfig_flags.pb` format) with the host `aconfig` tool. |

### Regenerating the read-write pack

After changing `rw_namespaces.conf`, or after a LineageOS or AOSP update:

```bash
device/generic/x86_64_tablet/scripts/aconfig_inventory.py scan . cp2a -o /tmp/cp2a.csv \
    --exclude-root device/generic/x86_64_tablet/release
device/generic/x86_64_tablet/scripts/aconfig_inventory.py rw-pack /tmp/cp2a.csv cp2a \
    device/generic/x86_64_tablet/release/aconfig/cp2a \
    --namespaces-file device/generic/x86_64_tablet/release/rw_namespaces.conf
```

Commit the result in the device tree. Fixed read-only flags are never put in the pack: a
`READ_WRITE` value on one fails the build.

## Changing a flag's built-in value

To ship a different default (for example a desktop feature turned on), add a `flag_value` to
the `desktop-aconfig` addon's patch for the release
(`vendor/lineage/release/aconfig/cp2a/<package>/`). Use `permission: READ_WRITE` unless the
flag is fixed read-only, so it stays switchable. This is the only way to change a fixed
read-only flag.

## Bliss Tweaks' flag tabs

Bliss Tweaks lists the read-write flags of the namespaces in
`addons/bliss-tweaks/tools/aconfig_namespaces.conf` as switches, one tab per namespace. The list
is generated, not written by hand. `tools/build.sh` regenerates it from source before packaging
every `--extras` build, so it always matches the flags that build ships.

To regenerate it without building (about 15 seconds):

```bash
bash vendor/ax86-lite/tools/refresh_bliss_tweaks_aconfig.sh --xml-only --from-source --release cp2a
```

This rewrites `addons/bliss-tweaks/packages/BlissTweaks/res/xml/bliss_settings_aconfig.xml`.
Commit it in the bliss-tweaks addon. Without `--from-source` the script reads the last build's
`aconfig_flags.pb` instead (`--product-out` / `--pb`).

## Related

* [Building Bass: Lineout](building-bass.md)
* [Addon Development: Bass Lineout](addon-development.md)
* [Bliss Tweaks](../applications/BlissTweaks/BlissTweaks.md)
* [Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md)
