# BootSight

BootSight is the Bass fleet and license UI used on images that manage devices through **Bass's own fleet backend** rather than a third-party MDM. On those images it shows up in Settings as **Device Status**, handles license checks, and can show an overlay banner or popup when a demo period expires or a device is unlicensed.

| | |
|---|---|
| **Package** | `com.bliss.bootsight` |
| **Settings entry** | Device Status |

See [Fleet Management](../../features/fleet-management.md) for how BootSight fits next to third-party MDM images.

## What you get

* Device Status screen with product serial and license state
* Device admin and overlay permissions set up at boot
* Optional overlay style: banner or popup

## License activation

Use Device Status to read the serial and check license state after purchase. Full steps: [License Activation](../../setup_and_configuration/license-activation.md).

Quick serial check over ADB:

```bash
adb shell getprop ro.bliss.serialnumber
```

## Overlay style

| Property | Purpose |
|----------|---------|
| `ro.bootsight.banner_type` | Image default (`banner` or `popup`) |
| `persist.bass.bootsight.banner_type` | Persisted overlay style |

## When BootSight is not on the image

Images prepared for a **third-party MDM** (or unmanaged consumer / lab images) do not include BootSight, so Settings will not show Device Status. Use the MDM console for fleet identity on those SKUs, or ask your Bass contact which management path your image uses.

## Related

* [Fleet Management](../../features/fleet-management.md)
* [License Activation](../../setup_and_configuration/license-activation.md)
