from argon2 import PasswordHasher

import tkinter as tk
from tkinter import ttk

import re
import subprocess
import os
import base64
from datetime import datetime

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

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
    try:
        with open("/ssec/.ssec.config", "r") as f:
            content = f.readlines()
        except IOError:
            return
     
    insert_index = content.index(insert_section)+1
    content.pop(insert_index)
    content.insert(insert_index, insert_text)
    
    if len(content) == 0:
        return
    
    with open("/ssec/.ssec.config", "w") as f:
        f.writelines(content)

def insert_to_config(insert_text, insert_section):
    try:
        with open("/ssec/.ssec.config", "r") as f:
            content = f.readlines()
        except IOError:
            return
            
    insert_index = content.index(insert_section)+1
    content.insert(insert_index, insert_text+'\n')

    if len(content) == 0:
        return

    with open(conf_path, "w") as f:
        f.writelines(content)

def find_encrypted_device():
    try:
        output = subprocess.check_output(
                ["lsblk", "-o", "NAME,VENDOR,MODEL", "-d", "-n"]).decode(
                "utf-8").splitlines()
        encrypted_device = ""
        for line in output:
            if "sd" in line:
                flash_name = find_in_config("[Flash name]")
                if flash_name.replace(" ", "").lower() in line.replace(" ", "").lower():
                    parts = line.split()
                    encrypted_device = f"/dev/{parts[0]}2"
        return encrypted_device
    except:
        return "/dev/sdb2" 

def error_window(root, error_text):
    error_window = tk.Toplevel(root)
    error_window.title("Error")
        
    error_label = tk.Label(error_window, height=10, width=40, text=error_text)
    error_label.pack()

    close_button = tk.Button(error_window,
            text="Close",
            command=error_window.destroy)
    close_button.pack()

def get_key():
    subprocess.run(
            f'cat /sys/class/dmi/id/product_uuid > /ssec/ssec_uuid.txt',
            shell=True)
    uuid_path = '/ssec/ssec_uuid.txt'
    with open(uuid_path, 'r') as file:
        uuid = file.readline().strip().replace('-', '')
    subprocess.run(f'echo "yes" | rm /ssec/ssec_uuid.txt', shell=True)
    return uuid.encode('utf-8')

def mac_address_function():
    subprocess.run(
            f"cat /sys/class/net/*/address | awk 'NR==1 {{print; exit}}'"+
            "> /ssec/ssec_tmp.txt 2>/ssec/ssec_err.log", shell=True)
    tmp_path = '/ssec/ssec_tmp.txt'
    with open(tmp_path, 'r') as file:
        computer_mac = file.readline().strip()
    subprocess.run(f'echo "yes" | rm /ssec/ssec_tmp.txt '+
            '2>/ssec/ssec_err.log', shell=True)
    return computer_mac

def error_function(error_text):
    err_path = "/ssec/ssec_err.log"
    with open(err_path, "a") as f:
        f.write(error_text)

def quit_window(root):
    root.quit()

def get_styles():        
    menu_button_style = ttk.Style()
    menu_button_style.configure("TMenuButton.TButton",
            padding=40,
            font=("Helvetica", 12),
            borderwidth=4,
            relief="solid",
            height=4,
            weight=1,
            background="white")
    menu_button_style.map("TMenuButton.TButton",
            background=[("active", "#CCCCCC")])

    entry_style = ttk.Style()
    entry_style.configure('Custom.TEntry',
            padding=20,
            borderwidth=4,
            weight=1,
            relief='solid')
