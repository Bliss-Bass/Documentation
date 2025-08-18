# How to edit grub from your Bass OS install

Follow these steps to edit EFI from rooted Bass OS

### Step 1:
Boot into Bass OS and select "DEBUG mode" from the grub menu. Once boot completes, press enter

### Step 2:
To list devices:
  
  `blkid`

The EFI partition will be the one that is formatted as VFAT
  
if you have nvme disk your EFI partition should be like this:

/dev/nvme0n1p1

You must use this partition for bottom commands.

Mount your EFI partition (usually first partition in disk):

  `mount /dev/sda1 /mnt`

### Step 3:
Change directory to /mnt/efi/boot:

  `cd /mnt/efi/boot`

### Step 4:
Edit the android.cfg using vi editor (nano editor may also be used):

  `vi android.cfg`

### Step 5:
Use Vi Editor to add your changes and save 
-  Press `insert` to enter edit mode
-  Press `Esc`, type `:w`, and press `Enter` to save.
-  Press `Esc`, type `:q`, and press `Enter` to exit.
- Also you can combine save & exit with `:wq`

### Step 6:
Now you can umount efi partition and reboot to see your changes:
```
  umount /dev/sda1
  reboot -f
```
