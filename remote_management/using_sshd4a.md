# Using Sshd4a

(These instructions are based off the project wiki found [here](https://github.com/tfonteyn/Sshd4a/wiki))

Some Bass builds will come with Sshd4a to provide a sshd server for remote shell access, rsync and scp/sftp services. 

## Startup options.

The Settings screen provides the following switches:

1. Start the service when your device is booted.
2. Start the service when this app is launched.
3. Allow starting the service by an external Intent.

   When enabled, the below Intents can be used to start/stop the service. There is no additional security; any app can send these intents when the option is enabled.

   Make sure options (1) and (2) above are both switched **OFF**
          
        am start -a com.hardbacknutter.sshd.fg.START

        am start -a com.hardbacknutter.sshd.fg.STOP

4. Foreground Service.

   The service will keep running even when this app is in the background. This is essential for using option (1) and very useful when using options (2) or (3).

Note it is the users (your) responsibility to set the desired combination of the above switches.

## Authentication methods.

The Settings screen provides individual switches to enable/disable all 3 methods.

### Public key authentication

This is the preferred (at least it is mine) method for giving access. Use the option menu to import a prepared "authorized_keys" file.
You can also add/edit the "authorized_keys" file directly (be careful!). Its location is

    /data/data/com.hardbacknutter.sshd/files/.dropbear/

The "/data/data" prefix **might** be different depending on device vendor, but the "files" directory is the default home directory if you login over ssh.

### Single-use password

An alternative authentication method which will print a single-user 8 character password in the log on screen. The user name is irrelevant. You will obviously need access to the device screen to see the required password.

### User and password

The password is stored as an SHA-512 (and base64) hash only. There is no "reverse-engineering" possible to retrieve the password you set.
On the other hand, anyone who can login to the SSH shell, can simply remove the password so it should **NOT** be seen as super-secure. The main/only reason for it's existence is for users who don't want to set-up public key access ("authorized_keys")
