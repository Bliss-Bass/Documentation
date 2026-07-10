# Bliss Touch Mapper (Input Mapper)

Touch Mapper binds USB touchscreens, mice, touchpads, and keyboards to specific displays. It can also flip inverted X/Y axes on mismatched digitizers. Included with `--extras`.

| | |
|---|---|
| **Settings UI** | Maps devices visually and can write `input-port-addon.xml` |
| **Build** | Included with `--extras` |
| **Hotplug** | `DisplayMonitorService` keeps bindings when monitors come and go |

## Map by vendor / product ID (slots 1 to 8)

Properties live under `persist.ax86.*` and survive reboot.

### Touchscreens

```bash
adb shell setprop persist.ax86.touch.1.vendor "27c6"
adb shell setprop persist.ax86.touch.1.product "0118"
adb shell setprop persist.ax86.touch.1.display "local:1"
adb shell setprop persist.ax86.touch.1.orientation "0"
adb shell setprop persist.ax86.touch.1.flip_x "0"
adb shell setprop persist.ax86.touch.1.flip_y "1"
```

### Other input types

| Namespace | Devices |
|-----------|---------|
| `persist.ax86.pointer.<SLOT>.*` | Mice / touchpads |
| `persist.ax86.keyboard.<SLOT>.*` | Physical keyboards |
| `persist.ax86.input.<SLOT>.*` | Generic inputs |

### Apply

Regenerate `.idc` files and refresh the input reader:

```bash
adb shell setprop sys.ax86.touch.update 1
```

Use `pointer`, `keyboard`, or `input` in place of `touch` when that is the namespace you changed.

## Map by USB port (`input-port-addon.xml`)

When two devices share the same vendor/product ID (identical dual monitors, for example), map by USB topology instead.

Touch Mapper bind-mounts `/data/misc/input-port-addon.xml` over `/vendor/etc/input-port-associations.xml` at boot. The Settings UI can generate and save that file.

Step-by-step port discovery: [Creating an input-port-addon.xml file](../../setup_and_configuration/input-port-associations.md).

Related IDC addon notes: [Using IDC Addon](../../setup_and_configuration/addon_idc.md).

## Related

* [Display Mapper](../BlissDisplayMapper/BlissDisplayMapper.md)
* [Button Manager](../Ax86ButtonManager/Ax86ButtonManager.md) for hardware function keys (P1/P2/P3)
* [Building Bass OS](../../development/building-bass.md)
