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
* **Frame generation** - LSFG-VK (Lossless Scaling) on Intel and AMD Mesa, experimental on
  x86_64 (Bionic containers only; needs Lossless Scaling from Steam)
* **GPU present path** - DRI3 dma-buf zero-copy presents on x86_64
* **Linux job engine** for the [Linux Services](../LinuxServices/LinuxServices.md) system addon:
  boot-started, scheduled, and auto-restarted Linux services, terminal programs, and GUI apps

## Linux environment

The Linux environment is an Ubuntu rootfs (about 1.2 GB) that GameNativeX64 downloads once and
runs under PRoot. Set it up from GameNativeX64's Terminal screen, from **Linux Terminal** in the
app drawer, or from the Linux Services settings card when that addon is on the image.

| Area | Behavior |
|------|----------|
| Display backend | **Android X** (native X server with DRI3) is the default for freeform Linux apps. **Xtigervnc** is an opt-in compatibility fallback. Both are under **Linux display backend** in settings |
| Windows | One freeform task per Linux app, titled with the app's name. The X screen follows the window size, so GTK and Qt apps reflow when you resize |
| Sizing | **App size** scales Linux apps relative to Android's own UI (applies when a session next starts). **App UI size** scales GameNativeX64's own library and settings screens |
| Closing apps | **When a Linux app is closed**: close the session, or keep it running so reopening is instant |
| Browsers | Firefox installs from Mozilla's APT repository (Ubuntu's snap stubs do not work under PRoot). Sound goes through the same PulseAudio bridge as games, AAC decodes through the system ffmpeg, and Widevine/EME is on by default (Firefox downloads the CDM on first use) |
| App drawer | With the stub installer on the image, Linux apps and installed games are published to the Android app drawer automatically, including after apt installs from the terminal. Removing an entry stops it from coming back until you add it again |
| Reset | **Linux Apps → trash icon (Reset Linux environment)** deletes the rootfs and everything installed with apt |

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
| Linux apps | - | Session manager, per-app windows, drawer stubs, Android X display |
| Linux jobs | - | Job engine for Linux Services (`LinuxJobService`) |
| Build flavor | `arm64` | `modernX64` |

Current release series: **v1.2.0-x64.*** (see GitHub releases for versionCode and notes).
Linux Services needs **v1.2.0-x64.17** (versionCode 152) or later.

## Related

* [GameNative-x64 README](https://github.com/Bliss-Bass/GameNative-x64/blob/bliss-x64/README.md)
* [Linux Services](../LinuxServices/LinuxServices.md) - run Linux jobs at boot or on a schedule
* [BlissDeck](../BlissDeck/BlissDeck.md) - game-library Home on gaming images
* [Building Bass OS](../../development/building-bass.md)
* [Lockdown install / uninstall block](../../features/lockdown-install-block.md) - kiosk
  lockdown images may block sideload; preinstall is required on those SKUs
