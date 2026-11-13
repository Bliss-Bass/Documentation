# Building Bass: Lineout

This page is the **Bass: Lineout** build guide (`vendor/ax86-lite`, `tools/build.sh`). Lineout is built on three LineageOS generations. Most steps are the same for all of them; where they differ, each generation has its own instructions, newest first.

| | Android 17 | Android 16 | Android 14 |
|---|---|---|---|
| LineageOS | 24.0 | 23.2 | 21.0 |
| Vendor branch | `ax86-lite-los-24.0` | `ax86-lite-los-23.2` | `ax86-lite-los-21.0` |
| Source manifest | `los-tv-x86/lineage_bass_android`, `lineage-24.0` | `los-tv-x86/lineage_bass_android`, `lineage-23.2` | `Bliss-Bass/lineage_bass_android`, `lineage-21.0` |
| Pinned snapshot | `manifests/bass-lineage-24.0-static.xml` | `manifests/bass-lineage-23.2-static.xml` | `manifests/bass-lineage-21.0-static.xml` |
| Lunch target | `lineage_x86_64_tablet-cp2a-userdebug` | `lineage_x86_64_tablet-bp4a-userdebug` | `lineage_x86_64_tablet-ap2a-userdebug` (TV: `lineage_x86_64_tv-ap2a-userdebug`) |
| Patch sets | `patches/api-37` | `patches/api-36` | `patches/api-34` |
| Profiles | `bass-lineage-24.0-base`, `-validate`, `-core`, `-pro`, `-desktop` | `bass-lineage-23.2-core`, `-pro` | `bass-lineage-21.0` (no `--profile` option) |
| Default OTA channel | `lineout-24.0` | `lineout-23.2` | `lineout-21.0` |

Classic **Bass OS (Android 12L)** instructions are retained in full under [Legacy Bass OS (classic, Android 12L)](#legacy-bass-os-classic-android-12l). Do not mix the two flows.

The build tooling has grown through several generations, each a rewrite of the last: [vendor_ag](https://github.com/android-generic/vendor_ag) and [ag-project-manager](https://github.com/android-generic/ag-project-manager) (Android-Generic), then the Bass toolkit (classic Bass OS), then ax86-lite (Lineout), first on Android 14 and reworked for Android 16 and 17. That is why the Android 14 steps below look different.

Licensed private addons and white-label assets are supplied separately to licensed builders. Public docs do not cover bypassing licensing.

---

## Machine requirements

| Resource | Minimum guidance |
|----------|------------------|
| CPU | 16+ cores recommended |
| RAM | 32 GB+ |
| Swap | 16 GB+ |
| Disk | 500-700 GB free (source + `out/`) |
| OS | **Ubuntu 22.04 LTS** or **Ubuntu 24.04 LTS** (officially targeted) |

First sync and full image can take many hours depending on network and hardware.

---

## Host dependencies

Install these **before** `repo sync` / `./build/unfold_lineage.sh` / `./build.sh`. Prefer `apt` packages on Ubuntu; use the optional blocks only when you need that feature.

### 1. Base build packages (AOSP / Lineage + ISO tools)

Enable `i386` multiarch once (needed for some 32-bit linker/ncurses packages on x86_64 hosts):

```bash
sudo dpkg --add-architecture i386
sudo apt-get update
```

```bash
sudo apt-get install -y \
  git-core git-lfs gnupg flex bison gperf build-essential zip curl \
  zlib1g-dev gcc-multilib g++-multilib libc6-dev-i386 \
  libncurses5 libncurses5:i386 lib32ncurses-dev \
  x11proto-core-dev libx11-dev lib32z1-dev \
  ccache libgl1-mesa-dev libxml2-utils xsltproc unzip \
  squashfs-tools python3-mako libssl-dev ninja-build lunzip \
  syslinux syslinux-utils gettext genisoimage bc xorriso xmlstarlet \
  meson glslang-tools libelf-dev aapt zstd rdfind nasm \
  rustc bindgen \
  swig device-tree-compiler mtools libgmp-dev libmpc-dev \
  cpio rsync dosfstools kmod gdisk lz4 cmake libglib2.0-dev \
  wget python-is-python3 openssl openjdk-17-jdk
```

Notes:

- Package names drift slightly between 22.04 and 24.04 (`lib32ncurses5-dev` vs `lib32ncurses-dev`). If `apt` rejects a name, install the closest `ncurses` / `lib32z` package your release offers.
- `rustc` / `bindgen` are used by parts of the Android / Mesa stack. Prefer distro packages; a separate `rustup` toolchain is not required for a normal Lineout image.
- `openjdk-17-jdk` covers host Java needs (signing helpers, some app tooling). Newer JDKs may work; 17 is the safe default.

### 2. Lineout host packages (`ax86_setup.sh`)

`vendor/ax86-lite/build/ax86_setup.sh` hard-checks these (kernel `.deb` packaging and related host work):

```bash
sudo apt-get install -y \
  debhelper dpkg-dev bc bison flex libssl-dev rsync cpio unzip libdw-dev
```

(`build-essential` and `wget` from section 1 cover the rest of the vendor README list.)

### 3. Meson / Python helpers (Mesa and other Meson components)

```bash
sudo apt-get install -y python3-pip pkg-config python3-dev ninja-build meson python3-mako
sudo pip3 install --user jinja2 ply pyyaml pyelftools
```

If your distro already ships usable `python3-jinja2` / `python3-yaml` / `python3-ply` / `python3-pyelftools`, prefer `apt` over `pip3`.

### 4. Aaropa installer (Podman) - needed for `--aaropa-local`

Lineout ISOs use the **Aaropa** installer. Building `install.sfs` on the host uses **rootless Podman** (preferred) via `bootable/aaropa/build/aaropa-prebuilt.sh`.

```bash
sudo apt-get install -y \
  podman uidmap slirp4netns fuse-overlayfs passt \
  squashfs-tools p7zip-full curl git rsync
```

`passt` provides `pasta` (Podman 5.x default networking). Older hosts may use `slirp4netns` instead; install both if unsure.

Configure rootless Podman (one-time):

```bash
# Confirm unprivileged user namespaces are allowed (should be 1)
cat /proc/sys/kernel/unprivileged_userns_clone

# Ensure /etc/subuid and /etc/subgid have an entry for your user, e.g.:
#   youruser:100000:65536
grep "^$USER:" /etc/subuid /etc/subgid
```

If entries are missing, add them as root (adjust IDs if your site policy differs), then log out and back in:

```bash
sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 "$USER"
```

Verify Aaropa deps (prints an `apt install` line if anything is missing):

```bash
# From the AOSP workspace root after sync
bash bootable/aaropa/build/aaropa-prebuilt.sh --check-deps
```

Alternatives:

- `--aaropa-fetch` on `build.sh` downloads release artifacts instead of a local Podman build (still needs `curl`/`wget`, `p7zip-full`, etc.).
- Docker can work for some Aaropa steps, but local export currently expects **Podman** `unshare`. Prefer Podman for Lineout.

### 5. `repo` and Git LFS

```bash
mkdir -p ~/bin
curl -fsSL https://storage.googleapis.com/git-repo-downloads/repo -o ~/bin/repo
chmod a+x ~/bin/repo
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

git lfs install
```

`unfold_lineage.sh` runs `repo init ... --git-lfs`.

### 6. Optional: GameNative (`--gamenative`)

Default path downloads a CI-signed APK with the **GitHub CLI** (no local Vulkan compile):

```bash
sudo apt-get install -y gh
gh auth login
```

Then `vendor/ax86-lite/build/gamenative_build.sh` (or enable `--gamenative` so setup stages it).

**Local from-source GameNative** (dev only: Podman/Docker container builds + Gradle) additionally needs:

```bash
# Same Podman stack as Aaropa (section 4), plus:
sudo apt-get install -y \
  openjdk-17-jdk \
  meson ninja-build python3-mako \
  llvm-19-dev libclang-19-dev libclc-19-dev \
  spirv-tools glslang-tools
```

`ax86_setup.sh` only **warns** if those guest-graphics packages are missing; a plain ROM build without local GameNative Vulkan compile does not need them. Pin `GUEST_GFX_LLVM_VERSION` if your distro uses a different LLVM major than `19`.

Never ship images built with `--gamenative-dev-key` / debug-signed GameNative. Details: [GameNativeX64](../applications/GameNativeX64/GameNativeX64.md).

### 7. Optional host utilities

| Tool | Why | Install |
|------|-----|---------|
| `gh` | GameNative release fetch; some addon/repo helpers | `sudo apt-get install -y gh` |
| `adb` / `fastboot` | Device tests after build | `sudo apt-get install -y adb fastboot` or Android platform-tools |
| `aapt` | Host APK / Settings-tile checks | From section 1, or Android SDK build-tools |
| Pillow + ImageMagick | Regenerating initrd boot banners (`tools/generate_boot_banner.py`) | `sudo apt-get install -y imagemagick` and `pip3 install --user pillow` |
| `rclone` | Optional image upload helper | `sudo apt-get install -y rclone` |

### Dependency check summary

| When | What checks it |
|------|----------------|
| Every `source build/envsetup.sh` / Lineout setup | `build/ax86_setup.sh` -> `check_host_dependencies` |
| GameNative guest Vulkan (optional) | `check_guest_graphics_dependencies` (warn only) |
| `--aaropa-local` | `aaropa-prebuilt.sh --check-deps` then Podman build |
| `--gamenative` default | `gh` + network to GitHub releases |

---

## Fetch sources and unfold

### Android 17 and Android 16

Layout expected by the vendor scripts:

```text
<parent>/
  vendor_ax86-lite/     # this git clone (ax86-lite-los-24.0 or ax86-lite-los-23.2)
  aosp-workspace/       # created/filled by unfold
```

```bash
# Android 17
git clone -b ax86-lite-los-24.0 <vendor_ax86-lite-url>
cd vendor_ax86-lite
./build/unfold_lineage.sh --profile bass-lineage-24.0-core

# Android 16
git clone -b ax86-lite-los-23.2 <vendor_ax86-lite-url>
cd vendor_ax86-lite
./build/unfold_lineage.sh --profile bass-lineage-23.2-core
```

Unfold activates the profile, then `repo init` / `repo sync` the LineageOS release that profile names (manifest, branch and pinned snapshot), and symlinks this tree to `aosp-workspace/vendor/ax86-lite`. On Android 17 the release comes from the profile's `vendor_manifest_url`, `vendor_manifest_branch` and `vendor_static_manifest` keys; Android 16 uses the 23.2 values built into the script.

If the workspace is already synced and you only need to relink:

```bash
AX86_SKIP_SYNC=1 ./build/unfold_lineage.sh --profile bass-lineage-24.0-core   # or ...-23.2-core
```

The pinned snapshot is a fully resolved `repo manifest -r` of the Bass-Core tree. Maintainers refresh it from a synced workspace with `manifests/update-static.sh`, which leaves commercial addon repos out.

### Android 14

The Android 14 tree keeps the vendor tree **inside** the workspace (`aosp-workspace/vendor/ax86-lite`), and its unfold script has no profile option:

```bash
git clone -b ax86-lite-los-21.0 <vendor_ax86-lite-url> vendor_ax86-lite
cd vendor_ax86-lite
./build/unfold_lineage.sh      # asks for confirmation, then syncs ../aosp-workspace
```

The script activates `bass-lineage-21.0`, runs `repo init` from `Bliss-Bass/lineage_bass_android` (`lineage-21.0`) with the pinned snapshot, and syncs. In that iteration of ax86-lite the setup script also cloned the vendor tree into the workspace for the developer: `vendor/ax86-lite` is a plain git clone of `ax86-lite-los-21.0`, not a `repo` project. If your workspace does not have it, clone it there yourself:

```bash
cd ../aosp-workspace
git clone -b ax86-lite-los-21.0 <vendor_ax86-lite-url> vendor/ax86-lite
```

### Private addons

Private / licensed addon trees: place or clone them as instructed by your Bass contact (see also [Addon Development: Bass Lineout](addon-development.md)), then continue. On Android 16 and 17, `build.sh` also clones missing addon repos it has access to when a flag enables them.

---

## Environment setup and build

```bash
cd aosp-workspace
source build/envsetup.sh
lunch lineage_x86_64_tablet-cp2a-userdebug   # Android 16: ...-bp4a-userdebug, Android 14: ...-ap2a-userdebug
```

Sourcing `envsetup.sh` runs vendor integration (patches for the tree's API level, addon integrate, device package staging) and creates the `./build.sh` wrapper at the workspace root (a symlink to `vendor/ax86-lite/tools/build.sh`). `build.sh` runs `lunch` itself, so the `lunch` line is only needed for manual `m` work.

### Android 17

```bash
# Bass-Core validation set
./build.sh --profile=bass-lineage-24.0-validate

# Pro profile
./build.sh --profile=bass-lineage-24.0-pro --clean --update-foss-userapps

# A profile plus extra flags (flags on the command line add to / override the profile)
./build.sh --profile=bass-lineage-24.0-validate --extras --bass-style --style-type=materialyou
```

### Android 16

```bash
# Core profile
./build.sh --profile=bass-lineage-23.2-core --clean

# Pro profile example
./build.sh --profile=bass-lineage-23.2-pro --clean --update-foss-userapps

# Local Aaropa installer + common addons (example)
./build.sh --profile=bass-lineage-23.2-pro --clean \
  --aaropa-local --ethernetconfig --extras
```

### Android 14

`build.sh` has no `--profile` option; it uses the active `vendor_config.cfg` (`bass-lineage-21.0`) and the flags you pass. The default lunch target is the tablet; pass `--target` for TV:

```bash
./build.sh --clean --aaropa-local --ethernetconfig --extras
./build.sh --target=lineage_x86_64_tv-ap2a-userdebug --extras
```

Run `./build.sh -h` on your tree for the full flag list. Successful images land under the product out tree (`out/target/product/x86_64_tablet/`); the default make goal is `iso_img`.

---

## Profiles

A profile is `configs/vendor/<id>/vendor_config.cfg` in the vendor tree. It sets the lunch and make targets and the build flags the image uses. The active profile is `vendor_config.cfg` in the vendor root, written by unfold or by `build.sh --profile=<id>`.

### Android 17

| Profile | Role |
|---------|------|
| `bass-lineage-24.0-base` | Release settings only (LineageOS 24.0 manifest, `cp2a` lunch target, pinned snapshot). The other profiles inherit it. |
| `bass-lineage-24.0-validate` | Bass-Core validation set: BootSight, Ethernet Config, Ax86 Logger, Ax86 Power, Dual Shade, BlissView, the Lineage setup wizard, the Bass Aaropa installer and ADB insecure (for testing). No other commercial addons. |
| `bass-lineage-24.0-core` | Smaller addon set (validation + Ethernet Config). |
| `bass-lineage-24.0-pro` | Broader addon set (extras, SmartDock, FOSS user apps, desktop aconfig, custom signing keys). |
| `bass-lineage-24.0-desktop` | The Material Desktop product build (SmartDock, Bass Style, OTA channel, ...). Builds once SmartDock is ported to Android 17. |

Android 17 profiles can build on each other and carry any `build.sh` option:

| Key | Meaning |
|-----|---------|
| `vendor_inherits=<id> [<id>...]` | Load these profiles first. Later values win; flags and options add up. |
| `vendor_build_flags="NAME=value ... --option"` | Environment flags and plain `build.sh` options, mixed. |
| `vendor_build_args=--option` | One `build.sh` option per line. Quote values with special characters: `vendor_build_args='--ota-uri=https://host/{channel}/builds'`. |

Turn any command into a profile with `--save-profile` (it writes the profile and exits without building):

```bash
./build.sh --profile=bass-lineage-24.0-base --save-profile=bass-lineage-24.0-kiosk \
  --extras --kui --bootsight --bs-hybrid
./build.sh --profile=bass-lineage-24.0-kiosk
```

One-off options (`--clean`, `--installclean`, `--dustoff`, `--profile`, `--save-profile`) are not saved. Set `AX86_PROFILES_DIR` to keep profiles outside the vendor tree.

### Android 16

| Profile | Role |
|---------|------|
| `bass-lineage-23.2-core` | Smaller addon set (validation + Ethernet Config, etc.) |
| `bass-lineage-23.2-pro` | Broader addon set (extras, SmartDock, FOSS user-apps, etc.) |

Android 16 profiles set `vendor_build_flags` only; there is no inheritance or `--save-profile`.

### Android 14

One profile, `bass-lineage-21.0`, activated by unfold. Add features with build flags.

Details: `vendor/ax86-lite/README.md` and `addons/README.md`.

---

## Lineout / ax86-lite build flags

Lineout builds use `vendor/ax86-lite/tools/build.sh`. The tables below group the flags by feature; **Available** says which generations have a flag (all = Android 14, 16 and 17). Always prefer `./build.sh -h` on your tree for the authoritative list. Addon flags are listed at the end of that help output.

### Build control

| Flag | Effect | Available |
|------|--------|-----------|
| `--profile=ID` | Use profile `configs/vendor/<ID>` | A16, A17 |
| `--save-profile=ID` | Save this command's options as profile `ID` and exit | A17 |
| `--target=TARGET` | Lunch target | all |
| `--module=MODULE` | Make goal (default `iso_img`) | all |
| `--clean` / `--installclean` / `--dirty` | `rm -rf out/` / `installclean` / incremental (default) | all |
| `--dustoff` | Remove kernel, `*.img`, `*.sfs`, `*.iso` and OTA zips from `out/`, then build | all |
| `--tuck` | Sign with custom keys (`TARGET_USE_CUSTOM_KEYS=true`) | all |
| `--noksu` | Disable KernelSU in the x86 kernel defconfigs | all |
| `--rebuild-aconfig-pb` | Do not seed `aconfig_flags.pb` from the vendor cache | A16, A17 |
| `--package-patches` / `--api-level=N` | Export local repo commits into `patches/api-N/` | all |

### Fleet and BootSight

| Flag | Effect | Available |
|------|--------|-----------|
| `--bootsight` | Include BootSight (Bass fleet backend / Device Status) | all |
| `--fleet-mgmt=mdm` | Image expects a third-party MDM (no BootSight) | all |
| `--fleet-mgmt=none` | No fleet component (default when neither flag is set) | all |
| `--bsbanner` | BootSight overlay banner (implies `--bootsight`) | all |
| `--bspopup` | BootSight overlay popup (implies `--bootsight`) | all |
| `--bs-offline` | BootSight offline-only licensing, no server sync or telemetry (implies `--bootsight`) | all |
| `--bs-hybrid` | BootSight hybrid licensing: offline file/code plus online sync (implies `--bootsight`) | all |

Do not combine `--bootsight` with `--fleet-mgmt=mdm`. Product overview: [Fleet Management](../features/fleet-management.md), [BootSight](../applications/BootSight/BootSight.md).

### Logger, Button Manager, and Power

| Flag | Effect | Available |
|------|--------|-----------|
| `--logger` | Include Ax86 Logger (capture off until enabled) | all |
| `--logging-enabled` | Include Ax86 Logger and start capture by default | all |
| `--btnmgr` | Include Ax86 Button Manager | all |
| `--ax86-power` | Include Ax86 Power (sleep/wake policy UI + AIDL) | all |

`--logging-enabled` implies `--logger`. `--extras` also includes Ax86 Power. Details: [Ax86 Logger](../applications/Ax86Logger/Ax86Logger.md), [Button Manager](../applications/Ax86ButtonManager/Ax86ButtonManager.md), [Ax86 Power](../applications/Ax86Power/Ax86Power.md).

### Branding and identity

| Flag | Effect | Available |
|------|--------|-----------|
| `--bootani` | Use `branding/bootanimation/bootanimation.zip` | all |
| `--wallpaper` | Use `branding/wallpaper/default_wallpaper.png` | all |
| `--nobootani` | Stock Android boot animation | all |
| `--nowallpaper` | Stock Android wallpaper | all |
| `--nobranding` | Stock boot animation and wallpaper | all |
| `--bass-id=TITLE` | Product ID string (`BASS_ID_TITLE`), e.g. `RETAIL.A17.M.DESKTOP.KSU` | all |
| `--special-variant=VARIANT` | Suffix for the version string (`LINEAGE_SPECIAL_VARIANT`), e.g. `-Material-Desktop` | all |
| `--spoof-fingerprint` | Spoof `BUILD_FINGERPRINT` (Pixel Tablet `tangorpro`) | A16, A17 |
| `--spoof-fingerprint-fugu` | Spoof it as the Nexus Player `fugu` (implies `--spoof-fingerprint`) | A16, A17 |

Default without the branding flags is the Lineage boot animation and wallpaper.

### Boot options and lockdown

| Flag | Effect | Available |
|------|--------|-----------|
| `--bass-boot-options` | Bass GRUB boot options. A16/A17: inject the Bass submenu via `custom.cfg` on first boot. A14: bake the full catalog into `install.sfs` (Calamares `10_bass`) | all |
| `--cxbbo` | Customer Bass boot catalog (`entries.customer.list`; implies boot options) | all |
| `--ldinstall` | Block install/uninstall in lockdown mode. A16/A17: UI, ADB `pm` and app APIs. A14: the install UI only | all |
| `--ldinstallstrict` | Also block ADB `pm` and PackageManager installs in lockdown | A14 |
| `--grublock` / `--grub-password-file=PATH` | GRUB password (pbkdf2 hash; default from `private/`) | A14 |
| `--grub-hidden` / `--grub-timeout=N` | Hidden GRUB menu / timeout, set at build time | A14 |

Details: [Bass boot options](../setup_and_configuration/bass-boot-options.md), [Lockdown install block](../features/lockdown-install-block.md).

### Aaropa installer

| Flag | Effect | Available |
|------|--------|-----------|
| `--aaropa-local` | Build Aaropa `install.sfs` locally with Podman before lunch | all |
| `--aaropa-fetch` | With `--aaropa-local`, download the GitHub release instead of building | all |
| `--aaropa-rebuild` | Ignore the stamp and refetch/rebuild installer artifacts | all |
| `--aaropa-source=bliss\|bass` | Installer flavor (default `bass`) | all |
| `--aaropa-branding=NAME` | Branding overlay (default: same as `--aaropa-source`) | all |
| `--newinstaller` | Use the legacy newinstaller GRUB and ncurses installer instead | all |

Requires section [4. Aaropa installer](#4-aaropa-installer-podman---needed-for---aaropa-local) when using `--aaropa-local`.

### Desktop and UI

| Flag | Effect | Available |
|------|--------|-----------|
| `--dui` / `--tui` / `--kui` | DesktopUI / TabletUI / KioskUI mode by default | all |
| `--blurui` | Blur on by default | all |
| `--notaskbar` | Disable the Android taskbar (Launcher3 patches) | all |
| `--smartdock` | SmartDock desktop dock + freeform/desktop mode | all |
| `--dual-shade` | SystemUI Dual Shade (floating Notifications and Quick Settings panels); on with `--smartdock` and `--bass-style` too | A16, A17 |
| `--desktop-aconfig` | Desktop and connected-display aconfig flag values (also on with `--smartdock`, `--dui`, `--bass-boot-options`) | A16, A17 |
| `--bass-style` | retro-style theme packs and the tablet system bar | A16, A17 |
| `--style-type=ID` | Default style: `materialyou` (default) or a pack id (`m3`, `kitkat`, `jellybean`, ...) | A16, A17 |
| `--style-layout=system_bar\|stock` | Default bottom bar (`system_bar` needs the taskbar: not with `--notaskbar` unless `--smartdock`) | A16, A17 |
| `--style-bar-bg=VALUE` | System bar home background: `stock`, `solid`, `gradient`, `translucent`, `transparent` | A16, A17 |
| `--style-black=on\|off` | Pure black dark mode by default | A16, A17 |
| `--gaming` | GamingUI mode by default (implies `--blissdeck`) | A16, A17 |
| `--blissdeck` | BlissDeck game-library Home preinstall (`gh` + network to GitHub releases) | A16, A17 |

On Android 17, feature flags stay switchable at runtime: see [Feature Flags (aconfig)](aconfig-flags.md).

### Apps and addons

| Flag | Effect | Available |
|------|--------|-----------|
| `--extras` | Bliss apps and mappers: Touch Mapper, Display Mapper, Config Overrides, Tweaks, Ax86Docs, Ax86 Power; A16/A17 also Aaropa options (does **not** include BootSight) | all |
| `--ethernetconfig` | Ethernet Config | all |
| `--internet-security` | Preinstall the Internet Security user app | all |
| `--monterey-standby` | Preinstall the Monterey Standby user app | all |
| `--restrictedlauncherpro` | Restricted Launcher Pro (private access) | all |
| `--rlptype=VARIANT` | RLP APK variant: `default` \| `gs` \| `gs_nh` \| `sl` (implies `--restrictedlauncherpro`) | all |
| `--foss-userapps` / `--update-foss-userapps` | FOSS user-app set / refresh from F-Droid metadata | all |
| `--fossapps`, `--aurora`, `--droidify`, `--min-foss`, `--min-foss-mg`, `--calyx-mg` | FOSS app store and microG sets | all |
| `--tbfv` | FrameworksValidation (BlissView) anti-tamper app | all |
| `--bassview-tamper` | Watermark the screen if BassView is missing | A16, A17 |
| `--bassaudio` | Bass Audio (Quick Settings mixer, HDMI/speaker routing, DSP) | A16, A17 |
| `--btferry` | BT Ferry (phone messages/contacts/calls + A2DP speaker bridge) | A16, A17 |
| `--gamenative` | GameNative x86_64 preinstall (see optional deps above) | A16, A17 |
| `--linux-services` | Linux Services: boot, scheduled, and auto-restarted Linux jobs (needs `--gamenative`) | A16, A17 |
| `--linuxwindow` | LinuxWindow (Linux apps in Android; needs the addon content) | A16, A17 |
| `--digitalis` | Digitalis ARM64-on-x86_64 native bridge (Berberis) | A16, A17 |

### OTA updates

| Flag | Effect | Available |
|------|--------|-----------|
| `--ota` | Also build the OTA zip, named like the ISO | all |
| `--ota-uri=URL` | Updater URI (`lineage.updater.uri`; `{channel}` and `{device}` are filled in); with `--ota` also writes the Updater JSON | all |
| `--ota-url=URL` | Alias for `--ota-uri` | A14 |
| `--ota-channel=NAME` | OTA channel (`ro.bass.ota.channel`); default in the table at the top | all |
| `--otadebug` | `persist.bass.ota.debug=1` (debugging only) | all |

### Hardware and platform

| Flag | Effect | Available |
|------|--------|-----------|
| `--gpu` / `--hals` | Build the graphics stack / hardware HALs | all |
| `--surface` / `--zenith` | Surface / Zenith board variants (`BOARD_IS_SURFACE_BUILD` / `BOARD_IS_ZENITH_BUILD`) | all |
| `--tv` / `--tv-lowram` / `--go` | Android TV / low-RAM TV / Go builds | all |
| `--widevine` | Widevine DRM | all |
| `--ax86parts` | Static android_x86_64 fstab/partitions | all |
| `--debian` | Fetch/build the Debian chroot | all |
| `--libndk-nb`, `--cros-houdini`, `--ndk-trans`, `--intel-houdini` | ARM native bridge choices | all |
| `--adbi` (alias `--sdbi`) | ADB insecure mode by default (debugging only) | all |

Examples:

```bash
# Android 17
./build.sh --profile=bass-lineage-24.0-validate \
  --aaropa-local --bootsight --bsbanner --btnmgr --ax86-power \
  --logging-enabled --ethernetconfig

# Android 16
./build.sh --target=lineage_x86_64_tablet-bp4a-userdebug \
  --aaropa-local --bootsight --bsbanner --btnmgr --ax86-power \
  --logging-enabled --ethernetconfig

# Android 14
./build.sh --target=lineage_x86_64_tablet-ap2a-userdebug \
  --aaropa-local --bootsight --bsbanner --btnmgr --ax86-power \
  --logging-enabled --ethernetconfig
```

---

## Related reading

| Topic | Doc |
|-------|-----|
| Addon layout and flags | [Addon Development: Bass Lineout](addon-development.md) |
| Runtime-switchable feature flags (aconfig) | [Feature Flags (aconfig)](aconfig-flags.md) |
| Fleet / MDM product overview | [Fleet Management](../features/fleet-management.md) |
| Product lines | [Bass Product Family Guide](../product-guide/bass-product-family.md) |
| High-level map | [High Level Overview](bass-high-level-overview.md) |
| Classic Bass OS build | [Legacy Bass OS (classic)](#legacy-bass-os-classic-android-12l) below |

---

## Legacy Bass OS (classic, Android 12L)

The rest of this page is the older **Bass OS Android 12L** flow (`unfold_bliss.sh` / `build_bass.sh`). It is **not** the Lineout path. For Lineout, use the sections above (`vendor/ax86-lite` / `./build.sh`).

[![License](https://img.shields.io/badge/license-GPL-blue)](https://opensource.org/licenses/gpl-3-0/)

Please refer to https://bliss-bass.blisscolabs.dev for release notes, hardware requirements and demos of the various options.

### Licensing

Much of Bass OS is published under the General Public License 3.0. All generic patches are regularly submitted to [Bliss OS](https://github.com/BlissRoms-x86) where they can be obtained under the Apache License.

Bass OS does have a number of options, features, applications, etc. that can be accessed through purchasing licensing for the private addons, features and tools. [See our licensing page](https://bliss-bass.blisscolabs.dev/licensing.html) for full details.

### Warning!

Bass OS is an open-source initiative maintained by Bliss Co-Labs. It is provided "as is" without any warranties or guarantees.

### Building from sources

Before building, ensure your system has at least 16 CPU cores, 32GB of RAM, a swap file is at least 16GB, and 500GB-700GB of free disk space available.

#### Install system packages

(Ubuntu 22.04 LTS is only supported for classic Bass. Building on other distributions can be done using docker.)

- [Install AOSP required packages](https://source.android.com/setup/build/initializing).

```bash
sudo apt-get install git-core gnupg flex bison gperf build-essential zip curl zlib1g-dev gcc-multilib g++-multilib libc6-dev-i386 lib32ncurses5-dev x11proto-core-dev libx11-dev lib32z-dev ccache libgl1-mesa-dev libxml2-utils xsltproc unzip squashfs-tools python3-mako libssl-dev ninja-build lunzip syslinux syslinux-utils gettext genisoimage gettext bc xorriso xmlstarlet meson glslang-tools git-lfs libncurses5 libncurses5:i386 libelf-dev aapt zstd rdfind nasm rustc bindgen
```

- Install additional packages

```bash
sudo apt-get install -y swig device-tree-compiler mtools libgmp-dev libmpc-dev cpio rsync dosfstools kmod gdisk lz4 cmake libglib2.0-dev
```

- Install additional packages (for building mesa3d, libcamera, and other meson-based components)

```bash
sudo apt-get install -y python3-pip pkg-config python3-dev ninja-build
sudo pip3 install mako jinja2 ply pyyaml pyelftools
```

- Install the `repo` tool

```bash
sudo apt-get install -y python-is-python3 wget
wget -P ~/bin http://commondatastorage.googleapis.com/git-repo-downloads/repo
chmod a+x ~/bin/repo
```

You can also reuse the broader Lineout host package lists at the top of this page where package names still match your Ubuntu release.

#### Fetching the sources and building the project

```bash
git clone --recurse-submodules https://github.com/Bliss-Bass/bass-os.git bass-os-12.1
cd bass-os-12.1
```

#### Setting up Bass OS Source

##### !!NOTICE FOR LICENSED ADDONS/FEATURES!!

If you hold an active license for any of the private addons and features for Bass OS, you will need to add the files that you were sent or given access to, into the `private/addons` or `private/manifests` folder. If your project requires any vendor patches, those are placed in the `patches-vendor/` folder. Once all items are placed properly, you can continue onto the unfolding steps. Please also check your organization's Bass-OS project folder to make sure it didn't come with those additions already added.

#### Unfolding the source

Bass source uses an unfolding sequence to grab the latest stable point in development for the source, then applies any required changes on top, along with any customizations, licensed addons, modules, etc.

To start the unfolding process, we use the `unfold_bliss.sh` script:

```bash
bash unfold_bliss.sh
```

This will sync the source, and patch it with the latest available updates for Bass OS. Once complete and all patches, and addons are applied successfully, you can move onto the next step.

### Building Bass OS

#### Build Options

##### Target Specific build scripts

(**!!NOTICE FOR LICENSED CUSTOMERS!!**) If you have been supplied with the source, then chances are your source comes with a separate build script specific to your device's needs. Please check the project folder for a script with your product name or invoice number in it. Examples: `build_ABC01.0.1.sh` or `build_Intel-AC013.sh`. These will include the specific set of arguments passed to the build_bass script, so all you will need to do is run your targeted script to build.

```bash
bash build_ABC01.0.1.sh
```

##### General Build Script Usage

We offer a number of options to configure your builds with. You can use the `-h` argument to see the latest integrations available.
We also symlink the build-x86 command with `build_bass.sh` and `build-x86.sh`, so the commands both act the same when building Bass OS.

Example:

```bash
bash build_bass.sh -h
Usage: build-x86.sh [options]
Options:
-h, --help             Display this help dialog
-c, --clean            Clean the project
-d, --dirty            Run in dirty mode
-t, --title (title)    Set the release title
-b, --blissbuildvariant (variant)   Set the Bliss build variant
-i, --isgo             Enable isgo version
-v, --specialvariant (variant)      Set the special variant
--grubcmdline "option1=1 option2=1" Set the grub cmdline options
--production           Disable Test Build watermark and sign builds (requires release/product signature keys)

Launcher Options:
--clearhotseat         Enable clear hotseat favorites for Launcher3 Quickstep
--disablesearch        Disable device search
-s, --smartdock        Enable smartdock
--smartdockb           Enable smartdock with Bliss customizations
-k, --kiosk            Enable kiosk launcher **requires private git access**
--restrictedlauncher   Enable restricted launcher
--restrictedlauncherpro   Enable restricted launcher pro **requires private git access**
--garliclauncher       Enable garlic launcher
--gamemodelauncher     Enable game mode launcher
--crosslauncher        Enable cross launcher
--tvlauncher           Enable tv launcher
--titaniuslauncher     Enable titanius launcher
--desktoponsecondary   Enable desktop on secondary displays

Navigation Options:
-t, --tabletnav        Enable tablet navigation
--taskbarnav           Enable taskbar navigation
--gesturenav    Enable gesture navigation
--externalnav          Enable navigation on external displays
--rightmouseasback     Enable right mouse button as back

Package Options:
--noksu                Disable KernelSU
-f, --fossapps         Enable fossapps
--minfossapps          Enable minimal fossapps
-e, --supervanilla     Enable supervanilla
-m, --minimal          Enable minimal packages
-r, --removeusertools  Enable removeusertools
--viabrowser           Enable viabrowser
-w, --wiz              Enable Bliss setupwizard
--ethernetmanager      Enable EthernetManager
--powermanager         Enable power manager
--buildextra           Build extra packages
--updatefossapps       Update fossapps
--usepos               Enable TabShop pos terminal app

Input Options:
--showkeyboard         Enable show keyboard
--perdisplayfocus      Enable per display focus
--gboard               Enable Google GBoard IME
--gboardlite           Enable Google GBoard Lite IME
--perdisplayfocusime      Enable per display focus with experiment IME
--perdisplayfocuszqyime   Enable per display focus with ZQY IME

Firmware & Driver Options:
--sof                  Include SOF firmware
--silead               Include Silead firmware

Other Options:
-a, --atom             Include Intel Atom specific configurations
-l, --lockdown         Enable secure lockdown build
--adblockdown          Enable lockdown ADB defaults
-m, --manifest         Generate manifest
--alwaysonsettings     Enable always on settings
--nolarge              Disable large screen settings
```

### Features

- Supports various navigation and UI switches
- Supports various use-case launcher options (requires recent changes to vendor/agp-apps)
- Automatically updates Grub menus and other build configs for launcher and mode options (requires recent changes to vendor/agp-apps)

Please note that some of the build options may require licensed access to the feature/addon/application in order to use it. In some cases, the build will continue with just a warning when these options are used. In other cases, the build will exit. To remedy this, use a different option or remove the offending option from the build command.

### Examples

Here are a few examples to help in understanding:

**Bass Desktop**: Desktop mode demo of Bass featuring SmartDock

```bash
bash build_bass.sh --clean --title "Bass" --blissbuildvariant vanilla --specialvariant "-Desktop" --ethernetmanager --tabletnav --smartdock --wiz --clearhotseat --perdisplayfocus --externalnav --externalstatusbar --nolarge --sof --silead --alwaysonsettings --minfossapps
```

**Bass Restricted**: Restricted mode demo of Bass featuring Bliss Restricted Launcher

```bash
bash build_bass.sh --clean --title "Bass" --blissbuildvariant foss --specialvariant "-Restricted" --restrictedlauncher --ethernetmanager --fossapps --gesturenav --clearhotseat --externalnav --noksu --showkeyboard --nolarge --alwaysonsettings --sof --silead
```

**Bass POS**: Point-Of-Sale version of Bass featuring TabShop

```bash
bash build_bass.sh --clean --title "Bass" --blissbuildvariant foss --specialvariant "-POS" --restrictedlauncher --usepos --ethernetmanager --fossapps --gesturenav --clearhotseat --externalnav --noksu --showkeyboard --nolarge --alwaysonsettings --supervanilla --minimal
```

**Bass Tablet Go**: Android Go based Tablet version of Bass OS

```bash
bash build_bass.sh --clean --title "Bass" --blissbuildvariant foss --specialvariant "-TabletGo" --isgo --ethernetmanager --fossapps --tabletnav --wiz --clearhotseat --perdisplayfocus --externalnav --externalstatusbar --noksu --showkeyboard --perdisplayfocus --nolarge
```

### Vendor Customization Layer

If you have licensed access to the vendor customization layer for Bass OS, it comes with an easy to use menu driven interface for rebranding the OS.
Below are a few combinations of the various command options put together in the form of Collections.

#### Features available

- Menu driven interface for updating assets and branding:
  ![Bass - Customization menu](assets/bass-customization.png)
- Generates default wallpaper overlays
- Generates branded bootanimation based on a single loop of frames
- Generates branded grub background

### Notes

- Depending on your hardware and internet connection, downloading and building may take 8h or more.
- After the successful build, find the images at `iso/` under the folder name based on your build name generated by the build system and can also be found in `aosptree/out/target/product/x86_64/`.
