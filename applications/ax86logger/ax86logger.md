# Ax86 Logger

Ax86 Logger is a privileged system service that captures rolling logcat output for field diagnostics. Use it when you need to pull recent system logs off a device without keeping a laptop attached the whole time.

| | |
|---|---|
| **Package** | `com.ax86.logger` |
| **Service / cmd** | `ax86_logger` |
| **Build flags** | `--logger` (include the app), `--logging-enabled` (start capture by default) |
| **Log directory** | `/data/misc/logs` |

`--logging-enabled` implies `--logger`. With only `--logger`, the app is installed but capture stays off until you enable it.

## Properties (`persist.ax86.logging.*`)

| Property | Default | Description |
|----------|---------|-------------|
| `enabled` | `false` | Start or stop capture |
| `level` | `E` | logcat filter: `E`, `W`, `I`, `D`, `V` |
| `max_bytes` | `10485760` | Max size per active file (10 MiB) |
| `max_files` | `10` | How many rotated files to keep |
| `dir` | `/data/misc/logs` | Output directory |

Log files are named `ax86-{sessionTag}.log`. The session tag is the UTC time capture started (`yyyyMMdd'T'HHmmss'Z'`), for example `ax86-20260702T213400Z.log`. That tag is set once when capture starts, so a later clock sync does not rename the active file.

When a file hits `max_bytes`, it rotates to `.log.1`, `.log.2`, and so on. Older files past `max_files` are removed.

## Enable and check status

```bash
adb shell setprop persist.ax86.logging.enabled true
adb shell cmd ax86_logger status
adb shell cmd ax86_logger list
```

Or use the helpers:

```bash
adb shell cmd ax86_logger enable
adb shell cmd ax86_logger disable
```

Change the filter level without rebuilding:

```bash
adb shell setprop persist.ax86.logging.level I
```

Valid levels: `E`, `W`, `I`, `D`, `V`. Higher verbosity fills the rolling files faster.

## Dump logs to USB

Plug in a USB drive, then run any of:

```bash
adb shell cmd ax86_logger dump
```

```bash
adb shell /vendor/bin/ax86_logger_dump.sh
```

You can also send the dump intent:

* Broadcast: `com.ax86.logger.action.DUMP_LOGS`
* Activity: same action opens `DumpActivity`

Exports land under `{USB}/ax86-logs/{timestamp}/`.

If you use [Button Manager](../Ax86ButtonManager/Ax86ButtonManager.md), map a hardware key to a **broadcast** action with intent `com.ax86.logger.action.DUMP_LOGS` so field techs can dump logs without ADB.

## Build-time defaults

Include the logger but leave it off until enabled at runtime:

```bash
./build.sh --logger ...
```

Include the logger and start capture on first boot:

```bash
./build.sh --logging-enabled ...
```

That sets `persist.ax86.logging.enabled=true` in the image.

## Related

* [Button Manager](../Ax86ButtonManager/Ax86ButtonManager.md) for mapping a dump key
* [Building Bass OS](../../development/building-bass.md) for Lineout / ax86-lite build flags
