# ADB Client Mode Overrides (Lineout)

This is a **Bass: Lineout** runtime override (`addon_init` / `set_usb_mode`), not a legacy Bass `private/addons/` package.

`FORCE_USE_ADB_CLIENT_MODE` is a GRUB / kernel command-line flag. At boot, `addon_peripherals.sh` maps it to Android properties. This page lists those properties and how to turn ADB **off** and **on** again at runtime.

| | |
|---|---|
| **Product** | Bass: Lineout (`vendor/ax86-lite`) |
| **Cmdline / `setprop`** | All Lineout images (core `addon_init`) |
| **File overlays** (`runtime_props.conf`, `settings_*.conf`, `persist.ax86.update_configs`) | Included with `--extras` ([Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md)) |
| **`--adbi`** | Uses mode `2` (USB `mtp,adb` + TCP 5555) |

Classic Bass OS does **not** use this `addon_init` path. Config file overlays and the master trigger are **not** on Lineout builds without `--extras`.

Full Lineout addon model: [Addon Development: Bass Lineout](../development/addon-development.md).  
Legacy Bass private addons: [Addon Development: Legacy Bass OS](../development/addon-development-legacy-bass.md).

## Command-line flag

Append to the kernel line:

```
FORCE_USE_ADB_CLIENT_MODE=<0|1|2|3>
```

Dynamic (`persist.*` / `service.*`) values are also written to `/data/misc/runtime_props.conf`. `ro.*` values are also written to `/data/vendor/device.prop`.

### Mode `0` — ADB off / secure

| Property | Value |
|----------|-------|
| `persist.usb.debug` | `0` |
| `persist.adb.notify` | `1` |
| `persist.sys.usb.config` | `mtp` |
| `ro.secure` | `1` |
| `ro.adb.secure` | `1` |
| `ro.debuggable` | `0` |
| `service.adb.root` | `0` |
| `persist.sys.root_access` | `0` |
| `persist.service.adb.enable` | `0` |

No `service.adb.tcp.port`.

### Modes `1`, `2`, `3` — insecure / root ADB

All three set the same properties:

| Property | Value |
|----------|-------|
| `persist.usb.debug` | `1` |
| `persist.adb.notify` | `0` |
| `persist.sys.usb.config` | `mtp,adb` |
| `ro.secure` | `0` |
| `ro.adb.secure` | `0` |
| `ro.debuggable` | `1` |
| `service.adb.root` | `1` |
| `persist.sys.root_access` | `1` |
| `persist.service.adb.enable` | `1` |
| `service.adb.tcp.port` | `5555` |

Mode `3` also sets Settings (not `setprop`):

```bash
settings put global adb_enabled 1
settings put global adb_wifi_enabled 1
```

`ro.secure`, `ro.adb.secure`, and `ro.debuggable` are applied at boot and do not reliably change later. After boot, toggle ADB with the persist/service properties and restart `adbd`.

---

## Turn ADB off and on at runtime

Needs a rooted shell (`adb root`, or local/UART if you are about to disable TCP ADB).

### Immediate `setprop`

**Off** (same as mode `0`, without the `ro.*` bits):

```bash
adb shell setprop persist.usb.debug 0
adb shell setprop persist.adb.notify 1
adb shell setprop persist.sys.usb.config mtp
adb shell setprop service.adb.root 0
adb shell setprop persist.sys.root_access 0
adb shell setprop persist.service.adb.enable 0
adb shell setprop service.adb.tcp.port 0
adb shell settings put global adb_enabled 0
adb shell settings put global adb_wifi_enabled 0
adb shell setprop ctl.restart adbd
```

**On** (same as modes `1` / `2` / `3`):

```bash
adb shell setprop persist.usb.debug 1
adb shell setprop persist.adb.notify 0
adb shell setprop persist.sys.usb.config mtp,adb
adb shell setprop service.adb.root 1
adb shell setprop persist.sys.root_access 1
adb shell setprop persist.service.adb.enable 1
adb shell setprop service.adb.tcp.port 5555
adb shell settings put global adb_enabled 1
adb shell settings put global adb_wifi_enabled 1
adb shell setprop ctl.restart adbd
```

If the only session is **TCP ADB**, turning it off drops that connection. Use USB ADB, or turn it back on from a local shell / UART.

### Persistent: `runtime_props.conf` (`--extras` only)

File-based overlays require [Bliss Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md), which ships on Lineout builds that include **`--extras`**. Without that flag, `persist.ax86.update_configs` will not apply `runtime_props.conf` / `settings_*.conf` — use immediate `setprop` above, or set `FORCE_USE_ADB_CLIENT_MODE` on the kernel command line and reboot.

On `--extras` images, BlissConfigOverrides applies `/data/misc/runtime_props.conf` on `boot_completed` and when you fire the master trigger.

**Off** — `/data/misc/runtime_props.conf`:

```ini
persist.usb.debug=0
persist.adb.notify=1
persist.sys.usb.config=mtp
service.adb.root=0
persist.sys.root_access=0
persist.service.adb.enable=0
service.adb.tcp.port=0
```

**On:**

```ini
persist.usb.debug=1
persist.adb.notify=0
persist.sys.usb.config=mtp,adb
service.adb.root=1
persist.sys.root_access=1
persist.service.adb.enable=1
service.adb.tcp.port=5555
```

From the host:

```bash
adb root
adb push runtime_props.conf /data/misc/runtime_props.conf
```

Optional Settings extras (mode `3`) in `/data/misc/settings_global.conf`:

```ini
adb_enabled=1
adb_wifi_enabled=1
```

Use `0` to disable.

Apply without reboot, then bounce `adbd`:

```bash
adb shell setprop persist.ax86.update_configs 1
adb shell setprop ctl.restart adbd
```

Init resets `persist.ax86.update_configs` to `0` when it finishes. Conf files are only reapplied if they are **newer** than `/data/misc/.custom_settings_applied` — push or touch the file after edits.

## Caveats

- `FORCE_USE_ADB_CLIENT_MODE` itself is cmdline-only. Changing the mode number requires a reboot.
- If GRUB still has `FORCE_USE_ADB_CLIENT_MODE=1|2|3`, boot will **append** the “on” values into `runtime_props.conf`. Last matching line wins when the file is applied. For a lasting off, set the cmdline to `0` or keep the off block last in the file.
- `ctl.restart adbd` is required. Writing props or the conf file alone does not always restart the daemon.
- `runtime_props.conf` / `settings_global.conf` / `persist.ax86.update_configs` only work on Lineout **`--extras`** builds.

## Related

* [Configuration through Command Line Parameters](Configuration-through-Command-Line-Parameters.md)
* [Bliss Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md) (`--extras`)
* [Addon Development: Bass Lineout](../development/addon-development.md)
* [Building Bass OS](../development/building-bass.md) (`--extras`, `--adbi`)
