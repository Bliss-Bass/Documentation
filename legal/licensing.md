# Licensing

Bass / Bass: Lineout products combine an open **Core** with separately licensed **addons** and toolkit materials. Binding terms for commercial use live in the [End User License Agreement](END_USER_LICENSE_AGREEMENT.md). This page is the plain-language map.

## Bass: Lineout Core vs addons and toolkits

| Layer | What it is | Typical licensing |
|-------|------------|-------------------|
| **Bass: Lineout Core** | AOSP / Lineage-derived platform and related GPL and Apache-licensed OS components | Open-source licenses that ship with those components (Apache 2.0 and GPL-family where applicable) |
| **Bass Addons** | Product modules (fleet/licensing UI, desktop/kiosk extras, audio, power, and similar) | Dual-licensed **GPLv3 or commercial**, **or commercial-only** (many production addons) |
| **Bass Toolkit / ax86-lite Toolkit patchsets** | Vendor patchsets, build/integration materials, and related toolkit output as supplied by Navotpala Tech | Dual-licensed **GPLv3 or commercial**, **or commercial-only**, per component |

Using Core under its OSS licenses does **not** grant production rights to Commercial Components. Shipping or deploying Company images that include paid addons, or using those addons outside a valid GPLv3 election and compliance path for dual-licensed components, requires commercial Device / SKU licensing under the [EULA](END_USER_LICENSE_AGREEMENT.md).

## Evaluation (demo) builds

Supported **Evaluation Builds** on the Downloads site may bundle a **selection of paid addons** so you can try the product. That bundle is for evaluation only. It is not a perpetual commercial license, not a right to strip licensing / integrity UI, and not permission to run production fleets or self-hosted OTA on the strength of the demo image alone. See the Downloads listing for which paid addons are included in a given demo, and [License Activation](../setup_and_configuration/license-activation.md) for turning evaluation into a licensed Device.

## Commercial licensing options

- **Commercial Device licenses** - appropriate when you deploy Company images or Commercial Components in production, or when you cannot or do not wish to comply with GPLv3 for dual-licensed addons / toolkit materials.
- **GPLv3 election (dual-licensed components only)** - appropriate when a specific addon or toolkit component is dual-licensed and you fully comply with GPLv3 for that component.
- **Commercial-only addons** - many addons have no OSS option; they require a commercial agreement even if you build Core from public trees.
- Alterations that remove, rebrand, or redistribute Commercial Components, or that bypass licensing / evaluation controls, require a commercial agreement (see EULA §§1B-1C, §3).
- **Branding / white-label:** Evaluation Builds may allow only custom boot animation, default wallpaper, and a company logo for kiosk launchers. Broader rebranding needs a **Custom Build Service Agreement** (EULA §1E). **OEM embedding / resale** and **hosted / as-a-service** use need separate written agreements (EULA §1F).
- Device seats are **SKU-scoped**; extra paid addons are not unlocked by side-loading or config tricks (EULA §1G).
- A Device license is **not** a support/SLA contract (EULA §§1H, 3E).

Bass documentation is available under commercial licenses from Navotpala Tech (Bliss Co-Labs), and under the terms of the GNU Free Documentation License (FDL) version 1.3, as published by the Free Software Foundation.

Educational licenses are available for students and educators in qualified educational institutions or universities.

## Purchasing and Sales Information

To purchase a Bass OS license, contact us with your request.

For further information and assistance about Bass OS licensing, contact our sales; see https://navotpala.tech for contact details.

## Third-Party Code in Bass OS

The following documents the open-source licenses used in different parts of Bass OS:

**Bass: Lineout Core** is built from AOSP / Lineage-class trees: much of the platform is Apache License 2.0; other components use GPL-family licenses (and projects such as Android-Generic may use GPL-2.0). For product use, we do not include proprietary components like Google Apps, Native-Bridge (Houdini or Libndk-translation), or Widevine. Rebranding toolkits and many Bass Addons require additional commercial licensing (see above).

- AOSP Licenses - Bliss OS License - Bliss ROM License - Android-Generic Project License - Boringdroid License -

For Bass OS/Bliss OS source, we do catalog all the repos used and their licenses. You can view that here.

## Device licenses, VMs, and updates

Commercial **per-device** licensing treats each install that can run as its own licensed seat. That includes:

- One physical machine = one Device
- One virtual machine / hypervisor guest (for example QEMU/KVM under Proxmox, virt-manager, or similar) = one Device

Cloning a disk image, templating VMs, or rebuilding guests so that more than one instance runs (even if default product / platform identity settings are pinned or copied so instances look like the same Device) still requires **one license per runnable instance**, unless you have a written **bulk** or **buyout** agreement that covers those seats. Sharing one single-device license across multiple VMs or hosts by spoofing identity is not permitted under the [End User License Agreement](END_USER_LICENSE_AGREEMENT.md).

**Website single-device licenses** are for genuine one-Device use (including a single VM guest). Multi-VM fleets, imaging pipelines, and deployments over our usual volume threshold (more than ten Device licenses, or any multi-instance production fleet) need a **bulk licensing** or **buyout** contract. Contact [info@navotpala.tech](mailto:info@navotpala.tech?subject=Licensing).

**Seat replacement:** A purchased seat is tied to a Device identity. Permanent hardware replacement or a same-seat rebuild can be reassigned through our replacement process; running old and new instances together still needs two seats. See EULA §1D.

**OTA / updates:** A standard Device license covers updates through Company-provided or Company-authorized channels for that product SKU. Hosting your own OTA/update feed, redirecting the on-device updater to private servers, or shipping a custom update pipeline for production Devices requires a separate **OTA service** and/or **custom / OEM build** agreement. Evaluation Builds do not include a production entitlement to operate independent OTA infrastructure.

**Branding, OEM, and SKUs:** On Evaluation Builds you may use only the documented boot-animation, default-wallpaper, and kiosk-launcher logo options. Any other white-label or rebrand work needs a **Custom Build Service Agreement**. Preinstalling on hardware you sell, or offering Bass as a hosted service, requires an OEM / redistribution agreement. Your seat only covers the SKU and addons you purchased. See EULA §§1E-1G.

Activation steps and purchase paths: [License Activation](../setup_and_configuration/license-activation.md). Binding legal terms: [EULA](END_USER_LICENSE_AGREEMENT.md).

## FAQ

**Q: Is Bass: Lineout Core free / open source?**

**A:** Core (AOSP / Lineage-derived GPL and Apache components) follows the open-source licenses that ship with those components. Bass Addons and Bass Toolkit / ax86-lite Toolkit patchsets are separate: dual-licensed GPLv3/commercial or commercial-only. See the table above and EULA §1B.

**Q: Demo builds include paid addons. Can I use those in production for free?**

**A:** No. Supported Evaluation Builds may bundle paid addons for testing (as listed on the Downloads site). Production use requires commercial Device / SKU licensing. Stripping BootSight, BassView, overlays, or other licensing controls does not create a free production entitlement.

**Q: Can I rebrand Bass as my own OS with a single-device license?**

**A:** Only in the narrow Evaluation Build sense: documented custom boot animation, default wallpaper, and company logo for kiosk launchers. Anything beyond those three options (OEM name, about screens, full white-label, shipping under your brand, and so on) requires a **Custom Build Service Agreement**. See EULA §1E.

**Q: Can I preinstall Bass on hardware I sell, or offer it as a hosted service?**

**A:** Not under a website single-Device license. Embedding, resale, channel SKUs, and multi-tenant / as-a-service offerings need an OEM or redistribution agreement. See EULA §1F.

**Q: If I buy a Device seat, do I get every addon / desktop / kiosk / gaming feature?**

**A:** No. Entitlements follow the SKU and features listed for your purchase. Side-loading addons or flipping props to unlock unpaid features is not licensed. See EULA §1G.

**Q: Does a Device license include support or an SLA?**

**A:** Not by itself. Support tiers and custom builds are separate agreements or published support policies. See EULA §§1H and 3E.

**Q: May I extract platform or license signing keys from an image?**

**A:** No. Company signing keys and build-pipeline secrets must not be extracted, shared, or used to sign unauthorized or impersonating builds. See EULA §3D.

**Q: Does a single-device license cover multiple VMs if I keep the same default product / platform identity?**

**A:** No. Each VM guest is a separate Device. Pinning or copying default product configuration or platform identity so clones share one licensing identity does not reduce seats owed. Use bulk or buyout licensing for fleets of VMs; see the [EULA](END_USER_LICENSE_AGREEMENT.md) (§1A, §3, §3A).

**Q: Can I point BootSight / the updater at my own OTA servers with a single-device license?**

**A:** No. Private or self-hosted OTA feeds and updater URI overrides for production use require an OTA service or custom-build agreement. See the [EULA](END_USER_LICENSE_AGREEMENT.md) (§3B) and [Updates and OTA](../features/updates-and-ota.md).

**Q: Can I share my offline license.pack with other machines?**

**A:** You may place the pack on every Device whose serial you purchased so each unit can activate. You may not redistribute packs or codes to activate serials you did not purchase, or run your own issuance. See EULA §3C.

**Q: Does Bass OS include proprietary software?**

**A:** Yes. Our FOSS and Vanilla builds might include some proprietary parts for drivers, firmware and media codecs. Supported Lineout Evaluation Builds may also include commercially licensed Bass Addons for evaluation only.

Proprietary redistributables in all Bliss OS public builds: 
- linux-firmware blobs 
- Proprietary linux drivers (broadcom-wl for example) 
- some media codecs (for decoding H.264/HEVC) 

**Q: Is Bass OS suitable for individuals?**

**A:** Yes, but we are targeting the product manufacturers directly with these releases, so the builds are all a little bare-bones and there are no plans of releasing Bass OS with any Proprietary Google components and services, like Play Store.

**Q: Is Bass OS suitable for companies?**

**A:** Yes. We produce minimal vanilla and FOSS builds of Bass OS with x86/x86_64 PC hardware support, and supported Lineout Evaluation Builds that include selected Commercial Components for testing. Core-only use under applicable OSS licenses is possible where you do not rely on Commercial Components. Production use of Company images that include paid addons, or commercial-only addons themselves, requires Device / commercial licensing under the [EULA](END_USER_LICENSE_AGREEMENT.md).
If your product requires Google Apps, ARM/ARM64 Native-Bridge, or Widevine, due to licensing restrictions from their holding companies, we are unable to provide support. In those cases, we suggest that you reach out and we can help you look into alternative options using open-source solutions.

**Q: Is there a Bass OS version with Google Play Store?**

**A:** No. Google Play Store and Google Mobile Services are not available to license for generic devices. This is why we use open-source alternatives for compatibility with most of what GMS offers. The open-source solutions we offer are:
- microG: A free-as-in-freedom re-implementation of Google’s proprietary Android user space apps and libraries. 
- Aurora Store: An unofficial FOSS client to Google Play with an elegant design and privacy
- Neo-Store: An F-Droid client with modern UI and an arsenal of extra features.
- Need Your Own?: Custom F-Droid based store options are available

**Q: Can my company use Bass OS in a product?**

**A:** For **Core** components, the open-source licenses that accompany them allow use subject to those licenses (including share-alike obligations where GPL applies). For **Bass Addons** and **toolkit patchsets**, you need either a valid GPLv3 path on dual-licensed components or a commercial agreement; commercial-only addons always need a commercial agreement. If you want to ship a branded Company image, paid addons, or closed changes to dual-licensed materials, contact us for per-device licensing and/or a development / OEM contract.

**Q: Does my company have to release any changes made to the collective source code of Bass OS?**

**A:** This all depends on where the changes in the source were made, as many repos in the project retain a different OSS Licenses, there are different requirements per repo. If you are unsure if your company needs to release the source for any of the changes made, please feel free to contact us.

Another thing to pay attention to is if the tools being used require the end product or alterations to be released. Some Apache 2.0 licensed projects allow for that requirement to be made. Some versions of Android-Generic Project also have similar licensing requirements. We have put together a toolkit to help identify these types of licenses within the source. You can find that here.

**Q: Do Bass builds work with the Bliss installers for Windows/Linux?**

**A:** No, the Bass builds use a new image setup for A/B OTA updates, and that prevents it from working when installed by the legacy Bliss OS/Android-x86 installers.

**Q: Can I still dual-boot with Bass builds?**

**A:** Yes, but we do not include a method in the installer to do this automatically. You will have to install to a separate ext4 partition, and make sure that you either A) update your host OS's bootloader to add entries for Bass builds. Or B) opt-in to let the installer install Grub, and manage using 2 bootloaders at the same time.
