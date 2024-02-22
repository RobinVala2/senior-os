import subprocess
import os

err_path = "/ssec/ssec_err.log"

try:
	pid = os.getpid()
	with open('/var/run/ssec.pid', 'w') as pidfile:
		pidfile.write(str(pid))
except FileNotFoundError:
	f = open(err_path, "a")
	f.write("Error: File /var/run/ssec.pid was not found")
	f.close()
except PermissionError:
	f = open(err_path, "a")
	f.write("Error: Insufficient permission to the /var/run/ssec.pid file")
	f.close()
except Exception as e:
	f = open(err_path, "a")
	f.write("An error occured: {e}")
	f.close()

password = 'komosny1'
encrypted_device = '/dev/sdb2'

try:
	tmp_path = '/ssec/ssec_tmp.txt'
	subprocess.run(f"cat /sys/class/net/*/address | awk 'NR==1 {{print; exit}}'"+
			"> /ssec/ssec_tmp.txt 2>/ssec/ssec_err.log", shell=True)
	with open(tmp_path, 'r') as file:
		computer_mac = file.readline()
	subprocess.run(f'echo "yes" | rm /ssec/ssec_tmp.txt '+
			'2>/ssec/ssec_err.log', shell=True)
except FileNotFoundError:
	f = open(err_path, "a")
	f.write("Error: {tmp_path} was not found")
	f.close()
except PermissionError:
	f = open(err_path, "a")
	f.write("Error: Insufficient permission to the {tmp_path} file")
	f.close()
except Exception as e:
	f = open(err_path, "a")
	f.write("An error occured: {e}")
	f.close()

file_path = '/ssec/ssec.config'
inside_identification = False
try:
	with open(file_path, 'r') as file:
		for line in file:
			line = line.strip()
			if line == '[Identification]':
				inside_identification = True
				continue
			if inside_identification:
				if line == computer_mac.strip():
					subprocess.run(f'echo "{password}"'+
							'| cryptsetup luksOpen {encrypted_device}'+
 							'EncHome 2>/ssec/ssec_err.log', shell=True)
					subprocess.run(f'mount /dev/mapper/EncHome'+
							' /home 2>/ssec/ssec_err.log', shell=True)
					subprocess.run(f'echo "Decrypted" >'+
							' /ssec/ssec_crypt.txt 2>/ssec/ssec_err.log', shell=True)
				else:
					subprocess.run(f'echo "Encrypted" >'+
							' /ssec/ssec_crypt.txt 2>/ssec/ssec_err.log', shell=True)
except FileNotFoundError:
	f = open(err_path, "a")
	f.write("Error: {file_path} was not found")
	f.close()
except PermissionError:
	f = open(err_path, "a")
	f.write("Error: Insufficient permission to the {file_path} file")
	f.close()
except Exception as e:
	f = open(err_path, "a")
	f.write("An error occured: {e}")
	f.close()
subprocess.run(f'echo "yes" | rm /var/run/ssec.pid 2>/ssec/ssec_err.log', shell=True)
