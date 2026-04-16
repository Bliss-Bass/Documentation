# Using ScreenView
ScreenView is used to view and control the primary screen from an external display. 
To use it, open the app on an external display.

### Remote Control via the Intent Interface

ScreenView features a remote configuration interface by means of Intents. This allows changing some settings from other apps or ADB.  
- Enable/Disable Input:
With ADB:
```
adb shell am start \
  -n com.example.screenoverlay/.MainActivity \
  --es pref_key "use_input" \
  --ez pref_value <true or false>
 ```
Or programatically:
```
val intent = Intent().apply {
    component = ComponentName("com.example.screenoverlay", "com.example.screenoverlay.MainActivity")
    putExtra("pref_key", "use_input")
    putExtra("pref_value", true)
    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)  // required if outside an Activity
}

context.startActivity(intent)
```
