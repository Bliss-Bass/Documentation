# License Activation

Some of the Bass OS builds do require licensing activation. After contacting us with your device serial numbers and purchasing a license, there are a few different ways it can be activated.

On images that include [BootSight](../applications/BootSight/BootSight.md) (Bass fleet backend), the on-device path is Settings → **Device Status**. Images prepared for a third-party MDM will not show that entry. See [Fleet Management](../features/fleet-management.md).

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

**Virtual machines and clones:** Each VM guest or rebuilt instance is a separate Device for licensing, even on the same hypervisor host. Pinning or copying default product / platform identity settings so multiple instances share one licensing identity does **not** let one single-device license cover a fleet. Those deployments need bulk or buyout licensing. Self-hosted or redirected OTA/update feeds are not included with a standard Device license; they require an OTA service or custom-build agreement.

**Offline packs:** You may place the same `license.pack` on every Device whose serial you purchased. Do not redistribute packs or codes to activate serials you did not buy.

**Evaluation builds:** Supported demo images may include paid addons for testing (see the Downloads site). That is not a production license; see [Licensing](../legal/licensing.md) and the [EULA](../legal/END_USER_LICENSE_AGREEMENT.md).

**Seat replacement:** For permanent hardware replacement or a same-seat rebuild, contact us to reassign the seat; running old and new instances together still needs two seats.

There are three ways to apply an offline license:

**1. USB drive + Files app (no ADB, no network)**

We provide a single `license.pack` file covering every serial you purchased. The same file can be placed on every device; each device automatically picks the entry that matches its own serial. Individual per-device `<serial>.lic` files are also accepted.

1. Copy `license.pack` (or the device's `.lic` file) to a USB drive and plug it into the device.
2. Either leave it on the drive, or use the Android **Files** app to copy it to the **Download** or **Documents** folder on the device.
3. If it was copied to Download/Documents, the device picks it up automatically within a few seconds. If it is still on the USB drive, go to Settings → **Device Status** → **Scan drives for license file**; BootSight scans any connected USB drives (and the Download/Documents folders) and activates on the spot.

The screen shows as **Licensed** immediately, with no reboot needed. The license is copied to internal storage during activation, so the USB drive can be removed afterwards.

**2. Drop the file with ADB (best for provisioning scripts)**

Push the same pack into the BootSight data directory:

```
adb push license.pack /data/misc/bootsight/license.pack
```

The device picks up the file within a few seconds and shows as **Licensed**. Provisioning scripts or factory imaging can place the file at the same path.

**3. Enter or scan an activation code**

On the device, go to Settings → **Device Status** → **Enter activation code**. Then either:

- Scan the QR label for that device with a USB barcode scanner (it types the code automatically), or
- Type or paste the activation code issued for that device.

Once verified, the device shows as **Licensed** immediately.

To obtain offline licenses, gather your device serial numbers (Option A or B above) and send them to us with your purchase; we return a `license.pack` (and printable QR labels on request). See [Fleet Management](../features/fleet-management.md) for bulk workflows.

## License Payment

### Single Device Licensing

We offer an easy method to purchase single device licenses through our website here: [BassOS Single Device Licensing](https://bassos.navotpala.tech/licensing/#device-license)

Use this path for one physical machine or one VM guest. It does not cover multi-VM fleets, cloned images used as additional instances, operating your own OTA/update servers, full white-label / Custom Build branding beyond the Evaluation Build boot-animation / wallpaper / kiosk-logo options, or preinstalling Bass on hardware you sell (OEM / redistribution).

### Bulk Licensing

We require a licensing contract for any more than 10 licenses, and for any multi-VM / multi-instance production deployment (including when guests are cloned or identity fields are held constant). Follow the steps above to gather the serial numbers required, and contact us at [info@navotpala.tech](mailto:info@navotpala.tech?subject=Licensing) with all the serial numbers you want to register. Once payment is confirmed, we will activate the license for each serial shared and send you a response when complete.

For fleets that need private update delivery or a company-specific updater feed, ask about an **OTA service** / custom-build agreement in the same conversation (or email subject line `OTA Service Licensing`). 

From there, you can manually navigate each device to Settings > Device Status & check license status from there, reboot each device, or use adb to reboot each device for it to confirm it's license status once it reconnects to the internet:

```
adb root
adb shell reboot -f
```

We also offer bulk license management through our Access Guard application which is available through contract only. For more info on that service, please contact us at [info@navotpala.tech](mailto:info@navotpala.tech?subject=Access Guard Licensing) and express your interest. 
