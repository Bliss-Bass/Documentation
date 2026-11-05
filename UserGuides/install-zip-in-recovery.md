---
label: Install a .zip in Recovery
---
# Install a .zip file with Recovery

> **Android 16 Lineout.** These steps were written for **Bass: Lineout** (Lineage **23.2** / Android **16**).

Sometimes we send you a **.zip file**: an update, a fix, or an add-on. You can't open it like a
photo or a document. It has to be installed from **Recovery**, a small repair menu that starts
*instead of* Android.

It takes about 5 minutes. Installing a .zip this way does **not** erase your apps or files
(unless the instructions that came with the file say so).

Go slowly and do one step at a time. Each step shows what the screen should look like, so you can
check you're in the right place before you press anything.

## Before you start

You need:

- **The .zip file** (for example `bass-update.zip`). Write its name down: you'll look for it later.
- **A keyboard.** A USB keyboard, or the one built into your laptop. A Bluetooth keyboard will not
  work in Recovery, and the mouse and touchscreen may not work either.
- **Power.** Plug in the charger if your device has a battery.

Put the .zip file in one of these two places:

- **On the device itself (easiest).** Download it with the web browser on the device. It goes into
  the **Download** folder.
- **On a USB stick.** Copy it onto a USB stick with another computer, then plug the stick into the
  device.

## The only keys you need

| Key | What it does |
|---|---|
| **Down arrow** / **Up arrow** | Moves the highlight (the colored bar) down or up |
| **Enter** | Chooses the highlighted item |
| **Backspace** or **Esc** | Goes back one screen |

Nothing happens until you press **Enter**. If you highlight the wrong thing, just move again.

## Step 1: Start Recovery

1. Restart the device the normal way (hold the power button, then **Restart**).
2. Watch the screen. After a moment it turns black and shows a **short list of words**, with a
   countdown. This is the start menu. It looks something like this:

   ```
   BlissOS
   Recovery
   Advanced
   ```

   The first word may be different on your device. That's fine. You're looking for **Recovery**.
3. As soon as you see the list, press **Down arrow** once. This stops the countdown.
4. Move the highlight to **Recovery** and press **Enter**.

> **Android started instead?** You missed the list. That's very common. Restart again, and this
> time start tapping the **Down arrow** key as soon as the screen goes dark.

## Step 2: Choose "Apply update"

Recovery opens with a menu like this:

```
Reboot system now
Apply update
Factory reset
Advanced
```

Move the highlight to **Apply update** and press **Enter**.

> **Stay away from "Factory reset".** It erases everything on the device. You never need it to
> install a .zip.

## Step 3: Choose where the file is

The next menu asks where your .zip file is:

```
Apply from ADB
Choose from internal storage (/sdcard)
Choose from MY_USB_STICK
```

- If you downloaded the file **on the device**, choose **Choose from internal storage (/sdcard)**.
- If the file is on a **USB stick**, choose **Choose from** followed by the name of your stick.
  (Your stick's name will be different from `MY_USB_STICK`.)

Don't choose **Apply from ADB**. That one is for developers.

> **No "internal storage" line, or no USB stick line?** Some devices don't show internal storage
> here: put the .zip on a USB stick instead. If your stick isn't listed, unplug it, plug it back
> in, press **Backspace**, and choose **Apply update** again.

## Step 4: Find your file and choose it

Now you see the files and folders, like this:

```
Choose a package to install:
/sdcard
../
Alarms/
DCIM/
Download/
Music/
```

How to read this list:

- A name that **ends with `/`** is a **folder**. Highlight it and press **Enter** to open it.
- **`../`** at the top means **go back** to the folder before.
- Only **.zip files** and folders are shown. Inside a folder, the .zip files are listed first.

If you downloaded the file on the device, open **`Download/`**. You'll see something like:

```
Choose a package to install:
/sdcard/Download
../
bass-update.zip
```

Highlight **your file** (the name you wrote down) and press **Enter**.

## Step 5: Answer "Yes" to the warning

Recovery now shows a warning:

```
Signature verification failed
Install anyway?
 No
 Yes
```

This is **normal** for add-ons and fixes. It only means the file doesn't carry the special
signature Recovery looks for. (Some update files do carry it: then you won't see this question at
all and the install just starts.)

> **The highlight starts on "No".** Press **Down arrow** once so **Yes** is highlighted, then press
> **Enter**. If you press **Enter** right away, you've chosen **No** and nothing is installed: just
> go back to Step 2.

Only answer **Yes** for files you got from us or from someone you trust.

## Step 6: Wait

Lines of text appear while the file installs. **Don't turn the device off.** This usually takes
a minute or two.

It's finished when you see this line, and the Recovery menu from Step 2 comes back:

```
Install completed with status 0.
```

**Status 0 means it worked.** Any other number means it didn't (see
[If something goes wrong](#if-something-goes-wrong)).

## Step 7: Restart into Android

Highlight **Reboot system now** (the first line) and press **Enter**.

Android starts again. The first start after an install can take a little longer than usual.
That's normal.

**You're done.**

## If something goes wrong

| What happened | What to do |
|---|---|
| Android started instead of Recovery | Restart and start tapping **Down arrow** as soon as the screen goes dark (Step 1). |
| The keys don't do anything | Use a wired USB keyboard, or the laptop's own keyboard. Try another USB port. |
| I can't find my file | Make sure you chose the right place in Step 3. Open **`Download/`** for files downloaded on the device. The name must end with **.zip**. |
| There's no "internal storage" choice | Copy the .zip to a USB stick and choose the stick in Step 3. |
| I pressed Enter on the warning and nothing happened | **No** was highlighted. Go back to Step 2 and choose **Yes** this time. |
| The screen turned red and says **Installation aborted.** | The file didn't install. It may not be meant for this device, or the download may be broken. Choose **Reboot system now**, download the file again, and try once more. If it fails again, ask us for help and tell us the file's name. |
| It says **status** with a number that isn't 0 | Same as above. |
| The text stopped moving for a long time | Wait at least 10 minutes before you do anything. Installing can pause for a while. |

## The short version (for next time)

Restart → **Recovery** → **Apply update** → choose where the file is → open folders until you see
your **.zip** → **Enter** → **Down arrow** to **Yes** → **Enter** → wait for **status 0** →
**Reboot system now**.
