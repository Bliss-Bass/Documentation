# Bass OS (Android 13-15) Install Process

This document will go over how to use our Devuan GNU-Linux based installer (aka: Aaropa initrd/installer). This is quite the departure from our normal install process using the Legacy Dialog based installer and allows a more fine tuned and catered install experience, as well as compatibility with a number of additional features. 

## Requirements:

- x86_64-v2 device
- 8+ GB USB drive
- BalenaEtcher (to flash the USB)

## Process:

Download the latest Bass OS Android 13/14/15 iso image, and use BalenaEtcher to flash the iso onto the USB drive. 
Once complete, plug in the USB drive and reboot the target device to the BIOS, and disable secure-boot and TPM, along with decrypting the target drive if needed. 
Then make sure that you allow the USB boot option to be selected in the boot menu, and reboot to that, selecting the USB drive. 

### Booting to USB

This should boot to Grub, where you select the Install BassOS* option. After that boots, you should see a simple Linux environment with the installer auto-launching. If it does not, there should be an icon on the desktop to start the BassOS Installer. 

### Selecting storage device

Select the Next button on the installer to continue. Then select your storage device scheme. We suggest using the entire drive here. 

### Selecting OS Options

This next screen will be a series of options and checkboxes. These represent all the dynamic options that Bliss Os and Bass OS come with. 

(**!!WARNING!! DO NOT SELECT ALL OPTIONS, THIS WILL BREAK THE INSTALLATION**)

For most devices, we suggest using the following options:

- Media Codecs > FFMPEG Codecs > Set FFMPEG Codec2 as default
- Audio > Set default Audio HAL to x86
- Bluetooth > Use btlinux Bluetooth HAL instead

Bass OS Options (all options underneath "miscellaneous") at the bottom will also have all the added features and configs available in Bass OS. To test initial compatibility, we suggest installing with a bare minimum set of options and then testing through Grub for target use-cases. Once the required options are defined through testing, you can reinstall with the required options.

After selecting your options, click Next, and then confirm the settings by clicking Install. Once complete, you will be prompted to reboot the device. Please also remove the USB at this point. 

### Booting into Bass OS

The initial boot option presented from Grub will contain all the boot options you have configured in the installer. Bass OS also includes a few of the default collections for boot modes into the grub boot menu. Those can act as a resource for testing the combinations of boot mode options. The boot mode collections are as follows:

- Bass boot options:
    - Tablet UI: various display and input options for the standard Android UI
    - Hybrid-Desktop UI: various display and input options for the a hybrid desktop/Android tablet UI
    - Desktop UI: various display and input options for the a multiwindow based desktop/Android tablet UI
    - Kiosk: Kiosk mode boot options (requires a Restricted Launcher or Kiosk Launcher based iso)
        - Lockdown: various display and input options. Locked down all Android options based on Restricted Launcher or Kiosk Launcher setup
        - Admin: various display and input options. All lockdown features are unlocked and available

**!!NOTICE!! Not all Bass boot options will work on all versions of Android. For example, Mouse Presentation features only work on Android 12L**

You can select any of the options you would like to boot into or look at the boot options used by tapping 'e'.

Once a boot option is selected. the system will start the init process, followed by a boot animation becoming visible. Afterwards, it should lead to the Android UI showing a lockscreen or the Setup Wizard. Use the mouse or touch to swipe up, or hit the space key on the keyboard to unlock the device. 

If the device goes to sleep on the lockscreen, it can be woken by using space, mouseclick, or power button click.

### Adjusting Boot Options After Install

Bass OS - All In One builds include a way to edit the boot options after install. Once the OS is setup, you can view/edit the current boot options by going to Settings > System > Boot Options, and seeing the used cmdline options on the first page. The tabs on the side panel will also allow you to select the other options that are available 

**Please Note:** Not all options will work across all versions of Bass OS. Please see the command line documentation for specific versions supported by your target option.

