# Ax86 Power

Ax86 Power is the sleep / wake **policy** UI and AIDL for Bass: Lineout (x86). It controls what may resume the machine and which suspend depth to use. It also hosts the legacy [BlissPowerManager](../../interfaces/BlissPowerManagerAIDL/power-management-aidl.md) binder (`blisspower`) so existing apps keep working with **no code changes**.

| | |
|---|---|
| **Package** | `org.ax86.power` |
| **Legacy service** | ServiceManager `blisspower` (`IBlissPower`) |
| **Ax86 service action** | `org.ax86.power.IAx86Power` |
| **Build flags** | `--ax86-power` (`USE_AX86_POWER=true`), or `--extras` |
| **Settings** | System → Ax86 Power (no app-drawer icon) |

Core vendor still applies wake defaults without this addon (`ignore_keyboard=1`, `ignore_pointer=1`, prefer `deep`). This package is the user-facing control plane.

## Architecture

```text
┌─────────────────┐     persist.ax86.wake.*      ┌──────────────────────────┐
│  Ax86Power app  │  persist.ax86.mem_sleep      │  addon_hardware.sh       │
│  IAx86Power     │ ──────────────────────────► │  apply_wake_policy()     │
│  IBlissPower    │  sys.ax86.wake.update=1      │  (sysfs / ACPI wakeup)   │
│  (blisspower)   │                             └──────────────────────────┘
└─────────────────┘
```

`apply_wake_policy` runs at post-fs-data, again on `sys.boot_completed`, and whenever `sys.ax86.wake.update` is set to `1`. Power-button ACPI paths are never disabled. The `blisspower` binder is registered at boot via BootReceiver and `Ax86Power.rc`.

## Legacy apps (no changes)

Keep using `BlissPowerManager.getInstance(context)` and your existing `bliss-power-framework.jar`. As long as the image includes Ax86 Power, `ServiceManager.getService("blisspower")` resolves to the same `IBlissPower` contract (`reboot` / `shutdown` / `sleep`).

See [AIDL Interface](AIDL_INTERFACE.md) for `service call` examples.

## Settings entry

Appears under **Settings → System** via `EXTRA_SETTINGS` + `com.android.settings.category.ia.system`. There is no launcher / app-drawer icon.

## What you can configure

| Control | Property | Default (first boot) |
|---------|----------|----------------------|
| Suspend depth | `persist.ax86.mem_sleep` | Prefer `deep` (S3); GRUB `androidboot.mem_sleep=` still wins |
| Ignore keyboard wake | `persist.ax86.wake.ignore_keyboard` | `1` |
| Ignore pointer wake | `persist.ax86.wake.ignore_pointer` | `1` |
| Ignore touch wake | `persist.ax86.wake.ignore_touch` | `0` |
| Allow Wi-Fi / PCIe PME wake | `persist.ax86.wake.allow_wifi` | `0` |

Supported mem_sleep values: `deep` (S3) or `s2idle`.

## Manual (no UI)

```bash
adb shell setprop persist.ax86.wake.ignore_keyboard 1
adb shell setprop persist.ax86.mem_sleep deep
adb shell setprop sys.ax86.wake.update 1
```

## Build

```bash
./build.sh --ax86-power ...
# or
./build.sh --extras ...
```

## Related

* [AIDL Interface](AIDL_INTERFACE.md)
* [Legacy Bliss Power Management API](../../interfaces/BlissPowerManagerAIDL/power-management-aidl.md)
* [Building Bass OS](../../development/building-bass.md)
* [Addon Development: Bass Lineout](../../development/addon-development.md)
