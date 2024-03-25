from ssec_func import *

def main():
    def encrypt(plain_text):
        iv = 16 * b'\x00'
        block_size = 16
        cipher = AES.new(get_key(), AES.MODE_CBC, iv)
        padded_text = pad(plain_text.encode('utf-8'), block_size)
        cipher_text = cipher.encrypt(padded_text)
        return base64.b64encode(cipher_text)

    def decryption_process(input_pass):
        encrypted_device = find_encrypted_device()
        try:
            completed_process = subprocess.run(
                        ['cryptsetup', 'luksOpen', 
                        encrypted_device, 'EncHome'],
                        input=input_pass.encode(),
                        stderr=subprocess.PIPE)
            if completed_process.returncode == 2:
                raise subprocess.CalledProcessError(
                        completed_process.returncode, 
                        completed_process.args)
            subprocess.run(
                    f'mount /dev/mapper/EncHome /home/encrypted',
                    shell=True)
            return True
        except subprocess.CalledProcessError as e:
            return False
    
    def insert_button(pass_entry1, pass_entry2):
        if pass_entry1.get() == pass_entry2.get():
            if decryption_process(pass_entry1.get()):
                enc_pass = encrypt(pass_entry1.get()).decode('utf-8')
                insert_to_config(enc_pass, '[Enc pass]\n')
                pop_in_config('default\n', '[Ssec insert]\n')
                root.quit()
            else:
                error_window(root, "Wrong password")
                return
        else:
            error_window(root, "Error: passwords do not match")

    def submit(pass_entry):
        input_pass = pass_entry.get()
        if decryption_process(input_pass):
            pop_in_config('default\n', '[Ssec decrypt]\n')
            root.quit()
        else:
            error_window(root, "Wrong password")
            return

    def decrypted_success():
        pop_in_config('default\n', '[Ssec decrypt]\n')
        root.quit()

    def encrypted_frame():
        encrypted_label = tk.Label(frame, 
                bg="white", 
                text="Automatic decrypting failed, please, enter your password mannually")
        encrypted_label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        pass_entry = ttk.Entry(frame, show="*" , style='Custom.TEntry')
        pass_entry.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        submit_button = tk.Button(frame,
                text="Submit",
                command=lambda: submit(pass_entry))
        submit_button.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        quit_button = tk.Button(frame, 
                text="Quit without decrypting drive",
                command=lambda: quit_window(root))
        quit_button.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

    def decrypted_frame():
        decrypted_label = tk.Label(frame,
                bg='white',
                text="Automatic decrypting successful, click on OK to continue")
        decrypted_label.grid(row=0, column=0, sticky='nsew')

        submit_button = tk.Button(frame, text="Ok", command=decrypted_success)
        submit_button.grid(row=1, column=0, columnspan=2, sticky='nsew')

    def insert_frame():
        insert_label1 = tk.Label(frame,
                bg='white',
                text="Enter the password for encryption")
        insert_label1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        insert_entry1 = ttk.Entry(frame, show="*", style='Custom.TEntry')
        insert_entry1.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        insert_label2 = tk.Label(frame, bg='white', text="Enter your password again")
        insert_label2.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        insert_entry2 = ttk.Entry(frame, show="*", style='Custom.TEntry')
        insert_entry2.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

        submit_button = tk.Button(frame,
                text="Submit",
                command=lambda: insert_button(insert_entry1, insert_entry2))
        submit_button.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')

    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(bg='white')

    insert_line = find_in_config('[Ssec insert]')
    decrypt_line = find_in_config('[Ssec decrypt]')

    get_styles()

    if insert_line == 'Insert':
        frame = tk.Frame(root, bg="white")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        insert_frame()
    elif decrypt_line == 'Decrypted':
        frame = tk.Frame(root, bg="white")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        decrypted_frame()
    else:
        frame = tk.Frame(root, bg="white")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        encrypted_frame()

    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    root.mainloop()

if __name__ == "__main__":
    main()

#completed_process = subprocess.run(f'echo "{input_pass}" | cryptsetup luksOpen {encrypted_device} EncHome', shell=True)

