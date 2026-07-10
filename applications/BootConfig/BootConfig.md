# Boot Config (aaropa-options)

Boot Config is the Settings UI for toggling boot / kernel command-line options without rebuilding the image. Changes apply on the next reboot.

| | |
|---|---|
| **Package** | `com.bliss.bootconfig` |
| **Options source** | `boot_options/options.yaml` |
| **Also see** | [Configuration through Command Line Parameters](../../setup_and_configuration/Configuration-through-Command-Line-Parameters.md) |

## What you can change

Categories include:

* **UI modes:** Desktop UI, Tablet UI, Kiosk UI, multi-display windowing (`BASSMDW`)
* **Display / graphics:** resolution, DPI, orientation, Vulkan / HWC options
* **Power:** fake battery for always-on AC setups, sleep timeouts, Doze-related flags
* **Hardware:** audio routing, delayed sensors, virtual Wi-Fi, camera emulation
* **Debug:** insecure ADB, default ADB modes, debug shells, logcat behavior

Open **Boot Config** from Settings → System (label may vary by build), flip the options you need, then reboot.

## Remote control (Messenger API)

Other privileged apps can read and set options through a bound `Messenger` service.

### Permission

```xml
<uses-permission android:name="com.bliss.bootconfig.ADD_OR_REMOVE_OPTIONS" />
```

### Bind

```java
Intent intent = new Intent();
intent.setClassName("com.bliss.bootconfig", "com.bliss.bootconfig.MessengerService");
bindService(intent, serviceConnection, Context.BIND_AUTO_CREATE);
```

### Message codes

| Code | Description | Bundle |
|------|-------------|--------|
| `MSG_SET_OPTIONS = 1` | Set boot options | `OPTIONS` = String array to set |
| `MSG_GET_OPTIONS = 2` | Get boot options | Reply `OPTIONS` = String array currently set (`msg.replyTo`) |

## Related

* [Config Overrides](../BlissConfigOverrides/BlissConfigOverrides.md) for `/data/misc` settings files
* [Configuration through Command Line Parameters](../../setup_and_configuration/Configuration-through-Command-Line-Parameters.md)
* [Building Bass OS](../../development/building-bass.md)
