# SISO - Reduced Operating System with Linux Kernel on USB Flash Drive

- The main aim was to create customized operating system based on Linux distribution Debian operating in read-only LiveCD mode. 
- Requirements for the customized operating system are to include local PDF browser and lightweight Web browser. 
- The whole system is runable from the USB Flash Drive and uses the remaining space of the storage media as an encrypted persistence for user data storage. 
- This goal is achivable via two methods. The first one uses specialized package  **live-build** and the second one builds the entire operating system **from scratch**. 
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
Pendrive or even Distribution Remixes are labels used to refer to the same issue over the internet. This issue peaked between 2005 and 2012, and throughout its existence, many labels were assigned to it. Due to its obsolescence a lot of information was recovered from web archives available on the internet.

The Live CD or Live System is described as a fully bootable computer installation mostly of the Linux operating systems with preset functionalities. This system is easily run on a PC without the need for installation on a computer’s hardware such as a hard disk. The whole system runs directly from the storage medium used to carry the Live system and its whole process, a run phase, is temporarily stored in the RAM of the computer.

## System Specification
Both systems consists of a local PDF browser XPDF and a lightweight Web browser Palemoon. In the home folder of both users a directory `PDF/` contains the `OS_03_ArchB.pdf` file. The auto-login feature is used by both systems.

#### Method live-build Package
| **Distribution** | Debian 11 |
| **Linux Kernel Release** | 5.10.0-28-amd64 |
| **Linux Kernel Verison** | 5.10.209-2 |
| **System Architecture** | x86_64 (64-bit) |
| **Build Date** | 2024/01/31 |
| **Build-in User** | user |


#### Method From Scratch
| **Distribution** | Debian 12 |
| **Linux Kernel Release** | 6.0.0-18-amd64 |
| **Linux Kernel Verison** | 6.1.76-1 |
| **System Architecture** | x86_64 (64-bit) |
| **Build Date** | 2024/02/01 |
| **Build-in User** | root |

## Linux Installation
Obtain the build ISO images through [Releases](https://github.com/forsenior/senior-os/releases) and [apply persistence setting](#apply-persistence-setting) or [build your own customized LiveCD](#build-your-own-customized-livecd) Debian distribution through the provided scripts. 

#### Apply Persistence Setting
- Modify the section `VARIABLES` in the `SISO_persistence.sh` script according to your Linux filesystem policy and USB Flash Drive parameters. 
- Its recommended to run script as a **root** user.
- The connected USB Flash Drive has to be **empty**, without any disk partition.

```bash
# Clone project repository
git clone https://github.com/forsenior/senior-os

# Change into project directory
cd senior-os/siso

# Modify VARIABLES in a script
nano SISO_persistence.sh

# Add Exacutable rights to the script 
sudo chmod a+x SISO_persistence.sh 

# Execute SISO_Persistence Script
sudo ./SISO_persistence.sh
```

#### Build Your Own Customized LiveCD
Chose one of the existing methods to create the customized LiveCD.

- Modify the section `VARIABLES` in the appropriate script according to your Linux filesystem policy and USB Flash Drive parameters.
- Its recommended to run script as a **root** user.
- The connected USB Flash Drive has to be **empty**, without any disk partition.

##### Method live-build Package
```bash
# Clone project repository
git clone https://github.com/forsenior/senior-os

# Change into project directory
cd senior-os/siso

# Method live-build Package
cd LiveCD \ Package/

# Modify VARIABLES in a script
nano SISO_430MB_Package.sh

# Add Exacutable rights to the script 
sudo chmod a+x SISO_430MB_Package.sh 

# Execute SISO_Persistence Script
sudo ./SISO_430MB_Package.sh
```

##### Method From Scratch
In the directory `LiveCD From Scratch` there are two bash scripts. Devices with [Nvidia hybrid graphics cards](https://wiki.debian.org/NvidiaGraphicsDrivers#NVIDIA_Proprietary_Driver) require additional setting within the custom LiveCD environment. If your device disposes witch such a component use `SISO_1200MB_From_Scratch_Nvidia_Hybrid.sh` script insted.

```bash
# Clone project repository
git clone https://github.com/forsenior/senior-os

# Change into project directory
cd senior-os/siso

# Method From Scratch
cd LiveCD\ From\ Scratch/

# Modify VARIABLES in a script
nano SISO_895MB_From_Scratch.sh

# Add Exacutable rights to the script 
sudo chmod a+x SISO_895MB_From_Scratch.sh 

# Execute SISO_Persistence Script
sudo ./SISO_895MB_From_Scratch.sh

```

## Project Usage
Although both systems are build differently their usage differs only slightly. Based on a stored BIOS on a device try one of the common keys **F2**, **F8**, **F12**, or others.

#### Change a Boot Device 
![BootDevice](https://github.com/forsenior/senior-os/blob/main/siso/LiveCD%20From%20Scratch/Screens/SISO_1_Boot.png)

#### Boot Menu startup
Based on the started ISO image the title in a penguin bubble changes from **USB live-build** to **USB From Scratch**. Select the only option by pressing the **ENTER** key on the keyboard.
![BootMenu](https://github.com/forsenior/senior-os/blob/main/siso/LiveCD%20Package/Screens/SISO_2_Grub.png)

#### Unlock the Encrypted Persistence
The corresponding cipher word has to be entered to enable persistence of the **/home** directory.

- $${\color{green} Correct \space password \space entered }$$ - mount partition with stored data on a storage medium into the Live System filesystem,
- $${\color{red} Incorrect \space password \space entered }$$ - prints the message about password re-entering, 
- $${\color{black}No \space password \space entered}$$ - the Live System is booted without any parition mount. Customizations in the persistence folder `/home` are **NOT** stored.

![EncryptedPersistence](https://github.com/forsenior/senior-os/blob/main/siso/VirtualBox/13_SISO_VB_Encrypted_Persistence.png)

#### Console Environment
![PackageConsoleEnvironment](https://github.com/forsenior/senior-os/blob/main/siso/VirtualBox/14_SISO_VB_Conole.png)

#### Both Browsers Start
Windows displayed by the Xorg server are automatically resized based on the screen resolution and the server’s default settings. Program windows are controlable through mouse control. To **Exit** the program window *Right Click* anywhere on a displayed program window and select *Exit* from the drop down menu or use key *q* on the keyboard.

> **NOTE** While entering the URL of the required Web page be aware of rewriting of entered characters.

- Local PDF browser start: `startx /usr/bin/xpdf PDF/OS_03_ArchB.pdf`
- Palemoon Web browser start: `startx /usr/bin/palemoon`

![PDFBrowser](https://github.com/forsenior/senior-os/blob/main/siso/LiveCD%20Package/Screens/SISO_5_PDF_Browser.png)

![PalemoonBrowser](https://github.com/forsenior/senior-os/blob/main/siso/LiveCD%20Package/Screens/SISO_6_Palemoon_Web_Browser.png)
