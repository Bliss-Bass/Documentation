# Linux Services AIDL

Binder API for MDMs and BootSight to provision and control [Linux Services](LinuxServices.md) jobs.

| | |
|---|---|
| **Bind action** | `org.ax86.linuxservices.ILinuxServices` |
| **Package** | `org.ax86.linuxservices` |
| **AIDL** | `org.ax86.linuxservices.ILinuxServices`, callback `ILinuxServicesCallback` |
| **API version** | `2` |

## Who may call it

A caller is allowed if it is one of these:

- the system uid;
- a holder of `org.ax86.linuxservices.permission.MANAGE_JOBS` (`signature|privileged`);
- the device owner;
- a package listed by certificate SHA-256 in `/system/etc/linux-services-callers.xml`.

Any other caller gets a `SecurityException`.

## Methods

| API | Role |
|-----|------|
| `apiVersion()` | Currently `2` |
| `listJobs()` / `getJob(id)` | Job definitions (JSON). See the [job schema](LinuxServices.md#job-schema) |
| `upsertJob(json)` / `deleteJob(id)` | Add, replace, or delete one job. `upsertJob` returns `null`, or the reason it refused the job |
| `importJson(json, replace)` / `exportJson()` | Whole document, all or nothing. `replace` deletes jobs not in the document |
| `startJob(id)` / `stopJob(id)` | Start now, whatever the triggers; stop and hold down |
| `status()` | JSON array, one entry per job. Fields: `id`, `name`, `type`, `enabled`, `state` (`stopped`/`starting`/`running`/`backoff`/`exited`/`failed`), `desired`, `pid`, `exitCode`, `restarts`, `startedAt`, `message`, `wanted`, `nextRun`, `engineConnected` |
| `inspect()` | `{takenAt, appPid, processes:[...], jobs:[...]}`. Each process has `pid`, `ppid`, `name`, `cmdline`, `status` (`running`/`sleeping`/`paused`/`stale`/`zombie`), `rssKb`, `cpuPercent`, and `owner` (a job id, `session`, or `orphan`). Each job has `processCount`, `rssKb`, `cpuPercent`, `stale`, `paused` |
| `endProcess(pid)` | SIGCONT, then SIGTERM, then SIGKILL after 500 ms. Only works on GameNativeX64 guest processes |
| `openLog(id)` | Read-only file descriptor for the job's log |
| `registerCallback(cb)` / `unregisterCallback(cb)` | `onJobState(id, stateJson)`; API 2 adds `onEnvironment(stateJson)` |
| `environment()` (API 2) | JSON object: `engineConnected`, `engineOutdated`, `supported`, `installed`, `displaySession`, `available`, `installing`, `progress {message, fraction}`, `error`, `requiredBytes`, `freeBytes` |
| `installEnvironment()` (API 2) | Downloads and installs the Linux environment headless, or completes a partial install. Returns false if GameNativeX64 is missing or too old, the device cannot run it, or an install is already running |

## Zero-touch example

A provisioning client typically:

1. Binds, checks `apiVersion() >= 2`, and registers a callback.
2. Calls `environment()`. If `installed` or `displaySession` is false, calls `installEnvironment()` and waits for an `onEnvironment` update with both true.
3. Calls `importJson(document, true)` with the fleet's job set.
4. Watches `onJobState` or polls `status()`.

Jobs marked `atBoot` then start on every boot without the client being present.
