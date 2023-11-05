from tkinter import *
import subprocess

encrypted_device = '/dev/sdb2'

def submit():
    input_sapp = entry2.get()
    subprocess.run(f'echo "{input_sapp}" | cryptsetup luksOpen {encrypted_device} EncHome', shell=True)
    subprocess.run(f'mount /dev/mapper/EncHome /home', shell=True)
    subprocess.run(f'echo "yes" | rm /ssec/ssec_crypt.txt', shell=True)
    root.quit()

def ok():
    subprocess.run(f'echo "yes" | rm /ssec/ssec_crypt.txt', shell=True)
    root.quit()

root = Tk()
root.attributes('-fullscreen', True)
root.configure(bg='lightblue')

file_path = '/ssec/ssec_crypt.txt'

with open(file_path, 'r') as file:
    first_line = file.readline()
    if first_line.strip() == 'Decrypted':
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

        entry2 = Entry(frame, bg='red')
        entry2.grid(row=1, column=1)

        submit_button = Button(frame, text="Submit", command=submit)
        submit_button.grid(row=2, column=0, columnspan=2)

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

root.mainloop()
