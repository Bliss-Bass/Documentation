# Bliss Config Overrides

Config Overrides lets you push flat config files to `/data/misc/` and have the device apply them on boot (or on demand). Useful for provisioning without an MDM or a custom setup app.

Included with `--extras`.

| | |
|---|---|
| **Trigger prop** | `persist.ax86.update_configs` |
| **Config location** | `/data/misc/` |
| **Example files** | [examples/](examples/) (from `vendor/ax86-lite/docs/examples`) |

## Supported files (BlissConfigOverrides)

Push these to `/data/misc/` (example: `adb push settings_system.conf /data/misc/`), then trigger an update or reboot.

| File | Applied by | Format |
|------|------------|--------|
| `settings_global.conf` | BlissConfigOverrides | `key=value` → `settings put global` |
| `settings_system.conf` | BlissConfigOverrides | `key=value` → `settings put system` |
| `settings_secure.conf` | BlissConfigOverrides | `key=value` → `settings put secure` |
| `runtime_props.conf` | BlissConfigOverrides | `key=value` → `setprop` |
| `device_config.conf` | BlissConfigOverrides | `namespace/key=value` → `device_config put` |

Lines starting with `#` and blank lines are ignored.

### Apply without reboot

```bash
adb shell setprop persist.ax86.update_configs 1
```

The system resets that property back to `0` when it finishes. The same files are also processed on `boot_completed`.

## Example: settings_global.conf

Full file: [examples/settings_global.conf](examples/settings_global.conf)

```ini
# Developer Options
development_settings_enabled=1
adb_enabled=1
adb_wifi_enabled=1

# Power & Multi-Display
stay_on_while_plugged_in=3
force_desktop_mode_on_external_displays=1
force_allow_on_external=1

# Time & Connectivity
time_zone=America/New_York
```

## Example: settings_system.conf

Full file: [examples/settings_system.conf](examples/settings_system.conf)

```ini
# Display & UI (brightness 0-255, timeouts in ms)
screen_brightness=128
screen_off_timeout=60000
sleep_timeout=86400000
accelerometer_rotation=0

# Time
time_12_24=24
```

## Example: settings_secure.conf

Full file: [examples/settings_secure.conf](examples/settings_secure.conf)

```ini
default_input_method=com.android.inputmethod.latin/.LatinIME
lock_screen_show_notifications=1
```

## Example: runtime_props.conf

Full file: [examples/runtime_props.conf](examples/runtime_props.conf)

```ini
# Display overrides
persist.ax86.display.1.resolution=1280x720
persist.ax86.display.1.orientation=1
persist.ax86.display.1.dpi=160

# Touchscreen mapping (slots 1-8)
persist.ax86.touch.1.vendor=27c6
persist.ax86.touch.1.product=0118
persist.ax86.touch.1.display=local:1
persist.ax86.touch.1.flip_y=1
persist.ax86.touch.1.orientation=1

# Radios / mock location
persist.ax86.wifi.enabled=1
persist.ax86.bluetooth.enabled=0
persist.ax86.gps.enabled=1
persist.ax86.location.lat=40.7128
persist.ax86.location.lon=-74.0060
```

After changing touch props, you may also need:

```bash
adb shell setprop sys.ax86.touch.update 1
```

See [Touch Mapper](../BlissTouchMapper/BlissTouchMapper.md).

## Example: device_config.conf

Full file: [examples/device_config.conf](examples/device_config.conf)

```ini
# Format: namespace/key=value
lse_desktop_experience/com.android.window.flags.enable_desktop_windowing=true
lse_desktop_experience/com.android.window.flags.enable_desktop_windowing_persistence=true
lse_desktop_experience/com.android.window.flags.enable_desktop_launcher=true
lse_desktop_experience/com.android.window.flags.enable_presentation_for_connected_displays=true
```

## Early-init: custom_device.prop

`ro.*` identity and other early properties must be set before the framework starts. Those go in `/data/misc/custom_device.prop` and are handled by the ramdisk `addon_init.sh` path (not BlissConfigOverrides). Push the file and **reboot**.

Full file: [examples/custom_device.prop](examples/custom_device.prop)

```ini
ro.product.manufacturer=BlissLabs
ro.product.model=Custom Arcade Cabinet
qemu.hw.mainkeys=1
ro.sf.lcd_density=240

persist.ax86.display.0.resolution=1920x1080
persist.ax86.display.0.dpi=240
persist.ax86.display.0.orientation=1
```

## Older example: custom_settings.conf

[examples/custom_settings.conf](examples/custom_settings.conf) is kept as a sample of a simplified provisioning layout (`device_name`, `language`, `ime_management`, and so on). BlissConfigOverrides does **not** read that filename today. Prefer the `settings_*.conf` / `runtime_props.conf` / `device_config.conf` files above.

## Quick push workflow

```bash
adb root
adb remount   # if needed for other paths; /data/misc is writable
adb push settings_global.conf /data/misc/
adb push settings_system.conf /data/misc/
adb push settings_secure.conf /data/misc/
adb push runtime_props.conf /data/misc/
adb push device_config.conf /data/misc/
adb shell setprop persist.ax86.update_configs 1
```

For `custom_device.prop`:

```bash
adb push custom_device.prop /data/misc/
adb reboot
```

## Related

* [examples/](examples/) full sample files
* [Touch Mapper](../BlissTouchMapper/BlissTouchMapper.md)
* [Display Mapper](../BlissDisplayMapper/BlissDisplayMapper.md)
* [Boot Config](../BootConfig/BootConfig.md)
* [Building Bass OS](../../development/building-bass.md)
