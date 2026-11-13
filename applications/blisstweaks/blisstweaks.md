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

## Feature flag tabs

The Desktop, Windowing, Multitasking, Surfaces, Display mgr, Large screen, Launcher3 and
SystemUI tabs list Android's switchable feature flags (aconfig flags in `device_config`), one
switch per flag, built from `res/xml/bliss_settings_aconfig.xml`. Each switch shows the flag's
live value.

* Only flags that can change at runtime (`READ_WRITE`) are listed. Read-only flags are fixed in
  the image.
* Launcher3 and SystemUI flags apply once that process restarts (Bliss Tweaks says so after
  saving). The others need a reboot.
* The list is generated for each build from the flags that build ships, so it changes with the
  Android version.

See [Feature Flags (aconfig)](../../development/aconfig-flags.md) for how the list is made and
how to regenerate it.

## Related

* [Display Mapper](../BlissDisplayMapper/BlissDisplayMapper.md)
* [Boot Config](../BootConfig/BootConfig.md)
* [Feature Flags (aconfig)](../../development/aconfig-flags.md)
* [Building Bass OS](../../development/building-bass.md)
