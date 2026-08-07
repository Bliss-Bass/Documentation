# Bass boot options

On Aaropa installs, GRUB only ships BlissOS / Recovery / Advanced entries by default. With this package enabled, a **Bass boot options** submenu is added on first boot by writing a separate config and linking it through GRUB's `custom.cfg` (already sourced by `41_custom` in Aaropa's `grub.cfg`).

| | |
|---|---|
| **Build flags** | `--bass-boot-options`, optional `--cxbbo` (customer catalog) |
| **Catalog** | `/vendor/etc/bass_boot/entries.list` (selected at build time) |
| **Generated config** | `/boot/grub/bass_boot_options.cfg` |

## Enable at build time

```bash
./build.sh --bass-boot-options ...
# USE_BASS_BOOT_OPTIONS=true

./build.sh --cxbbo ...
# USE_CX_BASS_BOOT_OPTIONS=true; selects the customer catalog
```

Catalog selection:

| Flag | Catalog installed as `entries.list` |
|------|--------------------------------------|
| `--cxbbo` | `entries.customer.list` - customer-specific catalog; takes precedence over UI mode |
| (none) | `entries.list` - full Tablet + Desktop + Kiosk |
| `--tui` | `entries.tablet.list` |
| `--dui` | `entries.desktop.list` |
| `--kui` | `entries.kiosk.list` |

## Behavior

1. Runs at `sys.boot_completed` via `init.bass_boot_options.rc`.
2. Parses the default `BlissOS` menuentry in `/boot/grub/grub.cfg`.
3. Generates `/boot/grub/bass_boot_options.cfg` from `/vendor/etc/bass_boot/entries.list`.
4. Ensures `/boot/grub/custom.cfg` contains a managed `source $prefix/bass_boot_options.cfg` block.
5. Backs up `grub.cfg` / `custom.cfg` as `*.bak.bass-<timestamp>` (keeps last 3) before edits; restores on failure.

## Runtime disable

```bash
adb shell setprop persist.bass.boot_options 0
# or boot with: androidboot.bass.boot_options=0
```

## Force reinstall

```bash
adb shell rm -f /data/misc/bass_boot_options/installed
# or: BASS_FORCE=1 /vendor/etc/bass_boot/bass_boot_options.sh
```

Catalog version bumps also regenerate on next boot when the marker/version no longer matches. Status is written to `/data/misc/bass_boot_options/status`.

## Related

* [Booting into lockdown builds](booting-into-lockdown-builds.md)
* [Building Bass OS](../development/building-bass.md)
