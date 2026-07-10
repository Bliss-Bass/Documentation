# Fleet Management

Bass builds declare how the device is managed with a single read-only property:

```text
ro.bass.fleet_mgmt
```

| Value | Meaning |
|-------|---------|
| `bootsight` | BootSight is included and is the fleet / license component |
| `mdm` | A third-party MDM is expected; BootSight is not included |
| `none` | No fleet component (default when neither flag is set) |

## Build flags

| Flag | Result |
|------|--------|
| `--bootsight` | Includes BootSight and sets `ro.bass.fleet_mgmt=bootsight` |
| `--fleet-mgmt=mdm` | Sets `ro.bass.fleet_mgmt=mdm` without BootSight |
| `--fleet-mgmt=none` | Sets `ro.bass.fleet_mgmt=none` without BootSight |

Do not combine `--bootsight` with `--fleet-mgmt=mdm`. Use `--bootsight` when you want BootSight; use `--fleet-mgmt` when you want a policy without BootSight.

Examples:

```bash
./build.sh --bootsight --bsbanner ...
./build.sh --fleet-mgmt=mdm ...
```

## Check on a device

```bash
adb shell getprop ro.bass.fleet_mgmt
```

## BootSight-only behavior

BootSight init and the bassboot watchdog only run when the property is `bootsight`. On `mdm` or `none` builds those scripts exit early.

More detail: [BootSight](../applications/BootSight/BootSight.md) and [License Activation](../setup_and_configuration/license-activation.md).
