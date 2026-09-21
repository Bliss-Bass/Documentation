**END USER LICENSE AGREEMENT (EULA)**

**Last Updated:** 2026-09-21

**IMPORTANT – PLEASE READ CAREFULLY:** This End User License Agreement ("Agreement") is a legal contract between you ("User") and Navotpala Tech ("Company") regarding the use of the Software (as defined below). By installing, copying, or otherwise using the Software, you agree to be bound by the terms of this Agreement. If you do not agree to the terms, do not install or use the Software.

**Note:** Plain-language product licensing details also appear in [Licensing](licensing.md) and [License Activation](../setup_and_configuration/license-activation.md). If those documents conflict with this Agreement, this Agreement controls until superseded by a signed commercial contract.

### **1 Definitions**

**"Software"** means the Company-distributed Bass / Bass: Lineout product materials you receive or download, including without limitation: system images and installers; proprietary and commercially licensed addons and modules; patchsets and tooling from the Bass Toolkit and ax86-lite Toolkit as supplied by the Company; branding and UI assets; licensing, integrity, and fleet components (including BootSight and BassView / BlissView); activation materials; and related documentation and configuration shipped with those builds. "Software" does not extinguish third-party open-source licenses that apply to specific included components (see Section 1B).

**"Device"** means each physical computer, tablet, kiosk, appliance, or other hardware unit, and each virtual machine, hypervisor guest, containerized guest, cloud instance, or other virtualized runtime that presents as a separate install of the Software. Each concurrent or separately installed instance counts as its own Device.

**"Commercial Components"** means Bass addons, modules, patchsets, branding assets, licensing/integrity components, and other materials that the Company offers only under commercial terms, or under a dual GPLv3 / commercial choice where you have not validly elected and complied with the GPLv3 option for that component.

**"Evaluation Build"** (also called a demo or trial build) means a Company-supported image distributed for evaluation that may include a selection of paid Commercial Components for testing, as described on the Company's Downloads site and related product materials.

### **1A License Grant**

The Company grants you a limited, non-exclusive, non-transferable, revocable license to use the Software on a single Device, subject to the terms of this Agreement, unless a separate written commercial agreement (for example, a bulk license, buyout, OEM, Custom Build Service Agreement, branding, or OTA service agreement) expressly authorizes additional Devices or different arrangements.

Cloning, imaging, templating, snapshot restore, or rebuilding that results in another runnable instance requires a separate per-Device license for that instance, unless your written bulk or buyout agreement covers those seats.

Pinning, copying, or spoofing a Device's default product configuration or licensing identity (including platform, firmware, or virtualization identity settings used to derive a serial or seat) so that more than one instance appears to share a single licensed identity does **not** reduce the number of Devices you must license. Those practices are prohibited under Section 3.

### **1B Open-source components and Commercial Components**

Bass: Lineout **Core** (the AOSP / Lineage-derived platform and related GPL and Apache-licensed components that form the open base of the OS) remains available under the open-source licenses that accompany those components (typically Apache License 2.0 for AOSP-originated code and GPL-family licenses where applicable). Nothing in this Agreement is intended to restrict your rights under those licenses for Core components alone.

**Bass Addons** and **patchsets / materials from the Bass Toolkit and ax86-lite Toolkit** are separate from Core. They are either:

- dual-licensed (GPLv3 or commercial), at the Company's election for that component; or
- available **only** under commercial license (many production addons).

Where a component is dual-licensed, exercising the GPLv3 option requires full compliance with GPLv3 for that component (and any applicable downstream obligations). Choosing commercial terms, or using Commercial Components as shipped in Company images without a valid GPLv3 election and compliance path, means those components are governed by this Agreement and any applicable commercial contract.

**Supported Evaluation Builds** may include a selection of paid Commercial Components so you can evaluate the product. Inclusion in a demo image is **not** a grant of production, redistribution, white-label, or perpetual commercial rights to those addons. Production use of Commercial Components requires the appropriate Device license and any addon / SKU entitlements stated for your purchase. See the Downloads site for which paid addons are bundled in a given Evaluation Build, and [Licensing](licensing.md) for the Core vs addons split.

### **1C Evaluation and production use**

Evaluation Builds are licensed only for internal evaluation and testing, for the period and under the conditions stated for that build (including any on-device overlay, trial window, or SKU limits). Evaluation Builds are **not** licensed for production fleets, revenue-generating deployments, redistribution as your product, or continued use after stripping licensing, integrity, or evaluation controls.

Production deployment of Company images that include Commercial Components requires a valid commercial Device license (and any required bulk, buyout, OEM, branding, or OTA agreements). A Device license for one SKU does not automatically unlock other paid addons or features.

### **1D Seat transfer and Device replacement**

The license is non-transferable to another organization without the Company's prior written consent. If a licensed Device is permanently retired, failed, or replaced (for example hardware RMA or a rebuild that is intended as the same licensed seat rather than an additional instance), you may request that the Company reassign that seat to a replacement Device identity under the Company's then-current replacement process. Until the Company confirms reassignment, the replacement instance is not licensed. Cloning or running old and new instances at the same time still requires seats for each runnable instance.

### **1E Branding and white-label**

Except for the limited Evaluation Build options below, a Device license does **not** include rights to rebrand, white-label, or present the Software as your own operating system or product.

**Evaluation Build limited branding (only):** Supported Evaluation Builds may include documented methods that let you supply (1) a custom boot animation, (2) a default wallpaper, and/or (3) a company logo for Company-provided kiosk launchers. Those three options are the **only** white-label / branding customizations offered on Evaluation Builds. Using them does not remove Company product identity elsewhere, does not grant OEM naming rights, and does not authorize shipping the image as your own OS.

**All other branding** (including without limitation OEM / manufacturer name, about screens, setup wizard branding, broader launcher or system UI rebranding, removing Company marks, or shipping images under your brand) requires a written **Custom Build Service Agreement** (and any applicable OEM / branding / toolkit terms). Standard production Device seats remain Company-branded unless that agreement says otherwise.

### **1F OEM, embedded, and redistribution**

Except as permitted under applicable open-source licenses for Core components alone, or under a written commercial agreement, you may not:

- Preinstall, embed, or bundle the Software (including Commercial Components) on hardware you sell or lease;
- Offer the Software as a hosted, multi-tenant, or "Android PC / kiosk as a service" product to third parties;
- Redistribute Company images, installers, or Commercial Components as part of your appliance, firmware drop, or channel SKU.

Those uses require an **OEM**, redistribution, or similar commercial agreement that states the permitted channel, seat model, and branding. A website single-Device license is for your own Device use, not for resale or embedding.

### **1G SKU and feature entitlements**

Licenses are SKU- and feature-scoped. A Device seat unlocks only the product line, build variant, and Commercial Components included in that purchase (or expressly listed in your contract). Enabling additional paid addons or modes by side-loading modules, flipping configuration properties, changing build flags on derived images, or otherwise unlocking features outside your entitlement is not licensed. Demo-bundled addons remain evaluation-only unless your production SKU includes them.

### **1H Support and services**

Unless a separate written support, SLA, custom-build, or professional-services agreement says otherwise, a Device license grants use rights only. It does **not** include guaranteed support response times, private update channels, custom images, on-site assistance, or indemnity beyond what this Agreement or your commercial contract expressly provides.

### **2 Ownership**

The Software is licensed, not sold. The Company retains all rights, title, and interest in and to the Commercial Components and Company-originated materials, including all intellectual property rights, subject to third-party open-source licenses for Core and other OSS components.

### **3 Restrictions**

You may not:

- Modify, adapt, translate, or create derivative works based on Commercial Components, except as expressly permitted under an applicable open-source license for a dual-licensed component where you have validly elected and complied with that license, or under a written commercial agreement with the Company.
- Repackage, redistribute, or remove any default components, content, or configurations included with Company images in a manner that circumvents commercial licensing, evaluation limits, or product SKU entitlements.
- Rebrand, white-label, or remove Company product identity except for the limited Evaluation Build boot-animation / wallpaper / kiosk-logo options in Section 1E, or under a written Custom Build Service Agreement (Section 1E).
- Preinstall, embed, resell, or offer the Software as a service to third parties except under a written OEM / redistribution agreement (Section 1F).
- Enable or use paid addons, SKUs, or feature modes outside your purchased entitlement (Section 1G).
- Disable, remove, bypass, or interfere with licensing, serial-number generation, integrity checks, EULA / BassView acceptance, BootSight or similar Device Status / overlay UI, evaluation banners or popups, or other technical measures that enforce licensing or evaluation terms.
- Circumvent, forge, clone, or share Device identity or licensing state across multiple Devices in order to use fewer licenses than the number of Devices in use (including by fixing or copying default product / platform identity settings on virtual machines or clones to reuse one seat).
- Copy, share, publish, resell, or redistribute offline license files, license packs, activation codes, QR labels, or signing materials except as needed to activate Devices you have purchased seats for; you may not use those materials to activate unpurchased serials or to operate your own license-issuance service.
- Extract, copy, share, or use Company platform signing keys, license-signing private keys, release certificates, or build-pipeline secrets; produce or distribute images signed to impersonate Company releases; or substitute unauthorized keys to bypass licensing or integrity checks (Section 3D).
- Operate, redirect, or configure a private, third-party, or self-hosted over-the-air (OTA) / update feed for the Software, or otherwise bypass the Company-provided updater channel, except under a written **OTA service**, custom-build, or OEM update agreement with the Company. A standard single-Device license does **not** include the right to host or point Devices at your own update servers.
- Reverse engineer, decompile, disassemble, or otherwise attempt to discover the source code of Commercial Components, except to the limited extent that applicable law prohibits this restriction or an open-source license covering a dual-licensed component expressly permits it after a valid election.
- Rent, lease, sell, sublicense, assign, or transfer your rights under this Agreement to any third party, except for a Company-approved Device replacement under Section 1D.
- Use the Software in violation of Section 3F (acceptable use).

### **3A Volume, bulk, and buyout licensing**

Website single-Device licenses are intended for genuine one-Device deployments (including a single VM guest treated as one Device). Deployments that involve multiple Devices (especially fleets of virtual machines, cloned images, or repeated rebuilds that create additional instances) require a **bulk licensing** or **buyout** agreement with the Company. As a practical threshold reflected in our product docs, purchasing or activating more than ten (10) Device licenses, or operating a multi-VM / multi-instance deployment, requires contacting the Company for a commercial contract rather than relying solely on repeated single-Device website purchases.

### **3B Updates and OTA service**

Unless your written agreement states otherwise:

- A licensed Device may receive updates only through Company-provided or Company-authorized update channels configured for that product SKU.
- Self-hosting an update catalog, changing updater URIs or properties to point at non-Company servers, or shipping a custom update pipeline for production Devices requires an **OTA service license** and/or a **custom / OEM build** agreement.
- Evaluation Builds do not grant a production entitlement to operate independent OTA infrastructure.

### **3C Offline activation materials**

Where the Company issues offline licenses (`license.pack`, per-Device `.lic` files, activation codes, or QR labels), those materials are licensed solely to activate the serials / seats you purchased. Placing the same pack on every purchased Device for activation is allowed. Redistributing packs or codes to third parties, using them on Devices beyond purchased seats, reverse-engineering issuance, or substituting your own signing keys is prohibited.

### **3D Signing keys and build pipeline**

Company platform keys, license-signing keys, certificates, and other build- or release-pipeline secrets remain Company property. Access granted under an OEM or builder agreement is limited to the scope of that agreement. You may not extract keys from Devices or images, share them, use them to sign unauthorized builds, or craft releases that appear to be genuine Company builds. Compromising or misusing those materials is grounds for immediate termination of this Agreement and any related commercial contracts.

### **3E Support versus license**

Purchase or activation of a Device license does not, by itself, create a support or SLA obligation. Support tiers, response times, custom builds, and professional services are only as stated in a separate written agreement or the Company's published support policy for your product tier.

### **3F Acceptable use**

You may not use the Software to:

- Operate unlawful surveillance, or other activity that violates applicable law;
- Attack, disrupt, or gain unauthorized access to networks, systems, or data;
- Provide a multi-tenant hosting platform or shared runtime to third parties beyond the Devices you have licensed (see also Section 1F);
- Circumvent technical or contractual limits described in this Agreement.

The Company may suspend or terminate licenses for material acceptable-use violations.

### **4 Device Information Collection**

By using the Software, you acknowledge and agree that the Company may collect and use your Device's serial number and related licensing identifiers for purposes such as software licensing, Device identification, multi-instance detection, and customer support. The collected information will be handled in accordance with the Company’s Privacy Policy. List of information collected is below:

- Build Vendor name  
- Build Vendor ID  
- Hardware SKU  
- License status  
- Device serial number

If the User is a corporation or business using a build with NT_MDM or third-party MDM suite, then the Company may also collect the following information:

- Any supported modules that are found to be installed (VNC, ScreenView, SSHD, etc)
- Any properties added to the Users MDM device profile
- Any settings added to the Users MDM device profile

The Company may also collect additional non-personal technical signals reasonably necessary to enforce per-Device licensing (for example, install or instance identifiers, and hashed hardware attributes), as described in the Privacy Policy when those capabilities are enabled.

### **5 Privacy**

The Company respects your privacy and will handle any personal data collected in connection with the Software in accordance with the Company’s Privacy Policy, which is incorporated into this Agreement by reference. You can review the Privacy Policy [here](https://github.com/Bliss-Bass/Documentation/legal/Navotpala\_Tech\_Privacy\_Policy.md)

### **6 Term and Termination**

This Agreement is effective until terminated. Your rights under this Agreement will terminate automatically without notice if you fail to comply with any term of this Agreement. Upon termination, you must cease all use of the Software and destroy all copies of the Software in your possession (including offline activation materials you are no longer entitled to use). Rights in Core components under their open-source licenses survive according to those licenses.

### **7 Disclaimer of Warranties**

The Software is provided "AS IS" without any warranties of any kind, either express or implied. To the maximum extent permitted by applicable law, the Company disclaims all warranties, including but not limited to implied warranties of merchantability, fitness for a particular purpose, and non-infringement.

### **8 Limitation of Liability**

To the fullest extent permitted by applicable law, in no event shall the Company be liable for any indirect, incidental, special, consequential, or punitive damages, or any damages whatsoever, arising out of or in connection with the use or inability to use the Software, even if the Company has been advised of the possibility of such damages.

### **9 Governing Law**

This Agreement shall be governed by and construed in accordance with the laws of Michigan, USA, without regard to its conflict of law principles.

### **10 Severability**

If any provision of this Agreement is found to be invalid or unenforceable, the remaining provisions will continue to be valid and enforceable.

### **11 Entire Agreement**

This Agreement constitutes the entire agreement between you and the Company with respect to the Software and supersedes all prior or contemporaneous understandings regarding such subject matter, except that a signed commercial agreement between you and the Company (bulk, buyout, OEM, branding / white-label, Custom Build Service Agreement, redistribution, OTA service, support/SLA, or similar) controls to the extent of any conflict with this EULA for the products and seats covered by that agreement.
