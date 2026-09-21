**END USER LICENSE AGREEMENT (EULA)**

**Last Updated:** 2026-09-21

**IMPORTANT – PLEASE READ CAREFULLY:** This End User License Agreement ("Agreement") is a legal contract between you ("User") and Navotpala Tech ("Company") regarding the use of the software application ("Software"). By installing, copying, or otherwise using the Software, you agree to be bound by the terms of this Agreement. If you do not agree to the terms, do not install or use the Software.

**Note:** Plain-language product licensing details also appear in [Licensing](licensing.md) and [License Activation](../setup_and_configuration/license-activation.md). If those documents conflict with this Agreement, this Agreement controls until superseded by a signed commercial contract.

### **1 License Grant**

The Company grants you a limited, non-exclusive, non-transferable, revocable license to use the Software on a single Device (as defined below), subject to the terms of this Agreement, unless a separate written commercial agreement (for example, a bulk license, buyout, OEM, or OTA service agreement) expressly authorizes additional Devices or different update arrangements.

### **1A Definition of Device**

For purposes of this Agreement, a **"Device"** means each of the following that runs an instance of the Software:

- A physical computer, tablet, kiosk, appliance, or other hardware unit; and
- A virtual machine, hypervisor guest, containerized guest, cloud instance, or other virtualized runtime that presents as a separate install of the Software.

Each concurrent or separately installed instance counts as its own Device. Cloning, imaging, templating, snapshot restore, or rebuilding that results in another runnable instance requires a separate per-Device license for that instance, unless your written bulk or buyout agreement covers those seats.

Pinning, copying, or spoofing a Device's default product configuration or licensing identity (including platform, firmware, or virtualization identity settings used to derive a serial or seat) so that more than one instance appears to share a single licensed identity does **not** reduce the number of Devices you must license. Those practices are prohibited under Section 3.

### **2 Ownership**

The Software is licensed, not sold. The Company retains all rights, title, and interest in and to the Software, including all intellectual property rights.

### **3 Restrictions**

You may not:

- Modify, adapt, translate, or create derivative works based on the Software, except as expressly permitted under an applicable open-source license for specific components, or under a written commercial agreement with the Company.
- Repackage, redistribute, or remove any default components, content, or configurations included with the Software.
- Disable any system services that are used in licensing or serial number generation.
- Circumvent, forge, clone, or share Device identity or licensing state across multiple Devices in order to use fewer licenses than the number of Devices in use (including by fixing or copying default product / platform identity settings on virtual machines or clones to reuse one seat).
- Operate, redirect, or configure a private, third-party, or self-hosted over-the-air (OTA) / update feed for the Software, or otherwise bypass the Company-provided updater channel, except under a written **OTA service**, custom-build, or OEM update agreement with the Company. A standard single-Device license does **not** include the right to host or point Devices at your own update servers.
- Reverse engineer, decompile, disassemble, or otherwise attempt to discover the source code of the Software, except to the limited extent that applicable law prohibits this restriction or an open-source license covering a specific component expressly permits it.
- Rent, lease, sell, sublicense, assign, or transfer your rights under this Agreement to any third party.



### **3A Volume, bulk, and buyout licensing**

Website single-Device licenses are intended for genuine one-Device deployments (including a single VM guest treated as one Device). Deployments that involve multiple Devices (especially fleets of virtual machines, cloned images, or repeated rebuilds that create additional instances) require a **bulk licensing** or **buyout** agreement with the Company. As a practical threshold reflected in our product docs, purchasing or activating more than ten (10) Device licenses, or operating a multi-VM / multi-instance deployment, requires contacting the Company for a commercial contract rather than relying solely on repeated single-Device website purchases.

### **3B Updates and OTA service**

Unless your written agreement states otherwise:

- A licensed Device may receive updates only through Company-provided or Company-authorized update channels configured for that product SKU.
- Self-hosting an update catalog, changing updater URIs or properties to point at non-Company servers, or shipping a custom update pipeline for production Devices requires an **OTA service license** and/or a **custom / OEM build** agreement.
- Evaluation or demo builds do not grant a production entitlement to operate independent OTA infrastructure.



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

The Company respects your privacy and will handle any personal data collected in connection with the Software in accordance with the Company’s Privacy Policy, which is incorporated into this Agreement by reference. You can review the Privacy Policy [here](https://github.com/Bliss-Bass/Documentation/legal/Navotpala_Tech_Privacy_Policy.md)

### **6 Term and Termination**

This Agreement is effective until terminated. Your rights under this Agreement will terminate automatically without notice if you fail to comply with any term of this Agreement. Upon termination, you must cease all use of the Software and destroy all copies of the Software in your possession.

### **7 Disclaimer of Warranties**

The Software is provided "AS IS" without any warranties of any kind, either express or implied. To the maximum extent permitted by applicable law, the Company disclaims all warranties, including but not limited to implied warranties of merchantability, fitness for a particular purpose, and non-infringement.

### **8 Limitation of Liability**

To the fullest extent permitted by applicable law, in no event shall the Company be liable for any indirect, incidental, special, consequential, or punitive damages, or any damages whatsoever, arising out of or in connection with the use or inability to use the Software, even if the Company has been advised of the possibility of such damages.

### **9 Governing Law**

This Agreement shall be governed by and construed in accordance with the laws of Michigan, USA, without regard to its conflict of law principles.

### **10 Severability**

If any provision of this Agreement is found to be invalid or unenforceable, the remaining provisions will continue to be valid and enforceable.

### **11 Entire Agreement**

This Agreement constitutes the entire agreement between you and the Company with respect to the Software and supersedes all prior or contemporaneous understandings regarding such subject matter, except that a signed commercial agreement between you and the Company (bulk, buyout, OEM, OTA service, or similar) controls to the extent of any conflict with this EULA for the products and seats covered by that agreement.