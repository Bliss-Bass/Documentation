# BlissDeck

> **Availability:** BlissDeck ships on **Bass: Lineout** x86_64 builds that enable the `blissdeck` addon (`--blissdeck`), and on gaming images (`--gaming`), where it is also the Home app.

BlissDeck is a landscape game-library **Home launcher** for Bass gaming images. It lists installed games and apps, shows recently played titles, and can fetch cover art from SteamGridDB.

| | |
|---|---|
| **Package** | `org.gamelauncher` |
| **Addon id** | `blissdeck` |
| **Build flags** | `--blissdeck` / `USE_BLISSDECK=true`; `--gaming` / `SET_GAMINGUI_MODE=true` (implies `--blissdeck`) |
| **Source & releases** | [Bliss-Bass/BlissDeck](https://github.com/Bliss-Bass/BlissDeck) |
| **License** | GPL-3.0, with a Bass commercial option |
| **Also see** | [User guide](../../UserGuides/blissdeck.md) |

## Enable

```bash
./build.sh --blissdeck ...
# USE_BLISSDECK=true

./build.sh --gaming ...
# SET_GAMINGUI_MODE=true (implies --blissdeck; kernel cmdline BASS_GAMINGUI=1)
```

`--gaming` also selects the gaming GRUB catalog when [Bass Boot Options](../../setup_and_configuration/bass-boot-options.md) is enabled, and [Boot Config](../BootConfig/BootConfig.md) can switch an installed device to Gaming mode with **Force Gaming UI** (`BASS_GAMINGUI=1`). Without BlissDeck on the image, that mode has no gaming Home to show.

## Prebuilt APK

The shippable APK is signed in BlissDeck CI. `vendor/ax86-lite/build/blissdeck_build.sh` (called from setup when the addon is enabled) downloads `app-x86_64-release.apk` from the latest, or pinned, GitHub release:

```bash
vendor/ax86-lite/build/blissdeck_build.sh
# or pin a release:
BLISSDECK_RELEASE_TAG=v0.1.4 vendor/ax86-lite/build/blissdeck_build.sh
```

`gh` must be authenticated. The APK is staged as `packages/BlissDeck/prebuilts/blissdeck.apk_all`. Pin a release for reproducible images in `packages/BlissDeck/prebuilts/release-tag.txt`.

## First boot

BlissDeck is installed once per build by a `sys.boot_completed` oneshot (`pm install -r -g`), which then grants the special accesses it needs so the user sees no prompts:

| Access | How |
|--------|-----|
| Declared runtime permissions | `pm install -g`, plus extra `pm grant` |
| Usage access (Last Played) | `appops set GET_USAGE_STATS allow` |
| Accessibility (close or switch freeform games) | `enabled_accessibility_services` with `.data.CloseGameService` |
| Notification listener (badges) | `enabled_notification_listeners` and `cmd notification allow_listener` |
| Home (Gaming mode only) | `pm set-home-activity org.gamelauncher/.MainActivity` |

Install marker: `/data/vendor/blissdeck_post_inst_complete` (keyed to `ro.build.date.utc`). Log: `/data/misc/bassapks/install_apk.log`.

## Licensing note

BlissDeck is GPL-3.0. Products that ship it must include a source-offer URL in their product documentation, for example [github.com/Bliss-Bass/BlissDeck](https://github.com/Bliss-Bass/BlissDeck).

## Related

- [Bass Boot Options](../../setup_and_configuration/bass-boot-options.md)
- [Boot Config](../BootConfig/BootConfig.md)
- [GameNativeX64](../GameNativeX64/GameNativeX64.md)
