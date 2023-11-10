from tkinter import *
import subprocess

def submit():
    input_mac = entry1.get()
    input_mac.strip()
    subprocess.run(f'echo "{input_mac}" >> /ssec/ssec.config', shell=True)
    root.quit()

root = Tk()
root.attributes('-fullscreen', True)
root.configure(bg='lightblue')

frame = Frame(root)
frame.pack(expand=True, fill="both")

label1 = Label(frame, text="Input permited MAC address: ")
label1.pack()

entry1 = Entry(frame, bg='lightyellow')
entry1.pack()

submit_button = Button(frame, text="Submit", command=submit)
submit_button.pack()

root.mainloop()
