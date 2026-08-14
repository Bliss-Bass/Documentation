# Bass Boot Options

> **Android 16 Lineout.** Screenshots and steps on these pages were taken on **Bass: Lineout** (Lineage **23.2** / Android **16**). On **Android 14** (Lineage **21.0**) the same tools can look different, sit in a different Settings place, or be missing from that image entirely.

Bass Boot Options is the **menu on the black GRUB screen before Android starts**. It is not an Android app.

## What it is for

Aaropa / Bliss-style installs often show only a short list (Android, Recovery, Advanced). Bass can add a fuller list: tablet, desktop, kiosk, and related start modes. You pick one with the keyboard (or timeout uses the last / default entry).

## How to use it

1. Power on (or reboot) and watch for the boot menu. Press a key if the menu would otherwise hide.
2. Use the arrow keys and Enter.
3. Choose the mode you want for this boot (names vary by image: Tablet, Desktop, Kiosk, and extras).

If you changed [Boot Config](boot-config.md) and the device misbehaves, pick a known-good entry here, or Recovery if you were instructed to.

You will not see this extra submenu on images that were built without Bass Boot Options.

## Related

- [Getting started](README.md)

- [Boot Config](boot-config.md): changes that apply *after* you are in Android
- Technical: [Bass Boot Options](../../setup_and_configuration/bass-boot-options.md)
