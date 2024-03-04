from tkinter import *
import subprocess
from argon2 import PasswordHasher

def find_in_config(section):
    inside_decrypt = False
    with open('/ssec/.ssec.config', 'r') as file:
        for line in file:
            line = line.strip()
            if line == section.strip():
                inside_decrypt = True
                continue
            if inside_decrypt == True:
                return line.strip()

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

def submit():
    input_mac = entry1.get()
    ph = PasswordHasher()
    mac_hash = ph.hash(input_mac.strip()) 
    insert_to_config(mac_hash, '[Identification]\n')
    pop_in_config('Insert\n', '[Ssec insert]\n')
    show_frame(block_frame)

def show_frame(frame):
    frame1.pack_forget()
    frame2.pack_forget()
    frame3.pack_forget()
    frame4.pack_forget()

    frame.pack(padx=50, pady=20)

#Main window and menu buttons
root = Tk()
root.title("Main window")
root.attributes('-fullscreen', True)
root.configure(bg='lightblue')

button_frame = Frame(root)
button1 = Button(button_frame, text="Input MAC address", command=lambda: show_frame(frame1))
button2 = Button(button_frame, text="MAC address history", command=lambda: show_frame(frame2))
button3 = Button(button_frame, text="Reset Ssec", command=lambda: show_frame(frame3))
button4 = Button(button_frame, text="Quit", command=lambda: show_frame(frame4))

button_frame.pack(side="top", fill="x")
button1.pack(side="left", fill="x", expand=True, padx=5, pady=5)
button2.pack(side="left", fill="x", expand=True, padx=5, pady=5)
button3.pack(side="left", fill="x", expand=True, padx=5, pady=5)
button4.pack(side="left", fill="x", expand=True, padx=5, pady=5)

frame3 = Frame(root)
frame4 = Frame(root)

label3 = Label(frame3, text="This is Frame 3")
label4 = Label(frame4, text="This is Frame 4")


#MAC address input  window
input_check = find_in_config('[Ssec insert]')
frame1 = Frame(root)
label1 = Label(frame1, text="Input permitted MAC address")
entry1 = Entry(frame1, bg='lightyellow')
submit_button = Button(frame1, text="Submit", command=submit)

block_frame = Frame(root)
input_block_label = Label(block_frame, text="Inputting blocked, please, insert flash disk into a computer")
input_block_label.pack(padx=20, pady=20)

if input_check == 'Insert':
    show_frame(block_frame)
else:
    entry1.pack()
    submit_button.pack()
    label1.pack(padx=20, pady=20)

#MAC history
frame2 = Frame(root)
label2 = Label(frame2, text="MAC adress history")
log_text = Text(frame2, height=20, width=50)

label2.pack(padx=20, pady=20)
log_text.pack(padx=10, pady=10)

try:
    with open("logfile.txt", "r") as file:
        log_text.delete(1.0, END)
        log_text.insert(END, file.read())
except FileNotFoundError:
    log_text.delete(1.0, END)
    log_text.insert(END, "Log file not found.")

#Reset button

#Quit button

label3.pack(padx=20, pady=20)
label4.pack(padx=20, pady=20)

#Main window
show_frame(frame1)
root.mainloop()
