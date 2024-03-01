#!/bin/bash

#  !!!  DISCLAIMER !!! 
    # 1. THIS SCRIPT MUST BE RUN AS A ROOT USER
	# 2. THE CONNECTED USB DRIVE HAS TO BE EMPTY

# CURRENT SIZE - 430 MB 

#----------------------------------------VARIABLES------------------------------------>
work_folder="LSDF"

file_dir="/root/Documents"
	pdf="OS_*"
	palemoon="palemoon-32.4.0.linux-x86_64-gtk2.tar.xz"

disk_partition="/dev/sdd"                                   # removable storage medium name
disk_write_speed="7M"                                       # removable storage medium speed
disk_partition_password="storage"                           # password for removable storage medium

#----------------------------------------PACKAGES------------------------------------->
apt-get install live-build

#------------------------------LIVE-SYSTEM-CUSTOMIZATION------------------------------>
	# LIVE SYSTEMS CONFIGURATION DIRECTORY
mkdir -p ${HOME}/${work_folder}/auto

	# COPY TEMPLATE OF THE CONFIGURATION - AUTO SCRIPT SKELETON
sudo cp -r /usr/share/doc/live-build/examples/auto/* "${HOME}/${work_folder}/auto"

	# AUTO SCRIPT - LIVE SYSTEM CONFIGURATION
sudo tee "${HOME}/${work_folder}/auto/config" << EOF
#!/bin/sh

DATE=\$(date +%F_%H:%M:%S)

set -e

lb config noauto \\
	--architecture amd64 \\
	--archive-areas "main contrib non-free" \\
	--bootappend-live "boot=live components persistence persistence-encryption=luks locales=en_US.UTF-8 keyboard-model=pc105 keyboard-layouts=cz nocomponents=xinit parameters hostname=debian-live silent noeject" \\
	--bootappend-live-failsafe none \\
	--cache false \\
	--checksums sha256 \\
	--clean \\
	--color \\
	--firmware-binary false \\
	--firmware-chroot false \\
	--image-name "iso-debian-live-package" \\
	--initramfs live-boot \\
	--iso-application "DebianLive" \\
	--iso-preparer "241110@vutbr.cz" \\
	--iso-publisher "Lada Struziakova" \\
	--iso-volume "DebianLive \${DATE}" \\
	--memtest none \\
	--quiet \\
	"\${@}"
EOF

	# LIVE SYSTEM SKELETON TREE, GENERATED BASED ON AUTO SCRIPT PARAMETERS
cd "${HOME}/${work_folder}" && lb config

	# LIVE SYSTEM PACKAGES
sudo tee "${HOME}/${work_folder}/config/package-lists/live.list.chroot" << EOF
	#DEFAULT 
live-boot
live-config
live-config-systemd
	#X Server + GUI
xserver-xorg-core
xserver-xorg-input-libinput
xserver-xorg-video-fbdev
	#PALEMOON
libasound2
libdbus-glib-1-2
libgtk2.0-0
ca-certificates
	#KEYBOARD SETTING
console-setup
	#DATA COMPRESSION
xz-utils
	#PERSISTENCE ENCRYPTION
cryptsetup
	#LOCAL PDF BROWSER, GUI START UTILITY
xpdf
xinit
EOF

	# LIVE SYSTEM PDF DIRECTORY
mkdir -p "${HOME}/${work_folder}/config/includes.chroot/home/user/PDF"

	# INCLUDE PDF FILES AND WEB BROWSER INTO LIVE SYSTEM
sudo cp -r "${file_dir}/"${pdf} "${HOME}/${work_folder}/config/includes.chroot/home/user/PDF"
sudo cp -r "${file_dir}/${palemoon}" "${HOME}/${work_folder}/config/includes.chroot/"


mkdir -p "${HOME}/${work_folder}/config/includes.chroot/lib/live/config"

	# LIVE SYSTEMS BOOT TIME HOOK - PALEMOON
sudo tee "${HOME}/${work_folder}/config/includes.chroot/lib/live/config/0999-Palemoon.sh" << EOF
#!/bin/sh

tar xvf /${palemoon} -C /

ln -s /palemoon/palemoon /usr/bin/palemoon

rm -rf /${palemoon}
EOF

	# ADD EXECUTABLE RIGHT FOR THE BOOT TIME HOOK
sudo chmod a+x "${HOME}/${work_folder}/config/includes.chroot/lib/live/config/0999-Palemoon.sh" 

mkdir -p "${HOME}/${work_folder}/config/bootloaders"

	# COPY TEMPLATEs OF BOOTLOADERS
sudo cp -r "/usr/share/live/build/bootloaders/"{syslinux*	,isolinux,grub-pc} "${HOME}/${work_folder}/config/bootloaders" 

#--------------------------------------BOOTLOADERS----------------------------------->
	### SYSLINUX MENU
sudo tee "${HOME}/${work_folder}/config/bootloaders/syslinux_common/menu.cfg" << EOF
menu hshift 0
menu width 82

menu title Boot menu 
	include stdmenu.cfg
	include live.cfg
	@OPTIONAL_INSTALLER_INCLUDE@

menu clear
EOF

	# SYSLINUX MENU CUSTOMIZATION
sudo tee "${HOME}/${work_folder}/config/bootloaders/syslinux_common/stdmenu.cfg" << EOF
menu background splash.png

menu color title	* #FFFFFFFF *
menu color border	* #00000000 #00000000 none

menu color sel		* #ffffffff #76a1d0ff *
menu color hotsel	1;7;37;40 #ffffffff #76a1d0ff *

menu color tabmsg	* #ffffffff #00000000 *
menu color help		37;40 #ffdddd00 #00000000 none

menu vshift 12
menu hshift 25
menu width 45

menu cmdlinerow 16
menu tabmsgrow 18
menu tabmsg Press ENTER to boot or TAB to edit a menu entry
EOF

	# SYSLINUX MENU ENTRY, KERNEL, INITRAM, ...
sudo tee "${HOME}/${work_folder}/config/bootloaders/syslinux_common/live.cfg.in" << EOF
label live-@FLAVOUR@
	menu label ^Live (@FLAVOUR@)
	menu default
	linux @LINUX@
	initrd @INITRD@
	append @APPEND_LIVE@
EOF

	# SYSLINUX SPLASH IMAGE
sudo cp "${file_dir}/splash.svg" "${HOME}/${work_folder}/config/bootloaders/syslinux_common/"


	### GRUB 
sudo tee "${HOME}/${work_folder}/config/bootloaders/grub-pc/grub.cfg" << EOF
source /boot/grub/config.cfg

#Live boot
@LINUX_LIVE@
EOF

	# GRUB THEME CONFIGURATION
sudo tee "${HOME}/${work_folder}/config/bootloaders/grub-pc/live-theme/theme.txt" << EOF
desktop-image: "../splash.png"
title-text: ""

message-font: "Unifont Regular 16"
terminal-font: "Unifont Regular 16"

#help bar at the bottom
+ label {
	top = 100%-50
	left = 0
	width = 100%
	height = 20
	text = "@KEYMAP_SHORT@"
	align = "center"
	color = "#ffffff"
	font = "DejaVu Sans Bold 14"
}

#boot menu
+ boot_menu {
	left = 50%
	width = 40%
	top = 50%
	height = 48%-80
	item_color = "#a8a8a8"
	item_font = "DejaVu Sans Bold 14"
	selected_item_color= "#ffffff"
	selected_item_font = "DejaVu Sans Bold 14"
	item_height = 16
	item_padding = 0
	item_spacing = 4
	icon_width = 0
	icon_heigh = 0
	item_icon_space = 0
}
EOF

	# GRUB SPLASH IMAGE
sudo cp "${file_dir}/splash.png" "${HOME}/${work_folder}/config/bootloaders/grub-pc/"

	# LIVE SYSTEM BUILD BASED ON PROVIDED CONFIGURATION
cd "${HOME}/${work_folder}" && lb build

#--------------------------------ENCRYPTED-PERSISTENCE-------------------------------->
    # UN-MOUNT ANY PARTITION MAPPED TO THE SYSTEM
#umount /media/${HOME}/DebianLive
    # DELETE ALL EXISTING PARTITIONS
dd if=/dev/zero of=/dev/${disk_partition} bs=512 count=1
     
     # COPY LIVE SYSTEM TO THE USB FLASH DRIVE
dd bs=${disk_write_speed} if=${HOME}/${work_folder}/iso-debian-live-package-amd64.hybrid.iso of=${disk_partition} oflag=sync

    # CREATE NEW PRIMARY PARTITION NUMBER 3
echo -e "n\np\n3\n\n\nw" | fdisk -w never "${disk_partition}" > /dev/null 2>&1

    # CREATE ENCRYPTED PARTITION
echo -n "${disk_partition_password}" | cryptsetup luksFormat ${disk_partition}3 -
    # OPEN ENCRYPTED PARITION
echo -e "${disk_partition_password}" | cryptsetup luksOpen ${disk_partition}3 live
    # FORMATE A CREATED PARTITION WITH FILESYSTEM TO ENABLE PERSISTENCE
mkfs.ext4 -L persistence /dev/mapper/live

    # CREATE A TEMPORARY MOUNT FOLDER, IF NOT EXISTS
mkdir -p /mnt/persistence
    # MOUNT DISK PARTITION INTO TEMPORARY FOLDER
mount /dev/mapper/live /mnt/persistence
    # WRITE PERSISTENCE CONDITION INTO PERSISTENCE.CONF FILE
echo "/home" > /mnt/persistence/persistence.conf
    # UMOUNT DISK PARTITION
umount /mnt/persistence

    # CLOSE ENCRYPTED PARTITION
cryptsetup luksClose live