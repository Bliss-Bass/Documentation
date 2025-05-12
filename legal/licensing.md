
# Licensing

Bass OS is available under different licensing options designed to accommodate the needs of our various users: 

- Bass OS licensed under commercial licenses is appropriate for development of proprietary/commercial software where you do not want to share any source code with third parties or otherwise cannot comply with the terms of the GNU GPL version 3.
- Bass OS licensed under the GNU General Public License (GPL) version 3 is appropriate for the development of Bass OS applications provided you can comply with the terms and conditions of the GNU GPL version 3.
- Bass OS components can be licensed under the GNU General Public License (GPL) version 3 or the commercial license choice of its developers.and are appropriate for the development of Bass OS applications commonly used with Bass OS addons or software components licensed under the commercial or GNU GPL version 3 terms and conditions.
- Any alterations to the Bass OS source or compiled images, including repackaging, distribution of altered images, or removal of included system components is subject to license compliance requirements. If you are unable to comply with the terms and conditions of the GNU GPL version 3, you must obtain a commercial license from Navotpala Tech (Bliss Co-Labs) to use Bass OS.


Bass OS also contains third-party code that is licensed under specific open-source licenses from the original authors (See Third-Party Code in Bass OS below). 

Note: For open-source licensed Bass OS, some specific parts (Bass OS addons) are available under the GNU General Public License (GPL). See the list of Bass OS modules for details. For commercial licensees, all Bass OS addons are available under individual, commercial Bass OS licenses.

Bass OS documentation  is available under commercial licenses from Navotpala Tech (Bliss Co-Labs), and under the terms of the GNU Free Documentation License (FDL) version 1.3, as published by the Free Software Foundation.

Bass OS addon examples  are available under commercial licenses from Navotpala Tech (Bliss Co-Labs), and under a GNU GPL version 3 license.

Educational licenses are available for students and educators in qualified educational institutions or universities.

## Purchasing and Sales Information

To purchase a Bass OS license, contact us with your request.

For further information and assistance about Bass OS licensing, contact our sales; see https://navotpala.tech for contact details.

## Third-Party Code in Bass OS

The following documents the open-source licenses used in different parts of Bass OS:

Bass OS core is GPL-3.0 and also inherits the same Apache v2 licensing that AOSP uses for most of the components, while many of the other components like Android-Generic Project use GPL-2.0 license. For product use, we do not include proprietary components like Google Apps, Native-Bridge (Houdini or Libndk-translation), or Widevine. Some features and toolkits like our rebranding toolkit do require additional licensing to be obtained by the customer (See Bass OS components above). 

- AOSP Licenses - Bliss OS License - Bliss ROM License - Android-Generic Project License - Boringdroid License -

For Bass OS/Bliss OS source, we do catalog all the repos used and their licenses. You can view that here.

## FAQ

**Q: Does Bass OS include proprietary software?**

**A:** Yes. Our FOSS and Vanilla builds might include some proprietary parts for drivers, firmware and media codecs. 

Proprietary redistributables in all Bliss OS public builds: 
- linux-firmware blobs 
- Proprietary linux drivers (broadcom-wl for example) 
- some media codecs (for decoding H.264/HEVC) 

**Q: Is Bass OS suitable for individuals?**

**A:** Yes, but we are targeting the product manufacturers directly with these releases, so the builds are all a little bare-bones and there are no plans of releasing Bass OS with any Proprietary Google components and services, like Play Store.

**Q: Is Bass OS suitable for companies?**

**A:** Yes. We produce minimal vanilla and FOSS builds of Bass OS with x86/x86_64 PC hardware support. Bass OS builds come with only proprietary drivers, firmware and media support included, and those are available to test with. While those builds are very basic, they do include much of what would be needed to base a product off of. If your product requires no additional changes on top of what is released to the public, then you are free to use it at no cost.
If your product requires Google Apps, ARM/ARM64 Native-Bridge, or Widevine, due to licensing restrictions from their holding companies, we are unable to provide support. In those cases, we suggest that you reach out and we can help you look into alternative options using open-source solutions.

**Q: Is there a Bass OS version with Google Play Store?**

**A:** No. Google Play Store and Google Mobile Services are not available to license for generic devices. This is why we use open-source alternatives for compatibility with most of what GMS offers. The open-source solutions we offer are:
- microG: A free-as-in-freedom re-implementation of Google’s proprietary Android user space apps and libraries. 
- Aurora Store: An unofficial FOSS client to Google Play with an elegant design and privacy
- Neo-Store: An F-Droid client with modern UI and an arsenal of extra features.
- Need Your Own?: Custom F-Droid based store options are available

**Q: Can my company use Bass OS in a product?**

**A:** Yes, This applies to Android-PC (AOSP), Bliss OS, Bliss OS Go or Bass OS sources. If you are an individual developer, a startup, or represent some other business enterprise and you are interested in using our project, the open-source licenses we maintain allow you to use the source at no cost as long as you use it: 
A) as-is, meaning you make no changes to how we release it.
B) you contribute any changes made back to our source repos.
C) produce the full source to the public independently, maintaining full git attribution.

If you would like to use our source and make changes to it that you do not plan on or are not able to  release as open-source, we request you contact us to work out a per-device licensing agreement and/or setup a development contract for branding, optimizations and specific needs.

**Q: Does my company have to release any changes made to the collective source code of Bass OS?**

**A:** This all depends on where the changes in the source were made, as many repos in the project retain a different OSS Licenses, there are different requirements per repo. If you are unsure if your company needs to release the source for any of the changes made, please feel free to contact us.

Another thing to pay attention to is if the tools being used require the end product or alterations to be released. Some Apache 2.0 licensed projects allow for that requirement to be made. Some versions of Android-Generic Project also have similar licensing requirements. We have put together a toolkit to help identify these types of licenses within the source. You can find that here.

**Q: Do Bass builds work with the Bliss installers for Windows/Linux?**

**A:** No, the Bass builds use a new image setup for A/B OTA updates, and that prevents it from working when installed by the legacy Bliss OS/Android-x86 installers.

**Q: Can I still dual-boot with Bass builds?**

**A:** Yes, but we do not include a method in the installer to do this automatically. You will have to install to a separate ext4 partition, and make sure that you either A) update your host OS's bootloader to add entries for Bass builds. Or B) opt-in to let the installer install Grub, and manage using 2 bootloaders at the same time.
