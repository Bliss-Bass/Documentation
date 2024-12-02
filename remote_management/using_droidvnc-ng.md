# Using DroidVNC-NG

(These instructions are based off the project readme found [here](https://github.com/bk138/droidVNC-NG))

Some Bass builds will come with droidVNC-NG as a VNC remote management solution that can work across the internet. 

## How to use

1. Launch the droidVNC-NG Admin Panel app.
2. Set a good password and consider turning the `Start on Boot` off.
3. Connect to your local Wi-Fi. For accepting a connection your device should be connected to some Local Area Network that you can control, normally it is a router. Connections via data networks (i.e. your mobile provider) are not supported.
4. Click `Start`
5. Set any permissions if requested
6. Connect to your device from a remote machine

### Keyboard Shortcuts From a VNC Viewer

* **Ctrl-Shift-Esc** triggers 'Recent Apps' overview
* **Home/Pos1** acts as Home button
* **End** acts as Power button
* **Escape** acts as Back button

### For accepting connections from outside

1. You should allow [Port Forwarding](https://en.wikipedia.org/wiki/Port_forwarding) in your router's Firewall settings. Login to your router's settings (usually open 192.168.1.1 in your browser, some routers have password written on them).
2. Find Port Forwarding, usually it's somewhere in **Network - Firewall - Port Forwards**.
3. Create a new rule, this is an example from OpenWRT firmware.
   
   Name: **VNC forwarding**
   
   Protocol: **TCP**
   
   Source zone: **wan** may be "internet", "modem", something that suggests the external source.
   
   External port: **5900** by default or whatever you specified in the app.
   
   Destination zone: **lan** something that suggests local network.
   
   Internal IP address: your device's local IP address, leaving **any** is less secure. The device's address may change over time! You can look it up in your routers' connected clients info.
   
   Internal port: same as external port.

4. Apply the settings, sometimes it requires rebooting a router.
5. Figure out your public address i.e. <https://www.hashemian.com/whoami/>.
6. Use this address and port from above to connect to your device.

### How to Pre-seed Preferences

DroidVNC-NG can read a JSON file with default settings that apply if settings were not changed
by the user. A file named `defaults.json` needs to created under
`<external files directory>/Android/data/net.christianbeier.droidvnc_ng/files/` where
depending on your device, `<external files directory>` is something like `/storage/emulated/0` if
the device shows two external storages or simply `/sdcard` if the device has one external storage.

An example `defaults.json` with completely new defaults (not all entries need to be provided) is:

```json
{
    "port": 5901,
    "portReverse": 5555,
    "portRepeater": 5556,
    "scaling": 0.7,
    "viewOnly": false,
    "showPointers": true,
    "fileTransfer": true,
    "password": "supersecure",
    "accessKey": "evenmoresecure",
    "startOnBoot": true,
    "startOnBootDelay": 0
}
```

### Remote Control via the Intent Interface

droidVNC-NG features a remote control interface by means of Intents. This allows starting the VNC
server from other apps or on certain events. It is designed to be working with automation apps
like [MacroDroid](https://www.macrodroid.com/), [Automate](https://llamalab.com/automate/) or
[Tasker](https://tasker.joaoapps.com/) as well as to be called from code.

You basically send an explicit Intent to `net.christianbeier.droidvnc_ng.MainService` with one of
the following Actions and associated Extras set:

* `net.christianbeier.droidvnc_ng.ACTION_START`: Starts the server.
  * `net.christianbeier.droidvnc_ng.EXTRA_ACCESS_KEY`: Required String Extra containing the remote control interface's access key. You can get/set this from the Admin Panel. 
  * `net.christianbeier.droidvnc_ng.EXTRA_REQUEST_ID`: Optional String Extra containing a unique id for this request. Used to identify the answer from the service.
  * `net.christianbeier.droidvnc_ng.EXTRA_PORT`: Optional Integer Extra setting the listening port. Set to `-1` to disable listening.
  * `net.christianbeier.droidvnc_ng.EXTRA_PASSWORD`: Optional String Extra containing VNC password.
  * `net.christianbeier.droidvnc_ng.EXTRA_SCALING`: Optional Float Extra between 0.0 and 1.0 describing the server-side framebuffer scaling.
  * `net.christianbeier.droidvnc_ng.EXTRA_VIEW_ONLY`:  Optional Boolean Extra toggling view-only mode.
  * `net.christianbeier.droidvnc_ng.EXTRA_SHOW_POINTERS`:  Optional Boolean Extra toggling per-client mouse pointers.
  * `net.christianbeier.droidvnc_ng.EXTRA_FILE_TRANSFER`: Optional Boolean Extra toggling the file transfer feature.
  * `net.christianbeier.droidvnc_ng.EXTRA_FALLBACK_SCREEN_CAPTURE`: Optional Boolean Extra indicating whether to start with fallback screen capture that does not need a
     user interaction to start but is slow and needs view-only to be off. Only applicable to Android 10 and newer.

* `net.christianbeier.droidvnc_ng.ACTION_CONNECT_REVERSE`: Make an outbound connection to a listening viewer.
  * `net.christianbeier.droidvnc_ng.EXTRA_ACCESS_KEY`: Required String Extra containing the remote control interface's access key. You can get/set this from the Admin Panel.
  * `net.christianbeier.droidvnc_ng.EXTRA_REQUEST_ID`: Optional String Extra containing a unique id for this request. Used to identify the answer from the service.
  * `net.christianbeier.droidvnc_ng.EXTRA_HOST`: Required String Extra setting the host to connect to.
  * `net.christianbeier.droidvnc_ng.EXTRA_PORT`: Optional Integer Extra setting the remote port.
  * `net.christianbeier.droidvnc_ng.EXTRA_RECONNECT_TRIES`: Optional Integer Extra setting the number of tries reconnecting a once established connection. Needs request id to be set.

* `net.christianbeier.droidvnc_ng.ACTION_CONNECT_REPEATER` Make an outbound connection to a repeater.
  * `net.christianbeier.droidvnc_ng.EXTRA_ACCESS_KEY`: Required String Extra containing the remote control interface's access key. You can get/set this from the Admin Panel.
  * `net.christianbeier.droidvnc_ng.EXTRA_REQUEST_ID`: Optional String Extra containing a unique id for this request. Used to identify the answer from the service.
  * `net.christianbeier.droidvnc_ng.EXTRA_HOST`: Required String Extra setting the host to connect to.
  * `net.christianbeier.droidvnc_ng.EXTRA_PORT`: Optional Integer Extra setting the remote port.
  * `net.christianbeier.droidvnc_ng.EXTRA_REPEATER_ID`: Required String Extra setting the ID on the repeater.
  * `net.christianbeier.droidvnc_ng.EXTRA_RECONNECT_TRIES`: Optional Integer Extra setting the number of tries reconnecting a once established connection. Needs request id to be set.

* `net.christianbeier.droidvnc_ng.ACTION_STOP`: Stops the server.
  * `net.christianbeier.droidvnc_ng.EXTRA_ACCESS_KEY`: Required String Extra containing the remote control interface's access key. You can get/set this from the Admin Panel.
  * `net.christianbeier.droidvnc_ng.EXTRA_REQUEST_ID`: Optional String Extra containing a unique id for this request. Used to identify the answer from the service.

The service answers with a Broadcast Intent with its Action mirroring your request:

* Action: one of the above Actions you requested
  * `net.christianbeier.droidvnc_ng.EXTRA_REQUEST_ID`: The request id this answer is for.
  * `net.christianbeier.droidvnc_ng.EXTRA_REQUEST_SUCCESS`: Boolean Extra describing the outcome of the request.

There is one special case where the service sends a Broadcast Intent with action
`net.christianbeier.droidvnc_ng.ACTION_STOP` without any extras: that is when it is stopped by the
system.

#### Examples

##### Start a password-protected view-only server on port 5901

Using `adb shell am` syntax:

```shell
adb shell am start-foreground-service \
 -n net.christianbeier.droidvnc_ng/.MainService \
 -a net.christianbeier.droidvnc_ng.ACTION_START \
 --es net.christianbeier.droidvnc_ng.EXTRA_ACCESS_KEY de32550a6efb43f8a5d145e6c07b2cde \
 --es net.christianbeier.droidvnc_ng.EXTRA_REQUEST_ID abc123 \
 --ei net.christianbeier.droidvnc_ng.EXTRA_PORT 5901 \
 --es net.christianbeier.droidvnc_ng.EXTRA_PASSWORD supersecure \
 --ez net.christianbeier.droidvnc_ng.EXTRA_VIEW_ONLY true
```

##### Start a server with defaults from Tasker

- Tasker action-category in menu is System -> Send Intent
- In there:
  - Action `net.christianbeier.droidvnc_ng.ACTION_START`
  - Extra `net.christianbeier.droidvnc_ng.EXTRA_ACCESS_KEY:<your api key from DroidVNC-NG start screen>`
  - Package `net.christianbeier.droidvnc_ng`
  - Class `net.christianbeier.droidvnc_ng.MainService`
  - Target: Service

##### Start a server with defaults from a Kotlin app

- For apps targeting API level 30+, you'll need to specify that your app is able to see/use
  droidVNC-NG. You do this by adding the following snippet to your AndroidManifest.xml, right under 
  the `<manifest>` namepace:
```xml
<queries>
    <package android:name="net.christianbeier.droidvnc_ng" />
</queries>
```

- In your Kotlin code, it's then:
```kotlin
val intent = Intent()
intent.setComponent(ComponentName("net.christianbeier.droidvnc_ng", "net.christianbeier.droidvnc_ng.MainService"))
intent.setAction("net.christianbeier.droidvnc_ng.ACTION_START")
intent.putExtra("net.christianbeier.droidvnc_ng.EXTRA_ACCESS_KEY", "<your api key from DroidVNC-NG start screen>")
startForegroundService(intent)
```

##### Make an outbound connection to a listening viewer from the running server

For example from Java code:

See [MainActivity.java](https://github.com/bk138/droidVNC-NG/blob/master/app/src/main/java/net/christianbeier/droidvnc_ng/MainActivity.java).

##### Stop the server again

Using `adb shell am` syntax again:

```shell
adb shell am start-foreground-service \
 -n net.christianbeier.droidvnc_ng/.MainService \
 -a net.christianbeier.droidvnc_ng.ACTION_STOP \
 --es net.christianbeier.droidvnc_ng.EXTRA_ACCESS_KEY de32550a6efb43f8a5d145e6c07b2cde \
 --es net.christianbeier.droidvnc_ng.EXTRA_REQUEST_ID def456
```
