# Ax86Docs (on-device documentation)

Ax86Docs is the offline documentation app shipped on Bass: Lineout builds that include `--extras`. It opens a WebView and renders markdown bundled into the image at build time.

| | |
|---|---|
| **Package** | `com.navotpala.ax86docs` |
| **Build** | Included with `--extras` |
| **Default doc** | `PRODUCT.md` (Bass: Lineout overview) |

## What it shows

At build time, `update_docs.sh` collects:

* Every `*.md` under `vendor/ax86-lite` (package READMEs, product docs, and so on)
* Selected external docs from SmartDock DFC and Ethernet Config

Those files are packed into `doc_data.js` and installed with the app. Pick a document from the dropdown in the app.

## Adding docs for a new package

1. Put a `README.md` (or other `.md`) in your `vendor_packages/<name>/` folder.
2. Rebuild with `--extras` so `build.sh` runs the Ax86Docs update step.
3. The new file shows up in the on-device list automatically.

To pull markdown from outside `vendor/ax86-lite`, add the path to `EXTERNAL_DOCS` in `vendor_packages/Ax86Docs/update_docs.sh`.

## Public docs vs on-device docs

| | Ax86Docs | This Documentation site |
|--|----------|-------------------------|
| Where | On the device | docs.blisscolabs.dev |
| Source | Vendor tree markdown (+ a few AOSP package docs) | This git repo |
| Best for | Field / offline reference next to the feature | Install, licensing, and the full product guide |

Many of the same topics appear in both places. Prefer this site for install and licensing; use Ax86Docs when you are already on the device.

## Related

* [Building Bass OS](../../development/building-bass.md) (`--extras`)
* Application pages under [Applications](../../README.md#applications)
