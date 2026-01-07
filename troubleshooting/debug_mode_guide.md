# Debug Mode Guide for Bliss OS/Bass OS

Bliss OS/Bass OS provides two debug modes: `DEBUG=1` and `DEBUG=2`. These modes offer different features and troubleshooting steps to help you debug a device that is not booting correctly. 

## `DEBUG=1`

When you set `DEBUG=1`, the following features are enabled:

- Detailed boot logs: This mode provides verbose boot logs that can help you identify any issues during the boot process.
- Serial console access: You can access the serial console to view and interact with the boot process.
- Debug kernel messages: This mode displays debug kernel messages that can provide insights into any kernel-related issues.

(Please note that you will have to enter 'exit' once from this debugging console to continue booting the OS)

To enable `DEBUG=1`, follow these steps:

1. Boot your device into the bootloader.
2. Press the appropriate key to access the bootloader menu (usually F2 or Esc).
3. Navigate to the "Debug" or "Advanced" menu.
4. Highlight the "Debug" option.
5. Tap 'e' to edit the boot option.
6. Set the `DEBUG` option to `1`.
7. Tap 'F10' to save the changes and boot the option.
8. The device will now boot into debug mode.

## `DEBUG=2`

When you set `DEBUG=2`, the following features are enabled:

- Detailed boot logs: This mode provides verbose boot logs that can help you identify any issues during the boot process.
- Serial console access: You can access the serial console to view and interact with the boot process.
- Debug kernel messages: This mode displays debug kernel messages that can provide insights into any kernel-related issues.
- Additional troubleshooting options: `DEBUG=2` drops you to console before the initial init layer starts. This allows you to modify boot parameters, access low-level system information, and perform other advanced troubleshooting tasks. 

(Please note that you will have to enter 'exit' twice from this debugging console to continue booting the OS)

To enable `DEBUG=2`, follow these steps:

1. Boot your device into the bootloader.
2. Press the appropriate key to access the bootloader menu (usually F2 or Esc).
3. Navigate to the "Debug" or "Advanced" menu.
4. Tap 'e' to edit the boot option.
5. Set the `DEBUG` option to `2`.
6. Tap 'F10' to save the changes and boot the option.
7. The device will now boot into debug mode.

## Troubleshooting Steps

Here are some common troubleshooting steps you can follow in debug mode:

1. Check the boot logs: Review the detailed boot logs to identify any errors or issues that may be causing the device to fail to boot. This command opens the boot log file in Vim for editing:

    ```
    vi /tmp/log
    ```

2. Access the serial console: Use the serial console to interact with the boot process and gather more information about the issue.
3. Check kernel messages: Review the debug kernel messages to identify any kernel-related issues.

    ```
    dmesg > /tmp/dmesg.log
    ```
    Then read it using Vim. 

    ```
    vi /tmp/dmesg.log
    ```

4. Change boot parameters: In `DEBUG=2` mode, you can modify boot parameters to troubleshoot specific issues.
5. Access low-level system information: In `DEBUG=2` mode, you can access low-level system information to diagnose hardware-related issues.


## Collecting the Boot Log from `/tmp/log` to an External USB Drive

1. Boot your device into debug mode (`DEBUG=1` or `DEBUG=2`).
2. Connect an external USB drive to your device.
3. Mount the USB drive to a directory on your device. For example, you can use the following command to mount the USB drive to `/mnt`:

   ```
   sudo mount /dev/sdX /mnt
   ```

   Replace `/dev/sdX` with the actual device name of your USB drive.

4. Copy the boot log from `/tmp/log` to the USB drive. You can use the following command to copy the file:

   ```
   sudo cp /tmp/log /mnt/boot_log.txt
   ```

   This command copies the contents of `/tmp/log` to the `/mnt/boot_log.txt` file on the USB drive.

5. Unmount the USB drive when you're done:

   ```
   sudo umount /mnt
   ```

   This command safely unmounts the USB drive from your device.

Now you have the boot log saved to the external USB drive for further analysis.

## Collecting `dmesg` Output to an External USB Drive

1. Boot your device into debug mode (`DEBUG=1` or `DEBUG=2`).
2. Connect an external USB drive to your device.
3. Mount the USB drive to a directory on your device. For example, you can use the following command to mount the USB drive to `/mnt`:

   ```
   sudo mount /dev/sdX /mnt
   ```

   Replace `/dev/sdX` with the actual device name of your USB drive.

4. Run the `dmesg` command to collect the kernel messages:

   ```
   sudo dmesg > /mnt/dmesg.txt
   ```

   This command redirects the output of `dmesg` to the `/mnt/dmesg.txt` file on the USB drive.

5. Unmount the USB drive when you're done:

   ```
   sudo umount /mnt
   ```

   This command safely unmounts the USB drive from your device.

Now you have the `dmesg` output saved to the external USB drive for further analysis.

Remember to consult the official documentation for Bliss OS/Bass OS for more detailed information on using the debug modes and troubleshooting specific issues.

## Navigating Saved Logs with Vim

Once you have saved the boot log or `dmesg` output to an external USB drive, you can use Vim to navigate and analyze the logs. Here are some common Vim commands to help you navigate the saved logs:

- `j`: Move down one line.
- `k`: Move up one line.
- `Ctrl + d`: Scroll down half a screen.
- `Ctrl + u`: Scroll up half a screen.
- `gg`: Move to the beginning of the file.
- `G`: Move to the end of the file.
- `i`: Enter insert mode at the beginning of a line.
- `a`: Enter insert mode at the end of a line.
- `Esc`: Exit insert mode.
- `yy`: Copy current line.
- `p`: Paste after the cursor.
- `P`: Paste before the cursor.
- `:w`: Save the file.
- `:q`: Quit the file.
- `:q!`: Quit the file without saving.
- `:wq`: Save the file and quit.

These commands should help you navigate and analyze the saved logs using Vim. Remember to consult the Vim documentation for more advanced commands and features.

## Debugging with a Live Linux (Ubuntu) USB

If you have access to a Live Linux (Ubuntu) USB, you can use it to debug your Bliss OS/Bass OS device. Here's how you can do it:

1. Boot your device into debug mode (`DEBUG=1` or `DEBUG=2`).
2. Type `'exit'` to continue booting the device.
3. Boot until the device hangs or encounters an issue.
4. Power off the device.
5. Boot into the Live Linux (Ubuntu) USB. Make sure it supports the architecture of your device (e.g., 32-bit or 64-bit).
6. Once the Live Linux (Ubuntu) USB is booted, connect it to your device using a USB cable.
7. Open a terminal on the Live Linux (Ubuntu) USB.
8. Run the following command to mount the drive of your Bliss OS/Bass OS device:

   ```
   sudo mount /dev/sdX /mnt
   ```

   Replace `/dev/sdX` with the actual device name of your Bliss OS/Bass OS device.

9. Navigate to the mounted drive using the `cd` command. For example:

   ```
   cd /mnt
   ```

10. Find the `/tmp/log` file on the mounted drive. You can use the `ls` command to list the files and directories. For example:

    ```
    ls
    ```

11. Copy the `/tmp/log` file from the mounted drive to the Live Linux (Ubuntu) USB. You can use the `cp` command to copy the file. For example:

    ```
    sudo cp /mnt/tmp/log /path/to/destination/on/the/Live/Linux/USB/log.txt
    ```

    Replace `/path/to/destination/on/the/Live/Linux/USB` with the actual path where you want to save the file on the Live Linux (Ubuntu) USB.

12. Unmount the drive when you're done:

    ```
    sudo umount /mnt
    ```

13. Now you can use the Live Linux (Ubuntu) USB to analyze the copied log file using tools like Vim, grep, or any other text editors or utilities available on the Live Linux (Ubuntu) USB.
