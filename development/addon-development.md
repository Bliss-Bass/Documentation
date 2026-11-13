# Addon Development: Bass Lineout

**This page is for Bass: Lineout** (`vendor/ax86-lite`, `tools/build.sh`).

If you are on classic Bass OS with `private/addons/` and `unfold_bliss.sh`, use the separate guide instead:

→ **[Addon Development: Legacy Bass OS](addon-development-legacy-bass.md)**

Do not mix the two. Lineout does **not** scan `private/addons/` the way older Bass unfold did.

---

## Lineout overview

On Lineout, "addon" work falls into two buckets:

| Bucket | Where it lives | How you enable it |
|--------|----------------|-------------------|
| **Build addons** | Android 16 / 17: `vendor/ax86-lite/addons/<id>/`. Android 14: `vendor/ax86-lite/vendor_packages/<Pkg>/` | `build.sh` flags (`--extras`, `--btnmgr`, ...) or a [profile](building-bass.md#profiles) |
| **Runtime overrides** | `/data/misc/`, GRUB flags, `addon_init` | Push files + cmdline / `setprop` |

How build addons are laid out differs by generation:

| | Android 17 (Lineage 24.0) | Android 16 (Lineage 23.2) | Android 14 (Lineage 21.0) |
|---|---|---|---|
| Layout | [`addons/<id>/`](#addons-on-android-16-and-17) | [`addons/<id>/`](#addons-on-android-16-and-17) | [`vendor_packages/<Pkg>/`](#android-14-vendor_packages) |
| Addon sources | One repo per addon | One repo per addon | In the vendor tree |
| Patch sets | `patches/api-37/` | `patches/api-36/` | Core queue only (`patches/api-34/`) |
| Per-release manifest fragments | `manifest-api-37.xml` | `manifest.xml` only | n/a |

---

## Addons on Android 16 and 17

Each addon is a self-contained unit and its own git repo. It carries everything it needs: sources, Soong wrappers, patches, product makefiles, repo manifest fragments and its build flags. Dropping `addons/<id>/` with an `addon.cfg` into the vendor tree is enough: there is no central list to edit.

```text
addons/<id>/
├── addon.cfg                        # metadata + enable flags (shell)
├── build/flags.sh                   # build.sh flags this addon adds (optional)
├── packages/<Pkg>/...               # app / script / prebuilt sources
├── device_wrappers/<ns>/ax86-addons/<Pkg>/
│   ├── Android.bp                   # Soong module (staged into the device tree)
│   └── .stagecfg                    # how to stage the sources (optional)
├── patches/api-<level>/<aosp-path>/*.patch   # AOSP patches (optional)
├── manifest.xml                     # repo local_manifest fragment (repo-backed addons)
├── manifest-api-<level>.xml         # per-release fragment (Android 17)
├── sync_<id>.sh                     # fetch script (optional)
├── <id>_product.mk                  # inherit-product makefile(s) (optional)
├── README.md                        # developers
└── USER_GUIDE.md                    # end users
```

### `addon.cfg`

| Field | Description |
|-------|-------------|
| `ADDON_ID` | Directory name / makefile variable suffix |
| `ADDON_NAME` | Human-readable label |
| `ADDON_LICENSE` | SPDX id or `GPLv2 OR Commercial` |
| `ADDON_ALWAYS` | `true` = always enabled when present |
| `ADDON_REQUIRES_ANY` | Space-separated build flags; **any** one set enables the addon |
| `ADDON_COMPAT` / `ADDON_INCOMPAT` | Release ids the addon is limited to / excluded from (`lineout`, `submix`) |
| `ADDON_PRESENT_TEST` | File (relative to the addon) that must exist for the addon to count as present |
| `ADDON_PRESENT_AOSP` | File (relative to the AOSP root) that must exist, for addons that live elsewhere in the tree |
| `ADDON_SYNC_SCRIPT` | Script that fetches missing content |
| `ADDON_MANIFEST` | repo `local_manifest` fragment to merge |
| `ADDON_PATCH_DIRS` | Patch roots under the addon; `aosp:<path>` is relative to the AOSP root (patches shipped by a synced repo) |
| `ADDON_PRODUCT_MKS` | Makefiles to `inherit-product` when enabled |
| `ADDON_STUB` | `true` = an enabled addon with missing content is skipped with a warning instead of stopping the build (unfinished port) |

### Build flags

`build/flags.sh` registers the addon's flags with `build.sh`, which picks them up for parsing and `--help`:

```bash
ax86_register_flag --my-feature USE_MY_FEATURE true \
    "Enable My Feature (one line of help)"
ax86_register_flag --my-feature-mode MY_FEATURE_MODE @VALUE \
    "My Feature mode: a | b (default: a)"
```

The environment variable is what `ADDON_REQUIRES_ANY` and the addon's makefiles test. Several addons can share one flag: `--extras` turns on the whole Bliss apps family, each app still its own addon.

### What happens during a build

1. `tools/build.sh` loads every `addons/*/build/flags.sh`, then the profile, then your command-line flags.
2. `apply-patches.sh` applies the core `patches/api-<level>/` queue, then runs `integrate-addons.sh`.
3. `integrate-addons.sh` reads every `addon.cfg`, enables the addons whose flags are set, and for each one:
   * fetches it if it is missing (see [Getting addons into a tree](#getting-addons-into-a-tree));
   * merges its manifest fragment and applies its patch set for the build's API level;
   * adds its `ADDON_PRODUCT_MKS` to `addons/enabled.mk`;
   * stages its `device_wrappers/` into the device tree.
4. `ax86_lite.mk` includes `addons/enabled.mk`, so the enabled addons join the product.

### Privileged apps: device-tree staging

Android 16 tightened `Android.bp` visibility: privileged, platform-signed app modules under `vendor/ax86-lite` are not visible to the product. So addons ship their Soong wrapper under `device_wrappers/<ns>/ax86-addons/<Pkg>/`, and the build copies the wrapper **and** the sources into `<device tree>/ax86-addons/<Pkg>/`. That copy is a build artifact (git-ignored in the device tree); edit the sources under `addons/<id>/`.

The vendor's core patch queue adds one line to the device tree's `device.mk`, `-include $(LOCAL_PATH)/ax86-addons/product.mk`, and git-ignores `ax86-addons/`. Staging writes that file; without it the line does nothing.

`.stagecfg` next to the wrapper describes the source layout:

| Field | Meaning | Default |
|-------|---------|---------|
| `STAGE_PKG` | Package dir under `addons/<id>/packages` | wrapper dir name |
| `STAGE_FROM` | Subdir of the package used as source root | `.` |
| `STAGE_ITEMS` | Items to copy | whole tree |
| `STAGE_EXCLUDE` | Paths to delete after copying (generated files) | none |

Vendor binaries and rc/sh-only addons (for example `chvt`, Config Overrides) build in the `vendor/ax86-lite` namespace and need no staging.

### Patches

* An addon patch set lives under `patches/api-<level>/<aosp-path>/` (`api-36` for Android 16, `api-37` for Android 17). A build only applies the set for its API level; an addon without a set for that level applies no patches there.
* Patches are `git format-patch` output of real commits in the target project, never hand-written diffs. Keep the source commits on a ref in the project (for example `refs/addon-patches/<id>/api-37`), change them there, and regenerate the files.
* Name them `000N-description.patch`; the build applies them in order with `git am -3` and records them as commits.
* A patch counts as applied when the same change (by content) is already a commit in the project. A patch whose change is only present as uncommitted edits, or whose subject matches a commit with different content, fails the build: fix the project or regenerate the patch.
* Moving to a new Android release: apply the old set with `git am -3` on a branch from the new tree, resolve conflicts, and export the new set from those commits. `tools/port_patch_queue.sh` does this for the core queue.

### Release compatibility

A profile's `vendor_release` (`lineout`, or `submix` for Waydroid-based builds) is checked against `ADDON_COMPAT` / `ADDON_INCOMPAT`. For example, `aaropa-options` builds on Lineout and is excluded on Submix.

### Boot check-ins

An addon's boot script should record that it ran, in `/data/misc/bass_checkins/<id>`: one line, overwritten each boot, written on **every** exit path. Use `key=value` fields with `boot=` (the current `/proc/sys/kernel/random/boot_id`) and `verdict=` last. `boot=` proves the check-in is current; the wall clock can be wrong early in boot. Copy the helper from the BootSight addon rather than sourcing another addon's file, and `chmod 0644` it. Assert the check-in in the addon's test.

### Creating a new addon

1. `mkdir -p addons/<id>` and write `addon.cfg`.
2. Add `packages/<Pkg>/`, and for privileged apps `device_wrappers/<ns>/ax86-addons/<Pkg>/Android.bp` (+ `.stagecfg`).
3. Add `build/flags.sh`.
4. Add the product makefile(s) and list them in `ADDON_PRODUCT_MKS`.
5. Run `tools/sync-vendor-package-symlinks.sh` (keeps `vendor_packages/<Pkg>` paths pointing at the addon).

Before calling it done, work through the vendor tree's `docs/ADDON_FEATURE_CHECKLIST.md`. In short:

* **Settings entry:** an `EXTRA_SETTINGS` activity with category, summary, a 24 dp white vector icon and `com.android.settings.icon_tintable=true`; no launcher icon for Settings-only tools.
* **UI:** Material 3, an explicit toolbar with back, content that does not draw under the status bar.
* **Properties:** document new `persist.*` / apply triggers in `OVERRIDES.md`.
* **Tests:** `tests/test_<id>.sh` that skips cleanly when the addon is not in the build, and a host check for the Settings tile metadata.
* **Docs:** `USER_GUIDE.md` for end users, `README.md` for developers.

### Android 17 differences

* **Per-release manifest fragments:** an addon can ship `manifest-api-37.xml` next to `manifest.xml` when it syncs different repos or branches on Android 17 (Digitalis does).
* **Bass-Core device tree:** the public Android 17 device tree carries no `vendor/ax86-lite` includes and no staging hook; the core patch queue adds both at build time. Addons reach the build only through that hook, so an addon must not edit committed device-tree files.
* **Feature flags:** aconfig flags stay switchable at runtime. An addon that changes a flag's built-in value should keep it `READ_WRITE` unless it must not change; see [Feature Flags (aconfig)](aconfig-flags.md).

---

## Packaging and distribution

These apply to Android 16 and 17. Android 14 addons live in the vendor tree itself.

### One repo per addon

Every addon is its own git repo in the [BlissBass-Addons](https://github.com/BlissBass-Addons) organization, named after the addon id (`BlissBass-Addons/<id>`), on the `lineout` branch. One branch serves Android 16 and 17: release-specific content goes in `patches/api-<level>/` and `manifest-api-<level>.xml`, not in separate branches.

Repos are public or private. Access to a private repo is what licenses that addon. The vendor repo does not track addon sources (`addons/*` is git-ignored), so an addon is versioned, released and licensed on its own.

### Getting addons into a tree

```bash
cd vendor/ax86-lite
tools/clone-addons.sh                          # the default set (repos you cannot reach are skipped)
tools/clone-addons.sh bliss-tweaks btnmgr      # specific addons
ADDON_GIT_ORG=MyOrg ADDON_GIT_BRANCH=lineout tools/clone-addons.sh   # another org or branch
tools/sync-vendor-package-symlinks.sh
```

You rarely need to do this by hand: when a build flag enables an addon that is missing, the build fetches it. If the repo cannot be reached, the build stops with a licensing contact message (Navotpala Tech, info@navotpala.tech) instead of producing an image without the feature.

### Repo-backed and synced addons

Some addons are thin: their content lives in other repos that go elsewhere in the tree.

| Kind | How it works | Examples |
|------|--------------|----------|
| Manifest fragment (`ADDON_MANIFEST`) | The fragment is merged into `.repo/local_manifests/ax86-lite-addons.xml` and the project is `repo sync`ed. On Android 17, `manifest-api-37.xml` replaces `manifest.xml` when present. | SmartDock, Digitalis, Ethernet Config, FOSS user apps |
| Sync script (`ADDON_SYNC_SCRIPT`) | The script clones the repo when it is missing; `ADDON_PRESENT_AOSP` names a file that proves it is there, and `aosp:` patch dirs point at patches inside it. | Bass Style (`vendor/retro-style`), Dual Shade (`vendor/dual-shade`) |

A synced repo is only cloned when missing. Update it later with `git -C vendor/<repo> pull`.

### Prebuilt apps

* Commit the **unsigned** APK under `packages/<Pkg>/prebuilts/` and import it with `android_app_import` (`certificate: "platform"` for privileged apps). The image build signs it with that build's keys.
* To test a new APK on a running device without rebuilding the image, sign it with the same platform key the image was built with, replace it at the package's `codePath`, and reboot. Never push an unsigned APK, or one signed with another key (such as AOSP test keys), over a privileged app: the device will not boot.
* Apps released elsewhere are fetched at build time instead of committed: GameNative and BlissDeck from their GitHub releases (needs `gh`), FOSS user apps from F-Droid (`--update-foss-userapps`).

### Pinning addon versions for a release

The AOSP pin (`manifests/bass-lineage-*-static.xml`) covers the Bass-Core tree only. Addons are pinned separately, so a release can be rebuilt with the same addon commits:

```bash
manifests/update-addons.sh
# writes (not committed):
#   private/manifests/addons-catalog.json   every addon, its remote and commit
#   private/manifests/addons-private.xml    repo manifest of those checkouts
```

Copy both files to another checkout's `private/manifests/`. Its unfold then clones those addon repos at those commits.

### Keeping addons out of Bass-Core

Bass-Core (the public LineageOS forks, device tree and manifest under [los-tv-x86](https://github.com/los-tv-x86)) never contains addon code:

* addon repos and private pins are removed before the static manifest is written;
* commercial patches sit on `bass-api-<level>` branches above the Bass-Core commits, and only commits tagged `bass-core/<branch>/<date>` are pushed to the public repos;
* addon patches apply at build time, in the builder's own tree.

---

## Android 14: `vendor_packages`

Android 14 (Lineage 21.0) Lineout trees have no addon framework: features are product packages in the vendor tree, gated by `ax86_lite.mk` and `tools/build.sh`. Only the private Restricted Launcher Pro uses `addons/`.

```text
vendor/ax86-lite/vendor_packages/<Name>/
  Android.bp / *.mk
  README.md          # picked up by Ax86Docs when present
  init .rc / .sh     # optional; keep package-local when possible
```

| Flag | Packages / behavior |
|------|---------------------|
| `--extras` | Touch Mapper, Display Mapper, Config Overrides, Tweaks, Ax86Docs, Ax86 Power |
| `--btnmgr` | Button Manager |
| `--logger` / `--logging-enabled` | Ax86 Logger |
| `--ax86-power` | Ax86 Power (also included with `--extras`) |
| `--bootsight` | BootSight (Bass fleet backend / Device Status) |
| `--smartdock` | SmartDock DFC |
| `--ethernetconfig` | Ethernet Config |
| `--internet-security` / `--monterey-standby` | Internet Security / Monterey Standby user apps |
| `--restrictedlauncherpro` | Restricted Launcher Pro (private) |
| `--bass-boot-options` / `--cxbbo` | Bass GRUB boot catalog |
| `--ldinstall` / `--ldinstallstrict` | Lockdown install/uninstall block |

BT Ferry, GameNative, Linux Services, BlissDeck, Bass Audio and Bass Style are Android 16 and 17 addons.

### Adding an Android 14 package

1. Create `vendor_packages/YourFeature/` with a product `.mk` and (for apps) `Android.bp`.
2. Wire it in `ax86_lite.mk` behind a flag (or always-on if that is intentional).
3. Add the flag to `tools/build.sh` help and export defaults.
4. Drop a `README.md` in the package so [Ax86Docs](../applications/Ax86Docs/Ax86Docs.md) picks it up on the next `--extras` build.
5. Prefer package-local `init.rc` / scripts. Avoid editing core `addon_init.rc` unless the feature is shared early-boot plumbing.

---

## Runtime overrides (`addon_init`)

Lineout also supports **on-device** overrides without rebuilding the ISO. Scripts under `/vendor/bin/addon_*.sh` run from `addon_init.rc` after `/data` is available. They can bind-mount files from `/data/misc/` over vendor/system paths, apply settings, and react to property triggers.

This is still the **Lineout** product path (same vendor tree). It is not the legacy Bass private-addon unfold flow.

| Path | Role |
|------|------|
| `/vendor/etc/init/addon_init.rc` | Triggers early and late init, mapper props |
| `/vendor/bin/addon_init.sh` | Orchestrator (DMI props, bind mounts, late boot) |
| `addon_hardware.sh` / `addon_peripherals.sh` / `addon_packages.sh` / `addon_mappers.sh` | Helpers used by `addon_init` |
| `/data/misc/` | Fleet- or tech-provided override files |

### GRUB / cmdline toggles (Lineout)

| Flag | Effect |
|------|--------|
| `ADDON_IDC=1` | Custom `.idc` files from `/data/system/devices/idc` |
| `BLISS_INPUT_PORTS_ADDON=1` | `/data/misc/input-port-addon.xml` for input↔display ports |
| `ADDON_BOOTANIMATION=1` | `/data/misc/bootanimation.zip` |
| `ADDON_BASSINIT=1` | Custom vendor init under `/data/vendor/etc/init/`. **Legacy:** not implemented on current Lineout builds |

How-tos:

* [Using IDC Addon](../setup_and_configuration/addon_idc.md)
* [Creating an input-port-addon.xml file](../setup_and_configuration/input-port-associations.md)

On `--extras` builds, [Touch Mapper](../applications/BlissTouchMapper/BlissTouchMapper.md) can generate the input-port file from Settings. Prefer that UI when available; GRUB flags still matter for headless imaging.

### Config files and property triggers (Lineout)

| Mechanism | Docs |
|-----------|------|
| `settings_*.conf`, `runtime_props.conf`, `device_config.conf` | [Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md) |
| `custom_device.prop` (early `ro.*`) | Same page; applied by `addon_init` before framework |
| Master apply | `setprop persist.ax86.update_configs 1` |
| Per-mapper apply | `sys.ax86.display.update`, `sys.ax86.touch.update`, `sys.ax86.radio.update`, `sys.ax86.location.update` |

Vendor reference (also in Ax86Docs): `OVERRIDES.md` and `VENDOR_DEPLOYMENT.md` in `vendor/ax86-lite`.

### Good uses for runtime overrides

* Field fixes (digitizer axes, DPI) without a new ISO
* Fleet imaging: push `/data/misc` files, set GRUB flags, reboot
* Config Override examples under `vendor/ax86-lite/docs/examples/`

Runtime overrides are **not** how you ship a new privileged app. New apps are build addons (`addons/<id>/` on Android 16 and 17, `vendor_packages/` on Android 14) behind a build flag.

---

## App docs

* [Touch Mapper](../applications/BlissTouchMapper/BlissTouchMapper.md)
* [Display Mapper](../applications/BlissDisplayMapper/BlissDisplayMapper.md)
* [Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md)
* [Bliss Tweaks](../applications/BlissTweaks/BlissTweaks.md)
* [Button Manager](../applications/Ax86ButtonManager/Ax86ButtonManager.md)
* [Ax86 Logger](../applications/Ax86Logger/Ax86Logger.md)
* [Ax86 Power](../applications/Ax86Power/Ax86Power.md)
* [BootSight](../applications/BootSight/BootSight.md)
* [BT Ferry](../applications/BTFerry/BTFerry.md)
* [GameNativeX64](../applications/GameNativeX64/GameNativeX64.md)
* [Bass boot options](../setup_and_configuration/bass-boot-options.md)
* [Lockdown install block](../features/lockdown-install-block.md)

## Related (Lineout)

* [Building Bass: Lineout](building-bass.md) (flags and profiles per generation)
* [Feature Flags (aconfig)](aconfig-flags.md)
* [Ax86Docs](../applications/Ax86Docs/Ax86Docs.md)
* [Config Overrides](../applications/BlissConfigOverrides/BlissConfigOverrides.md)
* [Fleet Management](../features/fleet-management.md)
* [Addon Development: Legacy Bass OS](addon-development-legacy-bass.md) (different product tree)
