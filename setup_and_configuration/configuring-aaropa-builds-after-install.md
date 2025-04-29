# Configuring Aaropa builds after install

When you install one of our Aaropa based builds, the Linux GUI based installer allows you to configure many of the properties in the build on install like codecs, audio HAL, bluetooth HAL, and more. 

But once installed, there is not obvious way to update the boot configuration from the Android UI. That is where this document comes in.

## Updating the boot configuration

Updating the boot configuration of the build can be done in a couple different ways:

1. Using the Bliss Boot Config editor to update the boot configuration. 
2. Using KernelSU and Termux with Nano or Vi editor to update the boot configuration. 
3. Using DEBUG mode terminal and Vi editor to update the boot configuration.

### Using the Bliss Boot Config editor

If your Bass OS build includes the Boot Config editor then this will be the easiest way to update/edit the boot config after install. You will be able to find the Bliss Boot Config editor UI from `Settings > System > Boot Options`. From there, the initial UI will display the currently in-use options found in the kernel cmdline. 

To explore the other options, the sidepanel displays icons for Slot and Other available options. 

### Using KernelSU and Termux with Nano or Vi editor

To update the boot configuration using KernelSU and Termux with Nano or Vi editor, follow these steps:

1. Launch KernelSU app and tap the shield at the bottom of the app view. 
2. Tap on the Termux icon, and enable root for the Termux app. 
3. Close the KernelSU app.
4. Launch the Termux app and type the following command:

```
/system/bin/su
nano /boot/grub/android.cfg
```

5. Edit the boot configuration using the Nano or Vi editor. 
6. Save the boot configuration and exit the editor.
7. Reboot the device.

### Using DEBUG mode terminal and Vi editor

To update the boot configuration using DEBUG mode terminal and Vi editor, follow these steps:

1. Boot into the device using the Debug mode boot option or by adding `DEBUG=1` to the boot command through Grub's editor ('e' key). 
2. at the first command prompt, type the following command:

```
vi /boot/grub/android.cfg
```

3. Edit the boot configuration using the Vi editor by tapping Insert, typing your changes, and then tapping Escape followed by :wq to save the changes and exit the editor.
4. Reboot the device.

That's it! You should now understand how to update the boot configuration of the build after install.
