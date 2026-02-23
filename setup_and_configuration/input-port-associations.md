# Creating an input-port-addon.xml file

## Steps to Configure Input-Display Associations

### Update the build config for the input-ports-addon:
Use the Boot Config editor from Settings > System to enable/add the following boot flag, or select the following boot flag from the installer during a fresh install:
```bash
BLISS_INPUT_PORTS_ADDON=1
```
### Obtain Display Port Numbers:
Use the dumpsys SurfaceFlinger command via adb shell to find the port numbers assigned to the connected displays.
```bash
adb shell dumpsys SurfaceFlinger --display-id
```
This command will output information like:
- Display 4693505326422272 (HWC display 0): port=0 ...
- Display 4693505326422273 (HWC display 1): port=1 ...

### Obtain Input Device Locations:
Use the getevent command via adb shell to find the unique "location" string for the touch input devices.
```bash
adb shell getevent -i | grep location
```
This command will output information like:
- location: "usb-xhci-hcd.0.auto-1.1/input0"
- location: "usb-xhci-hcd.0.auto-1.2/input0"

### Edit the input-port-addon.xml file:
Create the file to update the associations between the display ports and input locations.Example XML structure:
```xml
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<input-port-associations>
    <!-- Bind input device with location "usb-xhci-hcd.0.auto-1.1/input0" to display port "0" -->
    <port display="0" input="usb-0000:00:14.0-7.3.4/input0" />
    <!-- Bind input device with location "usb-xhci-hcd.0.auto-1.2/input0" to display port "1" -->
    <port display="1" input="usb-0000:00:14.0-7.2.4/input0" />
</input-port-associations>
```
### Push the change to the device:
Connect to the device using ADB and run the following commands:
```bash
adb root
adb push input-ports-addon.xml > /data/misc/inpot-port-addon.xml
```
On the next reboot, the device will pickup on the input ports associations and apply the changes. 
Some debugging may be needed in the event you have multiple touch controllers connected that share the same name/chipset. 
