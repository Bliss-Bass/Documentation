# Creating an input-port-addon.xml file (Lineout runtime override)

This is a **Bass: Lineout** runtime override: put XML under `/data/misc/` and enable `BLISS_INPUT_PORTS_ADDON=1` on the kernel command line. Early init bind-mounts that file over the vendor associations path.

It is **not** a legacy Bass `private/addons/` package.

* Lineout model: [Addon Development: Bass Lineout](../development/addon-development.md)
* Legacy Bass private addons: [Addon Development: Legacy Bass OS](../development/addon-development-legacy-bass.md)

Builds with `--extras` also include [Touch Mapper](../applications/BlissTouchMapper/BlissTouchMapper.md), which can generate and save this file from Settings. Use the steps below for imaging or when you prefer ADB.

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
- Display 4693505326422272 (HWC display 0): port=0 pnpId=DEL displayName="DELL P2314T"
- Display 4693505326422273 (HWC display 1): port=1 pnpId=DEL displayName="DELL P2314T"
- Display 4692921138614786 (HWC display 2): port=2 pnpId=DEL displayName="DELL S2740L"
- Display 18309706364381699 (HWC display 3): port=3 pnpId=PHL displayName="PHL 245C5"

### Obtain Input Device Locations:
Use the getevent command via adb shell to find the unique "location" string for the touch input devices.
```bash
adb shell getevent -i | grep location
```
This command will output information like:
- location: "usb-0000:00:14.0-7.3.4/input0"
- location: "usb-0000:00:14.0-7.2.4/input0"
- ...

### Edit the input-port-addon.xml file:
Create the file to update the associations between the display ports and input locations. Example XML structure:
```xml
<ports>
	<port display="0" input="usb-xhci-cdns3-1.1.4/input0" />
	<port display="1" input="usb-xhci-cdns3-1.2.4/input0" />
	<port display="2" input="usb-xhci-cdns3-1.3.4/input0" />
	<port display="3" input="usb-xhci-cdns3-1.4.4/input0" />
	<port display="0" input="usb-xhci-cdns3-1.4/input0" />
	<port display="0" input="usb-ci_hdrc.0-1.4/input0" />
</ports>
```
### Push the change to the device:
Connect to the device using ADB and run the following commands:
```bash
adb root
adb push input-port-addon.xml /data/misc/input-port-addon.xml
```
On the next reboot, the device will pickup on the input ports associations and apply the changes. 
Some debugging may be needed in the event you have multiple touch controllers connected that share the same name/chipset.

## Related

* [Addon Development: Bass Lineout](../development/addon-development.md)
* [Bliss Touch Mapper](../applications/BlissTouchMapper/BlissTouchMapper.md)
* [Using IDC Addon](addon_idc.md)
