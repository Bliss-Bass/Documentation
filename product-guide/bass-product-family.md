# Bass Product Family Guide

This guide explains what Bass is, how each product line differs, and how add-ons work across the whole family. It is written for readers who are new to Bass and do not need an engineering background. Use **product names only** in customer-facing material (never internal codenames).

---

## 1. Overview

**Bass** (Broad Apparatus Support System) turns everyday PC-class hardware into fully supported Android devices: tablets, panel PCs, POS terminals, mini PCs, and industrial computers. You do not need purpose-built Android hardware from a big OEM, and you do not need an engineering team to build Android from scratch.

One Bass image can adapt to the hardware it boots on (for most PC-class devices). Optional **add-ons** layer on kiosk lockdown, desktop productivity, fleet management, security, and per-customer branding. You pay for and receive only what your deployment needs.

In short:

> **Enterprise Android on the hardware you already have: one platform family, only the features you need.**

---

## 2. Choosing a product line

Every Bass product provides **Android apps and an Android-style experience**. The product lines differ in *how* that Android experience sits on the machine, and *who owns the underlying computer OS*.

Four questions help narrow the choice:

1. Do you want Android running as the main OS on the device?
2. Do you also need full Linux tools on the same box?
3. Do you already run your own Linux and only want Android added on top?
4. Are you standardized on Raspberry Pi or similar small boards?

| Your situation | Best fit | In one sentence |
|---|---|---|
| New tablet, kiosk, panel PC, or POS on PC hardware | **Bass: Lineout** | The current flagship: Android runs as the main OS on the device. |
| Same as above, but you also need full Linux services | **Bass: Submix** | A small Linux foundation runs the computer; Android runs on top in a container. |
| You already have Linux; you only want Android | **Waydroid_NT** | Bass supplies the Android-in-a-container piece for *your* Linux. |
| Existing Bass fleets / older Android range | **Bass OS** (classic) | The original Bass line; still supported for current deployments. |
| Raspberry Pi 4/5 (or similar arm boards) | **Bass-ARM** | The same Bass experience on those boards, as a dedicated per-board build. |

**Default for new PC-class projects:** Bass: Lineout.

---

## 3. Product lines in detail

### Bass: Lineout (flagship)

**What it is:** Android is the operating system on the device. You turn the machine on and work in Android (tablet UI, desktop UI, or kiosk), without managing a separate computer OS underneath.

**Who it is for:** New tablet, kiosk, digital signage, POS, and enterprise PC-hardware deployments.

**Benefits:**
- Dynamic hardware detection (displays, audio, touch, sensors, power) so one image covers many device models
- Easy switch between Tablet, Desktop, and Kiosk personalities (Bass boot options)
- Enterprise deployment, licensing, and on-device documentation built in
- Full access to the Bass add-on library

**Android versions:** Android 14 and Android 16 class releases.

---

### Bass: Submix

**What it is:** The computer boots a lightweight Linux foundation. Android runs *inside* that environment (in a container). Users still get a near-native Android experience, and IT also gets standard Linux tooling on the same box.

**Who it is for:** Deployments that need both Android apps *and* Linux-native services (custom daemons, host networking, Linux peripherals, familiar Linux admin workflows).

**Benefits:**
- Android apps and Linux tools on one machine
- Same Bass add-ons and configuration model on the Android side as Lineout
- Fits teams that are comfortable with Linux operations

**Android versions:** Android 16 class releases.

**Difference from Lineout:**
- **Lineout:** Android *is* the OS.
- **Submix:** Linux *hosts* the machine; Android runs on top.

---

### Bass OS (classic)

**What it is:** The original Bass product line. Android runs directly on the hardware, similar in spirit to Lineout, covering a broader older Android range.

**Who it is for:** Existing Bass fleets and organizations already standardized on classic Bass images.

**Benefits:** Continuity for fleets already in the field; broad legacy hardware coverage.

**Android versions:** Android 12L through Android 15 class releases.

**Note:** Classic remains supported. New projects should use Lineout or Submix unless there is a clear classic-only constraint.

---

### Waydroid_NT (“bring your own Linux”)

**What it is:** Bass does **not** replace your computer OS. You keep your Linux distribution. Bass provides customized Android images and container services that install into that environment, plus add-ons and configuration tooling on the Android side.

**Who it is for:** Platform teams that already own Linux and only want a supported, brandable Android runtime on top.

**Benefits:**
- No forced host OS swap
- Supported Android container experience with Bass kiosk, branding, and config options
- Commercial add-ons available through licensing

**How it relates to Submix:** If you already run Linux and only need Android, choose Waydroid_NT. If you want Bass to deliver the whole stack (Linux host + Android), choose Submix.

---

### Bass-ARM (Raspberry Pi and similar boards)

**What it is:** The same Bass building blocks and add-on library, delivered as a dedicated build for specific arm boards (today: Raspberry Pi 4/5 with Android 16 class releases).

**Who it is for:** Projects standardized on Raspberry Pi or similar boards.

**Benefits:** Desktop mode, kiosk, FOSS app set, and branding options through the same add-on / build-flag model used on PC-class Bass.

**Important difference from PC Bass:** On typical PC hardware, one generic image often adapts to many devices. On these boards, boot and setup are board-specific, so each supported board gets a **pre-tuned build**. The feature set is the same idea; the hardware flexibility is what differs.

---

## 4. How add-ons apply across all product lines

**Add-ons are shared capability, not a separate product family.**

Whatever product line you choose (Lineout, Submix, classic Bass OS, Waydroid_NT, or Bass-ARM), you still select from the **same Bass add-on catalog** for the Android experience: kiosk, desktop shell, fleet tools, security, branding, hardware helpers, and so on.

### What that means

| Point | Meaning |
|---|---|
| **One parts catalog** | Learn the add-ons once; they map across the product lines. |
| **Pay for what you need** | A signage build does not need a desktop shell; a kiosk build does not need unused modules. |
| **Private stays private** | Your branding, private apps, and private config are packaged for you—not mixed into the public core or another organization’s build. |
| **Same capabilities, different delivery** | Lineout / classic / Bass-ARM deliver Android as the main (or board) OS. Submix / Waydroid_NT deliver Android in a container. The add-ons still describe what the Android side can do. |

### How to think about it

> Bass is a chassis plus a parts catalog. The chassis is the product line that matches how you want Android to sit on the machine. The parts—kiosk, desktop, fleet, security, branding—are the same catalog. You only take the parts you need, and your private pieces stay yours.

### Choosing product line vs add-ons

1. **Choose the product line** from your OS and hardware situation (sections 2–3).
2. **Choose add-ons** from the deployment need (kiosk, desktop, fleet, branding, and so on)—not from the product-line name.
3. Capabilities such as SmartDock, Restricted Launcher, BootSight, and branding are **Bass capabilities**. Availability depends on licensing and the build assembled for your project, not on which product line name you use.
4. For **Submix** and **Waydroid_NT**, Linux-side benefits belong to the host; add-ons describe the Android-side experience.

---

## 5. The add-on catalog

### Hardware adaptation (make generic devices “just work”)

- **Display Mapper** — resolution, DPI, and orientation per screen, including multi-monitor.
- **Touch Mapper** — align touchscreens to the correct display; fix inverted or rotated touch.
- **Button Manager** — map POS / industrial hardware buttons to useful actions.
- **Dynamic hardware profiles** — automatic detection of displays, HDMI audio, sensors, lids, and power/battery behavior at boot.

### Configuration and branding (customize without writing an OS)

- **Config Overrides** — settings and policies from simple config files; ideal for fleets.
- **Boot Config / Bass boot options** — choose Tablet, Desktop, or Kiosk personality.
- **Tweaks** — switches in Android Settings.
- **Vendor configuration** — boot animation, wallpapers, preloads, and defaults packaged per organization.

### Kiosk and security (lock the device down)

- **Restricted Launcher** — admin/lockdown launcher, password unlock, app auto-start, logo watermark, hidden settings access.
- **Internet Security** — DNS-based restriction so devices only reach approved sites.
- **Admin restriction** — keep end users out of system settings.

### Fleet and lifecycle (operate at scale)

- **BootSight** — fleet identity, license activation, and status UI.
- **Ethernet Config** — wired-network provisioning for first-boot enrollment.
- **Logger** — on-device log capture for remote diagnostics.
- **Updates & OTA** — controlled update channels per fleet.

### User experience (optional front ends)

- **SmartDock DFC** — windowed desktop shell, taskbar, multi-monitor.
- **BassView** — web/content viewer for signage-style use.
- **Monterey Standby** — standby / idle display experience.
- **Ax86 Docs** — product documentation as an on-device app.
- **FOSS app set** — curated open-source apps with no Google account requirement.

---

## 6. How Bass compares to stock Android and OEM tablets

### Versus building from stock Android source yourself

Stock Android source is a starting point, not a finished product. Someone still has to make it install on real hardware, add kiosk and fleet tools, brand it, and maintain it. That is the work Bass already packages.

| Need | DIY stock Android | Bass |
|---|---|---|
| Runs on generic PC hardware | Usually not without heavy work | Yes (especially Lineout / classic on x86) |
| Installer and provisioning | Build it yourself | Guided installer and fleet tooling |
| Kiosk / lockdown | Build or buy third-party | Built-in add-ons |
| Desktop / multi-display | Minimal | SmartDock DFC add-on |
| Per-organization branding | Custom engineering | Config and vendor packaging |
| Ongoing maintenance | Your team | Bass release cadence across supported Android versions |

### Versus buying OEM Android tablets

| Concern | Typical OEM Android | Bass |
|---|---|---|
| Hardware choice | Locked to that OEM’s catalog | Compatible PC hardware you choose or already own |
| Google dependency | Often baked in | No Google account required by default |
| Support window | Tied to OEM refresh cycles | OS lifecycle managed with the Bass platform |
| Customization | Mostly MDM / surface settings | Boot modes, UI shells, preloads, hardware behavior |
| Kiosk | Often needs a paid MDM stack | Available as Bass add-ons |
| Software footprint | OEM / carrier extras | Only what your build includes |

**Cost perspective:** existing POS terminals or panel PCs can often be redeployed as locked-down Android devices instead of buying a full OEM tablet fleet plus separate MDM seats.

---

## 7. Common goals and which pieces fit

**Reuse existing PC hardware.**  
Lineout (or classic if already in use). One image adapts across many displays and peripherals. Fewer SKUs; hardware gets a second life.

**Locked-down kiosk.**  
Lockdown is a first-class personality, not a bolted-on app. Restricted Launcher, branded overlays, and optional DNS internet restriction. Where Bass boot options are enabled, a device can switch between Tablet, Desktop, and Kiosk personalities without reimaging.

**Hundreds of devices.**  
BootSight for identity and licensing, Ethernet provisioning, file-based config cloning, remote tools, and OTA channels. Same add-on model whether the fleet is Lineout, Submix, or Waydroid_NT on the Android side.

**Privacy / no Google account.**  
No Google account required by default; curated open-source apps. Private apps and configs stay private.

**Desktop, not tablet.**  
SmartDock DFC add-on: windowed multi-monitor desktop. Same add-on across product lines. See the [SmartDock DFC Guide](../applications/SmartDockDFC/SALES_GUIDE.md).

**Android and Linux on the same box.**  
- Full stack from Bass → **Submix**  
- Linux already in place → **Waydroid_NT**  
- Mostly Android, with limited Linux needs → **Lineout** (confirm the exact Linux requirements)

**Raspberry Pi / arm64 boards.**  
**Bass-ARM:** same Bass add-on model, dedicated board builds.

**Longevity.**  
The platform is designed so investment in configuration and add-ons can carry forward as Android versions advance. The goal is continuity of your product definition, not a one-off image.

---

## 8. Common questions

**Is this a hobbyist project?**  
No. Bass is a commercial product family with a defined release process, deployment tooling, licensing, documentation, and supported add-ons.

**Can it pass a security review?**  
Lockdown builds can restrict apps and network destinations. There is no Google account or Google telemetry requirement by default. Organization-specific security modules can be added privately.

**What if the hardware is not supported?**  
For PC-class hardware, evaluation is straightforward: boot the live installer on the target machine. Gaps become shared platform improvements that help similar hardware later.

**Who supports it?**  
One vendor for the OS product line, the add-ons, and private modules—no split between an OEM, an MDM vendor, and an app developer.

---

## 9. Quick reference

| Goal | Start with |
|---|---|
| Android kiosks / tablets on PC hardware | **Bass: Lineout** |
| Android and full Linux on the same box | **Bass: Submix** |
| Linux already in place; add Android | **Waydroid_NT** |
| Existing Bass fleet / older Android range | **Bass OS** (classic) |
| Raspberry Pi | **Bass-ARM** |
| Desktop UI / multi-monitor | Product line above **+ SmartDock DFC add-on** |
| Lockdown / no Google / fleet licensing | Product line above **+ kiosk / BootSight / security add-ons** |

---

## 10. Where to learn more

| Topic | Document |
|---|---|
| Technical overview of the Bass architecture | [High Level Overview](../development/bass-high-level-overview.md) |
| Installation walkthrough | [Install A13–A15 / Aaropa Installer](../Installation/x86_64-v2/bass_os_aio_android-13-15_install_process.md) |
| Kiosk / lockdown behavior | [Booting into lockdown builds](../setup_and_configuration/booting-into-lockdown-builds.md) |
| Restricted Launcher features | [Bliss Restricted Launcher](../applications/BlissRestrictedLauncher/BlissRestrictedLauncher.md) |
| Desktop shell overview | [SmartDock DFC Guide](../applications/SmartDockDFC/SALES_GUIDE.md) and [Marketing](../applications/SmartDockDFC/MARKETING.md) |
| Fleet management | [Fleet Management](../features/fleet-management.md) |
| DNS internet restriction | [DNS Internet Restriction](../features/dns-internet-restriction.md) |
| Updates | [Updates and OTA](../features/updates-and-ota.md) |

**Naming:** use **Bass OS**, **Bass: Lineout**, **Bass: Submix**, **Waydroid_NT**, and **Bass-ARM** in customer-facing material. Do not use engineering tree names.
