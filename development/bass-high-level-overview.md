# Bass - High Level Overview
Bass (Broad Apparatus Support System) is the combined operation of the various layers used in the Android OS stack that provides vendors, users, businesses, etc with additional configuration options that may be required to fine-tune a generic Android image to their hardware. 

## Overview
Bass comes with a number of parts that work together to make the system configurable and reliable as well as save time and effort.

### Bass - System Architecture
![Bass - System Architecture](assets/Bass-Stack.20240308.svg)
The various parts added to Android with Bass are as follows:

 * **BASS Configurable HAL's:**  These are switchable Hardware Abstraction Layers for Graphics cards & rendering engines, audio interfaces, network interfaces, input & sensor interfaces, and more.
 * **BASS Apps & Services:** These are the various apps and system services that interface with the hardware and added configurations and allow for a tailored out of the box solution using a generic build.
 * **BASS Vendor Configuration Layer:** This layer is what handles the targeted look and feel as well the individual configurations specific to the brand or target application. 
 * **Vendor Addons, Apps & Services:** These are all the private parts of the system that are not open-source or parts not meant for a generic audience. This provides the interface and middleware required for the addons and vendor specific apps or services to be included in the system that are specific to that devices target audience. 