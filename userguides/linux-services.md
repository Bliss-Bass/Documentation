# Linux Services

> **Android 16 Lineout.** Screenshots and steps on these pages were taken on **Bass: Lineout** (Lineage **23.2** / Android **16**). On **Android 14** (Lineage **21.0**) the same tools can look different, sit in a different Settings place, or be missing from that image entirely.

Linux Services runs Linux programs from GameNativeX64 **on their own**. It can start them when the device boots or on a schedule, and it restarts them if they stop. It works for background servers, terminal programs, and programs with a window.

Open it from **Settings → System → Linux Services** (it does not appear as a normal app icon).

## Before you start

Linux programs run in a Linux (Ubuntu) environment that is downloaded once, about 1.2 GB. GameNativeX64 (1.2.0-x64.17 or later) provides it, but you do not need to open GameNativeX64 to set it up:

- Open **Linux Services**. If Linux is not set up yet, a card at the top says **Set up the Linux environment**. Tap **Set up**. Setup continues in the background if you leave the screen, and the card shows its progress.
- Or open **Linux Terminal** from the app drawer. It takes you to the same card the first time.

If the card says **GameNative is not connected**, install or update GameNativeX64.

You never need to start Linux Services yourself. It starts with the device, and it comes back on its own if Android or an update closes it.

## Linux Terminal

**Linux Terminal** in the app drawer opens a terminal window in the Linux environment. Opening it again brings back the same window. You can also open it from **Open terminal** in the Linux Services menu.

## Jobs

Each program you set up is a **job**. The job list shows each job's state (running, stopped, restarting, or failed), what starts it, when it runs next, and how many times it has restarted.

- **Start** / **Stop**: run a job now, or stop it. A stopped job stays stopped until you start it again or its schedule comes around.
- **Logs**: see what the program printed. Turn on **Auto-refresh** in the menu to follow it live.
- **Edit**: change the job, or delete it.

Tap **Add job** to make a new one.

## Setting up a job

| Setting | What it does |
|---------|--------------|
| **ID** | A short name for the job (letters, digits, `.`, `_`, `-`). It cannot be changed later |
| **Name** | What the list shows |
| **Type** | **Service**: runs in the background with no window (a web server, a sync tool). **Terminal**: runs in a terminal window. **GUI app**: a program with its own window |
| **Command** | What to run, as you would type it in a Linux terminal |
| **Working directory** / **Environment** | Optional: the folder it runs in and extra `KEY=value` settings |
| **Start at boot** | Start the job every time the device starts, optionally after a delay |
| **Schedule** | Run it at set times (see below) |
| **Restart** | **Never**, **On failure** (only when it exits with an error), or **Always** |
| **Give up after...** | If the job keeps crashing (by default, 5 restarts within 120 seconds), it stops trying and you get a notification |

For **GUI app** and **Terminal** jobs you also choose the **Window**:

- **Fullscreen**: fills the screen.
- **Fullscreen, pinned**: fills the screen and is locked there, for kiosks and signage.
- **Freeform window**: a normal movable window. Optionally set its position and size as left,top,right,bottom. Windows smaller than 400 by 400 pixels are enlarged to that size.

Pick the **Display** to show it on. If that screen is not plugged in yet, Linux Services waits up to a minute for it, then uses the main screen.

Stopping a GUI or Terminal job closes its window. Closing the window yourself counts as the job ending normally.

## Schedules

Schedules use the classic cron format: **minute hour day month weekday**.

| Schedule | Runs |
|----------|------|
| `0 8 * * *` | Every day at 08:00 |
| `*/15 * * * *` | Every 15 minutes |
| `30 18 * * 1-5` | Weekdays at 18:30 |
| `0 3 1 * *` | 03:00 on the first of each month |

Weekday 0 or 7 is Sunday. Times follow the device's clock and time zone.

## Untracked programs

Below your jobs, the **Untracked** list shows Linux programs that are running now but are not jobs: apps you opened from the app drawer, and commands you started in the Linux Terminal. A command piped through others, such as `apt-get install foo | tail`, shows as one entry.

Tap **Add to jobs** to open the job editor already filled in with the program's command and folder, set to start at boot and restart on failure. Change anything you like, then save. Only the command itself is copied, not any redirection you typed after it, so add that back in the editor if you need it.

## Inspector

**Inspector** (in the menu) shows every Linux program that is running now, grouped by job, with its CPU and memory use.

- **Running**: using the CPU right now. A program counts as running when any of its threads is busy, so a browser playing a video shows as running even while its main thread waits.
- **Sleeping**: idle, waiting for input or a timer.
- **Paused**: stopped by Android or by a signal.
- **Stale**: left behind by a closed session, or a job that says it is running but has no program.
- **Zombie**: finished but not yet cleaned up.

Tap a program to **End process**. If it belongs to a job that restarts, the job starts it again.

## Import and export

Use **Import JSON** / **Export JSON** in the menu to copy jobs between devices or back them up. When importing, **Merge** adds and updates jobs; **Replace** also removes jobs that are not in the file.

Device managers can set up jobs remotely, and a sample set of jobs is available for trying things out. See the technical page below.

## Related

- [Getting started](README.md)
- Technical: [Linux Services](../applications/LinuxServices/LinuxServices.md)
