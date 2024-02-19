#!/bin/bash

function encrypted_disk {
	echo "ehoj"
}

function decrypted_disk {
	echo "dhoj"
}

while getopts ":hed" options; do
	case $options in
		h) echo "usage: $0 [-h] [-e] [-d]"; exit ;;
		e) encrypted_disk ;;
		d) decrypted_disk ;;
		?) echo "error: option -$OPTARG is invalid"; exit ;;
	esac
done


