# Bliss Ethernet AIDL client library

See **[AIDL_INTERFACE.md](../AIDL_INTERFACE.md)** for the full API.

## JAR

Copy `bliss-ethernet-framework.jar` into your app’s `system_libs/` (or reference this folder):

```gradle
implementation fileTree(dir: 'system_libs/', include: ['*.jar'])
```

The JAR includes AIDL stubs, `BlissEthernetManager`, and `BlissEthernetAssignment`.

**Note:** The legacy Bliss Ethernet Manager JAR used assignment values `-1/0/1`.
This JAR uses canonical `0/1/2` and adds ethernet tethering APIs. See the
[assignment migration table](../AIDL_INTERFACE.md#ip-assignment-modes) in the AIDL docs.
