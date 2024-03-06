from tkinter import *
import subprocess
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

encrypted_device = '/dev/sdb2'

def insert_to_config(insert_text, insert_section):
    conf_path = '/ssec/.ssec.config'
    with open(conf_path, "r") as f:
        content = f.readlines()
        f.close()

    insert_index = content.index(insert_section)+1
    content.insert(insert_index, insert_text+'\n')

    with open(conf_path, "w") as f:
        f.writelines(content)
        f.close()

def pop_in_config(insert_text, insert_section):
    with open("/ssec/.ssec.config", "r") as f:
        content = f.readlines()
        f.close()

    insert_index = content.index(insert_section)+1
    content.pop(insert_index)
    content.insert(insert_index, insert_text)

    with open("/ssec/.ssec.config", "w") as f:
        f.writelines(content)
        f.close()

def find_in_config(section):
    conf_path = '/ssec/.ssec.config'
    inside_decrypt = False
    with open(conf_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line == section.strip():
                inside_decrypt = True
                continue
            if inside_decrypt == True:
                return line.strip()

def generate_key():
    subprocess.run(f'cat /sys/class/dmi/id/product_uuid > /ssec/ssec_tmp.txt', shell=True)
    tmp_path = '/ssec/ssec_tmp.txt'
    with open(tmp_path, 'r') as file:
        uuid = file.readline().strip().replace('-', '')
    subprocess.run(f'echo "yes" | rm /ssec/ssec_tmp.txt', shell=True)
    return uuid.encode('utf-8')

def encrypt(plain_text):
    iv = 16 * b'\x00'
    block_size = 16
    cipher = AES.new(generate_key(), AES.MODE_CBC, iv)
    padded_text = pad(plain_text.encode('utf-8'), block_size)
    cipher_text = cipher.encrypt(padded_text)
    return base64.b64encode(cipher_text)

def insert_button():
    if entry3.get() == entry4.get():
        enc_pass = encrypt(entry3.get()).decode('utf-8')
        insert_to_config(enc_pass, '[Enc pass]\n')
        pop_in_config('default\n', '[Ssec insert]\n')
        root.quit()
    else:
        pass_not_match_window = Toplevel(root)
        pass_not_match_window.title("Error")
        
        pass_not_match_label = Label(pass_not_match_window, text="Error: passwords do not match" )
        pass_not_match_label.pack()

        close_button = Button(pass_not_match_window, text="Close", command=pass_not_match_window.destroy)
        close_button.pack()
        return

def submit():
    input_sapp = entry2.get()
    subprocess.run(f'echo "{input_sapp}" | cryptsetup luksOpen {encrypted_device} EncHome', shell=True)
    subprocess.run(f'mount /dev/mapper/EncHome /home/encrypted', shell=True)
    pop_in_config('default\n', '[Ssec decrypt]\n')
    root.quit()

def ok():
    pop_in_config('default\n', '[Ssec decrypt]\n')
    root.quit()

root = Tk()
root.attributes('-fullscreen', True)
root.configure(bg='lightblue')

insert_line = find_in_config('[Ssec insert]')
decrypt_line = find_in_config('[Ssec decrypt]')

if insert_line == 'Insert':
    frame = Frame(root)
    frame.pack()

    label3 = Label(frame, text="Enter the password for encryption")
    label3.pack()

    entry3 = Entry(frame, show="*", bg='lightblue')
    entry3.pack()

    label4 = Label(frame, text="Enter your password again")
    label4.pack()

    entry4 = Entry(frame, show="*" ,bg='lightblue')
    entry4.pack()

    submit_button = Button(frame, text="Submit", command=insert_button)
    submit_button.pack()
elif decrypt_line == 'Decrypted':
    frame = Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    label1 = Label(frame, text="Automatic decrypting successful, click on OK to continue")
    label1.grid(row=0, column=0, sticky='w')

    submit_button = Button(frame, text="Ok", command=ok)
    submit_button.grid(row=2, column=0, columnspan=2)
else:
    frame = Frame(root)
    frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

    label2 = Label(frame, text="Automatic decrypting failed, please, enter your password mannually")
    label2.grid(row=1, column=0, sticky='w')

    entry2 = Entry(frame, show="*" ,bg='lightblue')
    entry2.grid(row=1, column=1)

    submit_button = Button(frame, text="Submit", command=submit)
    submit_button.grid(row=2, column=0, columnspan=2)

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

root.mainloop()
