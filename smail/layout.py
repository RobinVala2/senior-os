import logging
import os
import subprocess
import threading
import tkinter as tk
from ttkwidgets import ScrolledListbox
import webbrowser
from tkinter import scrolledtext
import re

from smail.connection.style import (font_config, search_mail,
                                    get_language, button_hover, button_leave,
                                    images, image_config, app_color,
                                    height_config, play_sound, load_json_file, get_email_sender, load_credentials,
                                    load_show_url, load_button_colors)
from smail.connection.mail_connection import (send_email, read_mail,
                                              check_email_for_spam)
from smail.template import guiTemplate as temp
from smail.template import configActions as act

logger = logging.getLogger(__file__)


class one_frame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Background color
        self.background_color = app_color()
        self.configure(bg=self.background_color)

        # Import buttons from GUI template
        self.menu = temp.App(parent)
        self.redefine_template_buttons()
        self.button_state = None

        # Number of displayed lines in textarea and listbox
        (self.number_of_lines_listbox,
         self.number_of_lines_textarea) = height_config(self)

        # Grid configuration
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=3, uniform="a")

        # Frame configuration
        self.l_frame = self.left_frame()
        self.r_frame = self.right_read_frame()

        self.l_frame.grid(
            column=0
        )
        self.r_frame.grid(
            column=1, row=0
        )
        self.pack()

        # Start a background thread to load emails
        self.loading_emails = threading.Thread(target=self.periodic_email_loading)
        self.loading_emails.start()
        self.allow_show_email = True

    def load_emails(self):
        # Function that initializes loading emails
        self.insert_emails()

    def periodic_email_loading(self):
        # Load and insert emails
        while True:
            self.load_emails()
            self.after(10000,self.periodic_email_loading())



    def redefine_template_buttons(self):

        try:
            # Width and height configuration
            self.six_height = temp.resolutionMath()[2]
            self.six_width = temp.resolutionMath()[1]
            num_opt = act.jsonRed('buttons_info', "num_of_opt_on_frame")
            padx_value = act.jsonRed('buttons_info', "padx_value")

            # Calculating the width of each button according to screen width
            self.button_width = int(self.six_width - (padx_value * num_opt))

            # Language configuration
            self.language, self.text = get_language()

            # Image configuration
            self.img = images()
            self.exit_image = tk.PhotoImage(file=self.img["exit"])
            self.person1_image = image_config("Person1", self.six_height)
            self.person2_image = image_config("Person2", self.six_height)
            self.person3_image = image_config("Person3", self.six_height)
            self.person4_image = image_config("Person4", self.six_height)
            self.person5_image = image_config("Person5", self.six_height)
            self.person6_image = image_config("Person6", self.six_height)

        except Exception:
            logger.error("Failed loading language and images")

        try:
            # Access menu 1
            self.options_buttons_crt1 = (
                self.menu.menuFrameCreateButtonsVal.optButtons1
            )

            # Access menu 2
            self.options_buttons_crt2 = (
                self.menu.menuFrameCreateButtonsVal.optButtons2
            )

            # Saving buttons to local variables
            self.exit_button = self.options_buttons_crt1.button_dict[1]
            self.send_mail_person1 = self.options_buttons_crt1.button_dict[2]
            self.send_mail_person2 = self.options_buttons_crt1.button_dict[3]
            self.send_mail_person3 = self.options_buttons_crt1.button_dict[4]
            self.send_mail_person4 = self.options_buttons_crt2.button_dict[1]
            self.send_mail_person5 = self.options_buttons_crt2.button_dict[2]
            self.send_mail_person6 = self.options_buttons_crt2.button_dict[3]
            self.send_mail_to = self.options_buttons_crt2.button_dict[4]
            self.menu_button_1 = (
                self.menu.menuFrameCreateButtonsVal.button_dict)[1]
            self.menu_button_2 = (
                self.menu.menuFrameCreateButtonsVal.button_dict)[2]

            # Audio configuration buttons
            self.audio_configure(self.exit_button, "exitButton")
            self.audio_configure(self.send_mail_person1, "person1")
            self.audio_configure(self.send_mail_person2, "person2")
            self.audio_configure(self.send_mail_person3, "person3")
            self.audio_configure(self.send_mail_person4, "person4")
            self.audio_configure(self.send_mail_person5, "person5")
            self.audio_configure(self.send_mail_person6, "person6")
            self.audio_configure(self.send_mail_to, "sendToButton")
            self.audio_configure(self.menu_button_1, "menu1")
            self.audio_configure(self.menu_button_2, "menu2")

            self.exit_button.config(
                command = self.exit_app,
                image=self.exit_image,
                text="",
                width=self.button_width

            )
            self.send_mail_person1.config(
                command=lambda: self.fill_recipient(1),
                image=self.person1_image,
                text="",
                width=self.button_width
            )
            self.send_mail_person2.config(
                command=lambda: self.fill_recipient(2),
                image=self.person2_image,
                text="",
                width=self.button_width
            )
            self.send_mail_person3.config(
                command=lambda: self.fill_recipient(3),
                image=self.person3_image,
                text="",
                width=self.button_width
            )
            self.send_mail_person4.config(
                command=lambda: self.fill_recipient(4),
                image=self.person4_image,
                text="",
                width=self.button_width
            )
            self.send_mail_person5.config(
                command=lambda: self.fill_recipient(5),
                image=self.person5_image,
                text="",
                width=self.button_width
            )
            self.send_mail_person6.config(
                command=lambda: self.fill_recipient(6),
                image=self.person6_image,
                text="",
                width=self.button_width
            )
            self.send_mail_to.config(
                command=lambda: self.fill_recipient(0),
                text=self.text[f"smail_{self.language}_sendToButton"],
                width=self.button_width
            )

            self.buttons = (self.send_mail_to, self.send_mail_person1, self.send_mail_person2,
                            self.send_mail_person3, self.send_mail_person4, self.send_mail_person5,
                            self.send_mail_person6)

            logger.info("Buttons successfully redefined.")
        except AttributeError:
            logger.error("AttributeError:", exc_info=True)
        except KeyError:
            logger.error("KeyError:", exc_info=True)
        except Exception:
            logger.error("Error:", exc_info=True)

    def exit_app(self):
        self.master.destroy()
        subprocess.run(["kill", "-9", str(os.getpid())])

    def left_frame(self):

        # Fixed non-changing frame with received emails
        self.frame = tk.Frame(self)
        self.frame.configure(bg=self.background_color)

        # Grid configuration
        self.frame.columnconfigure(0, weight=1, uniform="a")
        self.frame.rowconfigure(0, weight=1, uniform="a")

        # Widget configuration
        self.inbox_label = tk.Label(
            self.frame, text=self.text[f"smail_{self.language}_inboxLabel"],
            font=font_config(), bg=self.background_color
        )

        self.inbox_list = ScrolledListbox(
            self.frame, font=font_config(),
            height=self.number_of_lines_listbox,
            activestyle="none", selectmode=tk.SINGLE
        )

        self.inbox_list.listbox.bind("<Enter>", self.activate_show_email)


        # Audio configuration
        self.audio_configure(self.inbox_list, "inbox")
        self.audio_configure(self.inbox_label, "inbox")

        # Widget placement
        self.inbox_label.grid(
            row=0, column=0,
            sticky="nsew", padx=10, pady=10, ipady=5
        )

        self.inbox_list.grid(
            row=1, column=0,
            sticky="nsew", padx=20, pady=20
        )

        logger.info("Created left frame with received emails in listbox.")
        return self.frame

    def activate_show_email(self, event):
        self.allow_show_email = True

    def right_write_frame(self):

        # Stopping phishing alert
        self.stop_alert()

        # Changeable frame
        self.rw_frame = tk.Frame(self)
        self.rw_frame.configure(bg=self.background_color)

        # Grid configuration
        self.rw_frame.columnconfigure((0, 1), weight=1, uniform="a")
        self.rw_frame.rowconfigure((0, 1, 2, 4), weight=1, uniform="a")
        self.rw_frame.rowconfigure(3, weight=2, uniform="a")

        # Widget configuration
        self.recipient_label = tk.Label(
            self.rw_frame,
            text=self.text[f"smail_{self.language}_recipientLabel"],
            font=font_config(), bg=self.background_color
        )

        self.subject_label = tk.Label(
            self.rw_frame,
            text=self.text[f"smail_{self.language}_subjectLabel"],
            font=font_config(), bg=self.background_color
        )

        self.content_label = tk.Label(
            self.rw_frame,
            text=self.text[f"smail_{self.language}_messageLabel"],
            font=font_config(), background=self.background_color
        )

        self.recipient_entry = tk.Entry(
            self.rw_frame, font=font_config()
        )

        self.subject_entry = tk.Entry(
            self.rw_frame, font=font_config()
        )

        self.content_entry = scrolledtext.ScrolledText(
            self.rw_frame, font=font_config(),
            height=self.number_of_lines_textarea
        )

        # Audio configuration
        self.audio_configure(self.recipient_entry, "recipient")
        self.audio_configure(self.recipient_label, "recipient")
        self.audio_configure(self.subject_entry, "subject")
        self.audio_configure(self.subject_label, "subject")
        self.audio_configure(self.content_entry, "write_message")
        self.audio_configure(self.content_label, "write_message")

        # Widget placement
        self.recipient_label.grid(
            row=0, column=0,
            sticky="e", padx=10, pady=10
        )

        self.subject_label.grid(
            row=1, column=0,
            sticky="e", padx=10, pady=10
        )

        self.content_label.grid(
            row=2, column=0,
            sticky="w", padx=10, pady=10
        )

        self.recipient_entry.grid(
            row=0, column=1,
            sticky="nsew", padx=10, pady=10
        )

        self.subject_entry.grid(
            row=1, column=1,
            sticky="nsew", padx=10, pady=10
        )

        self.content_entry.grid(
            row=3, column=0, columnspan=2, rowspan=2,
            padx=10, pady=10, ipady=10, sticky="new"
        )

        return self.rw_frame


    def right_read_frame(self):

        # Changeable frame
        self.rr_frame = tk.Frame(self)
        self.rr_frame.configure(bg=self.background_color)

        # Grid configuration
        self.rr_frame.columnconfigure(0, weight=2, uniform="a")
        self.rr_frame.rowconfigure(0, weight=1, uniform="a")

        # Widget configuration
        self.message_label = tk.Label(
            self.rr_frame,
            text=self.text[f"smail_{self.language}_messageLabel"],
            font=font_config(), bg=self.background_color
        )

        self.message_area = scrolledtext.ScrolledText(
            self.rr_frame, font=font_config(),
            height=self.number_of_lines_listbox
        )

        # Audio configuration
        self.audio_configure(self.message_area, "read_message")
        self.audio_configure(self.message_label, "read_message")

        # Widget placement
        self.message_label.grid(
            row=0, column=0, ipady=5,
            sticky="nsew", padx=10, pady=10
        )

        self.message_area.grid(
            row=1, column=0,
            sticky="nsew", padx=20, pady=20
        )

        return self.rr_frame

    def insert_emails(self):

        # Check if there is a change in emails before updating the inbox
        previous_emails = getattr(self, "reversed_list", [])

        # Get information from configuration file
        login, password, smtp_server, smtp_port, imap_server, imap_port = load_credentials("../sconf/SMAIL_config.json")
        language, text = get_language()

        # Getting emails from inbox
        self.emails, self.subject = read_mail(login, password, imap_server, imap_port, language, text)
        # Reversing emails - new emails will be on top of the listbox
        self.reversed_list = self.emails[::-1]

        # If there are changes in emails insert new emails into the inbox
        if previous_emails != self.reversed_list:
            try:
                # Filtering emails
                self.safe_emails, self.phish_emails = check_email_for_spam(self.reversed_list)
            except Exception:
                # In case filtering fails, all emails will be displayed
                self.safe_emails = self.reversed_list
                logger.critical("Failed to apply anti-phishing filters. Omitting security steps.", exc_info=True)

            # Inserting emails into the listbox,
            # for now safe_emails and phish_emails are separated
            self.inbox_list.listbox.delete(0, tk.END)
            print("Clearing the listbox")

            self.all_emails = self.safe_emails + self.phish_emails
            self.all_emails.sort(key=lambda x: x[1])
            self.tagged_emails = []

            for email_content, index, safe in self.all_emails:
                name = get_email_sender(email_content.split("\n")[1])
                sub = email_content.split("\n")[0].split(":", 1)[1]
                email_type = "Safe" if index in [i[1] for i in self.safe_emails] else "Phish"
                self.inbox_list.listbox.insert(tk.END, f"{name} - {sub}")
            # Binding listbox to text area to view email

            self.inbox_list.listbox.bind("<<ListboxSelect>>", self.show_email)

    def show_email(self, event):
        # If allow_show_email is not allowed, email will not be displayed
        if not self.allow_show_email:
            return
        # Switch frames to the reading frame
        self.switch_to_reading_mail()

        if not self.inbox_list.listbox.curselection():
            if (self.last_selected_index is not None
                    and self.last_selected_email is not None):
                self.configure_message_area(self.last_selected_email)
                return

        # Get the selected index from the listbox
        try:
            selected_index = self.inbox_list.listbox.curselection()[0]
        except IndexError:
            print("Index out of range.")
            return

        # Get the selected email based on the sorted combined list
        selected_email = self.all_emails[selected_index]
        if selected_email[2] == "phish":
            self.alert_buttons()
        else: self.stop_alert()

        # Configure the message area with the selected email content
        self.configure_message_area(selected_email[0])

        # Update the last selected index and email
        self.last_selected_index = selected_index
        self.last_selected_email = selected_email[0]



    def configure_message_area(self, email):

        # Inserting email into text area
        self.message_area.configure(state="normal")
        self.message_area.delete("1.0", tk.END)
        self.display_email(email)
        self.message_area.configure(state="disabled")

    def display_email(self, email):

        # Display the entire email content in the text area
        self.message_area.insert(tk.END, email)
        self.mark_email()

    def mark_email(self):

        show = load_show_url("../sconf/SMAIL_config.json")

        if show == 1:
            # Find all URLs in email and tag them
            for match in re.finditer(r'https?://\S+|www\.\S+', self.message_area.get("1.0", tk.END)):
                url = match.group()
                self.mark_and_link_url(url)

    def mark_and_link_url(self, url):

        # Assign name to URL and bind it for click event
        start_pos = "1.0"
        while True:
            start_index = self.message_area.search(url, start_pos, tk.END)
            # If there are no other URLs break
            if not start_index:
                break

            # Calculating the end of URL
            end_index = f"{start_index}+{len(url)}c"
            # Creating an original name for the URL: replacing . with _ to make the name valid
            tag_name = f"clickable_{start_index.replace('.', '_')}"

            # Name and URL config
            self.message_area.tag_add(tag_name, start_index, end_index)
            self.message_area.tag_config(tag_name, foreground="blue", underline=True)
            self.message_area.tag_bind(tag_name, "<Button-1>", lambda event, u=url: self.open_browser(event, u))

            start_pos = end_index

    def open_browser(self, event, url):
        # Open web browser when clicking on a URL.
        try:
            subprocess.run(["python3", "../sweb/main.py", url])
            self.exit_app()
        except Exception as e:
            webbrowser.open_new(url)
            logger.error("Failed to open sweb.")

    def alert_buttons(self):

        # Changing the color of all buttons to red,
        # playing warning sound.
        self.exit_button.config(
            bg = "red"
        )
        self.send_mail_person1.config(
            bg = "red"
        )
        self.send_mail_person2.config(
            bg="red"
        )
        self.send_mail_person3.config(
            bg="red"
        )
        self.send_mail_person4.config(
            bg="red"
        )
        self.send_mail_person5.config(
            bg="red"
        )
        self.send_mail_person6.config(
            bg="red"
        )
        self.send_mail_to.config(
            bg="red"
        )
        self.menu_button_1.config(
            bg="red"
        )
        self.menu_button_2.config(
            bg="red"
        )
        play_sound("alert")

    def stop_alert(self):

        # Switching the background color of each button back to default value.
        default_color, selected_color = load_button_colors("../sconf/config_old.json")

        self.exit_button.config(
            bg=default_color
        )
        self.send_mail_person1.config(
            bg=default_color
        )
        self.send_mail_person2.config(
            bg=default_color
        )
        self.send_mail_person3.config(
            bg=default_color
        )
        self.send_mail_person4.config(
            bg=default_color
        )
        self.send_mail_person5.config(
            bg=default_color
        )
        self.send_mail_person6.config(
            bg=default_color
        )
        self.send_mail_to.config(
            bg=default_color
        )
        self.menu_button_1.config(
            bg=default_color
        )
        self.menu_button_2.config(
            bg=default_color
        )

    def switch_to_reading_mail(self):

        # Switching frame
        self.r_frame = self.right_read_frame()
        self.r_frame.grid(
            column=1, row=0
        )
        self.pack()

    def switch_to_write_mail(self):

        # Switching frame
        self.r_frame = self.right_write_frame()

        self.r_frame.grid(
            column=1, row=0
        )
        self.pack()
        return self.recipient_entry

    def send_email_status(self):

        # Getting information from configuration file
        login, password, smtp_server, smtp_port, imap_server, imap_port = load_credentials("../sconf/SMAIL_config.json")

        # Sending email
        status = send_email(
            self.recipient_entry.get(), self.subject_entry.get(),
            self.content_entry.get("1.0", tk.END), login, password, smtp_server, smtp_port
        )

        # If successful, all entries are deleted
        if status == 1:
            self.recipient_entry.delete(0, tk.END)
            self.subject_entry.delete(0, tk.END)
            self.content_entry.delete("1.0", tk.END)

    def fill_recipient(self, id):

        # Disable showing email in text area
        self.allow_show_email = False

        if self.r_frame == self.rr_frame:
            self.r_frame = self.right_write_frame()
        # If every Entry obtains text, message will be sent
        # when pressing Person[id] button for the second time.
        if (self.recipient_entry.get() and self.subject_entry.get() and
                self.content_entry.get("1.0", tk.END).strip() and
                id == self.button_state):
            self.send_email_status()

        # If another Person[id] button is pressed:
        # entries will be deleted,
        # new recipient entry will be filled in.
        elif (self.subject_entry.get() or
              self.content_entry.get("1.0", tk.END).strip()):
            if id != self.button_state:
                print("No content to send.")
                email = search_mail(id)
                recipient = self.switch_to_write_mail()
                recipient.delete(0, tk.END)
                recipient.insert(0, email)
                recipient.configure(state="disabled")

            # If Person[id] button is pressed for the second time,
            # but one of the entry is not filled in, nothing will happen
            else:
                print("one of the entries is not filled in.")

        else:
            # If Send To button is pressed, frame is switched and
            # recipient entry is deleted.
            if id == 0:
                print("Send To button pressed")
                recipient = self.switch_to_write_mail()
                recipient.delete(0, tk.END)
            # If Person[id] button is pressed for the second time,
            # but none of the entry is filled in.
            else:
                print("Button pressed for the second time,"
                      " no entry is filled in.")
                email = search_mail(id)
                recipient = self.switch_to_write_mail()
                recipient.delete(0, tk.END)
                recipient.insert(0, email)
                recipient.configure(state="disabled")

        self.button_state = id

        default_color, select_color = load_button_colors("../sconf/config_old.json")

        for button in self.buttons:
            button.config(bg = default_color)
        self.buttons[id].config(bg = select_color)

    def audio_configure(self, button, button_name):

        enter_time = [None]
        # This event is triggered when the mouse cursor enters the button.
        button.bind("<Enter>",
                    lambda event, name=button_name,
                    et=enter_time: button_hover(button, name, et)
                    )
        # This event is triggered when the mouse cursor leaves the button.
        button.bind("<Leave>",
                    lambda event, et=enter_time: button_leave(button, et)
                    )
