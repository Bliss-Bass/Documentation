# Ax86 Power AIDL

Binder APIs for sleep / wake policy and power actions. Backed by vendor `apply_wake_policy` (`persist.ax86.wake.*`, `persist.ax86.mem_sleep`, `sys.ax86.wake.update`).

## Legacy BlissPowerManager (drop-in)

Existing apps that use `org.blissos.powermanager.BlissPowerManager` / `IBlissPower` need **no changes**. Ax86 Power registers the same ServiceManager binder at boot.

| | |
|---|---|
| **ServiceManager name** | `blisspower` |
| **AIDL** | `org.blissos.powermanager.IBlissPower` |
| **Client** | `BlissPowerManager.getInstance(context)` |
| **Permission** | platform / `DEVICE_POWER` on the host service |

```aidl
package org.blissos.powermanager;

interface IBlissPower {
    void reboot();    // transaction 1
    void shutdown();  // transaction 2
    void sleep();     // transaction 3
}
```

```java
import org.blissos.powermanager.BlissPowerManager;

BlissPowerManager blissPowerManager = BlissPowerManager.getInstance(this);
blissPowerManager.reboot();
blissPowerManager.shutdown();
blissPowerManager.sleep();
```

```bash
adb shell service list | grep blisspower
adb shell service call blisspower 1   # reboot
adb shell service call blisspower 2   # shutdown
adb shell service call blisspower 3   # sleep
```

Ship or keep your existing `bliss-power-framework.jar` (same as the [BlissPowerManager](https://github.com/Bliss-Bass/platform_packages_apps_BlissPowerManager) sample). Only the on-device `blisspower` service must be present (provided when Ax86 Power is built in).

## Ax86-native interface (`IAx86Power`)

Use this for wake-policy controls (or when binding the Ax86 Power service directly).

| | |
|---|---|
| **Package** | `org.ax86.power` |
| **Interface** | `IAx86Power` |
| **Intent action** | `org.ax86.power.IAx86Power` |
| **Service permission** | `android.permission.DEVICE_POWER` |

```aidl
package org.ax86.power;

interface IAx86Power {
    /** Suspend depth: "deep" (S3) or "s2idle". */
    void setMemSleep(String mode);
    String getMemSleep();
    /** Raw /sys/power/mem_sleep contents. */
    String getSupportedMemSleep();

    void setIgnoreKeyboardWake(boolean ignore);
    boolean getIgnoreKeyboardWake();
    void setIgnorePointerWake(boolean ignore);
    boolean getIgnorePointerWake();
    void setIgnoreTouchWake(boolean ignore);
    boolean getIgnoreTouchWake();
    void setAllowWifiWake(boolean allow);
    boolean getAllowWifiWake();

    /** Apply persist props to sysfs via vendor init. */
    void apply();

    /** Power actions (also on blisspower / IBlissPower). */
    void reboot();
    void shutdown();
    void sleep();
}
```

### API roles

| API | Role |
|-----|------|
| `set/getMemSleep`, `getSupportedMemSleep` | `deep` (S3) vs `s2idle` |
| `set/getIgnoreKeyboardWake` | USB/PS2 keyboard resume |
| `set/getIgnorePointerWake` | Mouse/touchpad resume |
| `set/getIgnoreTouchWake` | Touchscreen resume |
| `set/getAllowWifiWake` | ACPI `RP*` / Wi-Fi PME |
| `apply()` | Trigger vendor apply (`sys.ax86.wake.update=1`) |
| `reboot()` / `shutdown()` / `sleep()` | Power actions |

## Related

* [Ax86 Power](Ax86Power.md)
* [Legacy Bliss Power Management API](../../interfaces/BlissPowerManagerAIDL/power-management-aidl.md)
