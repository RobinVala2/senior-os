import subprocess
import os
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from argon2 import PasswordHasher

encrypted_device = '/dev/sdb2'
"""
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
"""
def error_function(error_text):
    err_path = "/ssec/ssec_err.log"
    with open(err_path, "a") as f:
        f.write(error_text)

def find_in_config(section):
    inside_section = False
    with open('/ssec/.ssec.config', 'r') as file:
        for line in file:
            line = line.strip()
            if line == section.strip():
                inside_section = True
                continue
            if inside_section == True:
                return line.strip()

def pop_in_config(insert_text, insert_section):
    with open("/ssec/.ssec.config", "r") as f:
        content = f.readlines()

    insert_index = content.index(insert_section)+1
    content.pop(insert_index)
    content.insert(insert_index, insert_text)

    with open("/ssec/.ssec.config", "w") as f:
        f.writelines(content)

def get_key():
    subprocess.run(f'cat /sys/class/dmi/id/product_uuid > /ssec/ssec_uuid.txt', shell=True)
    uuid_path = '/ssec/ssec_uuid.txt'
    with open(uuid_path, 'r') as file:
        uuid = file.readline().strip().replace('-', '')
    subprocess.run(f'echo "yes" | rm /ssec/ssec_uuid.txt', shell=True)
    return uuid.encode('utf-8')

def decrypt(cipher_text):
    iv = 16 * b'\x00'
    block_size = 16
    cipher = AES.new(get_key(), AES.MODE_CBC, iv)
    decoded_text = base64.b64decode(cipher_text)
    padded_text = cipher.decrypt(decoded_text)
    plain_text = unpad(padded_text, block_size)
    return plain_text

def mac_address_function():
    try:
        tmp_path = '/ssec/ssec_tmp.txt'
        subprocess.run(f"cat /sys/class/net/*/address | awk 'NR==1 {{print; exit}}'"+
                        "> /ssec/ssec_tmp.txt 2>/ssec/ssec_err.log", shell=True)
        ph = PasswordHasher()
        with open(tmp_path, 'r') as file:
            computer_mac = file.readline().strip()
        subprocess.run(f'echo "yes" | rm /ssec/ssec_tmp.txt '+
			'2>/ssec/ssec_err.log', shell=True)
        return computer_mac
    except FileNotFoundError:
        error_function("Error: {tmp_path was not found}")
    except PermissionError:
        error_fucntion("Error: Insufficient permission to the {tmp_path} file")
    except Exception as e:
        error_function("An error occured: {e}")

def get_cipher(cipher_index):
    with open("/ssec/.ssec.config", "r") as f:
        content = f.readlines()
    index = content.index('[Enc pass]\n')+cipher_index
    return content[index].strip()

def main():
    insert_check = find_in_config('[Ssec insert]')
    if insert_check == 'Insert':
        return

    ph = PasswordHasher()
    file_path = '/ssec/.ssec.config'
    inside_identification = False
    computer_mac = mac_address_function()
    cipher_index = 0
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line == '[Identification]':
                    inside_identification = True
                    continue
                if inside_identification:
                    if line == '\n':
                        break
                    cipher_index += 1
                    try:
                        if ph.verify(line, computer_mac):
                            password = decrypt(get_cipher(cipher_index)).decode('utf-8')
                            subprocess.run(f'echo "{password}" | cryptsetup luksOpen {encrypted_device} EncHome 2>/ssec/ssec_err.log', shell=True)
                            subprocess.run(f'mount /dev/mapper/EncHome /home/encrypted 2>/ssec/ssec_err.log', shell=True)
                            pop_in_config('Decrypted\n', '[Ssec decrypt]\n')
                            break
                        else:
                            pop_in_config('Encrypted\n', '[Ssec decrypt]\n')
                    except Exception as e:
                        pop_in_config('Encrypted\n', '[Ssec decrypt]\n')
                        pass
    except FileNotFoundError:
	    error_function("Error: {file_path} was not found")
    except PermissionError:
	    error_function("Error: Insufficient permission to the {file_path} file")
    except Exception as e:
	    error_function("An error occured: {e}")
#subprocess.run(f'echo "yes" | rm /var/run/ssec.pid 2>/ssec/ssec_err.log', shell=True)

main()
