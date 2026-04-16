# IDC Addon

## Input Device Configuration files from data

This addon allows us to place idc files in data/system/devices/idc
and if found, will bind mount them to system/usr/idc

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
Once you have your IDC file created, make sure you are using a Bass OS build with the IDC Addon or an AIO (All In One) build, and verify you have the following added to the kernel cmdline or install options:
`ADDON_IDC=1`

Then use ADB root to push it to the device (you may need to use mkdir to create the folder if not found):
```bash
adb connect 192.168.x.xxx:xxxx
adb root
adb push Vendor_0eef_Product_c005.idc data/system/devices/idc/Vendor_0eef_Product_c005.idc
```

Then reboot to test. If working, you will see your device show up in `dumpsys input` and `getevent -i`
