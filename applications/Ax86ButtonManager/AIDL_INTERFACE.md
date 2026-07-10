# Button Manager AIDL and cmd

The service registers with ServiceManager as `ax86_btnmgr`, so it is reachable from AIDL clients and from `cmd`.

## AIDL

Package `com.ax86.btnmgr`.

```aidl
interface IButtonManagerService {
    List<ButtonMapping> listMappings();
    void setMapping(in ButtonMapping mapping);
    void removeMapping(String buttonId);
    byte[] exportConfig();
    int importConfig(in byte[] data, boolean merge);
    void reload();
    void registerListener(IButtonEventListener listener);
    void unregisterListener(IButtonEventListener listener);
}

parcelable ButtonMapping {
    String id;
    String label;
    String deviceMatch;
    int scanCode;
    String androidKey;
    String action;
    String actionData;
    String emitKey;
    boolean longPress;
}

oneway interface IButtonEventListener {
    void onButtonTriggered(String buttonId, String action);
    void onConfigReloaded();
}
```

In-process clients resolve the binder with:

```text
IButtonManagerService.Stub.asInterface(ServiceManager.getService("ax86_btnmgr"))
```

## cmd handler

```bash
adb shell cmd ax86_btnmgr list
adb shell cmd ax86_btnmgr set P1 action=screenshot scan_code=0x190 device_match=gpio-keys
adb shell cmd ax86_btnmgr set P4 action=device_control control=brightness_toggle low=0 high=100
adb shell cmd ax86_btnmgr remove P4
adb shell cmd ax86_btnmgr export /sdcard/ax86_btn_manager.conf
adb shell cmd ax86_btnmgr import /data/misc/ax86_btn_manager.conf --merge
adb shell cmd ax86_btnmgr reload
```

## Related

* [Button Manager](Ax86ButtonManager.md)
* [Config Format](CONFIG_FORMAT.md)
