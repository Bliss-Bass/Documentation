# Bliss Tweaks

Bliss Tweaks lives under **Settings → System** and exposes low-level properties, secure settings, and window manager flags without needing an ADB shell. Included with `--extras`.

The UI is built from `res/xml/bliss_settings.xml` (switches and text fields for comma-separated display lists).

## Categories

### Launcher

* Disable primary or secondary taskbars
* Pin the taskbar
* Toggle the launcher desktop mode state

### Display

Useful for kiosks and presentations:

* Force displays as Presentation, Trusted, Secure, or Private
* Disable external presentation displays
* Disable scaling on specific displays

Fields that take display lists use comma-separated IDs (example: `1,2`).

### WindowManager

* Force freeform or fullscreen windowing
* Desktop experience developer options
* Window shadows, rounded corners, veiled resizing
* Live wallpapers in desktop mode
* Force desktop mode onto external displays

### Other

* Allow secure overlay settings
* Bypass alert-window restrictions in low-RAM situations

## How changes are stored

Depending on the tweak type, values go to:

| Type | Target |
|------|--------|
| `system_property` | `SystemProperties` (example: `persist.wm.debug.*`) |
| `global` | `Settings.Global` |
| `secure` | `Settings.Secure` |
| `system` | `Settings.System` |

`persist.*` changes often need a Settings restart or a full reboot before they stick.

## Related

* [Display Mapper](../BlissDisplayMapper/BlissDisplayMapper.md)
* [Boot Config](../BootConfig/BootConfig.md)
* [Building Bass OS](../../development/building-bass.md)
