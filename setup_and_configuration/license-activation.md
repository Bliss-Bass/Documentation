# License Activation

Some of the Bass OS builds do require licensing activation. After contacting us with your device serial numbers and purchasing a license, there are a few different ways it can be activated.

On builds that include [BootSight](../applications/BootSight/BootSight.md) (`--bootsight`, `ro.bass.fleet_mgmt=bootsight`), the on-device path is Settings → **Device Status**. Builds that use an MDM instead (`--fleet-mgmt=mdm`) will not show that entry. See [Fleet Management](../features/fleet-management.md).

### Option A: On Device

Start off by going into Android Settings
![Screenshot_20241107-131404_Settings](https://github.com/user-attachments/assets/fca68559-9dfe-4b29-9f35-f47dcc30ccec)

Then scroll down to the Device Status option (if it is not showing, close Settings and re-open)
![Screenshot_20241107-131417_Settings](https://github.com/user-attachments/assets/85c94a0e-bfee-4f95-9c1e-b06a2b75a0db)

After selecting the Device Status activity, you can see your product serial number here. This is the serial number you will need to report to us with in order for us to register your device. 
![Screenshot_20241107-131424_Bootsight](https://github.com/user-attachments/assets/ec426531-0da8-4f80-9b22-595062f679a2)

Once reported and license is purchased, you can click on the "Check Device Status" button to check it's activation status. Once activated, the screen will reflect the status by showing as "Licensed"

### Option B: Using ADB

Connect to the device using ADB, and run the following command to collect its serial number:
 
 `adb shell getprop ro.bliss.serialnumber`

### Option C: Offline Activation (no internet)

Some builds are configured for offline licensing (`persist.bass.bootsight.offline_licensing=1`, produced by `build.sh --bs-offline`). These devices never contact the license server and send no telemetry. They are activated with a signed license file or an activation code instead.

Offline licenses are cryptographically signed and bound to each device's serial and SKU, so a code only activates the device it was issued for and cannot be reused on another device. If a licensed disk image is cloned to different hardware, it reverts to unlicensed on that hardware.

There are two ways to apply an offline license:

**1. Drop a license file (best for fleets)**

We provide a single `license.pack` file covering every serial you purchased. The same file can be placed on every device; each device automatically picks the entry that matches its own serial. Push it into the BootSight data directory:

```
adb push license.pack /data/misc/bootsight/license.pack
```

The device picks up the file within a few seconds (no reboot needed) and shows as **Licensed**. Provisioning scripts or factory imaging can place the file at the same path. Individual per-device `<serial>.lic` files are also accepted.

**2. Enter or scan an activation code**

On the device, go to Settings → **Device Status** → **Enter activation code**. Then either:

- Scan the QR label for that device with a USB barcode scanner (it types the code automatically), or
- Type or paste the activation code issued for that device.

Once verified, the device shows as **Licensed** immediately.

To obtain offline licenses, gather your device serial numbers (Option A or B above) and send them to us with your purchase; we return a `license.pack` (and printable QR labels on request). See [Fleet Management](../features/fleet-management.md) for bulk workflows.

## License Payment

### Single Device Licensing

We offer an easy method to purchase single device licenses through our website here: [BassOS Single Device Licensing](https://bassos.navotpala.tech/licensing/#device-license)

### Bulk Licensing

We require a licensing contract for any more than 10 licenses. Follow the steps above to gather the serial numbers required, and contact us at [info@navotpala.tech](mailto:info@navotpala.tech?subject=Licensing) with all the serial numbers you want to register. Once payment is confirmed, we will activate the license for each serial shared and send you a response when complete. 

From there, you can manually navigate each device to Settings > Device Status & check license status from there, reboot each device, or use adb to reboot each device for it to confirm it's license status once it reconnects to the internet:

```
adb root
adb shell reboot -f
```

We also offer bulk license management through our Access Guard application which is available through contract only. For more info on that service, please contact us at [info@navotpala.tech](mailto:info@navotpala.tech?subject=Access Guard Licensing) and express your interest. 
