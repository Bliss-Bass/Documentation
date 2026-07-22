# Bass Product Family: Sales & Positioning Guide

This guide is for sales and business-development staff. It explains what Bass is, how each product line differs in plain language, and how add-ons work across the whole family. No engineering background is required. Use **product names only** with customers (never internal codenames).

---

## 1. Executive Summary

**Bass** (Broad Apparatus Support System) turns everyday PC-class hardware into fully supported Android devices: tablets, panel PCs, POS terminals, mini PCs, and industrial computers. Customers do not need purpose-built Android hardware from a big OEM, and they do not need an engineering team to build Android from scratch.

One Bass image can adapt to the hardware it boots on (for most PC-class devices). Optional **add-ons** layer on kiosk lockdown, desktop productivity, fleet management, security, and per-customer branding. Customers pay for and receive only what their deployment needs.

The core pitch in one sentence:

> **"Enterprise Android on the hardware you already have: one platform family, only the features you need."**

---

## 2. What customers are choosing (plain language)

Every Bass product gives the customer **Android apps and an Android-style experience**. The product lines differ in *how* that Android experience sits on the machine, and *who owns the underlying computer OS*.

Think of it as four buying questions:

1. Do they want Android running as the main OS on the device?
2. Do they also need real Linux tools on the same box?
3. Do they already run their own Linux and only want Android added on top?
4. Are they standardized on Raspberry Pi / similar small boards?

| Customer situation | Lead with | In one sentence |
|---|---|---|
| New tablet, kiosk, panel PC, or POS on PC hardware | **Bass: Lineout** | Our current flagship: Android runs as the main OS on the device. |
| Same as above, but they also need full Linux services | **Bass: Submix** | A small Linux foundation runs the computer; Android runs on top in a container. |
| They already have Linux; they only want Android | **Waydroid_NT** | We supply the Android-in-a-container piece for *their* Linux. |
| Existing Bass fleets / older Android range | **Bass OS** (classic) | The original Bass line; still supported for current customers. |
| Raspberry Pi 4/5 (or similar arm boards) | **Bass-ARM** | Same Bass experience on those boards, as a dedicated per-board build. |

**Default recommendation for new PC-class deals:** Bass: Lineout.

---

## 3. The product lines (what each is, and why it matters)

### Bass: Lineout (flagship)

**What it is:** Android is the operating system on the device. The customer turns the machine on and works in Android (tablet UI, desktop UI, or kiosk), without managing a separate computer OS underneath.

**Who it is for:** New tablet, kiosk, digital signage, POS, and enterprise PC-hardware deployments.

**Why customers care:**
- Dynamic hardware detection (displays, audio, touch, sensors, power) so one image covers many device models
- Easy switch between Tablet, Desktop, and Kiosk personalities (Bass boot options)
- Enterprise deployment, licensing, and on-device documentation built in
- Full access to the Bass add-on library

**Android versions (customer-facing):** Android 14 and Android 16 class releases.

---

### Bass: Submix

**What it is:** The computer boots a lightweight Linux foundation. Android runs *inside* that environment (in a container). Users still get a near-native Android experience, and IT also gets standard Linux tooling on the same box.

**Who it is for:** Deployments that need both Android apps *and* Linux-native services (custom daemons, host networking, Linux peripherals, familiar Linux admin workflows).

**Why customers care:**
- Android apps and Linux tools on one machine
- Same Bass add-ons and configuration model on the Android side as Lineout
- Fits teams that are comfortable with Linux operations

**Android versions (customer-facing):** Android 16 class releases.

**How to explain the difference from Lineout:**
- **Lineout:** Android *is* the OS.
- **Submix:** Linux *hosts* the machine; Android runs on top.

---

### Bass OS (classic)

**What it is:** The original Bass product line. Android runs directly on the hardware, similar in spirit to Lineout, covering a broader older Android range.

**Who it is for:** Existing Bass fleets and customers already standardized on classic Bass images.

**Why customers care:** Continuity for fleets already in the field; broad legacy hardware coverage.

**Android versions (customer-facing):** Android 12L through Android 15 class releases.

**Sales note:** Keep supporting existing classic customers. Steer **new** opportunities to Lineout or Submix unless the customer has a clear classic-only constraint.

---

### Waydroid_NT (“bring your own Linux”)

**What it is:** We do **not** replace the customer’s computer OS. They keep their Linux distribution. We provide Bass-customized Android images and container services that install into that environment, plus our add-ons and configuration tooling on the Android side.

**Who it is for:** Platform teams that already own Linux and only want a supported, brandable Android runtime on top.

**Why customers care:**
- No forced host OS swap
- Supported Android container experience with Bass kiosk, branding, and config options
- Commercial add-ons available through licensing

**Sales takeaway:** If they say “we already run Linux; we just need Android,” lead with Waydroid_NT. If they want us to deliver the whole stack (Linux host + Android), lead with Submix.

---

### Bass-ARM (Raspberry Pi and similar boards)

**What it is:** The same Bass building blocks and add-on library, delivered as a dedicated build for specific arm boards (today: Raspberry Pi 4/5 with Android 16 class releases).

**Who it is for:** Projects standardized on Raspberry Pi or similar boards.

**Why customers care:** Desktop mode, kiosk, FOSS app set, and branding options through the same add-on / build-flag model customers see on PC-class Bass.

**Important difference from PC Bass:** On typical PC hardware, one generic image often adapts to many devices. On these boards, boot and setup are board-specific, so each supported board gets a **pre-tuned build**. The customer-facing features are the same idea; the hardware flexibility is what differs.

---

## 4. How add-ons apply across all product lines

**Add-ons are shared capability, not a separate product family.**

Whatever product line you sell (Lineout, Submix, classic Bass OS, Waydroid_NT, or Bass-ARM), the customer is still choosing from the **same Bass add-on catalog** for the Android experience: kiosk, desktop shell, fleet tools, security, branding, hardware helpers, and so on.

### What that means for the customer

| Point | Plain-language meaning |
|---|---|
| **One parts catalog** | Learn the add-ons once; they map across the product lines. |
| **Pay for what you need** | A signage build does not need a desktop shell; a kiosk build does not need unused modules. |
| **Private stays private** | Customer branding, private apps, and private config are packaged for that customer—not mixed into the public core or another customer’s build. |
| **Same story, different delivery** | Lineout / classic / Bass-ARM deliver Android as the main (or board) OS. Submix / Waydroid_NT deliver Android in a container. The add-ons still describe what the Android side can do. |

### How to say it in a meeting

> “Bass is a chassis plus a parts catalog. The chassis is the product line that matches how you want Android to sit on the machine. The parts—kiosk, desktop, fleet, security, branding—are the same catalog. You only take the parts you need, and your private pieces stay yours.”

### Practical sales rules

1. **Pick the product line from the customer’s OS / hardware situation** (section 2–3).
2. **Pick add-ons from the deployment need** (kiosk, desktop, fleet, branding, etc.)—not from the product-line name.
3. **Do not imply** that SmartDock, Restricted Launcher, BootSight, or branding only exist on one line. They are Bass capabilities; availability is about licensing and the build you assemble for that customer.
4. **Submix and Waydroid_NT:** sell Linux-side benefits as host benefits; sell add-ons as Android-side benefits.

---

## 5. The add-on catalog (plain language)

### Hardware adaptation (make generic devices “just work”)

- **Display Mapper** — resolution, DPI, and orientation per screen, including multi-monitor.
- **Touch Mapper** — align touchscreens to the correct display; fix inverted or rotated touch.
- **Button Manager** — map POS / industrial hardware buttons to useful actions.
- **Dynamic hardware profiles** — automatic detection of displays, HDMI audio, sensors, lids, and power/battery behavior at boot.

### Configuration and branding (customize without writing an OS)

- **Config Overrides** — settings and policies from simple config files; ideal for fleets.
- **Boot Config / Bass boot options** — choose Tablet, Desktop, or Kiosk personality.
- **Tweaks** — customer-facing switches in Android Settings.
- **Vendor configuration** — boot animation, wallpapers, preloads, and defaults packaged per customer.

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

## 6. How Bass compares to “stock Android” and OEM tablets

### Versus building from stock Android source yourself

Stock Android source is a starting point, not a finished product. Someone still has to make it install on real hardware, add kiosk and fleet tools, brand it, and maintain it. That is the work Bass already packages.

| Need | DIY stock Android | Bass |
|---|---|---|
| Runs on generic PC hardware | Usually not without heavy work | Yes (especially Lineout / classic on x86) |
| Installer and provisioning | Build it yourself | Guided installer and fleet tooling |
| Kiosk / lockdown | Build or buy third-party | Built-in add-ons |
| Desktop / multi-display | Minimal | SmartDock DFC add-on |
| Per-customer branding | Custom engineering | Config and vendor packaging |
| Ongoing maintenance | Your team | Our release cadence across supported Android versions |

### Versus buying OEM Android tablets

| Concern | Typical OEM Android | Bass |
|---|---|---|
| Hardware choice | Locked to that OEM’s catalog | Compatible PC hardware you choose or already own |
| Google dependency | Often baked in | No Google account required by default |
| Support window | Tied to OEM refresh cycles | OS lifecycle managed with the Bass platform |
| Customization | Mostly MDM / surface settings | Boot modes, UI shells, preloads, hardware behavior |
| Kiosk | Often needs a paid MDM stack | Available as Bass add-ons |
| Software footprint | OEM / carrier extras | Only what the customer’s build includes |

**Cost story:** a customer with existing POS terminals or panel PCs can redeploy them as locked-down Android devices instead of buying a full OEM tablet fleet plus separate MDM seats.

---

## 7. Talking points by customer situation

**“We have existing PC hardware we’d like to reuse.”**  
Lead with Lineout (or classic if they are already on it). One image adapts across many displays and peripherals. Fewer SKUs; hardware gets a second life.

**“We need a locked-down kiosk.”**  
Lockdown is a first-class personality, not a random app. Restricted Launcher, branded overlays, and optional DNS internet restriction. Technicians can switch Tablet / Desktop / Kiosk personalities without reimaging where Bass boot options are enabled.

**“We deploy hundreds of devices.”**  
BootSight for identity and licensing, Ethernet provisioning, file-based config cloning, remote tools, and OTA channels. Same add-on story whether the fleet is Lineout, Submix, or Waydroid_NT on the Android side.

**“We’re worried about privacy / Google.”**  
No Google account required by default; curated open-source apps. Customer-private apps and configs stay private.

**“Our users need a desktop, not a tablet.”**  
SmartDock DFC add-on: windowed multi-monitor desktop. Same add-on pitch across product lines. See the [SmartDock DFC Sales Guide](../applications/SmartDockDFC/SALES_GUIDE.md).

**“We also run Linux software on these boxes.”**  
- Need the full stack from us → **Submix**  
- Already have Linux → **Waydroid_NT**  
- Mostly Android, with optional Linux helpers → **Lineout** (and discuss their exact Linux needs)

**“We’re standardized on Raspberry Pi.”**  
**Bass-ARM:** same Bass add-on ideas, dedicated board builds.

**“What happens in three years?”**  
The platform is designed so customer investment in configuration and add-ons can carry forward as Android versions advance. You are selling continuity of *their* product definition, not a one-off image.

---

## 8. Quick objection handling

**“Is this a hobbyist project?”**  
No. Bass is a commercial product family with a defined release process, deployment tooling, licensing, documentation, and supported add-ons. Community Android projects may inform engineering practice; they are not what the customer buys.

**“Can it pass our security review?”**  
Lockdown builds can restrict apps and network destinations. There is no Google account or Google telemetry requirement by default. Customer-specific security modules can be added privately.

**“What if our hardware isn’t supported?”**  
For PC-class hardware, evaluation is straightforward: boot the live installer on the target machine. Gaps become shared platform improvements that help similar hardware later.

**“Who supports it?”**  
One vendor for the OS product line, the add-ons, and the customer’s private modules—no finger-pointing between an OEM, an MDM vendor, and an app developer.

---

## 9. Cheatsheet: which product line to open with

| If the customer says… | Open with… |
|---|---|
| “We need Android kiosks / tablets on PC hardware.” | **Bass: Lineout** |
| “We need Android *and* full Linux on the same box.” | **Bass: Submix** |
| “We already run Linux; just give us Android.” | **Waydroid_NT** |
| “We’re already on Bass / need the older Android range.” | **Bass OS** (classic) |
| “We’re on Raspberry Pi.” | **Bass-ARM** |
| “We need a desktop UI / multi-monitor.” | Product line from above **+ SmartDock DFC add-on** |
| “We need lockdown / no Google / fleet licensing.” | Product line from above **+ kiosk / BootSight / security add-ons** |

---

## 10. Where to learn more

| Topic | Document |
|---|---|
| Technical overview of the Bass architecture | [High Level Overview](../development/bass-high-level-overview.md) |
| Installation walkthrough | [Install A13–A15 / Aaropa Installer](../Installation/x86_64-v2/bass_os_aio_android-13-15_install_process.md) |
| Kiosk / lockdown behavior | [Booting into lockdown builds](../setup_and_configuration/booting-into-lockdown-builds.md) |
| Restricted Launcher features | [Bliss Restricted Launcher](../applications/BlissRestrictedLauncher/BlissRestrictedLauncher.md) |
| Desktop shell sales material | [SmartDock DFC Sales Guide](../applications/SmartDockDFC/SALES_GUIDE.md) and [Marketing](../applications/SmartDockDFC/MARKETING.md) |
| Fleet management | [Fleet Management](../features/fleet-management.md) |
| DNS internet restriction | [DNS Internet Restriction](../features/dns-internet-restriction.md) |
| Updates | [Updates and OTA](../features/updates-and-ota.md) |

**Customer-facing naming:** always say **Bass OS**, **Bass: Lineout**, **Bass: Submix**, **Waydroid_NT**, and **Bass-ARM**. Do not use engineering tree names in sales material.
