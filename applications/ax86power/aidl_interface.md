# Ax86 Power AIDL

Binder API for sleep / wake policy and power actions. Backed by vendor `apply_wake_policy` (`persist.ax86.wake.*`, `persist.ax86.mem_sleep`, `sys.ax86.wake.update`).

| | |
|---|---|
| **Package** | `org.ax86.power` |
| **Interface** | `IAx86Power` |
| **Intent action** | `org.ax86.power.IAx86Power` |
| **Service permission** | `android.permission.DEVICE_POWER` |

## Interface

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

    /** Power actions (1:1 with legacy BlissPowerManager AIDL). */
    void reboot();
    void shutdown();
    void sleep();
}
```

## API roles

| API | Role |
|-----|------|
| `set/getMemSleep`, `getSupportedMemSleep` | `deep` (S3) vs `s2idle` |
| `set/getIgnoreKeyboardWake` | USB/PS2 keyboard resume |
| `set/getIgnorePointerWake` | Mouse/touchpad resume |
| `set/getIgnoreTouchWake` | Touchscreen resume |
| `set/getAllowWifiWake` | ACPI `RP*` / Wi-Fi PME |
| `apply()` | Trigger vendor apply (`sys.ax86.wake.update=1`) |
| `reboot()` / `shutdown()` / `sleep()` | Power actions (legacy BlissPowerManager parity) |

## Migrating from BlissPowerManager

| Legacy (`BlissPowerManager`) | Ax86 Power (`IAx86Power`) |
|------------------------------|---------------------------|
| `reboot()` | `reboot()` |
| `shutdown()` | `shutdown()` |
| `sleep()` | `sleep()` |

Wake / mem_sleep policy APIs are new on Ax86 Power; they have no BlissPowerManager equivalent.

## Related

* [Ax86 Power](Ax86Power.md)
* [Legacy Bliss Power Management API](../../interfaces/BlissPowerManagerAIDL/power-management-aidl.md)
