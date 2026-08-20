# BT Ferry (Bass BT Ferry)

> **Availability:** BT Ferry ships on **Bass: Lineout Android 16** (Lineage **23.2**) builds that enable the `bass-btferry` addon (`--btferry`). It is **not available on Android 14 / Lineage 21.0** images yet.

BT Ferry is a privileged Bluetooth **phone ferry** for Wi‑Fi/Bluetooth-only tablets and desktops that have no cellular modem. Pair an Android phone or iPhone over Classic Bluetooth; everyday phone presence (messages, contacts, calls, and media audio when supported) appears on the larger Bass Desktop surface. The phone keeps the cellular radio — there is no cloud relay.

| | |
|---|---|
| **Package** | `com.bass.btferry` |
| **Addon id** | `bass-btferry` |
| **Build flag** | `--btferry` / `USE_BTFERRY=true` |
| **Also see** | [User guide](../../UserGuides/bt-ferry.md) |

## What it does

| Feature | Bluetooth profile | Notes |
|---------|-------------------|--------|
| Contacts sync | **PBAP** | Phonebook into the platform PBAP client account |
| SMS inbox + send | **MAP** | MMS/RCS/iMessage chrome are best-effort / OEM-dependent |
| Answer / reject / hang up | **HFP** Hands-Free | Call audio via SCO when the stack routes it |
| Phone media on Desktop speakers | **A2DP Sink** + **AVRCP** | External-speaker mode + transport when the phone publishes metadata |

## How to enable (A16 Lineout)

On a Lineage **23.2** workspace with the addon cloned under `vendor/ax86-lite/addons/bass-btferry/`:

```bash
./build.sh --btferry
# or
USE_BTFERRY=true
```

The addon stages into `device/generic/x86_64_tablet/ax86-addons/BassBtFerry/` and inherits product Bluetooth accessory props (MAP/PBAP/HFP client, A2DP sink, SMS receiver package → `com.bass.btferry`).

## First-run checklist

1. Flash an image built with `--btferry`.
2. Confirm accessory props, e.g. `getprop bluetooth.profile.a2dp.sink.enabled` → `true` (also MAP/PBAP/HFP client roles and `bluetooth.profile.map_client.sms_receiver_package` → `com.bass.btferry`).
3. Open **BT Ferry** → **Bluetooth settings** → pair the phone.
4. Back in BT Ferry, select the phone / connect (PBAP + MAP + HFP + A2DP).
5. Approve contacts / messages / phonebook prompts on the phone.
6. Sync contacts, send a test SMS, place or receive a call, and confirm Desktop speakers for phone media.

## Non-goals (current)

* Guaranteed MMS/RCS or rich iMessage decorations  
* Full Messages/iCloud history browser  
* Arbitrary phone-app notification mirroring (optional iPhone ANCS later)  
* Pretending the Desktop is the cellular modem  

## Related

* [BT Ferry user guide](../../UserGuides/bt-ferry.md)
* [Building Bass OS](../../development/building-bass.md)
* [Addon Development: Bass Lineout](../../development/addon-development.md)
