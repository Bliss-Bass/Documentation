# GameNativeX64

> **Availability:** GameNativeX64 ships on **Bass: Lineout** x86_64 builds that enable the
> `gamenative` addon (`--gamenative`). It targets Intel and AMD Android tablets and desktops
> (ax86), not ARM handhelds.

GameNativeX64 is the [Bliss-Bass](https://github.com/Bliss-Bass/GameNative-x64) fork of
[GameNative](https://github.com/utkarshdalal/GameNative). Upstream targets ARM64 and uses
Box64/FEX translation; this fork runs **native x86_64** with Mesa Vulkan (ANV/RADV) and adds
Linux desktop app integration for Bass tablet deployments.

| | |
|---|---|
| **Package** | `app.gamenative` |
| **Display name** | GameNativeX64 |
| **Addon id** | `gamenative` |
| **Build flag** | `--gamenative` / `USE_GAMENATIVE=true` |
| **Source & releases** | [Bliss-Bass/GameNative-x64](https://github.com/Bliss-Bass/GameNative-x64) |
| **Upstream** | [utkarshdalal/GameNative](https://github.com/utkarshdalal/GameNative) |

## What it does

* Runs Steam, Epic, and GOG PC games through Proton/Wine on x86_64 Android - no ARM
  translation layer
* Uses hardware Vulkan where the device Mesa stack allows (Intel ANV, AMD RADV; lavapipe as
  software fallback)
* Ships a guest Vulkan payload in-APK (~50 MB compressed; extracted on first launch)
* **Linux apps** - install Debian packages inside a PRoot rootfs, launch GUI apps in per-app
  freeform windows, pin them to the app drawer via lightweight stub APKs

## Installing the APK standalone

For sideload or testing outside a Bass image, download **`app-modernX64-release.apk`** from
the [GameNative-x64 releases](https://github.com/Bliss-Bass/GameNative-x64/releases) page.
Requires an **x86_64** device (API 26+).

```bash
adb install -r app-modernX64-release.apk
```

The first game or Linux session start takes longer while the Vulkan payload unpacks.

## Bass: Lineout image integration

Licensed Lineout workspaces enable GameNative at build time:

```bash
./build.sh --gamenative
# or
USE_GAMENATIVE=true
```

The build downloads a CI-signed release APK (tagged `v*-x64.*` on GameNative-x64) and
preinstalls it on first boot. A privileged **stub installer** (`app.gamenative.stubinstaller`)
is built from source in the image so Linux app drawer entries can be added and removed without
per-install user prompts.

**Release images** must use the CI-signed APK and the release caller certificate list. Dev
images may use `--gamenative-dev-key` for local Gradle builds; do not ship that configuration
to customers.

See [Addon Development: Bass Lineout](../../development/addon-development.md) for how Lineout
addons are wired.

## Fork highlights (vs upstream ARM64)

| Area | Upstream | GameNativeX64 |
|------|----------|---------------|
| CPU | Box64 / FEX | Native x86_64 |
| Vulkan | Vortek ARM proxy | Mesa ANV / RADV |
| Linux apps | - | Session manager, per-app windows, drawer stubs |
| Build flavor | `arm64` | `modernX64` |

Current release series: **v1.2.0-x64.*** (see GitHub releases for versionCode and notes).

## Related

* [GameNative-x64 README](https://github.com/Bliss-Bass/GameNative-x64/blob/bliss-x64/README.md)
* [Building Bass OS](../../development/building-bass.md)
* [Lockdown install / uninstall block](../../features/lockdown-install-block.md) - kiosk
  lockdown images may block sideload; preinstall is required on those SKUs
