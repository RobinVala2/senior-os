#!/bin/bash

#  !!!  DISCLAIMER !!! 
    # 1. THIS SCRIPT MUST BE RUN AS A ROOT USER
    # 2. THE CONNECTED USB DRIVE HAS TO BE EMPTY
    # 3. ADD EXACUTABLE RIGHTS FOR THE SCRIPT

#----------------------------------------VARIABLES------------------------------------>
work_folder="SCRIPT"                                        # Directory where ISO image is stored
iso_name="iso-debian-from-scratch"                          # ISO image name

disk_partition="/dev/sdd"                                   # Removable storage medium name
disk_write_speed="7M"                                       # Removable storage medium speed
disk_partition_password="storage"                           # Password for removable storage medium

#----------------------------------------PACKAGES------------------------------------->
    # HOST SYSTEM REQUIREMENTS
sudo apt-get install -y cryptsetup

#--------------------------------ENCRYPTED-PERSISTENCE-------------------------------->
     # COPY LIVE SYSTEM TO THE USB FLASH DRIVE
dd bs=${disk_write_speed} if=${HOME}/${work_folder}/${iso_name}.iso of=${disk_partition} oflag=sync

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