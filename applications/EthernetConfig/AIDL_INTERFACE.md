# Ethernet Config — AIDL Interface

This document describes the **Bliss-compatible** AIDL API exposed by **Ethernet Config** (`com.example.ethernetconfig`). The interface matches the legacy [Bliss Ethernet Manager](../BlissEthernetManager/BlissEthernetManager.md) so existing integrations can migrate with minimal changes.

The service registers a system binder named **`blissethernet`**, which powers both the Java/Kotlin client API and `adb shell service call blissethernet`.

For end-to-end device validation (including `persist.bass.ethernet.*` auto-config), see **[Testing Guide](TESTING.md)**. Overview and prop setup: **[Ethernet Config](EthernetConfig.md)**.

---

## Prerequisites

- Ethernet Config installed as a privileged/system app (Bass ROM builds include it).
- The `blissethernet` service registered in `ServiceManager` (started at boot via init / `start-bliss-ethernet`).
- For third-party apps: caller must be **authorized** (see [Authorization](#authorization)).

---

## IP assignment modes

Use these integer values with `getIpAssignment` / `setIpAssignment`:

| Value | Constant     | Meaning                                      |
|------:|--------------|----------------------------------------------|
| 0     | `UNASSIGNED` | Interface administratively down / unassigned |
| 1     | `DHCP`       | Automatic IP via DHCP                        |
| 2     | `STATIC`     | Static IP, gateway, and DNS                  |

**Static IP address format:** `<IPv4>/<prefix>` (e.g. `192.168.1.100/24`).

---

## Client usage

### Gradle

```gradle
implementation fileTree(dir: 'system_libs/', include: ['*.jar'])
```

Or copy the AIDL sources into your module and enable `buildFeatures { aidl = true }`.

### Java

```java
import org.blissos.ethernet.BlissEthernetManager;
import org.blissos.ethernet.BlissEthernetAssignment;

BlissEthernetManager blissEthernetManager = BlissEthernetManager.getInstance(context);

String[] interfaces = blissEthernetManager.getAvailableInterfaces();
boolean up = blissEthernetManager.isAvailable("eth0");

blissEthernetManager.setIpAssignment("eth0", BlissEthernetAssignment.STATIC);
blissEthernetManager.setIpAddress("eth0", "192.168.1.100/24");
blissEthernetManager.setGateway("eth0", "192.168.1.1");
blissEthernetManager.setDnses("eth0", new String[] { "8.8.8.8", "8.8.4.4" });
```

### Manifest (client app)

```xml
<uses-permission android:name="org.blissos.ethernet.permission.ACCESS_ETHERNET_MANAGER" />
```

### AIDLs

**`IBlissEthernet.aidl`:**

```
package org.blissos.ethernet;

import org.blissos.ethernet.IBlissEthernetServiceListener;

interface IBlissEthernet {
    String[] getAvailableInterfaces();
    boolean isAvailable(String iface);
    void setListener(in IBlissEthernetServiceListener listener);

    void setInterfaceUp(String iface);
    void setInterfaceDown(String iface);

    String getEthernetMacAddress(String ifname);
    int getIpAssignment(String iface);
    void setIpAssignment(String iface, int assignment);
    String getIpAddress(String iface);
    void setIpAddress(String iface, String ipAddress);
    String getGateway(String iface);
    void setGateway(String iface, String gateway);
    String[] getDnses(String iface);
    void setDnses(String iface, in String[] dnses);
}
```

**`IBlissEthernetServiceListener.aidl`:**

```
package org.blissos.ethernet;

oneway interface IBlissEthernetServiceListener {
    void onAvailabilityChanged(String iface, boolean isAvailable);
}
```

### Method reference

| Method | Description |
|--------|-------------|
| `getAvailableInterfaces()` | Detected Ethernet interface names |
| `isAvailable(String iface)` | Whether the interface is available |
| `setListener(...)` | Availability callbacks (`null` to clear) |
| `setInterfaceUp` / `setInterfaceDown` | Bring interface up or down |
| `getEthernetMacAddress` | MAC from sysfs / `NetworkInterface` |
| `getIpAssignment` / `setIpAssignment` | `0` UNASSIGNED, `1` DHCP, `2` STATIC |
| `getIpAddress` / `setIpAddress` | Static address as `ip/prefix` |
| `getGateway` / `setGateway` | Default gateway |
| `getDnses` / `setDnses` | DNS servers |

Partial updates (`setIpAddress`, `setGateway`, `setDnses`) merge with the current interface configuration before applying.

---

## Authorization

A call succeeds only if the caller is one of:

1. **System UID** or **shell UID** (e.g. `adb shell service call …`)
2. **Same app** as the server (`com.example.ethernetconfig`)
3. Holder of **`org.blissos.ethernet.permission.ACCESS_ETHERNET_MANAGER`**
4. Package listed in `bliss_ethernet_authorized_packages`, or allow-all mode enabled in the server app resources

Unauthorized callers receive `SecurityException`.

---

## ADB interface

```bash
adb shell service call blissethernet <code> [parameters...]
```

**`<code>`** is the 1-based transaction ID matching AIDL method order.

| Code | AIDL method | Parameters |
|-----:|-------------|------------|
| 1 | `getAvailableInterfaces` | — |
| 2 | `isAvailable` | `s16` interface name |
| 3 | `setListener` | listener binder (uncommon from shell) |
| 4 | `setInterfaceUp` | `s16` interface name |
| 5 | `setInterfaceDown` | `s16` interface name |
| 6 | `getEthernetMacAddress` | `s16` interface name |
| 7 | `getIpAssignment` | `s16` interface name |
| 8 | `setIpAssignment` | `s16` iface, `i32` assignment |
| 9 | `getIpAddress` | `s16` interface name |
| 10 | `setIpAddress` | `s16` iface, `s16` `ip/prefix` |
| 11 | `getGateway` | `s16` interface name |
| 12 | `setGateway` | `s16` iface, `s16` gateway |
| 13 | `getDnses` | `s16` interface name |
| 14 | `setDnses` | `s16` iface, string array |

### Examples

```bash
# List interfaces
adb shell service call blissethernet 1

# isAvailable(eth0)
adb shell service call blissethernet 2 s16 eth0

# getIpAssignment — 0=UNASSIGNED, 1=DHCP, 2=STATIC
adb shell service call blissethernet 7 s16 eth0

# Set static IP
adb shell service call blissethernet 8 s16 eth0 i32 2
adb shell service call blissethernet 10 s16 eth0 s16 192.168.1.100/24
adb shell service call blissethernet 12 s16 eth0 s16 192.168.1.1
```

### Verify service registration

```bash
adb shell service list | grep blissethernet
```

If missing after boot, see [Ethernet Config — Boot start](EthernetConfig.md#boot-start).

---

## Compatibility notes

- **Package namespace:** `org.blissos.ethernet` (unchanged from Bliss Ethernet Manager)
- **Service name:** `blissethernet` (unchanged)
- **AIDL signatures:** Match the published Bliss Co-Labs interface
- **Listener:** `onAvailabilityChanged` fires while `BlissEthernetService` is running
