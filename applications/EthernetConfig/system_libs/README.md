# Bliss Ethernet AIDL client library

See **[AIDL Interface](../AIDL_INTERFACE.md)** for the full API.

## Download

**[Download bliss-ethernet-framework.jar](bliss-ethernet-framework.jar)**

Same file is also published under docs static assets:

**[Download (static mirror)](/static/downloads/bliss-ethernet-framework.jar)**

Source tree (for integrators with repo access):
[Bliss-Bass/packages_apps_EthernetConfig](https://github.com/Bliss-Bass/packages_apps_EthernetConfig)
(`system_libs/bliss-ethernet-framework.jar`).

## Add to your app

Copy the JAR into your app’s `system_libs/` (or reference this folder):

```gradle
implementation fileTree(dir: 'system_libs/', include: ['*.jar'])
```

The JAR includes AIDL stubs, `BlissEthernetManager`, and `BlissEthernetAssignment`.

**Note:** The legacy Bliss Ethernet Manager JAR used assignment values `-1/0/1`.
This JAR uses canonical `0/1/2`<!-- and adds ethernet tethering APIs-->. See the
[assignment migration table](../AIDL_INTERFACE.md#ip-assignment-modes) in the AIDL docs.
