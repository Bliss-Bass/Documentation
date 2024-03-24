## Booting into lockdown builds:

#### Restricted Launcher & POS Builds

**!!WARNING!! - THESE BUILDS ARE MEANT TO REPLACE YOUR EXISTING OPERATING SYSTEM OR BE INSTALLED ON NEW HARDWARE. THESE ARE NOT INTENDED FOR DUAL-BOOTING**

**!!Notice!!**: These builds come with A/B OTA Update support, and might not work in Live mode. Only supported installer is the Bootable USB install method we include in the .iso.

##### Booting into the OS

(**!!NOTICE FOR BUILDS THAT HIDE GRUB!!**) When the device reboots, it will not show the grub menu by default, and automatically boot into the last known boot mode. In order to show the grub menu, tap shift multiple times while the initial BIOS boot logo is displayed. If done correctly, you will be presented with the Grub menu. If no keys are pressed, the bios boot menu will show a black screen afterwards while Grub is loading the configuration in the background.

(**!!PLEASE NOTE!!**): Only Admin mode will have access to the Android notification stack, navigation options, status bar, etc. In some builds, lockdown mode removes all these functions at the system level for redundancy and added security.
The options used to configure those restrictions can be overridden with the following options:

 - Navigation: 
	Disables the system navigation gestures
    options: true, false
    
    ```FORCE_DISABLE_NAVIGATION=*```

 - Navigation Gesture Handle:
	Disables the gestural navigation handle
    options: true, false
    
    ```FORCE_DISABLE_NAV_HANDLE=*```

 - Navigation Taskbar (only on large-screen devices):
    Disables SystemUI Taskbar (not Launcher3)
    options: true, false
    
    ```FORCE_DISABLE_NAV_TASKBAR=*```

 - Statusbar:
	Disabled the statusbar at the top of the screen (does not disable Launcher3s gesture to show notification drawer)
    options: true, false
    
    ```FORCE_DISABLE_STATUSBAR=*```

#### Restricted Launcher Setup

(**!!NOTICE FOR INITIAL SETUP!!**) We recommend disconnecting all but the primary display when starting up the OS. Once setup is complete, you can connect any displays and continue testing and operation.

Once the device boots into Grub, the top option or two will be our locked down mode (**Intel Default** or **AMD Default**)

While the Admin modes can be found in the **Other Options** section of the boot menu. 

The **Restricted Launcher & POS builds** will initially require setup through Admin mode. So after install, you will want to reboot, the tap the shift key until the Grub menu shows. From there, select **Other Options** > and select one of the Admin options from there. 

Once booted, you should setup the devices wifi/network. Afterwards, you will want to tap on the Sprocket icon at the top right, and navigate to the Security tab, and tap on **Change Password**. 

After setting the admin password, we can select the default features we want available in Lockdown mode, and navigate back to the Restricted Launcher page, and configure your Appearance, Apps and System options. 

**Appearance**: Allows you to set the default positions/placement of the on-screen logo overlay and settings button overlay

**Apps**: Allows you to set your whitelisted apps up, you can also set what whitelisted apps you want to auto-launch per-display. 

**System**: Allows you to change options for default screen timeout and on-screen keyboard display

Once setup is complete, we can then back out and test our lockdown settings by hitting the Lock icon at the top right of the home screen, or reboot the device, and select the top boot option (some builds offer specific boot options per CPU manufacturer: **Intel Default** or **AMD Default**) to enter Lockdown mode. 

#### Kiosk Launcher Setup

By default, the Bliss Kiosk Launcher UI will have two modes, Lockdown and Admin modes. 

To configure the launcher, we want to start off by booting onto Admin mode. Then we cna start the Kiosk Launcher and configure it from there. The default password for the kiosk launcher settings is `123`. 

Please see [BlissKioskLauncher](../applications/BlissKioskLauncher/BlissKioskLauncher.md) for further details on the launchers usage.



