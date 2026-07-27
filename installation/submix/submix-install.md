# Bass: Submix - Quick Start Guide

**Bass: Submix** is a minimal Debian host that boots into a Wayland compositor and runs LineageOS / Android inside a **Waydroid LXC container**. This guide is the short path from a downloaded ISO to a working install - flash, install, connect Wi-Fi, and reach the device from your PC.

This document ships with public builds (SourceForge, FossHub, and mirrors). For architecture diagrams, the full override catalog, mapper apps, and developer docs, use the project repository:

**[https://github.com/Bliss-Bass/bass-submix](https://github.com/Bliss-Bass/bass-submix)**

| Topic | On GitHub |
|-------|-----------|
| System architecture | [`ARCHITECTURE.md`](https://github.com/Bliss-Bass/bass-submix/blob/main/ARCHITECTURE.md) |
| Host + container overrides (`persist.ax86.*`, GRUB flags, `/data/misc/`) | [`OVERRIDES.md`](https://github.com/Bliss-Bass/bass-submix/blob/main/OVERRIDES.md) |
| Full vendor deployment / fleet provisioning | [`VENDOR_DEPLOYMENT.md`](https://github.com/Bliss-Bass/bass-submix/blob/main/VENDOR_DEPLOYMENT.md) |
| Build host setup | [`README.md`](https://github.com/Bliss-Bass/bass-submix/blob/main/README.md) |
| Issues & discussion | [Issues](https://github.com/Bliss-Bass/bass-submix/issues) |

On-device **Ax86Docs** (when included in the image) opens the same guides from the Documentation section.

---

## 1. Flash the ISO to USB

**Recommended:** [Balena Etcher](https://etcher.balena.io/) - select the `.iso`, choose your USB drive, and click **Flash!**

Alternatives: Rufus (Windows), or `dd` on Linux/macOS:

```bash
sudo dd if=Bass-Submix-*.iso of=/dev/sdX bs=4M status=progress conv=fsync
```

Replace `/dev/sdX` with the correct **disk** device (not a partition). Unplug other removable drives first so you do not overwrite the wrong disk.

---

## 2. Boot from USB

1. Insert the USB drive and power on the target PC.
2. Enter the firmware boot menu (often **F12**, **F2**, or **Esc** - varies by manufacturer).
3. Select the USB drive under **UEFI** (preferred over Legacy/CSM when available).
4. The GRUB menu appears (about 10 seconds). Choose one of the entries below.

| GRUB entry | When to use |
|------------|-------------|
| **Waydroid Host OS (Live)** | Try the full OS without installing - compositor + Waydroid + Android. |
| **Control Panel (Network & Settings)** | Install to disk, configure host Wi-Fi, or edit boot options - **without** starting the full Android session. |

You can try **Live** first to confirm hardware compatibility, then reboot and use **Control Panel** to install.

---

## 3. Install to disk (Control Panel)

1. Boot **Control Panel (Network & Settings)** or **Install Waydroid Linux (Graphical)**.
2. Open the **Install OS** tab (default on live USB).
3. Click **Refresh Drives** and select the target disk.
4. Choose **ext4** (recommended) and a **Data Type** (Folder or `data.img` size).
5. For a clean single-disk setup, enable **Auto-Partition Entire Drive** (wipes the selected disk).
6. Click **Erase & Install OS** and confirm.
7. Wait for **Installation Complete**, then reboot and remove the USB drive.

On first boot from the installed disk, Waydroid initializes automatically and Android runs the **setup wizard**. Complete the wizard before configuring Wi-Fi.

### Default host credentials

| Context | Username | Password |
|---------|----------|----------|
| Host TTY / SSH | `waydroid` | `waydroid` |

The `waydroid` user has passwordless `sudo`. Switch to a host TTY with **Alt+F2** (etc.) while the compositor runs on the primary session. **Change the password after deployment** on any device that faces a network.

---

## 4. Connect to Wi-Fi (after setup wizard)

Stay in the **normal** Android session (the installed Waydroid entry - not Control Panel).

**Important:** open **Ethernet Config** before joining Wi-Fi. Network policy does not run correctly on first boot until that app has been launched once.

### Step 1 - Open Ethernet Config (required first)

1. Open **Ethernet Config** from the app drawer.
2. Tap **Refresh** next to the interface dropdown.

You do not need to change settings yet - opening the app and refreshing interfaces is enough to prime the service.

### Step 2 - Join Wi-Fi in Settings

1. Open **Settings → Network & Internet → Internet**.
2. Select your SSID, enter the password, and wait until Android reports **Connected**.

### Step 3 - Verify routing in Ethernet Config

1. Tap **Refresh** if needed, then select **wlan0**:
   - IPv4 address on your LAN
   - **Default route: Yes** (needed for browser/DNS)
   - **ADB connect:** `adb connect <ip>:5555`
2. Select **eth0**. If it shows **192.168.240.x** with **Default route: Yes** while Wi-Fi is connected, the Waydroid bridge is still winning over Wi-Fi.
3. On **eth0**, tap **Apply prefer_wifi demote**, or **Disable Ethernet tracking** / **Management only (no Internet)**.
4. Select **wlan0** again and confirm **Default route: Yes**.

Optional check from ADB:

```bash
adb shell ip route show default          # expect wlan0, not eth0
adb shell cmd ethernet get-interface-enabled eth0   # expect false when demoted
```

### If Wi-Fi does not work in Android

| Symptom | Next step |
|---------|-----------|
| **wlan0** missing in Ethernet Config | Adapter not passed through - use [§5](#5-control-panel-host-wi-fi-and-passthrough). |
| Wi-Fi connects but no Internet | Demote **eth0** in Ethernet Config (step 3 above). |
| Skipped Ethernet Config first | Open the app, tap **Refresh**, then retry Wi-Fi in Settings. |

---

## 5. Control Panel: host Wi-Fi and passthrough

Use this when Android has no **wlan0**, or when you need to configure networking from the host before the full session.

1. Reboot and select **Control Panel (Network & Settings)** from GRUB.
2. Click **Refresh hardware**, then **Scan Wi-Fi**; connect to your SSID.
3. Under **Hardware & drivers**, enable **Passthrough → Android** on the Wi-Fi interface. Equivalently, **turn off** **Keep host network connection (pin virtual eth0)** (see note below).
4. Expand **Android network (Waydroid)** and enable **Prefer Wi-Fi in Android** (`androidboot.ax86_prefer_wifi`) - recommended on Wi-Fi-only hardware.
5. Reboot a **normal** GRUB entry (not Control Panel).
6. Return to [§4](#4-connect-to-wi-fi-after-setup-wizard): open **Ethernet Config** first, then confirm Wi-Fi and routing.

> **Host connection (virtual eth0)** is **on by default**. While on, Wi-Fi passthrough is disabled: the host keeps its own LAN IP and stays reachable over SSH (including multi-display **MD-2** boots). Android still reaches the internet through bridged `eth0` (NAT). Turn it **off** to hand the physical Wi-Fi NIC to Android; then reach the host via Android's Wi-Fi IP on port **8022**.

Host TTY equivalents:

```bash
# Keep host network (virtual eth0 sticks - default):
echo wifi_passthrough=false | sudo tee /var/lib/waydroid/passthrough-devices.conf
# Hand Wi-Fi to Android (passthrough):
echo wifi_passthrough=auto  | sudo tee /var/lib/waydroid/passthrough-devices.conf

sudo waydroid-boot-option.sh ax86_prefer_wifi 1
sudo reboot
```

---

## 6. Prefer Wi-Fi (routing preference)

`androidboot.ax86_prefer_wifi=1` tells Android to prefer Wi-Fi for Internet instead of the Waydroid management bridge **`eth0`** (`192.168.240.x`). Without it, browsers may fail DNS and ADB may show the bridge address instead of your LAN IP.

- **Control Panel** / `waydroid-boot-option.sh` persist the flag across reboots.
- **Ethernet Config → Apply prefer_wifi demote** fixes routing immediately after you connect Wi-Fi.

Keep it enabled on typical Wi-Fi devices. Full policy details: [OVERRIDES.md](https://github.com/Bliss-Bass/bass-submix/blob/main/OVERRIDES.md) and [VENDOR_DEPLOYMENT.md](https://github.com/Bliss-Bass/bass-submix/blob/main/VENDOR_DEPLOYMENT.md).

---

## 7. Connect from your PC (ADB and SSH)

**Default credentials:** user `waydroid`, password `waydroid` (change in production).

| Boot mode | Android (ADB) | Host (SSH) |
|-----------|---------------|------------|
| Installed + Wi-Fi passthrough (typical) | `adb connect <android-wifi-ip>:5555` | `ssh waydroid@<android-wifi-ip> -p 8022` |
| Control Panel | Often unavailable until Android starts | `ssh waydroid@<host-lan-ip>` (port **22**) |
| Installed, no passthrough | Bridge / host-managed | `ssh waydroid@<host-lan-ip>` (port **22**) |

Find the Android Wi-Fi IP in **Settings → Network & Internet**, the **Ethernet Config** status panel, or:

```bash
waydroid shell ip -4 addr show wlan0
```

### ADB

Enable **Settings → Developer options → Wireless debugging** (or ADB over network on port 5555). PC and device on the same LAN:

```bash
adb kill-server 2>/dev/null || true
adb start-server
adb connect 192.168.1.x:5555
adb devices -l
adb shell getprop ro.build.display.id
```

### SSH (host)

```bash
# Passthrough mode (host via Android Wi-Fi address):
ssh waydroid@192.168.1.x -p 8022

# Control Panel / host LAN:
ssh waydroid@192.168.1.x
```

Useful after SSH:

```bash
systemctl status waydroid-container waydroid-session
waydroid status
```

On the device keyboard (no network): log in as `waydroid` on a TTY, then use `waydroid shell` / `waydroid adb`.

More detail: [VENDOR_DEPLOYMENT.md §2](https://github.com/Bliss-Bass/bass-submix/blob/main/VENDOR_DEPLOYMENT.md#2-connecting-via-adb-and-ssh-from-your-pc).

---

## 8. Next steps (full documentation)

Once the OS is installed and online:

| Goal | Where to look |
|------|----------------|
| Architecture / how the stack fits together | [ARCHITECTURE.md](https://github.com/Bliss-Bass/bass-submix/blob/main/ARCHITECTURE.md) |
| GRUB flags, `persist.ax86.*`, `/data/misc/` files | [OVERRIDES.md](https://github.com/Bliss-Bass/bass-submix/blob/main/OVERRIDES.md) |
| Display resolution / DPI | BlissDisplayMapper (on device) + [docs on GitHub](https://github.com/Bliss-Bass/bass-submix) |
| Touchscreen / pointer mapping | BlissTouchMapper (on device) + GitHub docs |
| Flat-file Android provisioning | BlissConfigOverrides + [OVERRIDES.md](https://github.com/Bliss-Bass/bass-submix/blob/main/OVERRIDES.md) |
| Fleet scripts, host config paths, mapper triggers | [VENDOR_DEPLOYMENT.md](https://github.com/Bliss-Bass/bass-submix/blob/main/VENDOR_DEPLOYMENT.md) |

---

## 9. Custom Builds & Services

Bass: Submix covers a broad range of x86 deployments out of the box. If you need a **tailored image** for a specific device, industry, or workflow - hardware bring-up, custom launcher/UI, kiosk or restricted modes, multi-display layouts, OTA/update infrastructure, or ongoing production support - Navotpala Tech can help.

**[View customization services](https://navotpala.tech/services)** - custom OS development, application & framework work, build/OTA hosting, and end-to-end solution delivery.

Typical engagements include:

- Bass / Submix custom builds and hardware-specific optimizations
- System apps, frameworks, and device-management integrations
- Security hardening, multi-architecture support, and fleet provisioning
- Professional support, consultation, and enterprise partnership options

Ready to talk about your use case? Start from the services page above, or open a conversation at [navotpala.tech](https://navotpala.tech/).

---

## Links

- Project & docs: [https://github.com/Bliss-Bass/bass-submix](https://github.com/Bliss-Bass/bass-submix)
- Customization services: [https://navotpala.tech/services](https://navotpala.tech/services)
- Navotpala Tech: [https://navotpala.tech/](https://navotpala.tech/)
