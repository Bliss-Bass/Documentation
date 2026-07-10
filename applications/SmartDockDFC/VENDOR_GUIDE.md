# Vendor Implementation Guide: SmartDock DFC

This guide provides exhaustive documentation for Original Equipment Manufacturers (OEMs) and AOSP integrators to integrate and pre-configure SmartDock DFC.

## 1. Integration Instructions

### Source Placement
Extract your licensed SmartDock DFC distribution tarball into your AOSP source tree at the following location:
`vendor/agp-apps/smartdock`

### Inclusion in Product Build
To include SmartDock DFC, its associated system overlays, and permission whitelists in your build, add the following line to your main product makefile (e.g., `device/vendor/model/product.mk`):

```makefile
$(call inherit-product, vendor/agp-apps/smartdock/SmartDock.mk)
```

### Overriding Default Configuration
SmartDock DFC is designed to be highly flexible. While `SmartDock.mk` provides a set of sensible defaults in `PRODUCT_PROPERTY_OVERRIDES`, you can override any of these flags in your target device's specific makefile or `build.prop` to achieve the desired combination of features for your hardware.

### Boot-time Secure Settings (`init.rc`)
For critical system integrations, such as enabling accessibility services and notification listeners from boot, configuring settings via an `init.rc` script is the most robust method in AOSP. This ensures settings are applied at a high privilege level during the early boot sequence, before the application starts.

SmartDock ships `smartdock_dfc_init.rc` and `smartdock_grant_permissions.sh` under `aosp/`. `SmartDock.mk` installs them to:

*   `/vendor/etc/init/smartdock_dfc_init.rc`
*   `/vendor/bin/smartdock_grant_permissions.sh`

On `sys.boot_completed`, `smartdock_dfc_init.rc` only enables overlay settings (safe before unlock).

On `sys.user.0.ce_available=1`, init enables the accessibility service, starts `DockService`, and runs `smartdock_grant_permissions`. Both `DockService` and `NotificationService` defer CE-dependent initialization (SharedPreferences, dock UI) until credential storage is unlocked.

The **oneshot** service `smartdock_grant_permissions` waits for CE storage (`sys.user.0.ce_available` or `cmd user is-unlocked`), then applies:

*   `pm grant` and `appops set` (overlay, usage stats, secure settings, etc.)
*   **Notification Listener** (`enabled_notification_listeners` + `cmd notification allow_listener`)
*   **Device Administrator** via `dpm set-active-admin`

`sys.user.0.ce_available=1` starts the grant script and enables accessibility / DockService. After grants complete, the script restarts SmartDock so the notification listener binds without a stale crashed state.

**Note on Placement & SELinux:**
*   Files are copied via `SmartDock.mk` `PRODUCT_COPY_FILES` (see above paths).
*   You will almost certainly need to adjust your SELinux policies to permit `init` (or other relevant domains like `system_server`) to write to `Settings.Secure`. This usually involves adding rules to `.te` files in your device's `sepolicy` directory.

## 2. Comprehensive Property Directory

### Core Shell Behavior
| Property | Valid Values | Description |
| :--- | :--- | :--- |
| `persist.bass.sd.layout` | `phone`, `tablet`, `desktop` | Sets the initial UI density and layout rules. |
| `persist.bass.sd.docked` | `docked`, `hidden` | Sets whether the dock is pinned (visible) or hidden by default on first boot. |
| `persist.bass.sd.activation_method` | `nav`, `swipe`, `handle` | `nav`: Uses the navigation handle area. `swipe`: Edge-based trigger. `handle`: Visible button. |
| `persist.bass.sd.reserve_space` | `true`, `false` | If true, the system reserves screen real estate at the bottom so apps do not overlap the dock. |

### Visuals & Theming
| Property | Valid Values | Description |
| :--- | :--- | :--- |
| `persist.bass.sd.theme` | `system`, `dark`, `light`, `black`, `transparent`, `material`, `fallback`, `expressive` | Sets the default theme. `expressive` enables Material 3 Expressive dynamic coloring. |
| `persist.bass.sd.icon_bg_style` | `none`, `circles`, `islands` | Sets how app icons are presented in the dock and menu. |
| `persist.bass.sd.dynamic_wallpaper_contrast` | `true`, `false` | Icons automatically flip contrast based on the wallpaper pixels beneath them. |
| `persist.bass.sd.rounded_corners` | `true`, `false` | Enables/Disables heavily rounded corners for the dock container. |
| `persist.bass.sd.dock_height` | `50` to `70` | The base height of the dock in DP. |
| `persist.bass.sd.dock_scale` | `0.5` to `1.5` | Universal UI scale multiplier for all dock elements. |
| `persist.bass.sd.enable_blur` | `true`, `false` | Enables background blur for the Apps Menu and QS drawer (Android 12+). |
| `persist.bass.sd.enable_dock_blur` | `true`, `false` | Enables background blur for the main dock bar (Android 12+). |
| `persist.bass.sd.override_panel_alpha` | `true`, `false` | Enables manual transparency override for major panels and islands. |
| `persist.bass.sd.panel_alpha` | `0` to `255` | Default transparency for panels when override is enabled. |
| `persist.bass.sd.qs_height_ratio` | `0.33`, `0.66`, `0.99` | Sets the maximum vertical height ratio for the Notification Panel. |
| `persist.bass.sd.qs_panel_width` | `100` to `200` | Sets the default relative width percentage for the Notification/QS Panel. |
| `persist.bass.sd.qs_panel_scale` | `50` to `150` | Sets the default UI scale percentage for the Notification/QS Panel. |

### App Menu Configuration
| Property | Valid Values | Description |
| :--- | :--- | :--- |
| `persist.bass.sd.center_app_menu` | `true`, `false` | Centers the Apps Menu panel on the screen instead of aligning to the button. |
| `persist.bass.sd.center_apps_menu_button` | `true`, `false` | Places the Apps Menu trigger button in the center of the taskbar. |
| `persist.bass.sd.enable_continue_left_off` | `true`, `false` | Enables "Continue where you left off" (Recent Docs/Webpages) in the menu. |
| `persist.bass.sd.enable_recent_apps_menu` | `true`, `false` | Shows a row of recently used apps at the top of the Apps Menu. |

### System Overlays (Visual Modification)
| Property                              | Default | Description |
|:--------------------------------------| :--- | :--- |
| `persist.bass.sd.hide_status_bar`     | `false` | Enables the overlay to set system status bar height to 0. |
| `persist.bass.sd.hide_nav_bar`        | `false` | Enables the overlay to hide the AOSP navigation bar. |
| `persist.bass.sd.hide_taskbar`        | `false` | Disables the AOSP 12L+ Taskbar on large screens via overlay. |
| `persist.bass.sd.use_custom_qs`       | `true` | Replaces the system notification shade with the Material Design QS drawer. |
| `persist.bass.sd.enable_blur_overlay` | `false` | Enables system-wide background blur support via overlay. |

### Advanced Window Type Overrides
These properties allow for direct control over the `WindowManager.LayoutParams.type` value used for SmartDock's windows. This is an advanced configuration option primarily for AOSP integrators to fine-tune layering behavior or resolve conflicts with other system UI components. Values are integers corresponding to `WindowManager.LayoutParams.TYPE_` constants.

| Property                                  | Default (Auto-detected) | Description |
|:------------------------------------------| :--- | :--- |
| `persist.smartdock.window_type_override`          | `2032` (A14-), `2019` (A15+) | Overrides the WindowManager.LayoutParams.TYPE_ for the main dock on the primary display. |
| `persist.smartdock.window_type_override_handle`   | `2032` (A14-), `2024` (A15+) | Overrides the WindowManager.LayoutParams.TYPE_ for the dock handle on the primary display. |
| `persist.smartdock.window_type_override_secondary`| `2024` | Overrides the WindowManager.LayoutParams.TYPE_ for the main dock on secondary displays. |
| `persist.smartdock.window_type_override_handle_secondary` | `2024` | Overrides the WindowManager.LayoutParams.TYPE_ for the dock handle on secondary displays. |

**Common Window Types for Overlays:**
| Value | `WindowManager.LayoutParams.TYPE_` Constant (SDK 34) | Description |
| :--- | :--- | :--- |
| `2000` | `TYPE_PHONE` | Application window that is not a full-screen activity. Often used for pop-ups and overlays. |
| `2003` | `TYPE_STATUS_BAR` | The status bar itself. **Highly restricted.** |
| `2011` | `TYPE_TOAST` | A transient, non-interactive overlay like a toast message. |
| `2019` | `TYPE_NAVIGATION_BAR` | The system navigation bar. **Highly restricted on modern Android.** |
| `2024` | `TYPE_NAVIGATION_BAR_PANEL` | A panel on top of the navigation bar. Less restricted than `TYPE_NAVIGATION_BAR`. |
| `2032` | `TYPE_ACCESSIBILITY_OVERLAY` | An overlay window for accessibility services. Generally well-suited for system-level overlays. |
| `2038` | `TYPE_APPLICATION_OVERLAY` | Standard application overlay window. Requires `SYSTEM_ALERT_WINDOW` permission. |

### Functional Restrictions & Production Lock-down
| Property | Default | Description |
| :--- | :--- | :--- |
| `persist.bass.sd.disable_statusbar_dpm` | `false` | Functionally disables the status bar and notification shade expansion via DevicePolicyManager. |
| `persist.bass.sd.disable_navbar_dpm` | `false` | Functionally disables the system navigation buttons at the framework level. |
| `persist.bass.sd.skip_onboarding` | `false` | Automatically marks the onboarding wizard as complete on first boot. |
| `persist.bass.sd.disable_customization` | `false` | Hides shell and visual customization options in the Settings activity for production devices. |

### Navigation & Display
| Property | Valid Values | Description |
| :--- | :--- | :--- |
| `persist.bass.sd.nav_mode` | `system`, `gesture`, `2button`, `3button` | Overrides the system navigation mode for the SmartDock handle. |
| `persist.bass.sd.nav_btn_justification` | `left`, `center`, `right` | Horizontal alignment of navigation buttons within the dock. |
| `persist.bass.sd.multi_display` | `true`, `false` | Enables independent dock instances on all connected displays. |
| `persist.bass.sd.supported_displays` | `primary`, `external`, `all` | Filter for which display types should initialize a SmartDock instance. |

### Input & Advanced Interaction
| Property | Default | Description |
| :--- | :--- | :--- |
| `persist.bass.sd.enable_touchpad` | `false` | Enables the Virtual Touchpad dock button by default. |
| `persist.bass.sd.auto_show_touchpad` | `false` | Automatically show the touchpad on the primary display when a secondary screen is detected. |
| `persist.bass.sd.enable_routing` | `false` | Enables the Physical Pointer Routing dock button by default. |

## 3. Deployment Check-list
1.  **Priv-App Status:** Ensure SmartDock is in `/product/priv-app/`.
2.  **Permissions:** Verify `privapp-permissions-smartdock.xml` is in `/product/etc/permissions/`.
3.  **Stability:** Verify `sysconfig-smartdock.xml` is in `/product/etc/sysconfig/`.
4.  **Boot-time Settings:** Ensure `smartdock_dfc_init.rc` is correctly placed and configured as per the "Boot-time Secure Settings" section to grant critical permissions early in the boot process.
5.  **Other Properties:** Add any other desired defaults to `build.prop` using the tables above.
