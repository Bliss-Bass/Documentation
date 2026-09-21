# Fleet Management

**In plain English:** Bass can run as a managed Android fleet without Google Mobile Services (GMS), Google accounts, or Google's Android Enterprise cloud. Images support two management styles: **Bass's own fleet / licensing backend** (BootSight Device Status), or a **third-party MDM** you already use. This page explains both paths, what Bass unlocks that GMS fleets usually cannot, and how other MDMs typically talk to Bass add-ons.

Your image is assembled for a specific management path as part of the product you receive. For product-line choice, see the [Bass Product Family Guide](../product-guide/bass-product-family.md). For Device Status / licensing UI, see [BootSight](../applications/BootSight/BootSight.md) and [License Activation](../setup_and_configuration/license-activation.md).

---

## Management modes

| Mode | What you get |
|------|----------------|
| **Bass fleet backend (BootSight)** | On-device Device Status, license activation, and Bass-side fleet identity. Common when you want Bass-native management without a third-party MDM console. |
| **Third-party MDM** | Your vendor's agent / console (for example Headwind, ScaleFusion, Syncfusion, or another DPC). Bass still supplies kiosk, lockdown, white-label, and PC add-on surfaces underneath. |
| **Unmanaged** | Lab, consumer, or desktop-style images with no fleet agent. |

Licensing and fleet identity on BootSight images use Device Status and the supported activation flow. Work with your Bass contact for the correct image SKU rather than trying to change management after delivery.

---

## Android Enterprise-style management without GMS

Stock "Android Enterprise" marketing often assumes:

- Google Play / Play Protect
- a Google account or managed Google domain
- Android Management API (AMAPI), zero-touch, or QR enrollment tied to Google's cloud

Bass Lineout / Submix / legacy fleets are usually **FOSS / no-GMS by default**. Management still uses the same Android **Device Policy** building blocks (Device Admin / Device Owner via `DevicePolicyManager` and `dpm`), but **without** requiring GMS or Google's enrollment cloud.

### What Bass does on-device

| Capability | How Bass supports it without GMS |
|---|---|
| **Device Owner / Device Admin** | Restricted Launcher (and Pro), BootSight, and SmartDock use Android device-admin / device-owner hooks where the image is configured for them. |
| **Kiosk / lockdown personality** | GRUB **Bass boot options** (Tablet / Desktop / Kiosk Admin / Kiosk Lockdown) plus Restricted Launcher or Kiosk Launcher - not a Play-managed "dedicated device" profile. |
| **Install / uninstall lock** | Supported lockdown images can block PackageInstaller and `pm install` / `pm uninstall` while booted in lockdown. See [Lockdown install block](lockdown-install-block.md). |
| **Settings / admin gates** | [Admin Restriction](admin-restriction.md) and launcher admin password flows keep end users out of system settings. |
| **Network allowlists** | [DNS Internet Restriction](dns-internet-restriction.md) without Google DNS / Chrome policy. |
| **Identity and licensing** | BootSight Device Status and the documented license activation path. No Play licensing. |
| **First-boot / clone provisioning** | Flat files under `/data/misc/` via [Bliss Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md); Ethernet first-boot via [Ethernet Config](../applications/EthernetConfig/EthernetConfig.md). |
| **White-label** | Shared OS image with customer boot animation / wallpaper / branding - no per-customer Google-signed SKU. See the [High Level Overview](../development/bass-high-level-overview.md) white-label section. |

These are **platform** policy hooks. They do not need Google Play Services to function.

### What "managed" looks like day to day (Bass fleet backend)

1. Receive / install the image your project was provisioned with.
2. Optionally apply Config Overrides under `/data/misc/` and complete license activation.
3. Complete Admin-mode setup for kiosk (whitelist, auto-launch, password).
4. Reboot into Lockdown (or leave Desktop/Tablet personality).
5. Use BootSight Device Status for license / serial state.

---

## What Bass allows that GMS fleets usually cannot

GMS + Android Enterprise is powerful for phone/tablet fleets that live inside Google's ecosystem. It is a poor fit for many Bass use cases. Things that work on Bass and typically **do not** work (or are blocked / unsupported) on sealed GMS Enterprise devices:

| Bass capability | Why GMS Enterprise usually cannot |
|---|---|
| **No Google account / no Play Services** | AMAPI and many MDM features assume GMS. Bass FOSS images run without them. |
| **PC-class hardware adaptation** | Phone Enterprise images do not ship Bass configurable HALs, mappers, or PC GPU/display bring-up. |
| **Boot-time personalities** (Tablet / Desktop / Kiosk Admin / Lockdown) | Not an Android Enterprise policy surface; GRUB / Bass boot options are OS-level. |
| **White-label on one shared OS** | Enterprise customers often need separate OEM builds or Play-managed branding limits; Bass overrides branding without a new platform fork. |
| **Privileged add-ons with vendor AIDL** | Power sleep policy, ethernet static/DHCP/tether, hardware button maps - exposed as system services MDMs can call, not as Play APIs. |
| **File-based fleet cloning** (`/data/misc/*.conf`) | Works offline and without Google's zero-touch; GMS fleets expect cloud enrollment. |
| **Lockdown that blocks even `pm install`** | Bass lockdown install block is tied to boot mode, not a Play Protect policy. |
| **Discretion / no kiss-and-tell** | Bass does not require publishing the fleet into a Google-managed customer directory. |

If a requirement is "must enroll in Google zero-touch / AMAPI," that is a different product shape. Use a GMS-bearing image only when the customer truly needs that cloud, and accept the tradeoffs above.

---

## Third-party MDMs (generic pattern)

Products such as **Headwind MDM**, **ScaleFusion**, **Syncfusion** (and many others) follow the same Android pattern on Bass:

1. Start from an image your Bass contact provisioned for third-party MDM.
2. Install the vendor's **Device Policy Controller (DPC)** / agent per that vendor's guide.
3. Make the DPC **Device Owner** (or Device Admin, depending on the product) using the enrollment method that vendor supports on AOSP / no-GMS devices (factory provisioning, QR/NFC if available without Google, or their documented `dpm` flow).
4. Use the MDM console for app push, remote wipe, location, and policy **where that agent supports AOSP**.
5. For Bass-specific behavior (power, ethernet, buttons, config files, boot mode), drive the **Bass surfaces below** from the agent's scripting, remote shell, or a small companion app - do not expect Google Play Enterprise APIs to expose them.

Bass does not certify every MDM. Treat the names above as examples of the class. Validate Device Owner on your FOSS Bass image before you commit a fleet.

### What the MDM owns vs what Bass owns

| Layer | Typical owner |
|---|---|
| App catalog, remote lock/wipe, compliance UI | Third-party MDM agent + console |
| Device Owner / admin rights | MDM DPC on third-party MDM images; Restricted Launcher / BootSight on Bass fleet-backend images |
| Boot personality, install block, DNS lockdown, white-label | Bass OS / add-ons |
| Power, ethernet, POS buttons, config files | Bass AIDL / `cmd` / `/data/misc` (callable from MDM scripts) |

---

## Integration surfaces (API, AIDL, command line)

Use these from an MDM remote shell, a privileged companion app, or approved imaging scripts. Full contracts live in the linked docs.

### Boot mode and identity (when present)

```bash
adb shell getprop ro.boot.bliss.bootmode          # e.g. lockdown, admin, ...
adb shell getprop ro.bliss.serialnumber          # licensing / device identity on BootSight images
```

### Config Overrides (file push)

Push key/value files, then trigger apply (or reboot):

```bash
adb push settings_global.conf /data/misc/
adb push settings_system.conf /data/misc/
adb push settings_secure.conf /data/misc/
adb push runtime_props.conf /data/misc/
adb push device_config.conf /data/misc/
adb shell setprop persist.ax86.update_configs 1
```

Details and examples: [Bliss Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md).

### Ax86 Power (AIDL + `service call`)

| | |
|---|---|
| ServiceManager | `blisspower` (legacy `IBlissPower`) |
| Native | `IAx86Power` / `org.ax86.power` |

```bash
adb shell service list | grep blisspower
adb shell service call blisspower 1   # reboot
adb shell service call blisspower 2   # shutdown
adb shell service call blisspower 3   # sleep
```

Full AIDL: [Ax86 Power AIDL](../applications/Ax86Power/AIDL_INTERFACE.md), legacy notes: [Power Management AIDL](../interfaces/BlissPowerManagerAIDL/power-management-aidl.md).

### Ethernet Config (AIDL + `service call`)

| | |
|---|---|
| ServiceManager | `blissethernet` |

```bash
adb shell service list | grep blissethernet
# Transaction codes and static/DHCP/tether helpers:
# see Ethernet Config AIDL doc
```

Full AIDL: [Ethernet Config AIDL](../applications/EthernetConfig/AIDL_INTERFACE.md).

### Button Manager (`cmd` + AIDL)

| | |
|---|---|
| ServiceManager | `ax86_btnmgr` |
| Shell | `cmd ax86_btnmgr ...` |

```bash
adb shell cmd ax86_btnmgr list
adb shell cmd ax86_btnmgr export /sdcard/ax86_btn_manager.conf
adb shell cmd ax86_btnmgr import /data/misc/ax86_btn_manager.conf --merge
adb shell cmd ax86_btnmgr reload
```

Full AIDL: [Button Manager AIDL](../applications/Ax86ButtonManager/AIDL_INTERFACE.md).

### Device policy (`dpm`)

```bash
adb shell dpm list-owners
adb shell dumpsys device_policy
```

Use the component names required by your DPC or by the Bass components on your image. SmartDock documents Device Admin usage in its [Vendor Guide](../applications/SmartDockDFC/VENDOR_GUIDE.md).

### Imaging notes

- Lineout: approved factory process can clone `/data/misc` and boot options as part of imaging ([Addon development](../development/addon-development.md) for builders).
- Submix: see vendor deployment docs linked from [Submix install](../Installation/submix/submix-install.md) for host + Android provisioning.

---

## Choosing a path

| Goal | What to ask for |
|---|---|
| License + Device Status, Bass-native kiosk | Image with Bass fleet backend (BootSight) (+ Restricted Launcher / lockdown as needed) |
| Existing MDM console (Headwind, ScaleFusion, Syncfusion, etc.) | Image prepared for third-party MDM + vendor DPC; use Bass AIDL/`cmd`/files for PC extras |
| Lab / consumer / no fleet agent | Unmanaged image |
| Strict lockdown + no sideload | Lockdown-capable image with install/uninstall block enabled |

---

## Related reading

| Topic | Doc |
|---|---|
| BootSight / Device Status | [BootSight](../applications/BootSight/BootSight.md), [User guide](../UserGuides/bootsight.md) |
| License activation | [License Activation](../setup_and_configuration/license-activation.md) |
| Kiosk boot flow | [Booting into lockdown builds](../setup_and_configuration/booting-into-lockdown-builds.md) |
| Restricted Launcher | [Bliss Restricted Launcher](../applications/BlissRestrictedLauncher/BlissRestrictedLauncher.md) |
| Updates | [Updates and OTA](updates-and-ota.md) |
| High-level platform map | [High Level Overview](../development/bass-high-level-overview.md) |
