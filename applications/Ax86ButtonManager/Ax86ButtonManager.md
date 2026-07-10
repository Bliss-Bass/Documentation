# Ax86 Button Manager

Button Manager maps hardware function keys (P1, P2, P3, and similar) on generic x86 devices to actions and device controls. It is a privileged, platform-signed system app with a Settings entry, an AIDL service, and a `cmd` handler.

| | |
|---|---|
| **Package** | `com.ax86.btnmgr` |
| **Service / cmd** | `ax86_btnmgr` |
| **Build flag** | `--btnmgr` (`USE_BTNMGR=true`) |
| **Config** | `/data/misc/ax86_btn_manager.conf` |
| **Settings** | System → Button Manager |

`--btnmgr` is independent of `--extras`.

## What it does

Open **Button Manager** from Settings, then add or edit a mapping:

1. Enter a label for the button.
2. Tap **Learn button**, then press the hardware key. The app fills in the device name, scan code, and suggested Android keycode.
3. Pick an action (screenshot, key event, key combo, activity, device control, broadcast, or passthrough).
4. Save.

Learn mode uses the raw evdev path (MSC_SCAN), so it works for keys that Android does not always deliver as normal KeyEvents (for example Dell WMI hotkeys).

## Actions

| Action | Use for |
|--------|---------|
| `screenshot` | Capture the screen |
| `keyevent` | Emit a single Android keycode |
| `keycombo` | Emit a combo such as `alt+KEYCODE_TAB` |
| `activity` | Launch a component |
| `device_control` | Brightness, volume, Wi-Fi, Bluetooth, and other toggles |
| `broadcast` | Send an intent (for example dump logs) |
| `passthrough` | Let the key through to Android unchanged |

Config field details: [Config Format](CONFIG_FORMAT.md).  
AIDL and `cmd` reference: [AIDL Interface](AIDL_INTERFACE.md).

## Common ADB commands

```bash
adb shell cmd ax86_btnmgr list
adb shell cmd ax86_btnmgr reload
adb shell cmd ax86_btnmgr export /sdcard/ax86_btn_manager.conf
adb shell cmd ax86_btnmgr import /data/misc/ax86_btn_manager.conf --merge
```

Push a hand-edited config and reload:

```bash
adb push ax86_btn_manager.conf /data/misc/
adb shell cmd ax86_btnmgr reload
```

## Dump logs from a hardware key

If the build also includes [Ax86 Logger](../Ax86Logger/Ax86Logger.md), map a button to **broadcast** with intent:

```text
com.ax86.logger.action.DUMP_LOGS
```

Pressing that key copies the rolling logs to a mounted USB drive.

## Build

```bash
./build.sh --btnmgr ...
```

## Related

* [Config Format](CONFIG_FORMAT.md)
* [AIDL Interface](AIDL_INTERFACE.md)
* [Ax86 Logger](../Ax86Logger/Ax86Logger.md)
* [Building Bass OS](../../development/building-bass.md)
