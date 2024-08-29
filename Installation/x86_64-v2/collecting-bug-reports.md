## Collecting Bug Reports

This process is mostly the same as Android-x86 builds, but with a few additions that help things along. 
If you need to collect logs in order to submit a bug report, then the first thing you will want to do is reboot your Bass OS install using debug mode. We do this through Grub with the command:
```
DEBUG=2 
```
Once your device starts to boot, you will be presented with a root console, just before the Android systems init process starts. 
From here, you can use root commands to remount as read/write, or do basic filesystem and kernel debugging. 
In order to proceed to Android, you will need to type 'exit' followed by Return twice in the console, and the system will continue to boot. 

While in debug mode, there are logs found in both /tmp/log for early boot, as well as /data/log for Android boot. You will need those logs to submit a bug report.
