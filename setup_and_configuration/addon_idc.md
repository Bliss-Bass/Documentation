# IDC Addon (Lineout runtime override)

## Input Device Configuration files from data

This is a **Bass: Lineout** runtime override (part of `addon_init`), not a legacy Bass `private/addons/` package.

Place `.idc` files under `/data/system/devices/idc`. When enabled, early init bind-mounts them so Android's input stack picks them up (same idea as stock `/system/usr/idc`, but writable after install).

Full Lineout addon model: [Addon Development: Bass Lineout](../development/addon-development.md).  
Legacy Bass private addons: [Addon Development: Legacy Bass OS](../development/addon-development-legacy-bass.md).

## What you will need

You will first need to find the USB ID for your touchscreen:
```bash
adb connect
adb root
adb shell lsusb > lsusb.log
```

You should see the ID of your USB connected touchscreen device in the results. 
Example:
`EETI8082:00 0EEF:C005`

So you would then take that and create a new .idc file using the last 2 places (vendor:product):
Example:
`Vendor_0eef_Product_c005.idc`
And edit its contents with the following:
```bash
device.internal = 1
touch.deviceType = touchScreen

```
Once you have your IDC file created, make sure you are using a Lineout build that includes the IDC addon path, and verify you have the following added to the kernel cmdline or install options:
`ADDON_IDC=1`

Then use ADB root to push it to the device (you may need to use mkdir to create the folder if not found):
```bash
adb connect 192.168.x.xxx:xxxx
adb root
adb push Vendor_0eef_Product_c005.idc data/system/devices/idc/Vendor_0eef_Product_c005.idc
```

Then reboot to test. If working, you will see your device show up in `dumpsys input` and `getevent -i`

## Related

* [Addon Development: Bass Lineout](../development/addon-development.md)
* [Bliss Touch Mapper](../applications/BlissTouchMapper/BlissTouchMapper.md) (property-based mapping on `--extras` builds)
* [Creating an input-port-addon.xml file](input-port-associations.md)
