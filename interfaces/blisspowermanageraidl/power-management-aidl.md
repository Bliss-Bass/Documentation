# Power Management API (legacy)

> **Lineout note:** New builds should use **[Ax86 Power](../../applications/Ax86Power/Ax86Power.md)** (`IAx86Power`) for reboot / shutdown / sleep **and** sleep/wake policy. This page documents the older BlissPowerManager AIDL still referenced by some apps and samples.

We include a simple app to demonstrate the (legacy) power management API.

## Bliss Power Management AIDL Interface:

```
package org.blissos.powermanagerclient;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import org.blissos.powermanager.BlissPowerManager;

public class MainActivity extends AppCompatActivity {

   @Override
   protected void onCreate(Bundle savedInstanceState) {
       super.onCreate(savedInstanceState);
       setContentView(R.layout.activity_main);

       Button rebootBtn = findViewById(R.id.rebootBtn);
       Button shutdownBtn = findViewById(R.id.shutdownBtn);
       Button sleepBtn = findViewById(R.id.sleepBtn);

       BlissPowerManager blissPowerManager = BlissPowerManager.getInstance(this);

       rebootBtn.setOnClickListener(v -> blissPowerManager.reboot());
       shutdownBtn.setOnClickListener(v -> blissPowerManager.shutdown());
       sleepBtn.setOnClickListener(v -> blissPowerManager.sleep());
   }
}
```

1) copy paste “**system_libs/bliss-power-framework.jar**” from sample app 

2) gradle:

```
implementation fileTree(dir: 'system_libs/', include: ['*.jar'])
```

3) java:

```
import org.blissos.powermanager.BlissPowerManager;

BlissPowerManager blissPowerManager = BlissPowerManager.getInstance(this);
blissPowerManager.reboot()
blissPowerManager.shutdown()
blissPowerManager.sleep()
```

##### ADB Interface:

```
adb shell service call blisspower <parameters>
```

**&lt;parameters>** is the method number in aidl 

1: reboot 

2: shutdown 

3: sleep
