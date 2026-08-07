# Lockdown install / uninstall block

Blocks package install and uninstall while the device is booted in lockdown mode. Enable with `--ldinstall` on Lineout builds.

| | |
|---|---|
| **Build flag** | `--ldinstall` |
| **Property** | `ro.bass.lockdown_block_install=1` |

## Gate

Active when **both** are true:

| Property | Value |
|----------|--------|
| `ro.bass.lockdown_block_install` | `1` |
| `ro.boot.bliss.bootmode` | `lockdown` |

Without `ro.bass.lockdown_block_install=1`, the hooks are no-ops.

## What is blocked

| Path | Layer |
|------|--------|
| PackageInstaller UI (APK picker, uninstall dialog) | PackageInstaller app |
| `pm install` / `pm uninstall` (ADB / shell) | `PackageManagerShellCommand` |
| `PackageManager.deletePackage()` / PackageInstaller sessions | framework helpers |

Admin / non-lockdown boots are unaffected.

## Build

```bash
./build.sh ... --ldinstall
```

## Related

* [Booting into lockdown builds](../setup_and_configuration/booting-into-lockdown-builds.md)
* [Admin Restriction](admin-restriction.md)
* [Building Bass OS](../development/building-bass.md)
