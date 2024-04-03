#!/bin/bash

mkdir /ssec
mkdir /home/encrypted

source_dir="./"
destination_dir="/ssec/"
files_to_move=(
    "ssec.py"
    "ssec_func.py"
    "ssec_startup.py"
    "ssec_app.py"
)
echo "Moving files from $source_dir to $destination_dir"
for file in "${files_to_move[@]}"; do
    mv "$source_dir/$file" "$destination_dir"
done

cat > /etc/systemd/system/ssec.service << EOF
[Unit]
Description=Automated LUKS decryption
Before=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /ssec/ssec.py
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable ssec.service

cat > /etc/xdg/autostart/ssec.desktop << EOF
[Desktop Entry]
Type=application
Name=Ssec login window
Exec=sudo /usr/bin/python3 /ssec/ssec_startup.py
Terminal=false
Type=Application
Categories=

X-GNOME-Autostart-enabled=true
X-GNOME-Autostart-Delay=0
EOF
echo "ubuntu ALL=(ALL) ALL" | sudo EDITOR='tee -a' visudo
echo "ubuntu ALL=(ALL) NOPASSWD: /usr/bin/python3 /ssec/ssec_startup.py" | sudo EDITOR='tee -a' visudo

echo "Available flash disks:"
lsblk -o NAME,SIZE,TYPE,VENDOR,MODEL | grep -i "disk"
read -p "Enter the name of the flash disk you want to encrypt (e.g. sdb): " disk_name
if [ ! -b "/dev/$disk_name" ]; then
    echo "Error: Disk $disk_name does not exist."
    exit 1
fi

read -s -p "Enter the password for LUKS encryption: " luks_password
echo
echo "Encrypting the second partition of /dev/$disk_name with LUKS..."
cryptsetup --verbose --verify-passphrase luksFormat "/dev/${disk_name}2" <<< $luks_password
echo "Opening the encrypted partition..."
cryptsetup luksOpen "/dev/${disk_name}2" "${disk_name}2_crypt"

echo "Formatting the encrypted partition..."
mkfs.ext4 -L "${disk_name}_encrypted" "/dev/mapper/${disk_name}2_crypt"
echo "Mounting the encrypted partition..."
mount "/dev/mapper/${disk_name}2_crypt" "/mnt/${disk_name}_encrypted"
echo "Encryption and mounting completed successfully."

disk_info=$(lsblk -o NAME,VENDOR,MODEL | grep -i "$disk_name")
flash_name=$(echo "$disk_info" | awk -v disk_name="$disk_name" '$1 == disk_name {for (i=2; i<=NF; i++) printf "%s ", $i; printf "\n"}')

cat > /ssec/.ssec.config << EOF
[Flash name]
$flash_name

[Ssec decrypt]
default

[Ssec insert]
default

[Computer names]

[Identification]

[Enc pass]

[MAC history]
EOF
echo ".ssec.config file created successfully."
echo "Systemd service setup completed successfully."

