# Ethernet Config — Test & Validation Guide

Validate **BlissEthernetService**, the **`blissethernet`** AIDL binder, and **`persist.bass.ethernet.*`** prop-based auto-config on a live device.

Overview: [Ethernet Config](EthernetConfig.md). AIDL codes: [AIDL Interface](AIDL_INTERFACE.md).

## Boot start paths

`BlissEthernetService` should start without a manual `am start-service`:

| Path | Trigger | Behavior |
|---|---|---|
| `/system_ext/etc/init/ethernet_config.rc` | `sys.boot_completed=1` | Runs `/system/bin/sh /system_ext/bin/start-bliss-ethernet` |
| `start-bliss-ethernet` | eth iface present **or** `persist.bass.ethernet.mode` set | `pm enable` + `cmd package unstop` + start service (with retries) |
| Vendor `bass_init` bootcomplete | same eth/prop gate | Belt-and-suspenders start |

If `service call blissethernet` fails right after boot:

```bash
adb logcat -d | grep start-bliss-ethernet
adb shell /system/bin/sh /system_ext/bin/start-bliss-ethernet
```

## Quick health check

```bash
adb connect <CURRENT_IP>:5555
adb root
adb connect <CURRENT_IP>:5555

adb shell pm path com.example.ethernetconfig
adb shell am start-service -n com.example.ethernetconfig/.aidl.BlissEthernetService --user 0

# AIDL: list interfaces (expect eth0)
adb shell service call blissethernet 1

# AIDL: assignment — 0=UNASSIGNED, 1=DHCP, 2=STATIC
adb shell service call blissethernet 7 s16 eth0

adb shell ip -4 addr show eth0
```

If `service call blissethernet` fails with “service not found”, start the service (or reboot) as above.

---

## Test A — Prop-based static IP auto-config (recommended)

### 1. Set Bass ethernet props

Replace values as needed for your LAN:

```bash
adb shell setprop persist.bass.ethernet.mode static
adb shell setprop persist.bass.ethernet.iface eth0
adb shell setprop persist.bass.ethernet.ip 192.168.1.199
adb shell setprop persist.bass.ethernet.mask 255.255.255.0
adb shell setprop persist.bass.ethernet.gateway 192.168.1.1
adb shell setprop persist.bass.ethernet.dns1 8.8.8.8
adb shell setprop persist.bass.ethernet.dns2 8.8.4.4
```

Optional instead of mask: `persist.bass.ethernet.prefix=24`.

### 2. Restart the service so props are applied

On a normal boot, `ethernet_config.rc` and/or `bass_init` already start `BlissEthernetService` when an ethernet iface is present (or props are set). After changing props on a running device, restart the service:

```bash
adb shell am force-stop com.example.ethernetconfig
adb shell /system/bin/sh /system_ext/bin/start-bliss-ethernet
# or:
adb shell am start-service -n com.example.ethernetconfig/.aidl.BlissEthernetService --user 0
```

Expect the old ADB session to drop once the address changes.

### 3. Reconnect ADB on the new IP

```bash
adb disconnect
adb connect 192.168.1.199:5555
adb devices -l
adb -s 192.168.1.199:5555 shell id
adb -s 192.168.1.199:5555 shell ip -4 addr show eth0
```

### 4. Validate

| Check | Command / expectation |
|---|---|
| Interface address | `ip -4 addr show eth0` → `inet 192.168.1.199/24` |
| Props persisted | `getprop persist.bass.ethernet.ip` → `192.168.1.199` |
| AIDL assignment | `service call blissethernet 7 s16 eth0` → `i32 2` (STATIC) |
| AIDL IP | `service call blissethernet 9 s16 eth0` → UTF-16 `192.168.1.199/24` |
| AIDL gateway | `service call blissethernet 11 s16 eth0` → UTF-16 `192.168.1.1` |
| Auto-config logs | `adb logcat -d \| grep EthPropAutoConfig` |

Successful apply looks like:

```text
I EthPropAutoConfig: Applying prop ethernet config (availability:eth0): mode=STATIC iface=eth0
I EthPropAutoConfig: Prop ethernet config applied on eth0
D EthPropAutoConfig: Skip apply (service-onCreate): already applied STATIC|eth0|...
```

Idempotent skips on later callbacks are expected.

### 5. Build-time defaults (optional)

See [Ethernet Config — Build-time defaults](EthernetConfig.md#build-time-defaults).

---

## Test B — AIDL `service call` static IP (manual)

Useful when props are unset and you want a one-shot change:

```bash
# STATIC = 2
adb shell service call blissethernet 8 s16 eth0 i32 2
adb shell service call blissethernet 10 s16 eth0 s16 192.168.1.199/24
adb shell service call blissethernet 12 s16 eth0 s16 192.168.1.1
# then reconnect ADB to the new IP and verify as in Test A §3–4
```

---

## Test C — Revert to DHCP

```bash
adb shell setprop persist.bass.ethernet.mode dhcp
adb shell am force-stop com.example.ethernetconfig
adb shell am start-service -n com.example.ethernetconfig/.aidl.BlissEthernetService --user 0
```

Or via AIDL:

```bash
adb shell service call blissethernet 8 s16 eth0 i32 1
```

Then reconnect to whatever address DHCP assigns. To disable prop auto-config entirely:

```bash
adb shell setprop persist.bass.ethernet.mode ""
```

---

## Notes / caveats

- Changing the device IP **will drop** the current network ADB session; always reconnect to the new address.
- Same-subnet ADB works even if a default route via the gateway is not visible in `ip route`.
- `net.dns1` / `net.dns2` may stay empty; DNS from EthernetManager is carried in the interface `IpConfiguration`.
- System priv-apps can stay “stopped” until first launch; `start-bliss-ethernet` / `pm enable` exists to unblock boot start.
