# A14 Physical Pointer Routing

SmartDock is a priv-app with `ASSOCIATE_INPUT_DEVICE_TO_DISPLAY`. On Android 14,
physical mice and touchpads should be routed via framework APIs — not the software
overlay relay used as a fallback.

## Correct API (A14+)

Association uses **display uniqueId**, not numeric displayId:

```java
// InputManager / InputManagerGlobal / IInputManager
addUniqueIdAssociationByDescriptor(inputDeviceDescriptor, displayUniqueId);
addUniqueIdAssociationByPort(inputPort, displayUniqueId);
```

SmartDock calls these via reflection in `InputRoutingManager.routeDeviceByUniqueId()`.

Logcat on success:

```
SmartDock Input Routing: SUCCESS: Routed '...' via InputManager.addUniqueIdAssociationByDescriptor -> displayUniqueId=local:...
SmartDock Input Routing: Physical pointer mode: PHYSICAL_HARDWARE
```

## Verify on device

```bash
adb logcat -s "SmartDock Input Routing" DisplayPointerController

# List input device locations (ports)
adb shell dumpsys input | grep -A5 "Input Device"

# List display unique IDs
adb shell dumpsys display | grep -i unique
```

## If routing still fails (0/N devices)

Your A14 build may not expose the association APIs to priv-apps, or pointer-class
devices need a framework patch. Options:

### 1. Enable `cmd input` shell commands (recommended for vendor trees)

Add to `frameworks/base/services/core/java/com/android/server/input/InputShellCommand.java`:

- `set-pointer-display-id <displayId>`
- `associate <descriptor> <displayId>` → calls `addUniqueIdAssociationByDescriptor`

SmartDock already tries these shell commands as a fallback.

### 2. Static port associations

For fixed kiosk wiring, `/vendor/etc/input-port-associations.xml` maps USB input
ports to display ports (see [AOSP input routing](https://source.android.com/docs/core/display/multi_display/input-routing)).

### 3. Software relay (interim)

When hardware routing fails, SmartDock uses `PHYSICAL_SOFTWARE` mode:

- SmartDock cursor overlay on target display
- Relative movement relay from off-target displays
- Click injection via `dispatchGesture` at overlay position
- Native cursor hidden on all displays (best-effort)

This is **not** equivalent to true routing — hover events cannot be pilfered on A14
(`Can't pilfer: no touching devices` in logcat). Virtual touchpad remains the
recommended precise input path.

## Pointer modes

| Mode | When | Overlay | Native cursor |
|------|------|---------|-----------------|
| `VIRTUAL_TOUCHPAD` | Touchpad open | Yes | Hidden on target |
| `PHYSICAL_HARDWARE` | Association succeeded | No | On target display |
| `PHYSICAL_SOFTWARE` | Association failed | Yes | Hidden (best-effort) |
| `OFF` | Routing disabled | No | Normal |

## Permissions

Already in `aosp/privapp-permissions-smartdock.xml`:

- `ASSOCIATE_INPUT_DEVICE_TO_DISPLAY`
- `MONITOR_INPUT`
- `INJECT_EVENTS`
