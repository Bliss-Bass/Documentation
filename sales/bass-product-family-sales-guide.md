# Bass Product Family: Sales & Positioning Guide

This guide is for sales and business-development staff. It explains what the Bass product family is, how the three product lines differ, how they compare to stock Android alternatives, and how the modular addon system translates into customer value. No engineering background is required.

---

## 1. Executive Summary

**Bass** (Broad Apparatus Support System) turns generic x86_64 hardware — tablets, panel PCs, POS terminals, mini PCs, industrial computers — into fully supported Android devices. One generic OS image adapts itself to the hardware it boots on, and a library of modular addons layers on kiosk lockdown, desktop productivity, fleet management, and per-customer branding.

The core pitch in one sentence:

> **"Enterprise Android on the hardware you already have — one image, any device, only the features you need."**

Customers do not need to buy purpose-built Android hardware from an OEM, and they do not need an engineering team to customize AOSP. Bass delivers a supported, configurable, brandable Android platform with the private customer-specific pieces kept private.

---

## 2. The Product Family at a Glance

There are three product lines. All share the same configuration model, addon library, and deployment tooling — they differ in how Android is delivered to the hardware.

| | **Bass OS** (classic) | **Bass: Lineout** | **Bass: Submix** |
|---|---|---|---|
| **What it is** | The original Bass product line, built on the Android-x86 / Bliss OS lineage | The current flagship: a stable, extensible tablet & kiosk OS built on **LineageOS** with the `vendor_ax86-lite` engineering tree | A lightweight **Debian Linux host** that runs Android (LineageOS) inside a **Waydroid container** |
| **Android versions** | Android 12L – 15 | Android 14 / 16 | Android 16 (LineageOS 23) |
| **How Android runs** | Directly on the hardware | Directly on the hardware, with an optional Debian subsystem alongside | Inside a container on top of a minimal Linux host |
| **Best fit** | Existing deployments, broadest legacy hardware coverage | New tablet, kiosk, and enterprise deployments — the default recommendation | Deployments that need full Linux host services (custom daemons, Linux-native peripherals, host-level networking) *and* Android apps on the same box |
| **Internal codename** | — | `vendor_ax86-lite` lineage | `ax86-lite_waydroid` |

Points worth internalizing:

- **Bass: Lineout is what we sell first.** It is the actively developed line: dynamic hardware detection (displays, audio, sensors, power), GRUB "Bass boot options" for switching between Tablet UI / Desktop UI / Kiosk modes, enterprise deployment tooling, and on-device documentation.
- **Bass: Submix is the answer when the customer says "we also need Linux."** Because the host is Debian, the customer gets standard Linux tooling (`apt`, `systemd`, SSH) underneath a near-native Android experience. Same addons, same configuration model.
- **Bass OS (classic) remains supported** for existing fleets and covers the older Android range, but new opportunities should be steered to Lineout or Submix.

---

## 3. How Bass Compares to AOSP and OEM Android

### Versus stock AOSP

AOSP is a source-code reference, not a product. To go from AOSP to a shippable device, someone must do hardware enablement, build an installer, add provisioning, add kiosk features, and maintain it across Android releases. That is precisely the work Bass has already done.

| Need | Stock AOSP | Bass |
|---|---|---|
| Runs on generic x86_64 hardware | No — targets reference boards and phones | Yes — dynamic detection of displays, audio, touch, sensors, power |
| Installer | None | Guided USB installer (Aaropa) with GRUB integration |
| Kiosk / lockdown mode | Build it yourself | Included (Restricted Launcher, lockdown boot modes, DNS restriction) |
| Fleet provisioning & licensing | Build it yourself | Included (BootSight, Ethernet provisioning, config cloning) |
| Desktop / multi-display mode | Minimal | SmartDock DFC desktop shell addon |
| Per-customer branding | Build it yourself | Vendor configuration layer — branding without code changes |
| Ongoing maintenance | Your engineering team | Our release cadence across Android versions |

### Versus an OEM Android device

| Concern | OEM Android (Samsung, Lenovo, etc.) | Bass |
|---|---|---|
| **Hardware choice** | Locked to that OEM's catalog and pricing | Any compatible x86_64 hardware — including hardware the customer already owns |
| **Google dependency** | Google services, accounts, and telemetry baked in | No Google account required; curated FOSS app set; privacy-friendly by default |
| **Support window** | Typically 2–4 years, then forced hardware refresh | OS updates decoupled from the hardware vendor; on Lineout the Linux kernel is even updatable independently of Android |
| **Customization** | Surface-level (wallpaper, MDM policies) | Deep: boot modes, UI shells, preinstalled apps, hardware behavior, all configurable per customer |
| **Kiosk features** | Requires a third-party MDM subscription | Built into the OS, no per-seat MDM fee required |
| **Bloatware** | OEM and carrier apps included | Only what the customer's build flags include |

**The cost story sells itself:** a customer with 200 existing POS terminals or panel PCs can redeploy them as locked-down Android kiosks instead of purchasing 200 new OEM tablets plus an MDM subscription.

---

## 4. Talking Points by Customer Situation

**"We have existing x86 hardware we'd like to reuse."**
One generic image adapts to different displays, touchscreens, and peripherals automatically. No per-model firmware. Fewer SKUs to manage, and existing hardware gets a second life.

**"We need a locked-down kiosk."**
Lockdown is a first-class boot mode, not an app bolted on top. The Restricted Launcher provides admin/lockdown modes with password-protected unlock, auto-start of the customer's app, branded overlays (company logo watermark, hidden settings access), and DNS-level internet restriction so devices can only reach approved sites. On A14/A16 builds, GRUB "Bass boot options" let a technician switch a device between Tablet, Desktop, and Kiosk personalities without reimaging.

**"We deploy hundreds of devices."**
BootSight handles fleet identity and license activation. Ethernet provisioning configures devices on first boot. Configuration is file- and property-based, so a golden config can be cloned across the fleet. Remote management works over VNC or scrcpy, and OTA updates keep fleets current.

**"We're worried about privacy / Google."**
Bass builds require no Google account and ship with curated open-source applications. Customer-private applications and configurations stay in private repositories — they are never published with the generic OS.

**"Our users need a desktop, not a tablet."**
SmartDock DFC turns any Bass device into a windowed, multi-monitor desktop workstation with taskbar, freeform windows, and per-display scaling. (See the dedicated [SmartDock DFC Sales Guide](../applications/SmartDockDFC/SALES_GUIDE.md).)

**"We also run Linux software on these boxes."**
Bass: Lineout ships an optional Debian subsystem alongside Android; Bass: Submix inverts the stack entirely, running Android in a container on a Debian host. Either way the customer gets `apt`, `systemd`, and standard Linux tools on the same device that runs their Android apps.

**"What happens in three years?"**
The platform is engineered for portability across Android versions ("work with all future versions of Android with little to no changes" is a core project principle). The customer's investment in configuration and addons carries forward.

---

## 5. The Modularity Story: What the Addons Do and Why

### Why Bass is built as a modular system

Every Bass image is assembled from a **stable generic core** plus **optional addons**, each toggled with a simple build flag. This architecture is deliberate, and it is a selling point in itself:

1. **Customers only get (and pay for) what they need.** A signage build doesn't carry kiosk-launcher code; a kiosk build doesn't carry a desktop shell.
2. **Private things stay private.** Each addon lives in its own repository. A customer's branded launcher, security app, or configuration never mixes with another customer's build or with the public core.
3. **One core, many products.** The same tested core ships to every customer, so quality improvements benefit everyone at once, while differentiation happens in the addon layer.
4. **Fast turnaround.** Adding a customer-specific preinstalled app is a drop-in package and a build flag — not an engineering project.

### The addon catalog, in plain language

**Hardware adaptation** — makes generic hardware "just work":

- **Display Mapper** — per-display resolution, DPI, and orientation, including multi-monitor setups.
- **Touch Mapper** — aligns touchscreens to the right display, fixes inverted or rotated touch.
- **Button Manager** — maps the hardware buttons found on POS and industrial devices to Android actions.
- **Dynamic hardware profiles** — automatic detection of displays, HDMI audio, rotation sensors, lid switches, and power/battery behavior at boot.

**Configuration & branding** — the "zero-code customization" layer:

- **Config Overrides** — settings and system properties applied from simple config files, ideal for fleet-wide policies.
- **Boot Config / Bass boot options** — on-device and GRUB-level selection of boot personality (Tablet UI, Desktop UI, Kiosk).
- **Tweaks** — customer-facing switches added to Android Settings.
- **Vendor configuration layer** — each customer's look-and-feel (boot animation, wallpapers, preloads, default settings) packaged separately from the OS core.

**Kiosk & security** — the lockdown product:

- **Restricted Launcher Pro** — admin/lockdown launcher with password-protected unlock, app auto-start, logo watermark overlay, and hidden settings access.
- **Internet Security** — DNS-based restriction so locked-down devices reach only approved sites.
- **Admin restriction features** — keep end users out of system settings entirely.

**Fleet & lifecycle** — operations at scale:

- **BootSight** — fleet identity, license activation, and status UI.
- **Ethernet Config** — wired-network provisioning for first-boot enrollment.
- **Logger** — rolling on-device log capture for remote diagnostics.
- **Updates & OTA** — controlled update channels per fleet.

**User experience** — optional front-ends:

- **SmartDock DFC** — full desktop shell with taskbar, windows, and multi-monitor support.
- **BassView** — web/content viewer for signage-style deployments.
- **Monterey Standby** — standby/idle display experience.
- **Ax86 Docs** — the product documentation compiled into an on-device app.
- **FOSS app set** — curated open-source apps (file manager, terminal, email, and more) with no Google dependency.

### How to phrase it to a customer

> "Think of Bass as a chassis and a parts catalog. The chassis — the OS core — is identical and battle-tested across all of our customers. Your product is assembled from that chassis plus exactly the modules your deployment needs: your branding, your launcher, your security policy, your preloaded apps. When we improve the chassis, you benefit automatically; when you need something bespoke, it's a private module only you receive."

---

## 6. Quick Objection Handling

**"Is this a hobbyist Android fork?"**
No. Bass: Lineout is built on LineageOS with an enterprise vendor layer, a defined release process, deployment tooling, licensing infrastructure, and product documentation. The hobbyist projects it descends from are the *reference*, not the product.

**"Can it pass our security review?"**
Lockdown builds restrict the device to approved apps and approved network destinations (DNS restriction). There is no Google account or Google telemetry requirement. Customer-specific security modules can be added privately.

**"What if our hardware isn't supported?"**
The platform is designed for generic x86_64 hardware with dynamic detection. Evaluation is straightforward: boot the live installer on the target hardware. Hardware enablement gaps become engineering tickets against the shared core — which then benefits every deployment on similar hardware.

**"Who supports it?"**
We do — the OS core, the addons, and the customer's private modules all come from one vendor. There is no finger-pointing between an OEM, an MDM vendor, and an app developer.

---

## 7. Where to Learn More

| Topic | Document |
|---|---|
| Technical overview of the Bass architecture | [High Level Overview](../development/bass-high-level-overview.md) |
| Installation walkthrough | [Install A13-A15 / Aaropa Installer](../Installation/x86_64-v2/bass_os_aio_android-13-15_install_process.md) |
| Kiosk / lockdown behavior | [Booting into lockdown builds](../setup_and_configuration/booting-into-lockdown-builds.md) |
| Restricted Launcher features | [Bliss Restricted Launcher](../applications/BlissRestrictedLauncher/BlissRestrictedLauncher.md) |
| Desktop shell sales material | [SmartDock DFC Sales Guide](../applications/SmartDockDFC/SALES_GUIDE.md) and [Marketing](../applications/SmartDockDFC/MARKETING.md) |
| Fleet management | [Fleet Management](../features/fleet-management.md) |
| DNS internet restriction | [DNS Internet Restriction](../features/dns-internet-restriction.md) |
| Updates | [Updates and OTA](../features/updates-and-ota.md) |

For product-line naming rules (when to say "Bass: Lineout" vs. the engineering codename), sales staff should always use the **product names** — Bass OS, Bass: Lineout, Bass: Submix — in customer-facing material.
