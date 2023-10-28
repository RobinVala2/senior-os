import subprocess

encrypted_device = '/dev/sdb2'
password = 'komosny1'
computer_id = subprocess.run(f'dmidecode | grep -w UUID | sed "s/^.UUID\: //g"')

file_path = '/../sconf/sconf.config'
inside_identification = False

with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        if line == '[Identification]':
            inside_identification = True
            continue
            
        if inside_identification:
            if line == computer_id:
                try:
                    subprocess.run(f'echo "{password}" | cryptsetup luksOpen {encrypted_device} EncHomeFoo -d -', shell=True)
                    return 0;
                except:
                    print("Decrypting failed, please, enter your password mannually")
                    return 1;
        if not line:
            inside_identification = False
return 1;




