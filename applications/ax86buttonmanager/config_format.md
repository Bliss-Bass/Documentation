# Button Manager Config Format

INI-style config at `/data/misc/ax86_btn_manager.conf`. This file is the source of truth. Keylayout (`.kl`) overlays under `/data/system/devices/keylayout/` are generated from it and are not meant to be edited by hand.

## Top level

```ini
version=1
```

## Button sections

One `[button.<id>]` section per mapping.

| Field | Required | Description |
|-------|----------|-------------|
| `label` | no | Name shown in the UI |
| `device_match` | yes | Input device name, or `*` for any device |
| `scan_code` | for intercept | evdev scan code, hex (`0x190`) or decimal |
| `android_key` | no | Symbolic Android keycode. Prefer `KEYCODE_BUTTON_1` through `KEYCODE_BUTTON_16` for hardware P-keys |
| `action` | yes | `screenshot`, `keyevent`, `keycombo`, `activity`, `device_control`, `broadcast`, `passthrough` |
| `long_press` | no | `true` / `false` |

### Action-specific fields

| Action | Fields |
|--------|--------|
| `keyevent` | `emit_key=KEYCODE_*` (falls back to `android_key`) |
| `keycombo` | `keys=ctrl+alt+backspace` |
| `activity` | `component=pkg/.Activity`, optional `flags=NEW_TASK` |
| `device_control` | `control=...` plus control params |
| `broadcast` | `intent=<action>`, optional `component=pkg/.Receiver` |

### device_control params

Percent values are 0-100.

| `control` | Params |
|-----------|--------|
| `brightness_toggle` | `low`, `high` |
| `brightness_set` | `level` |
| `volume_up` / `volume_down` | `stream` (media/ring/alarm/notification/system), `step` |
| `volume_mute_toggle` | `stream` |
| `volume_set` | `stream`, `level` |
| `rotation_lock_toggle`, `auto_brightness_toggle`, `night_mode_toggle`, `screen_timeout_cycle`, `wifi_toggle`, `bluetooth_toggle`, `airplane_mode_toggle`, `location_toggle`, `mic_mute_toggle`, `ringer_mode_cycle`, `speakerphone_toggle`, `dnd_toggle`, `media_play_pause`, `media_next`, `media_previous`, `lock_screen`, `show_touches_toggle` | none required |

## Global section

```ini
[global]
intercept_mode=consume
reload_on_boot=true
```

## Android keycodes and `.kl` overlays

For hardware function keys (P1/P2/P3), use **`KEYCODE_BUTTON_1` through `KEYCODE_BUTTON_16`**. Those produce valid `.kl` labels (`BUTTON_1`, and so on). `KEYCODE_F1` through `F12` also work. Names like `PROG1` are not valid `.kl` labels.

## Example

```ini
[button.P4]
label=Brightness
device_match=*
scan_code=0x193
action=device_control
control=brightness_toggle
low=0
high=100
```

## Apply / reload

```bash
adb push ax86_btn_manager.conf /data/misc/
adb shell cmd ax86_btnmgr reload
```

Or:

```bash
adb shell setprop persist.ax86.btnmgr.reload 1
```

## Related

* [Button Manager](Ax86ButtonManager.md)
* [AIDL Interface](AIDL_INTERFACE.md)
