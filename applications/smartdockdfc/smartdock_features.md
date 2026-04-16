# SmartDock DFC (Desktop Framework Component) - Feature Overview

SmartDock DFC is a deep-integration desktop framework for Android, designed to transform mobile interfaces into productive, multi-display desktop environments.

## 1. Taskbar & Application Management
*   **Dynamic Taskbar:** A persistent or auto-hiding dock that displays pinned and currently running applications.
*   **Center Apps Menu Button:** Option to center the primary app launcher button within the running tasks list for a symmetrical, modern layout.
*   **Running Task Indicators:** Visual indicators for active apps, including task counters for multiple instances of the same package.
*   **Task Selection Menu:** Long-press or secondary-click functionality to select between multiple running instances of an application.
*   **Contextual Actions:** Right-click/Long-press support for quick access to app info, pinning, or closing tasks.
*   **Intelligent Placement:** Flexible alignment options including "Center Running Apps" and "Island" grouping modes.
*   **Auto-Pin Logic:** Configurable behavior to pin the dock on startup, auto-pin when windowed apps are present, and auto-unpin when an app enters fullscreen.
*   **Taskbar Constraints:** Customizable limits for running apps in both portrait and landscape modes.

## 2. Navigation & Gestures
*   **Unified Navigation Handle:** A consolidated gesture area that supports classic pill-based navigation and expanded button layouts.
*   **Quick-Access Nav Buttons:** On-screen buttons for Back, Home, Recents, Assistant, Power, Volume, and IME switching.
*   **Hot Corners:** Customizable actions (like Overview/Recents) triggered by moving the pointer to defined screen corners (Top-Right, Bottom-Right) with adjustable activation delay.
*   **Hover Activation:** Support for desktop-class mouse hover to reveal the dock when hidden, with a customizable activation area.
*   **Nav Handle Customization:** Adjustable width, opacity, and theme-aware colors (Light/Dark) for the navigation handle.
*   **System Gesture Integration:** Deep integration with Android system insets to prevent UI overlap and gesture conflicts.

## 3. Quick Settings & Notification Center
*   **Material 3 Expressive Panel:** A custom-built Quick Settings drawer utilizing the latest M3 design tokens.
*   **Live Notification Updates:** Real-time notification syncing with support for progress bars, live titles, and action buttons.
*   **QS Tile Pagination:** Paginated tile layout with centered indicator dots for navigating multiple pages of toggles.
*   **Panel Scaling & Dimensions:** Independent scaling (width and height ratio) to optimize the panel for various display sizes and densities.
*   **Section Persistence:** The drawer remembers the expanded or collapsed state of Quick Settings, Sliders, and Notifications.
*   **Expressive Sliders:** High-fidelity sliders for Brightness and Volume with immediate visual feedback.
*   **Notification Management:** User-configurable timeout for heads-up notifications and quick access to system notification settings.
*   **Tray Toggles:** Individual toggles for Bluetooth, Battery, Wi-Fi, Volume, Date, and Pin indicators in the system tray.

## 4. Virtual Input & Peripheral Control
*   **Virtual Touchpad:** A floating, resizable touchpad window for controlling pointers on secondary displays.
    *   **Multi-Touch Gestures:** Support for 2-finger scrolling and 2-finger tap for right-click.
    *   **Dynamic Resizing:** Polished resize handle to adjust the touchpad area on the fly.
    *   **Keyboard Integration:** Quick toggle for the system soft keyboard from within the touchpad interface.
*   **Auto-Prompt:** Intelligent detection of external displays to prompt the user to open the virtual touchpad.

## 5. System Tray & Status
*   **Interactive Tray Icons:** One-tap toggles for Wi-Fi, Bluetooth, and Volume.
*   **Enhanced Battery Meter:** Integrated battery status with support for charging indicators and numerical percentage display.
*   **Desktop Clock:** A persistent TextClock with support for custom date/time formats.
*   **Quick Scaling Badge:** A dynamic notification badge that scales with the dock and provides a quick entry point to the notification center.
*   **Status Icon Blacklist:** Granular control to hide specific system icons from the tray to reduce clutter.

## 6. Theming & Customization
*   **Dynamic System Theme:** Automatically adjusts colors based on the current wallpaper (Material You) or active application's status bar (API 36+).
*   **Icon Pack Support:** Compatibility with third-party icon packs for a fully personalized look.
*   **Custom Color Theming:** Manual control over theme main colors, icon background colors, and icon foreground (tint) colors.
*   **Icon Shaping:** Support for multiple icon background shapes including Circle, Round Rect, and Square.
*   **Island Mode:** Support for a floating "Island" dock layout with adjustable height and background transparency.
*   **Panel Appearance:** Adjustable panel height ratio and manual transparency overrides for Apps Menu and QS Panels.
*   **Background Blur:** Material Design blur effects for the Apps Menu and Notification Panel backgrounds (Android 12+).
*   **Dock Layouts:** Pre-defined layout templates for different usage scenarios.
*   **App Menu Customization:** Choice between compact or full-screen Application Menu with adjustable grid columns and custom user profiles (name/icon).
*   **Smart Content:** "Continue where you left off" feature for quick access to documents and recent apps within the menu.

## 7. Advanced System Integration
*   **Multi-Display Optimization:** Intelligent SmartDock instances for connected displays with filterable display types (Internal, External, Virtual).
*   **Window Management:** "Launch Mode" selection (Standard, Windowed, Fullscreen) for apps, with games-specific fullscreen auto-detection.
*   **Default App Mapping:** Ability to map global shortcuts and tray actions to preferred Browser, File Manager, Music Player, and Terminal apps.
*   **Desktop Keyboard Shortcuts:** Extensive support for Meta-key combinations for launching apps, toggling the dock, and locking the device.
*   **System Overlays:** Ability to hide the system status bar, navigation bar, and native launcher taskbar using overlay injection (requires Root or System App status).
*   **Per-Display Density (DPI):** Dynamic adjustment of display density for both the primary device and connected external monitors.
*   **App Lifecycle Management:** Advanced features for freezing apps, uninstalling system apps, and managing "Heads-up" notifications.
*   **Backup & Restore:** Full configuration portability via `.sdp` backup files.

## 8. Vendor & OEM Configuration Features
SmartDock DFC provides an extensive `persist.bass.sd.*` property system for deep integration by OEMs and system integrators.

*   **Production Lockdown:** Ability to hide all customization options in the user-facing Settings activity for managed or kiosk-mode devices.
*   **Onboarding Bypass:** Feature to automatically skip the first-boot onboarding wizard for pre-configured enterprise deployments.
*   **System UI Replacement:** Deep functional overrides to replace the stock status bar and navigation bar behavior via DevicePolicyManager (DPM) integration.
*   **Dynamic Contrast Adjustment:** Automatic icon contrast flipping based on real-time wallpaper analysis behind dock elements.
*   **Initial Layout Persistence:** OEM-defined default layouts (Phone, Tablet, Desktop) and dock states (Pinned vs. Hidden) on a per-device model basis.
*   **Justification Control:** Fine-grained horizontal alignment (Left, Center, Right) for navigation buttons within the system dock.
*   **Privileged Taskbar Control:** Native ability to disable the AOSP 12L+ Taskbar on large-screen devices via overlay management.

---

## 9. Experimental & Ongoing Development (In-Progress)

### **Standalone Input Routing Service (AIDL)**
*   **Goal:** A centralized system service to pair specific input devices (USB mice, touchscreens) to specific displays via bind-mount configuration injection.
*   **Status:** Designing the `IInputRoutingService.aidl` interface and investigating dynamic port-association strategies. Currently facing stability issues with direct pointer event redirection.

### **Enhanced Workspace Switcher**
*   **Goal:** A visual representation of Android 15/16 Freeform desktops within the dock.
*   **Status:** Researching Launcher3 (Recents) triggers for desktop creation and context menu integration for moving windows between virtual desktops.

### **Per-Display Scaling Persistence**
*   **Goal:** The ability to store and automatically re-apply unique scaling and DPI values for specific monitors based on their hardware descriptors.
*   **Status:** Updating data store logic to use unique display identifiers rather than transient display IDs.

### **Intelligent Tray Condensing**
*   **Goal:** Automatically condense the system tray into the notification drawer footer on small or highly-scaled displays to maximize taskbar space.
*   **Status:** Designing triggers based on DPI/Scale and implementing the migration of audio and power functions to the QS footer.

### **Advanced Window Management**
*   **Goal:** Deep integration with `ActivityTaskManager` for enhanced snapshotting and window arrangement.
*   **Status:** Ongoing refinement of internal/hidden API usage for stability across AOSP builds.
