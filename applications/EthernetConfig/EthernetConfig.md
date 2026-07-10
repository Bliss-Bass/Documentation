# Ethernet Config

Ethernet Config is the privileged system app used on current Bass OS builds (Android 13+) to manage wired Ethernet. It replaces the older [Bliss Ethernet Manager](../BlissEthernetManager/BlissEthernetManager.md) while keeping the same **`blissethernet`** AIDL contract so existing integrations continue to work.

| | |
|---|---|
| **Package** | `com.example.ethernetconfig` |
| **AIDL service** | `blissethernet` |
| **AIDL namespace** | `org.blissos.ethernet` |
| **AIDL reference** | [AIDL Interface](AIDL_INTERFACE.md) |
| **Test / validate** | [Testing Guide](TESTING.md) |

## Setting up Ethernet interfaces

Open **Ethernet Config** from the launcher (or Settings shortcuts on builds that expose it).

1. Select the target interface (for example `eth0`). Tap **Refresh** if the list is empty.
2. Choose **DHCP (Auto)** or **Static IP (Manual)**.
3. For static mode, enter IP, subnet mask, gateway, and DNS.
4. Tap **Apply configuration**.
5. Confirm link state and addresses in the status panel.

Notes:

* **IP and subnet** may be shown as separate fields in the UI; the AIDL API uses `<IP>/<prefix>` (for example `192.168.1.100/24`).
* On Android 13+, Ethernet changes require a **platform-signed privileged** install. Bass ROM builds include Ethernet Config that way via `ethernet_config.mk`.

## Prop-based auto-config (Bass)

Bass can apply a static (or DHCP) Ethernet profile at boot from persistent system properties. `BlissEthernetService` reads these props and applies them when the service starts or when the interface becomes available.

| Property | Example | Purpose |
|----------|---------|---------|
| `persist.bass.ethernet.mode` | `static` or `dhcp` | Enable auto-config (`""` disables) |
| `persist.bass.ethernet.iface` | `eth0` | Target interface |
| `persist.bass.ethernet.ip` | `192.168.1.199` | Static IPv4 address |
| `persist.bass.ethernet.mask` | `255.255.255.0` | Subnet mask |
| `persist.bass.ethernet.prefix` | `24` | Optional instead of mask |
| `persist.bass.ethernet.gateway` | `192.168.1.1` | Default gateway |
| `persist.bass.ethernet.dns1` | `8.8.8.8` | Primary DNS |
| `persist.bass.ethernet.dns2` | `8.8.4.4` | Secondary DNS |

### Set props on a running device

```bash
adb shell setprop persist.bass.ethernet.mode static
adb shell setprop persist.bass.ethernet.iface eth0
adb shell setprop persist.bass.ethernet.ip 192.168.1.199
adb shell setprop persist.bass.ethernet.mask 255.255.255.0
adb shell setprop persist.bass.ethernet.gateway 192.168.1.1
adb shell setprop persist.bass.ethernet.dns1 8.8.8.8
adb shell setprop persist.bass.ethernet.dns2 8.8.4.4
```

Restart the service (or reboot) so props are applied. Changing the device IP will drop a network ADB session — reconnect to the new address. Full steps: [Testing Guide](TESTING.md).

### Build-time defaults

Uncomment or add in product makefiles (for example `vendor/bass/branding.mk` or `ethernet_config.mk`):

```makefile
PRODUCT_PROPERTY_OVERRIDES += \
    persist.bass.ethernet.mode=static \
    persist.bass.ethernet.iface=eth0 \
    persist.bass.ethernet.ip=192.168.1.199 \
    persist.bass.ethernet.mask=255.255.255.0 \
    persist.bass.ethernet.gateway=192.168.1.1 \
    persist.bass.ethernet.dns1=8.8.8.8 \
    persist.bass.ethernet.dns2=8.8.4.4
```

## Boot start

`BlissEthernetService` registers the `blissethernet` binder. On Bass ROM builds it is started without opening the UI:

| Path | Trigger |
|------|---------|
| `/system_ext/etc/init/ethernet_config.rc` | `sys.boot_completed=1` → `start-bliss-ethernet` |
| `start-bliss-ethernet` | Ethernet iface present **or** `persist.bass.ethernet.mode` set |
| Vendor `bass_init` bootcomplete | Same eth/prop gate (belt-and-suspenders) |

If the binder is missing after boot:

```bash
adb shell /system/bin/sh /system_ext/bin/start-bliss-ethernet
# or:
adb shell am start-service -n com.example.ethernetconfig/.aidl.BlissEthernetService --user 0
adb shell service list | grep blissethernet
```

## AOSP / Bass integration

```makefile
$(call inherit-product, packages/apps/EthernetConfig/ethernet_config.mk)
```

The product makefile installs the platform-signed privileged app, priv-app permissions, init rc, and `start-bliss-ethernet` helper under `system_ext`.

## Related docs

* [AIDL Interface](AIDL_INTERFACE.md) — Java/Kotlin client API and `service call` codes
* [Testing Guide](TESTING.md) — prop auto-config, AIDL smoke tests, ADB reconnect
* [Bliss Ethernet Manager](../BlissEthernetManager/BlissEthernetManager.md) — legacy app docs (older builds)
