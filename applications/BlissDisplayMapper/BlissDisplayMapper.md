# Bliss Display Mapper

Display Mapper controls resolution, DPI, and orientation for the built-in panel and external monitors. Open it from Settings on builds that include `--extras`.

| | |
|---|---|
| **Package** | BlissDisplayMapper (privileged / platform-signed) |
| **Build** | Included with `--extras` |
| **Background service** | `OrientationService` (applies saved rules on boot and hotplug) |

## What you can set

* Per-display resolution and DPI
* Per-display orientation (portrait, landscape, reverse, sensor)
* Global / hardware rotation overrides
* HDMI rotation lock and single-display mode
* Show or hide the software navigation bar (`mainkeys`)

When a new display is plugged in, the background service applies any saved orientation rules for that display.

## Properties

| Property | Description |
|----------|-------------|
| `persist.ax86.display.<ID>.resolution` | Resolution for display ID |
| `persist.ax86.display.<ID>.dpi` | Density (DPI) for display ID |
| `persist.ax86.display.<ID>.orientation` | Orientation lock for display ID |
| `persist.debug.per_window_input_rotation` | Per-window input rotation |
| `persist.sys.app.rotation` | App rotation policy |
| `ro.sf.hwrotation` | SurfaceFlinger hardware rotation |
| `persist.ax86.display.hdmirotationlock` | Lock rotation on HDMI displays |
| `persist.ax86.hw.mainkeys` | Nav bar: `0` show, `1` hide |

Most changes are made from the UI. Properties are listed here for scripting and support.

## Related

* [Touch Mapper](../BlissTouchMapper/BlissTouchMapper.md) for binding inputs to displays
* [Bliss Tweaks](../BlissTweaks/BlissTweaks.md) for window manager / desktop flags
* [Building Bass OS](../../development/building-bass.md)
