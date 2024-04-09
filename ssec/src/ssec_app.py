from ssec_func import *

def main():
    def show_frame(frame):
        for f in [frame1, frame2, frame3, block_frame]:
            f.grid_forget()
        frame.grid(row=1, column=0, columnspan=4, sticky='ew')

    def mac_validate(mac_address):
        mac_address_pattern = re.compile(
                r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
        if mac_address_pattern.match(mac_address):
            return True
        else:
            return False

    def hash_mac_func(input_mac):
        ph = PasswordHasher()
        mac_hash = ph.hash(input_mac.strip()) 
        
        insert_to_config(mac_hash, '[Identification]\n')
        pop_in_config('Insert\n', '[Ssec insert]\n')
        
        show_frame(block_frame)

    def submit(name_entry, mac_entry):
        input_mac = mac_entry.get().lower()

        if name_entry.get() == "":
            error_window(root, "Name cannot be empty")
            return

        if mac_entry.get() == "":
            error_window(root, "MAC adress cannot be empty")
            return

        if verify_macs(input_mac):
            error_window(root, "MAC adress is already permited")
            return

        if mac_validate(input_mac):
            insert_to_config(name_entry.get(), '[Computer names]\n')
            hash_mac_func(input_mac)
        else:
            error_window(root, "Error: MAC adress is not in a correct format")

    def verify_hash(line, computer_mac):
        ph = PasswordHasher()
        try:
            ph.verify(line, computer_mac)
            return True
        except:
            return False

    def verify_macs(input_mac):
        file_path = "/ssec/.ssec.config"
        inside_identification = False
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line == '[Identification]':
                    inside_identification = True
                    continue
                if inside_identification:
                    if line == '\n':
                        break
                    if verify_hash(line, input_mac):
                        return True
        return False

    def get_flash_disks():
        try:
            output = subprocess.check_output(
                    ["lsblk", "-o",
                    "NAME,VENDOR,MODEL",
                    "-d", "-n"]).decode(
                    "utf-8").splitlines()
            flash_disks = []
            for line in output:
                if "sd" in line:
                    flash_disks.append(line)
            return flash_disks
        except subprocess.CalledProcessError:
            return []

    def select_flash_disk(event):
        selected_disk = event.widget.get()

    def add_this_computer(name_entry):
        computer_mac = mac_address_function()
        if name_entry.get() == "":
            error_window(root, "Name cannot be empty")
            return

        if verify_macs(computer_mac):
            error_window(root, "MAC adress is already permited")
            return
        
        hash_mac_func(computer_mac)

    def insert_block():
        input_check = find_in_config('[Ssec insert]')
        if input_check == 'Insert':
            show_frame(block_frame)
        else:
            show_frame(frame1)       

    def insert_frame_widgets():
        insert_label = tk.Label(frame1,
                width=30,
                bg="white",
                text="Input permitted MAC\naddress manually here:")
        insert_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        name_label = tk.Label(frame1,
                width=50,
                bg="white",
                text="Choose a name for entered computer:")
        name_label.grid(row=0, column=1, padx=0, pady=0, sticky="ew")
        name_entry = ttk.Entry(frame1, width=70, style="Custom.TEntry")
        name_entry.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        mac_label = tk.Label(frame1,
                width=50, 
                bg="white",
                text="MAC address:")
        mac_label.grid(row=2, column=1, padx=0, pady=0, sticky="ew")
        mac_entry = ttk.Entry(frame1, width=70, style="Custom.TEntry")
        mac_entry.grid(row=3, column=1, padx=20, pady=20, sticky="ew")

        submit_button = tk.Button(frame1,
                text="Submit",
                command=lambda: submit(name_entry, mac_entry))
        submit_button.grid(row=4, column=1, padx=20, pady=20, sticky="ew")

        add_computer_label = tk.Label(frame1,
                width=30,
                bg="white",
                text="Add computer MAC\naddress without entering it:")
        add_computer_label.grid(row=5,
                column=0,
                padx=20,
                pady=20,
                sticky="nsew")
        add_this_computer_button = tk.Button(frame1,
                text="Add this computer",
                command=lambda: add_this_computer(name_entry))
        add_this_computer_button.grid(row=5,
                column=1, 
                padx=20,
                pady=40,
                sticky="ew")

        name_text_label = tk.Label(frame1,
                bg="white",
                text="Permitted computer names:")
        name_text_label.grid(row=0,
                column=2, 
                padx=20, 
                pady=40,
                sticky="ew")

        name_text = tk.Text(frame1,
                height=20,
                width=30,
                state="disabled")
        name_text.grid(row=1, column=2, rowspan=10, padx=60, pady=40)

        load_config(name_text, "[Computer names]")

    def block_frame_widgets():
        input_block_label = tk.Label(block_frame,
                bg="white",
                text="Inputting blocked, please, insert\nflash disk into a computer")
        input_block_label.pack(padx=20, pady=20)       

    def history_widgets():
        history_label = tk.Label(frame2, bg="white", text="MAC adress history")
        history_label.pack(padx=20, pady=20)

        log_text = tk.Text(frame2, height=20, width=100, state="disabled")
        log_text.pack(padx=10, pady=10)

        load_config(log_text, "[MAC history]")

    def load_config(text_field, section):
        try:
            with open("/ssec/.ssec.config", "r") as file:
                found_section = False
                content = ""
                for line in file:
                    if line.strip() == section:
                        found_section = True
                    elif found_section and line.startswith("["):
                        break
                    elif found_section:
                        content += line
                log_load(content, text_field)
        except FileNotFoundError:
            log_load("Log file not found", text_field)
        except PermissionError:
            log_load("Insufficient permission to open log file", text_field)

    def log_load(log_content, log_text_field):
            log_text_field.config(state="normal")
            log_text_field.delete(1.0, tk.END)
            log_text_field.insert(tk.END, log_content)
            log_text_field.config(state="disabled")

    def flash_disk_widgets():
        selected_disk_source = tk.StringVar(value="Select Flash Disk")
        selected_disk_destination = tk.StringVar(value="Select Flash Disk")

        label_source = tk.Label(frame3,
                bg="white",
                text="Select source flash disk")
        label_source.pack(padx=10, pady=10)

        dropdown_source = ttk.Combobox(frame3,
                textvariable=selected_disk_source,
                values=flash_disks)
        dropdown_source.pack(padx=10, pady=10)
        dropdown_source.bind("<<ComboboxSelected>>", select_flash_disk)

        label_source_pass = tk.Label(frame3,
                bg="white",
                text="Enter password for encrypted partition")
        label_source_pass.pack(padx=10, pady=10)

        source_entry = ttk.Entry(frame3, show="*" , style='Custom.TEntry')
        source_entry.pack(padx=10, pady=10)

        label_destination = tk.Label(frame3,
                bg="white",
                text="Select destination flash disk")
        label_destination.pack(padx=10, pady=10)

        dropdown_destination = ttk.Combobox(frame3,
                textvariable=selected_disk_destination,
                values=flash_disks)
        dropdown_destination.pack(padx=10, pady=10)
        dropdown_destination.bind("<<ComboboxSelected>>", select_flash_disk)

        label_destination_pass = tk.Label(frame3,
                bg="white",
                text="Enter password for encrypted partition")
        label_destination_pass.pack(padx=10, pady=10)

        destination_entry = ttk.Entry(frame3, show="*", style='Custom.TEntry')
        destination_entry.pack(padx=10, pady=10)

        copy_data_button = tk.Button(frame3, 
                text="Copy data", 
                command=lambda: 
                copy_event(dropdown_source, 
                dropdown_destination, 
                source_entry.get(),
                destination_entry.get()))
        copy_data_button.pack(padx=20, pady=40)

    def flash_not_found():
        label = tk.Label(frame3, text="No flash disks found.")
        label.pack(padx=10, pady=10)

    def copy_event(source_box, destination_box, source_pass, destination_pass):
        selected_source = source_box.get()
        selected_destination = destination_box.get()

        source_parts = selected_source.split()
        destination_parts = selected_destination.split()

        source = f"/dev/{source_parts[0]}2"
        destination = f"/dev/{destination_parts[0]}2"

        copy_partition_data(source, destination, source_pass, destination_pass)

    def copy_partition_data(source_partition, destination_partition, source_pass, destination_pass):
        random_number = random.randint(100000000, 999999999)

        temp_path_source = f"/mnt/partition_data_backup{random_number}"
        temp_path_destination = f"/mnt/destination_partition_temp{random_number}"

        progress_label = tk.Label(frame3, text="Copying Files:")
        progress_label.pack(padx=10, pady=5)
        progress_bar = ttk.Progressbar(frame3, 
                orient=tk.HORIZONTAL, 
                length=300, 
                mode='determinate')
        progress_bar.pack(padx=10, pady=5)

        update_progress(1, 100, progress_bar)
        
        try:
            subprocess.run(["umount", source_partition])
            subprocess.run(["umount", destination_partition])
            
            subprocess.run(["umount", "/dev/mapper/EncHome"])
            subprocess.run(f'cryptsetup luksClose EncHome', shell=True)
            
            subprocess.run(
                    ['cryptsetup', 'luksOpen', 
                    source_partition, 'EncSource'],
                    input=source_pass.encode(),
                    stderr=subprocess.PIPE)
            subprocess.run(
                    ['cryptsetup', 'luksOpen', 
                    destination_partition, 'EncDestination'],
                    input=destination_pass.encode(),
                    stderr=subprocess.PIPE)

            os.makedirs(temp_path_source)
            os.makedirs(temp_path_destination)

            subprocess.run(["mount", 
                    "/dev/mapper/EncSource",
                    temp_path_source])
            subprocess.run(["mount", 
                    "/dev/mapper/EncDestination", 
                    temp_path_destination])
                    
            source_files = os.listdir(temp_path_source)
            total_files = len(source_files)

            for i, filename in enumerate(source_files, 1):
                source_file_path = os.path.join(temp_path_source, filename)
                destination_file_path = os.path.join(
                        temp_path_destination,
                        filename)
                subprocess.run(["cp", "-r", 
                        temp_path_source, 
                        temp_path_destination])
                update_progress(i, total_files)

            subprocess.run(["umount", "/dev/mapper/EncSource"])
            subprocess.run(f'cryptsetup luksClose EncSource', shell=True)

            subprocess.run(["umount", "/dev/mapper/EncDestination"])
            subprocess.run(f'cryptsetup luksClose EncDestination', shell=True)

            os.rmdir(temp_path_source)
            os.rmdir(temp_path_destination)
            
            return

        except Exception as e:
            print(f"Error: {e}")
            return
        
        restart_window(root, "Copying done, please, restrart your computer")
        
    def update_progress(current_value, total_files, progress_bar):
        progress_value = int((current_value / total_files) * 100)
        progress_bar['value'] = progress_value
        root.update_idletasks()
        
    def restart_window(root, text):
        restart_window = tk.Toplevel(root)
        restart_window.title("Success")
            
        restart_label = tk.Label(restart_window, height=10, width=40, text=text)
        restart_label.pack()

        restart_button = tk.Button(restart_window,
                text="Ok",
                command=restart_window.destroy)
        restart_button.pack()

    # Main window
    root = tk.Tk()
    root.title("Ssec managment app")
    root.attributes('-fullscreen', True)
    root.configure(bg='white')

    # Menu Buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=0, column=0, columnspan=4, sticky='ew')

    menu_button1 = ttk.Button(button_frame, 
                    text="Add permitted computer", 
                    style="TMenuButton.TButton",
                    command=lambda: insert_block())
    menu_button2 = ttk.Button(button_frame, 
                    text="MAC address history", 
                    style="TMenuButton.TButton",
                    command=lambda: show_frame(frame2))
    menu_button3 = ttk.Button(button_frame,
                    text="User data copy", 
                    style="TMenuButton.TButton",
                    command=lambda: show_frame(frame3))
    menu_button4 = ttk.Button(button_frame,
                    text="Quit", 
                    style="TMenuButton.TButton",
                    command=lambda: quit_window(root))

    # Packing 
    menu_button1.grid(row=0, column=0, sticky='ew')
    menu_button2.grid(row=0, column=1, sticky='ew')
    menu_button3.grid(row=0, column=2, sticky='ew')
    menu_button4.grid(row=0, column=3, sticky='ew')

    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)
    button_frame.columnconfigure(3, weight=1)

    # Define frames
    frame1 = tk.Frame(root, bg="white")
    frame1.grid(row=1, column=0, padx=20, pady=20, sticky='nsew')
    frame2 = tk.Frame(root, bg="white")
    frame2.grid(row=1, column=0, columnspan=4, sticky='ew')
    frame3 = tk.Frame(root, bg="white")
    frame3.grid(row=1, column=0, columnspan=4, sticky='ew')
    block_frame = tk.Frame(root, bg="white")
    block_frame.grid(row=1, column=0, columnspan=4, sticky='ew')

    get_styles()

    # MAC address input  window
    block_frame_widgets()
    insert_frame_widgets()
    insert_block()

    # MAC history
    history_widgets()

    # Flash disk backup
    flash_disks = get_flash_disks()
    if flash_disks:
        flash_disk_widgets()
    else:
        flash_not_found()

    root.mainloop()

if __name__ == "__main__":
    main()

