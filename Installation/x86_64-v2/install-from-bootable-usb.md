---
description: Install from bootable USB Installer
---

# Install From Bootable USB

## Manual Install Bass OS

##### Install Steps:

{% hint style="info" %}
WARNING THIS WILL DELETE ANY DATA ON THE DRIVE
{% endhint %}

We will want to start by booting into the installer by selecting the top Install option from Grub

From here we will want to change the drive partition scheme to be A) EFI (VFAT) B) Android (ext4). This means that we need to delete all partitions except for the top EFI partition, and create a single new partition with the remaining space.  You will need to start by selecting "Create/Modify partitions", then remove all partitions on the device. ![Partitioning p1](../../.gitbook/assets/uefi-create.png)

In the next screen, we need to make **two** partitions for this to work, as Bliss needs to install a bootloader to boot to. If you have a pre-existing install of linux, this step may be unnecessary.

First create the EFI partition, this is the partition that is used to install the bootloader. 

1. Create a [ new ] partition
2. Leave First Sector default (Just press enter)
3. For "Size in Sectors" all we need to do is enter `+512M`
4. Set type as ef00 (or EFI)
5. We don't necessairly need to name this partition, but it is best practice to name it `EFI`

![Partitioning p2](../../.gitbook/assets/uefi-android.png)

Next we need to make the second partition, this is the partition that the bulk of android will be installed to.

1. Press down until the largest chunk of free space is slected, and click [ NEW ]
2. We can leave everything default. Although a name is not necesary we can call it ANDROID.
3. Lastly we click [ WRITE ] and [ QUIT ] 

![Partitioned](../../.gitbook/assets/uefi-partitioned.png)

Now that we have the drives partitioned, we can start to install android. Select the ANDROID partition that we have made before, and format it as ext4. This is the recomended format unless windows compatibility is needed, in that case select NTFS, and click < Yes > on the next screen.

![Format Drive p1](../../.gitbook/assets/uefi-ext4.png)
![Format Drive p2](../../.gitbook/assets/uefi-risks.png)

The installer will procede to format and install android, you will then be prompted to install EFI GRUB2. We need to accept that, unless you have a pre-existing grub or other bootloader install.

![Install Grub](../../.gitbook/assets/uefi-grub.png)

The installer will begin to write the changes to the disk. This will take some time. Go grab another coffee!

![Grab a coffee](../../.gitbook/assets/grab-a-coffee.png)

After this step, it will also prepare the install for A/B updates. This process will take a couple minutes at most. 

Congratulations! You should now have a functional UEFI-boot with Bass OS!

## Using OEM Install (EFI)

**WARNING THIS WILL DELETE ANY DATA ON THE DRIVE**

To start with we will boot into the installer and select OEM installer. 

<img width="1920" height="1080" alt="Step1" src="https://github.com/user-attachments/assets/255b0ac0-7101-4cf9-be8f-724623c3361d" />

We will then look for "BassOS_KIOSK [ Build Date ] Force EFI OEM Install to detected harddisk" and select it.

<img width="1920" height="1080" alt="Step2" src="https://github.com/user-attachments/assets/5d700e24-8336-4bdc-af17-bf92e1de7b38" />

The installer will then format the disk to prepare it for installation.

<img width="1920" height="1080" alt="Step3" src="https://github.com/user-attachments/assets/01d7fee1-5439-4d5e-8f2e-1f07fc4a8f06" />

At this point it will run a filesystem check to verify the formatting was done correctly.

<img width="1920" height="1080" alt="Step4" src="https://github.com/user-attachments/assets/257cbce3-5cb8-429d-94e4-5c59e4f70498" />

Installing (This takes the longest)

<img width="1920" height="1080" alt="Step5" src="https://github.com/user-attachments/assets/cd1dc249-2e69-4669-b030-4c8354e1ca50" />

Preparing a seprate partition for updates (A/B partitions)

<img width="1920" height="1080" alt="Step6" src="https://github.com/user-attachments/assets/6e7f785a-a647-4f18-9ad3-6b0f2b215119" />

Now it will reboot and we can unplug the USB drive.

<img width="1920" height="1080" alt="Step7" src="https://github.com/user-attachments/assets/93690acf-d224-4c99-9079-4a659c94bd34" />
