from ssec_func import *

def main():
    def decrypt(cipher_text):
        iv = 16 * b'\x00'
        block_size = 16
        cipher = AES.new(get_key(), AES.MODE_CBC, iv)
        decoded_text = base64.b64decode(cipher_text)
        padded_text = cipher.decrypt(decoded_text)
        plain_text = unpad(padded_text, block_size)
        return plain_text

    def create_log(text, index):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if text == "":
            computer_name = get_conf_index(index, '[Computer names]\n')
            log_entry = "{} {}".format(timestamp, computer_name)
            insert_to_config(log_entry, "[MAC history]\n")
        else:
            log_entry = "{} {}".format(timestamp, text)
            insert_to_config(log_entry, "[MAC history]\n")

    def get_conf_index(index, section):
        with open("/ssec/.ssec.config", "r") as f:
            content = f.readlines()
        index = content.index(section)+index
        return content[index].strip()

    def verify_hash(line, computer_mac):
        ph = PasswordHasher()
        try:
            if ph.verify(line, computer_mac):
                return True
            else:
                return False
        except:
            return False

    def get_identification():
        encrypted_device = find_encrypted_device()
        mapper_device = '/dev/mapper/EncHome'
        mount_point = '/home/encrypted'
        
        inside_identification = False
        computer_mac = mac_address_function()
        index = 0

        for line in file:
            line = line.strip()
            if line == '[Identification]':
                inside_identification = True
                continue
            if inside_identification:
                if line == '\n':
                    break
                index += 1
                if verify_hash(line, computer_mac):
                    password = decrypt(get_conf_index(index, 
                            '[Enc pass]\n')).decode('utf-8')
                    subprocess.run(
                            ['cryptsetup', 'luksOpen',
                            encrypted_device, 'EncHome'],
                            input=password.encode(),
                            stderr=subprocess.PIPE)
                    subprocess.run(
                            ['mount', mapper_device, mount_point],
                            stderr=subprocess.PIPE)
                    pop_in_config('Decrypted\n', '[Ssec decrypt]\n')
                    create_log("", index)
                    break
        
        pop_in_config('Encrypted\n', '[Ssec decrypt]\n')
        create_log(f"{computer_mac}", index)

    insert_check = find_in_config('[Ssec insert]')
    if insert_check == 'Insert':
        return

    file_path = '/ssec/.ssec.config'
    with open(file_path, 'r') as file:
            get_identification()

if __name__ == "__main__":
    main()
