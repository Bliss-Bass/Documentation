# Linux Services

> **Availability:** Linux Services ships on **Bass: Lineout Android 16** (Lineage **23.2**) x86_64 builds that enable the `linux-services` addon (`--linux-services`). It needs [GameNativeX64](../GameNativeX64/GameNativeX64.md) **1.2.0-x64.17** or later on the device, which provides the Linux environment and runs the jobs.

Linux Services boot-starts, schedules, and auto-restarts **Linux jobs** (background services, terminal programs, and GUI apps) that run in GameNativeX64's Linux environment, and keeps Android from killing them. Jobs can be set up on the device, imported as JSON, or provisioned by an MDM or BootSight through an AIDL interface.

| | |
|---|---|
| **Package** | `org.ax86.linuxservices` (platform-signed priv-app, persistent) |
| **Addon id** | `linux-services` |
| **Build flag** | `--linux-services` / `USE_LINUX_SERVICES=true` (separate from `--gamenative`) |
| **Settings entry** | Settings → System → Linux Services |
| **App drawer** | **Linux Terminal** only |
| **Also see** | [User guide](../../UserGuides/linux-services.md), [AIDL interface](AIDL_INTERFACE.md) |

## How it is split

| Part | Owns |
|------|------|
| **Linux Services** (`org.ax86.linuxservices`) | The job definitions and *when* a job runs: at boot, on a cron schedule, or when the UI or an MDM asks. It also keeps GameNativeX64 alive and opens GUI windows |
| **GameNativeX64** (`app.gamenative`, `LinuxJobService`) | *How* a job runs: it writes the job script into the rootfs, runs it under PRoot, restarts it according to its policy, rotates its log, and reports state |

The addon binds GameNativeX64's job engine with `BIND_IMPORTANT`. The engine admits only callers that share GameNativeX64's uid, or `org.ax86.linuxservices` when it is a system app signed with the platform key.

Nothing needs starting by hand. The addon is `persistent`, so the system launches it once the user unlocks and relaunches it if it dies; `BOOT_COMPLETED` covers a launch before unlock. Either way it starts its API service, binds the engine (starting GameNativeX64's `LinuxJobService`), re-arms cron alarms, and runs the jobs marked to start at boot.

## Environment setup and Linux Terminal

The Linux environment (an Ubuntu rootfs of about 1.2 GB, plus xterm and the X session packages) can be installed without opening GameNativeX64:

- **Settings screen:** a card shows whatever is missing (GameNativeX64, a newer GameNativeX64, the environment, or the graphical session) with a **Set up** / **Finish setup** / **Retry** button, and a progress bar while an install runs.
- **`installEnvironment()`** on the AIDL, for MDM and BootSight zero-touch provisioning. Progress arrives through the `onEnvironment` callback.
- **Linux Terminal** in the app drawer opens one xterm window in GameNativeX64, reusing the open one if there is one, or the setup card when the environment is not ready.

The install runs in GameNativeX64's foreground service for the whole download. Installs are serialized, so one started from GameNativeX64's own Terminal screen and one started from Linux Services cannot undo each other.

## Keeping jobs alive

| Android limit | What the addon does |
|---------------|---------------------|
| Phantom-process killer (more than 32 children, or CPU use in the background) | Ships `persist.sys.fflag.override.settings_enable_monitor_phantom_procs=false` and also writes `settings_enable_monitor_phantom_procs=false` to `Settings.Global` |
| Cached-app freezer | While any job is wanted, GameNativeX64 runs `LinuxJobService` in the foreground (`specialUse`), and the addon holds a `BIND_IMPORTANT` binding to it |
| Doze / App Standby | Adds `app.gamenative` to the permanent power allowlist, allows `RUN_ANY_IN_BACKGROUND` / `RUN_IN_BACKGROUND`, and sets the standby bucket to `ACTIVE` |
| Background FGS / activity starts | Holds `START_FOREGROUND_SERVICES_FROM_BACKGROUND` and `START_ACTIVITIES_FROM_BACKGROUND`, and sends GUI launches with `MODE_BACKGROUND_ACTIVITY_START_ALLOW_ALWAYS` |
| Notification for the FGS | Grants `app.gamenative` `POST_NOTIFICATIONS` |

The exemptions are re-applied when GameNativeX64 is installed or updated. The engine is rebound if it dies, or if a binding goes 10 seconds without connecting (a GameNativeX64 process killed while the bind is coming up otherwise leaves it pending). Jobs that were running before a rebind are restarted.

## Job schema

Jobs are stored in `/data/user/0/org.ax86.linuxservices/files/jobs.json`. They are imported and exported as `{"version": 1, "jobs": [...]}`; a bare array is also accepted.

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "web",
      "name": "Web server",
      "enabled": true,
      "type": "service",
      "shell": "python3 -m http.server 8080",
      "cwd": "/srv/www",
      "env": { "PYTHONUNBUFFERED": "1" },
      "triggers": { "atBoot": true, "delaySec": 20 },
      "restart": { "policy": "always", "maxRestarts": 5, "windowSec": 120 },
      "logs": { "maxKb": 1024 }
    },
    {
      "id": "clock",
      "name": "Wall clock",
      "type": "gui",
      "argv": ["xclock", "-digital"],
      "triggers": { "cron": "0 8 * * 1-5" },
      "restart": { "policy": "on-failure" },
      "gui": { "windowMode": "freeform", "display": "local:4619827259835644672", "bounds": [100, 100, 700, 500] }
    }
  ]
}
```

| Field | Default | Meaning |
|-------|---------|---------|
| `id` | required | 1-64 characters: `A-Z a-z 0-9 . _ -`, starting with a letter or digit |
| `name` | `id` | Display name |
| `enabled` | `true` | Disabled jobs are not started by triggers or `startJob` |
| `type` | `service` | `service` (headless), `terminal` (an xterm window), `gui` (a window) |
| `argv` / `shell` | one required | Either an exec argv list or a `/bin/sh` script body; exactly one |
| `cwd`, `env` | none | Working directory and environment variables inside the rootfs |
| `triggers.atBoot` | `false` | Start once per boot |
| `triggers.delaySec` | `0` | How long to wait after boot (0 to 3600 seconds) |
| `triggers.cron` | none | Five fields, in local time: `min hour day month weekday`. Accepts `*`, numbers, `a-b` ranges, `a,b` lists, and `/n` steps; weekday 0 and 7 are both Sunday. Month and day names and `@daily`-style macros are not supported |
| `restart.policy` | `never` | `never`, `on-failure` (non-zero exit), `always` |
| `restart.maxRestarts` / `windowSec` | `5` / `120` | The job is marked `failed` after this many restarts within this many seconds |
| `logs.maxKb` | `1024` | Log size cap (up to 16 MB). The log rotates to `<id>.log.1` when it passes the cap |
| `gui.windowMode` | `fullscreen` | `fullscreen`, `fullscreen-pinned` (lock task), `freeform`. Split-screen is not offered |
| `gui.display` | default display | The `Display.getUniqueId()` of the target display. If it is absent, the addon waits up to 60 seconds for it to connect, then uses the default display |
| `gui.bounds` | none | Freeform window rectangle: `[left, top, right, bottom]`. Grown to at least 400x400 px, since GameNativeX64 needs a 320 px client area before it opens the X session |

Restarts back off from 1 second, doubling up to 60 seconds; the delay resets after a run of 60 seconds or more. Stopping a job keeps it down until it is started again or one of its triggers fires.

Every job script runs with `LINUX_SERVICES_JOB=<id>` in its environment, and the job's processes inherit it. When a job exits or is stopped, GameNativeX64 ends any process still carrying it, so a killed PRoot cannot leave a copy of the job running (and holding its port) next to the restarted one. The Inspector uses the same variable to attribute processes to jobs.

Terminal and GUI jobs run in a GameNativeX64 session window. Closing the window counts as the job exiting with code 0, and stopping the job closes the window. Terminal jobs with policy `never` use `xterm -hold`, so their output stays readable.

Logs are kept in GameNativeX64's data directory, under `files/linux-services/logs/<id>.log`. Lines the engine writes itself are prefixed with `[linux-services <time>]`.

## Debugging from adb

```bash
S=org.ax86.linuxservices/.LinuxServicesService
adb shell dumpsys activity service $S status     # also: jobs | inspect | environment
# Debuggable builds only (also: install-environment):
adb shell "dumpsys activity service $S import '{\"jobs\":[{\"id\":\"t\",\"shell\":\"sleep 30\",\"restart\":{\"policy\":\"always\"}}]}'"
adb shell dumpsys activity service $S start t    # also: stop ID | delete ID
adb logcat -s LinuxServices
```

The addon ships `examples/sample-jobs.json`, which exercises every job type, trigger, and restart policy: a web server on port 8080, a heartbeat logger, a crash-looping service, a cron report, `top` in a terminal, a hello-world window, and a Firefox window that starts disabled.

```bash
adb push examples/sample-jobs.json /data/local/tmp/
adb shell 'dumpsys activity service '$S' import "$(cat /data/local/tmp/sample-jobs.json)" replace'
```

## Related

- [Linux Services AIDL](AIDL_INTERFACE.md)
- [GameNativeX64](../GameNativeX64/GameNativeX64.md)
- [Addon Development: Bass Lineout](../../development/addon-development.md)
