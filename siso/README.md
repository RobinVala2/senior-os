# SISO - Reduced Operating System with Linux Kernel on USB Flash Drive

- The main aim was to create a customized operating system based on the Linux distribution Debian operating in read-only LiveCD mode. 
- Requirements for the customized operating system are to include a local PDF browser and a lightweight Web browser. 
- The whole system is runnable from the USB Flash Drive and uses the remaining space of the storage media as an encrypted persistence for user data storage. 
- This goal is achievable via two methods. The first one uses a specialized package  **live-build** and the second one builds the entire operating system **from scratch**. 
- For more information about this issue see a thesis text available from: TBD.

---

## Table of Content
- [What is a LiveCD solution?](#what-is-a-livecd-solution)
- [System Specification](#system-specification)
- [Linux Installation](#linux-installation)
- [Project Usage](#project-usage)

---

## What is a LiveCD Solution?
A Live CD/DVD, Live USB, Live ISO, Live Operating System, Live Image, Live
Pendrive or even Distribution Remixes are labels used to refer to the same issue over the internet. This issue peaked between 2005 and 2012, and throughout its existence, many labels were assigned to it. Due to its obsolescence, a lot of information was recovered from web archives available on the internet.

The Live CD or Live System is described as a fully bootable computer installation mostly of the Linux operating systems with preset functionalities. This system is easily run on a PC without the need for installation on a computer’s hardware such as a hard disk. The whole system runs directly from the storage medium used to carry the Live system and its whole process, a run phase, is temporarily stored in the RAM of the computer.

## System Specification
Both systems consists of a local PDF browser XPDF and a lightweight Web browser Palemoon. In the home folder of both users a directory `PDF/` contains the `OS_03_ArchB.pdf` file. The auto-login feature is used by both systems.

|   |  From Scratch | Package live-build |
|:-----:|:-----:| :-----:|
| **Distribution** |  Debian 12 | Debian 11 |
| **Linux Kernel Release** |  6.0.0-18-amd64 | 5.10.0-28-amd64 |
| **Linux Kernel Version** |  6.1.76-1 | 5.10.209-2 |
| **System Architecture** | x86_64 (64-bit) | x86_64 (64-bit) |
| **Build Date** | 2024/02/01 | 2024/01/31 |
| **Build-in User** | root | user |


## Linux Installation
Obtain the build ISO images through [Releases](https://github.com/forsenior/senior-os/releases) and [apply persistence setting](#apply-persistence-setting) or [build your own customized LiveCD](#build-your-own-customized-livecd) Debian distribution through the provided scripts. 

#### Apply Persistence Setting
- Modify the section `VARIABLES` in the `SISO_persistence.sh` script according to your Linux filesystem policy and USB Flash Drive parameters. 
- It is recommended to run the script as a **root** user.
- The connected USB Flash Drive has to be **empty**, without any disk partition.

```bash
# Clone project repository
git clone https://github.com/forsenior/senior-os

# Change into the project directory
cd senior-os/siso

# Modify VARIABLES in a script
nano SISO_persistence.sh

# Add Executable rights to the script 
sudo chmod a+x SISO_persistence.sh 

# Execute SISO_Persistence Script
sudo ./SISO_persistence.sh
```

#### Build Your Own Customized LiveCD
Choose one of the existing methods to create the customized LiveCD.

- Modify the section `VARIABLES` in the appropriate script according to your Linux filesystem policy and USB Flash Drive parameters.
- It is recommended to run the script as a **root** user.
- The connected USB Flash Drive has to be **empty**, without any disk partition.

##### Method live-build Package
```bash
# Clone project repository
git clone https://github.com/forsenior/senior-os

# Change into the project directory
cd senior-os/siso

# Method live-build Package
cd LiveCD \ Package/

# Modify VARIABLES in a script
nano SISO_430MB_Package.sh

# Add Executable rights to the script 
sudo chmod a+x SISO_430MB_Package.sh 

# Execute SISO_Persistence Script
sudo ./SISO_430MB_Package.sh
```

##### Method From Scratch
In the directory `LiveCD From Scratch` there are two bash scripts. Devices with [Nvidia hybrid graphics cards](https://wiki.debian.org/NvidiaGraphicsDrivers#NVIDIA_Proprietary_Driver) require additional settings within the custom LiveCD environment. If your device disposes witch such a component use `SISO_1200MB_From_Scratch_Nvidia_Hybrid.sh` script instead.

```bash
# Clone project repository
git clone https://github.com/forsenior/senior-os

# Change into the project directory
cd senior-os/siso

# Method From Scratch
cd LiveCD\ From\ Scratch/

# Modify VARIABLES in a script
nano SISO_895MB_From_Scratch.sh

# Add Executable rights to the script 
sudo chmod a+x SISO_895MB_From_Scratch.sh 

# Execute SISO_Persistence Script
sudo ./SISO_895MB_From_Scratch.sh

```

## Project Usage
Although both systems are built differently their usage differs only slightly. Based on a stored BIOS on a device try one of the common keys **F2**, **F8**, **F12**, or others.

#### Change a Boot Device 
<p align="center">
  <img src="https://github.com/forsenior/senior-os/blob/main/siso/LiveCD%20From%20Scratch/Screens/SISO_1_Boot.png" alt="BootDevicePC1" width=60%> 
</p>

#### Boot Menu startup
Based on the started ISO image the title in a penguin bubble changes from **USB live-build** to **USB From Scratch**. Select the only option by pressing the **ENTER** key on the keyboard.

<p align="center">
  <img src="https://github.com/forsenior/senior-os/blob/main/siso/LiveCD%20Package/Screens/SISO_2_Grub.png" alt="BootMenu" width=60%> 
</p>

#### Unlock the Encrypted Persistence
The corresponding cipher word has to be entered to enable the persistence of the **/home** directory.

- **Correct password entered** - mount partition with stored data on a storage medium into the Live System filesystem,
- **Incorrect password entered** - prints the message about password re-entering,
- **No password entered** - the Live System is booted without any partition mount. Customizations in the persistence folder `/home` are **NOT** stored.

<p align="center">
  <img src="https://github.com/forsenior/senior-os/blob/main/siso/VirtualBox/13_SISO_VB_Encrypted_Persistence.png" alt="EncryptedPersistence" width=60%>
</p>

#### Console Environment

<p align="center">
  <img src="https://github.com/forsenior/senior-os/blob/main/siso/VirtualBox/14_SISO_VB_Conole.png" alt="PackageConsoleEnvironment" width=60%> 
</p>

#### Both Browsers Start
Windows displayed by the Xorg server are automatically resized based on the screen resolution and the server’s default settings. Program windows are controllable through mouse control. To **Exit** the program window *Right-click* anywhere on a displayed program window and select *Exit* from the drop-down menu or use key *q* on the keyboard.

> [!WARNING]
> While entering the URL of the required Web page be aware of rewriting of entered characters.

- Local PDF browser start: `startx /usr/bin/xpdf PDF/OS_03_ArchB.pdf`
- Palemoon Web browser start: `startx /usr/bin/palemoon`

<p align="center">
  <img src="https://github.com/forsenior/senior-os/blob/main/siso/LiveCD%20Package/Screens/SISO_5_PDF_Browser.png" alt="PDFBrowser" width=60%> 

  <img src="https://github.com/forsenior/senior-os/blob/main/siso/LiveCD%20Package/Screens/SISO_6_Palemoon_Web_Browser.png" alt="PalemoonBrowser" width=60%> 
</p>
