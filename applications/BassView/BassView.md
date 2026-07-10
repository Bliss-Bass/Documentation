# BassView

BassView (BlissView) is a privileged system service used on Bass builds for platform integrity checks, EULA acceptance, and optional device analytics.

| | |
|---|---|
| **Role** | Anti-tamper validation, EULA gate, analytics client |
| **Build** | Included via the BassView / BlissView product makefile |

## What it does

* Checks the platform signing key (SHA-256) against a hash baked in at build time
* Blocks or flags unexpected unpack/repack or signing changes
* Requires EULA acceptance before related services / analytics run
* Can report non-personal build info (CPU arch, Build ID, and similar) for usage tracking

This is not an end-user settings app. Most of the time you only notice it during first boot (EULA) or if a build fails integrity checks.

## Related

* [License Activation](../../setup_and_configuration/license-activation.md)
* [BootSight](../BootSight/BootSight.md)
* Legal pages under [Legal](../../README.md#legal)
