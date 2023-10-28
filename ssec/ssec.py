import subprocess

password = 'komosny1'
encrypted_device = '/dev/sdb2'

subprocess.run(f"cat /sys/class/net/*/address | awk 'NR==1 {{print; exit}}' > ssec_tmp.txt", shell=True)
with open('ssec_tmp.txt', 'r') as file:
	computer_mac = file.readline()
subprocess.run(f'echo "yes" | rm ssec_tmp.txt', shell=True)

file_path = './ssec.config'
inside_identification = False

with open(file_path, 'r') as file:
	for line in file:
		line = line.strip()
		if line == '[Identification]':
			inside_identification = True
			continue
		if inside_identification:
			if line == computer_mac.strip():
				subprocess.run(f'echo "{password}" | cryptsetup luksOpen {encrypted_device} EncHome', shell=True)
				subprocess.run(f'mount /dev/mapper/EncHome /home', shell=True)
				subprocess.run(f'echo "Decrypted" > ssec_crypt.txt', shell=True)
			else:
				subprocess.run(f'echo "Encrypted" > ssec_crypt.txt', shell=True)
