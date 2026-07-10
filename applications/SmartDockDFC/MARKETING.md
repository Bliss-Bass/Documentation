# SmartDock DFC: Marketing the Right Experience for Every Device

SmartDock DFC is one shell that can wear many hats. The same privileged desktop framework can look and behave like a locked kiosk, a checkout terminal, a multi-monitor workstation, a tablet productivity UI, or a phone that docks into a desk. Configuration is property-driven, so OEMs and integrators can ship different "personalities" of the same product without forking the app.

This page is about **how to talk about those setups**. For feature lists see [SMARTDOCK_FEATURES.md](SMARTDOCK_FEATURES.md). For OEM props see [VENDOR_GUIDE.md](VENDOR_GUIDE.md). For sales talking points see [SALES_GUIDE.md](SALES_GUIDE.md).

---

## The pitch in one line

**Your hardware. One shell. Many roles.** SmartDock DFC turns Android into the front end customers actually use, whether that front end is a single full-screen app or a full desktop with freeform windows and external displays.

---

## Form factors

### Phone
* Handheld first: compact dock, gesture-friendly navigation, touch-optimized layouts.
* Dock it to HDMI or a USB-C display and the same device becomes a small workstation: independent dock on the external screen, virtual touchpad or physical pointer routing, freeform apps on the big panel.
* Marketing angle: "The phone that becomes a PC when you plug it in."

### Tablet
* Natural home for SmartDock: pinned or auto-hiding taskbar, freeform multitasking, Material Quick Settings.
* Works with keyboard and trackpad for field / education / mobile office kits.
* Marketing angle: "Laptop productivity without buying a second computer."

### Desktop / laptop-class x86
* Full desktop layout (`persist.bass.sd.layout=desktop`), reserved dock space, mouse hover to reveal the bar, hot corners, keyboard shortcuts.
* Multi-monitor: separate SmartDock instances on external displays, per-display DPI, pointer routing.
* Marketing angle: "Android that feels like a workstation, not a stretched phone UI."

### Foldables and convertible 2-in-1s
* Same binary; layout and dock behavior can follow how the device is used (handheld vs open vs docked).
* Marketing angle: "One SKU, many postures."

---

## Vertical use cases

### Kiosk
**Story:** A single purpose device that always looks the same and never invites tinkering.

What to highlight:
* Production lockdown (hide SmartDock customization from end users)
* Skip onboarding for imaged fleets
* Hide or replace stock status / nav / taskbar so only your shell (and your app) show
* Optional pairing with Bass lockdown / restricted or kiosk launchers for app allowlists

Talk track: "Stand it up, lock it down, clone the config across the fleet."

### POS (point of sale)
**Story:** Fast, reliable chrome around a POS app: dock for support tools, tray for network/volume, freeform only when the cashier needs it.

What to highlight:
* Persistent dock for pinned utilities (browser, settings under admin, receipt tools)
* Stable priv-app integration (does not get killed under load)
* Property defaults so every register boots identical
* `.sdp` backup/restore for store rollouts

Talk track: "Same shell on every register. Swap the POS APK, keep the chrome."

### Self-checkout / customer-facing terminal
**Story:** Clean, branded, distraction-free UI facing the customer; staff tools on a second display or behind admin unlock.

What to highlight:
* Full-screen launch mode for the checkout app
* Secondary display support (customer-facing vs attendant)
* Lockdown of customization and system chrome
* High-contrast / themed dock that matches retail branding

Talk track: "Customer screen stays simple. Staff screen stays capable."

### Desktop productivity / mobile office
**Story:** Replace or reduce laptop spend for knowledge workers on tablets and mini PCs.

What to highlight:
* Freeform overlapping windows
* Unified Quick Settings and notifications
* "Continue where you left off" for docs and web
* External monitor + keyboard/mouse as a first-class setup

Talk track: "Dock, keyboard, monitor: instant desk. Undock: instant tablet."

### Education / shared devices
**Story:** Predictable UI for labs and loaners; easy reset via backup.

What to highlight:
* Locked customization for students
* Fast clone of a "golden" `.sdp` image
* Multi-display for classroom carts and teacher stations

Talk track: "Image once. Restore everywhere."

### Industrial / field / rugged
**Story:** Always-available navigation and system tray on devices that live in harsh environments.

What to highlight:
* Persistent dock and tray toggles (Wi-Fi, Bluetooth, volume)
* Works with Bass rugged / tablet builds and hardware function keys (Button Manager)
* Low overhead as a system component

Talk track: "Controls stay reachable with gloves on and apps crashing around them."

### Automotive / infotainment / signage
**Story:** Dense, branded shell on fixed displays.

What to highlight:
* Overlay control of system bars
* Layout and density tuned per panel
* Multi-display for cluster + center stack style setups (where the platform allows)

Talk track: "Your brand owns the chrome, not stock Android."

### Healthcare / hospitality / service desks
**Story:** Shared terminals that must be simple for guests and powerful for staff.

What to highlight:
* Role-like setups via properties (guest vs staff image)
* Quick Settings for volume/brightness without exposing full Settings
* Pairing with license / fleet tools (BootSight or MDM) on Bass builds

Talk track: "Guest mode stays clean. Staff mode stays complete."

---

## How one product becomes many SKUs

| Setup | Typical layout | Dock | Lockdown | Displays |
|-------|----------------|------|----------|----------|
| Phone handheld | `phone` | Hidden or handle | Optional | Internal |
| Phone + monitor | `phone` / `desktop` | Pinned on external | Optional | Internal + HDMI |
| Tablet productivity | `tablet` | Pinned or auto-pin | Light | Internal ± external |
| Desktop / mini PC | `desktop` | Pinned, reserve space | Optional | Multi-monitor |
| Kiosk | `tablet` or `desktop` | Minimal or hidden | Strong | Usually single |
| POS | `tablet` or `desktop` | Pinned utilities | Strong | 1-2 |
| Self-checkout | `tablet` | Hidden / branded | Strong | Customer ± attendant |
| Education lab | `tablet` | Pinned | Strong | Cart / teacher external |

All of the above are the **same SmartDock DFC binary**, steered with `persist.bass.sd.*` (and Bass build flags where applicable). That is the marketing lever: one license conversation, many product stories.

---

## Messaging tips

* Lead with the **role** (kiosk, POS, desk), then the **form factor** (tablet, phone, x86), then the **tech** (freeform, multi-display, props).
* For retail and kiosk buyers, stress **sameness across the fleet** and **lockdown**.
* For OEM / consumer buyers, stress **docked desktop** and **brandable chrome**.
* For IT, stress **priv-app stability**, **property config**, and **`.sdp` clone**.
* Point technical evaluators at the [Vendor Guide](VENDOR_GUIDE.md); keep this page about outcomes.

---

## Closing

SmartDock DFC is not only a "desktop mode for Android." It is a configurable front end for whatever you need the device to be today: phone, tablet, desk, register, kiosk, or checkout lane.

**One shell. Many markets. Your hardware in the middle.**
