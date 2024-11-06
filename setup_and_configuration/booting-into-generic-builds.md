## Booting into generic builds:

### Tablet/PC/IOT/IIOT/Game Mode builds

**!!WARNING!! - THESE BUILDS ARE MEANT TO REPLACE YOUR EXISTING OPERATING SYSTEM OR BE INSTALLED ON NEW HARDWARE. THESE ARE NOT INTENDED FOR DUAL-BOOTING**

**!!Notice!!**: These builds come with A/B OTA Update support, and might not work in Live mode. Only supported installer is the Bootable USB install method we include in the .iso.

##### Booting into the OS

(**!!NOTICE FOR BUILDS THAT HIDE GRUB!!**) When the device reboots, it will not show the grub menu by default, and automatically boot into the last known boot mode. In order to show the grub menu, tap shift multiple times while the initial BIOS boot logo is displayed. If done correctly, you will be presented with the Grub menu. If no keys are pressed, the bios boot menu will show a black screen afterwards while Grub is loading the configuration in the background.

Once the device boots into Grub, the top option or two will be our default mode (some builds offer specific boot options per CPU manufacturer: **Intel Default** or **AMD Default**) boot options.

While the Debugging modes can be found in the **Other Options** section of the boot menu. 

#### Setup Steps for Ad/Signage Builds

(This section only applies to our Ad/Signage builds using Garlic Launcher)

##### Initial Setup

Go through the builds SetupWizard and connect to a network. Then once complete, the Garlic-Launcher should load. Launch the Player from Garlic-Launcher and grant the permissions it requests. Swipe down and hit the power button or use ctrl-alt-del to reboot the device now. 

##### SMIL Control setup

(You will need to have created an account on https://admin.smil-control.com and be logged in)

After the device reboots, you should see a SMIL Control screen with a code on it. 

Access the https://admin.smil-control.com website and going to Player > Transfer, and enter the code from the device in there. Once registered, your device will show on the Players default screen. You can then setup a playlist and other options from the SMIL Control web UI. 

##### !! Playback Notice !!

Sometimes the playlist will show a black screen when starting. In the event this happens, we suggest sending the player commands from SMIL COntrol site to reboot and clear video & web cache. This may need you to reboot the device or wait till the next update period is sent from SMIL Control. 
