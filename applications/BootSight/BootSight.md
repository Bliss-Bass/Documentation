# BootSight

BootSight is the Bass fleet and license UI used on builds that manage devices through BootSight rather than a third-party MDM. On those builds it shows up in Settings as **Device Status**, handles license checks, and can show an overlay banner or popup when a demo period expires or a device is unlicensed.

| | |
|---|---|
| **Package** | `com.bliss.bootsight` |
| **Build flag** | `--bootsight` (`USE_BOOTSIGHT=true`) |
| **Fleet property** | `ro.bass.fleet_mgmt=bootsight` |
| **Settings entry** | Device Status |

`--bootsight` is independent of `--extras`. Including BootSight also sets the fleet policy to `bootsight`. See [Fleet Management](../../features/fleet-management.md).

## What you get

* Device Status screen with product serial and license state
* Device admin and overlay permissions set up at boot
* Optional overlay style: banner or popup
* Watchdog scripts that only run when `ro.bass.fleet_mgmt` is `bootsight`

## License activation

Use Device Status to read the serial and check license state after purchase. Full steps: [License Activation](../../setup_and_configuration/license-activation.md).

Quick serial check over ADB:

```bash
adb shell getprop ro.bliss.serialnumber
```

## Overlay style

At build time:

```bash
./build.sh --bootsight --bsbanner ...
./build.sh --bootsight --bspopup ...
```

| Flag | Effect |
|------|--------|
| `--bsbanner` | Overlay banner (implies `--bootsight`) |
| `--bspopup` | Overlay popup (implies `--bootsight`) |

Runtime / product props:

| Property | Purpose |
|----------|---------|
| `ro.bootsight.banner_type` | Build-time default (`banner` or `popup`) |
| `persist.bass.bootsight.banner_type` | Persisted overlay style |

## When BootSight is not included

If the fleet uses an MDM instead, build with `--fleet-mgmt=mdm` and do **not** pass `--bootsight`. BootSight init and watchdog scripts exit early unless `ro.bass.fleet_mgmt` is `bootsight`, so they will not run on MDM or `none` builds even if leftover files are present.

## Related

* [Fleet Management](../../features/fleet-management.md)
* [License Activation](../../setup_and_configuration/license-activation.md)
* [Building Bass OS](../../development/building-bass.md)
