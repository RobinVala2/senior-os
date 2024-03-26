import customtkinter
from customtkinter import filedialog
from screeninfo import get_monitors
import sgive.src.CaregiverApp.configurationActions as ryuConf
import logging
import os
import re  # regex

#  from functools import lru_cache

"""
Author: RYUseless
Github: https://github.com/RYUseless
"""
Version = "0.1.1(Alpha)"  # lmao the most useless thing ever :)

logger = logging.getLogger(__file__)
logger.info("initiated logging")

# restore global config, if there is non:
fullpath = os.getcwd()
path_split = fullpath.split("sgive")
config_folder = os.path.join(path_split[0], "sconf")
if not (os.path.exists(config_folder) and os.path.isfile(os.path.join(config_folder, "config.json"))):
    ryuConf.main_config_default(config_folder)

_colorScheme = ryuConf.red_main_config("GlobalConfiguration", "colorMode")
customtkinter.set_appearance_mode(_colorScheme)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


class FrameElements:
    def __init__(self, frame_root, original_width, original_height, frame_name):
        self.master = frame_root
        self.original_width = original_width
        self.original_height = original_height
        self.font_family = ryuConf.red_main_config("GlobalConfiguration", "fontFamily")
        self.widget_font_size = ryuConf.red_main_config("GlobalConfiguration", "fontSize")
        self.font_weight = ryuConf.red_main_config("GlobalConfiguration", "fontThickness")
        self.menu_font_size = ryuConf.red_main_config("GlobalConfiguration", "controlFontSize")
        self.current_menu_font_size = self.menu_font_size
        self.label_font_size = self.widget_font_size * 1.65
        self.current_label_font = self.label_font_size
        self.current_widget_font = self.widget_font_size
        self.label_names = ryuConf.red_main_config("careConf", frame_name)
        self.percentage_above = 0
        # for true original fullscreen sizes:
        screenNum = ryuConf.red_main_config("GlobalConfiguration", "numOfScreen")
        self.screenWidth = get_monitors()[screenNum].width  # screen width_frame
        self.screenHeight = get_monitors()[screenNum].height  # screen height
        self.heightDivisor = ryuConf.red_main_config("GUI_template", "height_divisor")

    def is_window_resized(self, widgets_array):
        """checking if window is in resized down or if it isn't,
                  because resize event isn't triggered when I resize down and switch frame"""
        real_width = self.master.winfo_width()
        real_height = self.master.winfo_height()
        self.master.update_idletasks()
        # real_height = self.master.winfo_height()
        if self.screenWidth > real_width and self.screenHeight > real_height:
            self.original_width = self.screenWidth
            self.original_height = self.screenHeight - (self.screenHeight / self.heightDivisor)
            self.resize_font(widgets_array)
            self.resize_widgets(widgets_array)

    def get_correct_size(self):
        self.master.update()
        if ((not self.original_height < self.master.winfo_height())
                or (not self.original_width < self.master.winfo_width())):
            self.original_height = self.master.winfo_height()
            self.original_width = self.master.winfo_width()

        widget_height = int(self.original_height * ((10 / 11) / len(self.label_names)) + 1)
        return widget_height

    def resize_widgets(self, widgets_array):
        height_frame = self.master.winfo_height()
        width_frame = self.master.winfo_width()

        widget_height = height_frame * ((10 / 11) / len(self.label_names))
        # rounding up
        widget_height = int(widget_height + 1)
        label_width = width_frame * (2 / 5)
        button_width = width_frame * (1 / 5)

        for widget_list in widgets_array:
            for name, widget in widget_list.items():
                if isinstance(widget, customtkinter.CTkLabel):
                    widget.configure(width=label_width, height=widget_height)
                elif isinstance(widget, customtkinter.CTkEntry):
                    widget.configure(width=label_width - 2, height=widget_height - 2)
                elif isinstance(widget, customtkinter.CTkButton):
                    if name == "picture0":  # this button needs to be 2/5 in length
                        widget.configure(width=label_width - 2, height=widget_height - 2)
                    elif name == "restore_widget" or name == "refresh_widget":
                        widget.configure(width=label_width - 2, height=widget_height - 2, anchor=customtkinter.CENTER)
                    else:
                        widget.configure(width=button_width - 2, height=widget_height - 2)
                else:
                    print("Instance jinačího typu:", type(widget))

    def resize_font(self, widgets_array):
        new_height = self.master.winfo_height()
        new_width = self.master.winfo_width()

        if new_height != self.original_height or new_width != self.original_width:
            percentage_change = float(new_height / self.original_height)

            # if new percentil is above 100 (1.0), for next run I need amount above 100%
            if percentage_change > float(1.0) and new_width == self.original_width:
                self.percentage_above = percentage_change - 1
            else:
                percentage_change = percentage_change + self.percentage_above
                self.percentage_above = 0  # just in case

            if new_height < self.original_height and new_height != 1:
                self.current_widget_font = int(self.current_widget_font * percentage_change)
                self.current_label_font = int(self.label_font_size * percentage_change)
                self.current_menu_font_size = int(self.current_menu_font_size * percentage_change)
            else:
                self.current_widget_font = int(self.widget_font_size)
                self.current_label_font = int(self.label_font_size)
                self.current_menu_font_size = int(self.menu_font_size)

            new_label_font = (self.font_family, self.current_label_font * 1.05, self.font_weight)
            new_widget_font = (self.font_family, self.current_widget_font, self.font_weight)
            new_menu_font = (self.font_family, self.current_menu_font_size, self.font_weight)

            self.original_height = new_height
            self.original_width = new_width

            for widget_list in widgets_array:
                for key, widget in widget_list.items():
                    if isinstance(widget, customtkinter.CTkLabel):
                        widget.configure(font=new_label_font)
                    elif isinstance(widget, customtkinter.CTkButton) or isinstance(widget, customtkinter.CTkEntry):
                        if key == "restore_widget" or key == "refresh_widget":
                            widget.configure(font=new_menu_font)
                        else:
                            widget.configure(font=new_widget_font)
                    else:
                        print(f"Widget is in unsuspected type ({type(widget)}), skipping.")

    def create_labels(self, height_widget):
        labels = {}
        font_label = (self.font_family, self.label_font_size, self.font_weight)
        y_position = float(0)
        for name in self.label_names:
            labels[name] = customtkinter.CTkLabel(self.master,
                                                  text=name,
                                                  font=font_label,
                                                  width=self.original_width * (2 / 5),
                                                  height=height_widget,
                                                  fg_color=("#D3D3D3", "#171717")
                                                  )
            labels[name].place(relx=0, rely=y_position * (10 / 11))
            y_position += 1 / len(self.label_names)
        return labels


class LogsFrameWidgets:
    def __init__(self, frame_root, width, height):
        logger.info("Creating and showing frame for viewing Logs.")
        self.master = frame_root
        self.height = height
        self.width = width
        self.log_filter = None
        self.log_file = None

        self.options_toolbar_frame = customtkinter.CTkFrame(frame_root)
        self.options_toolbar_frame.pack_propagate(False)
        self.options_toolbar_frame.configure(width=width, height=height * 0.10,
                                             fg_color=("#dbd9d9", "#222222"))

        self.options_toolbar_frame.pack(side=customtkinter.TOP)
        self.log_file_choice = None
        self.log_files_names = []
        self.toolbar_buttons = {}
        self.textbox = None

        self.find_log_files()
        self.options_toolbar()
        self.log_textbox(None)

        self.master.bind("<Configure>", lambda event: self.resize_event_handler())

    def resize_event_handler(self):
        new_width = self.master.winfo_width()
        new_height = self.master.winfo_height()
        self.width = new_width
        self.height = new_height
        self.options_toolbar_frame.configure(width=new_width, height=new_height * 0.10)
        for widget_object in self.toolbar_buttons:
            self.toolbar_buttons[widget_object].configure(height=new_height * 0.10,
                                                          width=new_width * (1 / 5))

        self.textbox.configure(height=self.height - (self.height * 0.10),
                               width=self.width)

    def refresh(self):
        for widget in self.options_toolbar_frame.winfo_children():  # for toolbar widgets
            widget.pack_forget()
            widget.place_forget()
        for frame in self.master.winfo_children():  # for log text widget
            frame.place_forget()
        self.options_toolbar()
        self.log_textbox(None)

    def find_log_files(self):
        relative_path = "../../../../senior-os/sconf/logs/"
        # Relativní cesta k hledané složce, skipuje deep dive do diru, který má tento .py
        base_path = os.path.abspath(relative_path)

        if os.path.exists(base_path):  # Zkontroluje, zda složka existuje
            for entry in os.listdir(base_path):  # Prochází všechny položky ve složce
                full_path = os.path.join(base_path, entry)
                if os.path.isfile(full_path) and entry.endswith(".log"):  # Pokud je položka soubor s příponou .log
                    self.log_files_names.append(entry)
        else:
            logger.error("There is no folder named: \"/sconf/logs\" in senior-os.")
            return

    def option_menu_call(self, choice):
        print("Selected option:", choice)
        self.log_file_choice = choice  # for the self.option_filter_Call() function
        # call
        self.log_textbox(choice)

    def option_filter_call(self, choice):
        print("Selected option:", choice)
        if choice == "ALL":
            self.log_filter = None
        else:
            self.log_filter = choice
        # call
        self.log_textbox(self.log_file_choice)

    def options_toolbar(self):
        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontSize") * 0.80,
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))
        # pick log folder:
        for widget in range(3):
            if widget < 2:
                self.toolbar_buttons[widget] = customtkinter.CTkOptionMenu(master=self.options_toolbar_frame,
                                                                           corner_radius=0,
                                                                           height=self.height * 0.10,
                                                                           width=self.width * (1 / 5),
                                                                           font=font_value,
                                                                           fg_color=("#636363", "#454444"),
                                                                           button_color=("#3b3b3b", "#5c5b5b"),
                                                                           button_hover_color=("#292828", "#6b6a6a"),
                                                                           dropdown_font=font_value,
                                                                           anchor=customtkinter.CENTER
                                                                           )
                self.toolbar_buttons[widget].pack(side=customtkinter.LEFT, fill=customtkinter.Y)
            else:
                self.toolbar_buttons[widget] = customtkinter.CTkButton(master=self.options_toolbar_frame,
                                                                       height=self.height * 0.10,
                                                                       corner_radius=0,
                                                                       width=self.width * (1 / 5),
                                                                       fg_color=("#636363", "#454444"),
                                                                       hover_color=("#757474", "#6b6a6a"),
                                                                       text="Refresh",
                                                                       font=font_value,
                                                                       command=lambda: self.refresh()
                                                                       )
                self.toolbar_buttons[widget].pack(side=customtkinter.RIGHT, fill=customtkinter.Y)

        # first option menu button
        folderOption_var = customtkinter.StringVar(value="Choose log file")
        self.toolbar_buttons[0].configure(values=self.log_files_names, variable=folderOption_var,
                                          command=self.option_menu_call)
        # second option menu button
        filter_options = ["INFO", "WARNING", "CRITICAL", "ERROR", "ALL"]
        filterOption_var = customtkinter.StringVar(value="Choose log filter")
        self.toolbar_buttons[1].configure(values=filter_options, variable=filterOption_var,
                                          command=self.option_filter_call)

    def log_textbox(self, choice):
        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontSize") * 0.80)
        self.textbox = customtkinter.CTkTextbox(self.master)
        self.textbox.configure(height=self.master.winfo_height() - (self.master.winfo_height() * 0.10),
                               width=self.master.winfo_width(),
                               font=font_value,
                               fg_color=("#D3D3D3", "#171717"),
                               scrollbar_button_color=("black", "white"),
                               scrollbar_button_hover_color=("#3b3b3b", "#636363"),
                               )
        self.textbox.place(relx=0, rely=1 * 0.10)
        file = ryuConf.read_log(self.log_filter, choice)
        if file is None:
            self.textbox.insert(customtkinter.END, "No log file was selected, nothing to show ...")
        else:
            for f in file:
                self.textbox.insert(customtkinter.END, f)
        self.textbox.configure(state="disabled")  # disable editing


class WebFrameWidgets:
    def __init__(self, frame_root, width, height_frame, restore, refresh):
        logger.info("Creating and showing frame for Web configuration.")
        self.master = frame_root
        self.height_frame = height_frame
        self.height_frame_origin = height_frame
        self.width_frame_origin = width
        self.width_frame = width
        self.action_widgets = {"restore_widget": restore, "refresh_widget": refresh}
        self.label_names = ryuConf.red_main_config("careConf", "SwebFrameLabels")
        self.url_web = 1
        self.url_allowed = 1
        self.dummy_counter = 1
        # lists: --------------------
        self.widget_entry = {}
        self.widget_btn = {}
        self.submit_btn = {}
        self.picture_btn = {}
        # CALLS: --------------------
        resize_event_instance = FrameElements(frame_root, width, height_frame, "SwebFrameLabels")
        self.height_widget = resize_event_instance.get_correct_size()
        self.labels = resize_event_instance.create_labels(self.height_widget)
        widget_list_array = [self.widget_entry, self.widget_btn, self.submit_btn, self.picture_btn, self.labels,
                             self.action_widgets]
        self.create_widgets()
        resize_event_instance.is_window_resized(widget_list_array)
        # event for resizing:
        self.master.bind("<Configure>",
                         lambda _: [resize_event_instance.resize_font(widget_list_array),
                                    resize_event_instance.resize_widgets(widget_list_array)])

    def entry_update(self, entry_id):
        url_pattern = r'https?://(?:www\.)?[\w\.-]+\.\w+'
        user_input = self.widget_entry[f"entry:{entry_id}"].get()
        entry_key = {
            0: "url_web",
            1: "url_allowed",
        }

        if entry_id == 0:
            self.dummy_counter = self.url_web
        else:
            self.dummy_counter = self.url_allowed

        if re.match(url_pattern, user_input):
            if self.dummy_counter == 6:
                self.dummy_counter = 1
                self.submit_btn[f"submit:{entry_id}"].configure(text=f"Add URL {self.dummy_counter}")
            else:
                self.submit_btn[f"submit:{entry_id}"].configure(text=f"Add URL {self.dummy_counter + 1}")
                self.dummy_counter += 1

            print("URL value for:", entry_key.get(entry_id, entry_id))

            if entry_id == 0:
                self.url_web = self.dummy_counter
            else:
                self.url_allowed = self.dummy_counter
            return
        else:
            print("URL není platná")

    def buttons_update(self, button_name):
        selected_button = ryuConf.red_main_config("GlobalConfiguration", "hoverColor")
        sel_btn_hover = ryuConf.red_main_config("GlobalConfiguration", "hoverColorLighten")
        button_name_split = button_name.split(":")
        """
        I do selected button change like this, because at start, i dont know which button is selected, so i just
        restore both and then select value that triggered this function (Bit of redundant)
        """
        for numero in range(2):
            btn_key = f"{button_name_split[0]}:{numero}"
            self.widget_btn[btn_key].configure(fg_color=("#636363", "#222222"),
                                               hover_color=("#757474", "#3b3b3b"))
        self.widget_btn[button_name].configure(fg_color=(selected_button, selected_button),
                                               hover_color=(sel_btn_hover, sel_btn_hover))

    def create_widgets(self):
        font_entry = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontSize"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))

        entry_text = {
            0: "Add full URL for website  (Up to six) →",
            1: "Add full URL for enabled website →",
        }

        for entry_widget in range(2):
            self.widget_entry[f"entry:{entry_widget}"] = customtkinter.CTkEntry(self.master,
                                                                                placeholder_text=entry_text.get(
                                                                                    entry_widget,
                                                                                    entry_widget),
                                                                                font=font_entry,
                                                                                width=self.width_frame * (2 / 5) - 2,
                                                                                height=self.height_widget - 2,
                                                                                border_width=0,
                                                                                corner_radius=0
                                                                                )
            self.submit_btn[f"submit:{entry_widget}"] = customtkinter.CTkButton(self.master,
                                                                                text="Add URL 1",
                                                                                font=font_entry,
                                                                                width=self.width_frame * (1 / 5) - 2,
                                                                                height=self.height_widget - 2,
                                                                                fg_color=("#636363", "#222222"),
                                                                                hover_color=("#757474", "#3b3b3b"),
                                                                                border_width=0,
                                                                                corner_radius=0,
                                                                                command=lambda btn_id=entry_widget:
                                                                                self.entry_update(btn_id)
                                                                                )
        self.picture_btn["picture0"] = customtkinter.CTkButton(self.master,
                                                               text="Add picture for selected URL → ",
                                                               font=font_entry,
                                                               width=self.width_frame * (2 / 5) - 2,
                                                               height=self.height_widget - 2,
                                                               fg_color=("#636363", "#222222"),
                                                               hover_color=("#757474", "#3b3b3b"),
                                                               border_width=0,
                                                               corner_radius=0
                                                               )
        self.picture_btn["submit"] = customtkinter.CTkButton(self.master,
                                                             text="First URL",
                                                             font=font_entry,
                                                             width=self.width_frame * (1 / 5) - 2,
                                                             height=self.height_widget - 2,
                                                             fg_color=("#636363", "#222222"),
                                                             hover_color=("#757474", "#3b3b3b"),
                                                             border_width=0,
                                                             corner_radius=0
                                                             )
        button_name = {
            0: ["phishing_warning:0", "Disable"],
            1: ["phishing_warning:1", "Enable"],
            2: ["phishing_formular:0", "Disable"],
            3: ["phishing_formular:1", "Enable"],
            4: ["website_posting:0", "Disable"],
            5: ["website_posting:1", "Enable"],
        }
        for button_widget in range(6):
            name = button_name.get(button_widget, button_widget)
            self.widget_btn[name[0]] = customtkinter.CTkButton(self.master,
                                                               text=name[1],
                                                               font=font_entry,
                                                               width=self.width_frame * (1 / 5) - 2,
                                                               height=self.height_widget - 2,
                                                               fg_color=("#636363", "#222222"),
                                                               hover_color=("#757474", "#3b3b3b"),
                                                               border_width=0,
                                                               corner_radius=0,
                                                               command=lambda button_id=name[0]:
                                                               self.buttons_update(button_id)
                                                               )
        # show widgets:
        self.show_widgets(button_name)

    def show_widgets(self, button_name):
        y_position = float(0)
        x_position = float(1 * (2 / 5))

        # first entry website URL
        self.widget_entry["entry:0"].place(relx=x_position, rely=y_position * (10 / 11))
        self.submit_btn["submit:0"].place(relx=x_position + 1 * (2 / 5), rely=y_position * (10 / 11))
        y_position += 1 / len(button_name)
        self.picture_btn["picture0"].place(relx=x_position, rely=y_position * (10 / 11))
        self.picture_btn["submit"].place(relx=x_position + 1 * (2 / 5), rely=y_position * (10 / 11))
        y_position += 1 / len(button_name)

        # buttons choice: send phishing, phishing formular, website posting
        buttons_in_row = 1
        for _, widget_btn in self.widget_btn.items():
            if buttons_in_row == 1:
                widget_btn.place(relx=x_position, rely=y_position * (10 / 11))
                x_position += 1 * (1 / 5)
                buttons_in_row += 1
            else:
                widget_btn.place(relx=x_position, rely=y_position * (10 / 11))
                y_position += 1 / len(button_name)
                x_position = 1 * (2 / 5)
                buttons_in_row = 1
        # website posting
        self.widget_entry["entry:1"].place(relx=x_position, rely=y_position * (10 / 11))
        self.submit_btn["submit:1"].place(relx=x_position + 1 * (2 / 5), rely=y_position * (10 / 11))


class MailFrameWidgets:
    """
    This class creates widgets, that are visible in SMAIL configuration frame
    The frame itself isn't created here, it's created in Frames class, as other frames are
    """

    def __init__(self, frame_root, width, height_frame, restore, refresh):
        logger.info("Creating and showing frame for Mail configuration.")
        self.master = frame_root
        self.height_frame = height_frame
        self.width_frame = width
        self.label_names = ryuConf.red_main_config("careConf", "SMailFrameLabels")
        self.hover_alert_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")
        self.action_widgets = {"restore_widget": restore, "refresh_widget": refresh}

        # ------
        self.person_counter = 1  # counter for person name key
        self.filedialog_counter = 1
        self.button_height_fract = 11
        self.entry_widgets = {}
        self.submit_entry_btn = {}
        self.caregiver_warning = {}
        self.url_link = {}
        self.choose_pictures = {}
        self.filename_picture = None
        self.combo_x = 0
        self.combo_y = 0
        # -----------------
        # calls:
        resize_event_instance = FrameElements(frame_root, width, height_frame, "SMailFrameLabels")
        self.widget_height = resize_event_instance.get_correct_size()
        self.labels = resize_event_instance.create_labels(self.widget_height)
        widget_list_array = [self.labels, self.entry_widgets, self.submit_entry_btn, self.caregiver_warning,
                             self.url_link, self.choose_pictures, self.action_widgets
                             ]
        self.create_widgets()
        self.load_defaults()
        resize_event_instance.is_window_resized(widget_list_array)
        # resize events:
        self.master.bind("<Configure>",
                         lambda _: resize_event_instance.resize_font(widget_list_array))
        self.master.bind("<Configure>",
                         lambda _: resize_event_instance.resize_widgets(widget_list_array))

    def load_defaults(self):
        value_mapping = {1: "Enable", 0: "Disable"}
        load_hover = ryuConf.red_main_config("GlobalConfiguration", "hoverColor")
        hover_color = (load_hover, load_hover)
        load_lighten = ryuConf.red_main_config("GlobalConfiguration", "hoverColorLighten")
        hover_color_lighten = (load_lighten, load_lighten)

        resend_email = ryuConf.read_smail_config(None, "resend_email")
        resend_email = value_mapping.get(resend_email, resend_email)
        self.caregiver_warning[resend_email].configure(fg_color=hover_color, hover_color=hover_color_lighten)

        show_url = ryuConf.read_smail_config(None, "show_url")
        show_url = value_mapping.get(show_url, show_url)
        self.url_link[show_url].configure(fg_color=hover_color, hover_color=hover_color_lighten)

        email_entry = ryuConf.read_smail_config("credentials", "username")
        caregiver_entry = ryuConf.read_smail_config(None, "guardian_email")

        entry_placeholderText_values = [f"Enter here (current: {email_entry})",
                                        "Add senior's password here",
                                        f"Enter here (current: {caregiver_entry})",
                                        "Use: <name>@<domain.name>"]

        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontSize"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))
        for index, value in enumerate(entry_placeholderText_values):
            self.entry_widgets[index].configure(placeholder_text=value,
                                                font=font_value)

    @staticmethod
    def update_buttons_widget(key, name, value, button_id, button_list):
        # I refuse to do two if statements here, so this is where we land at
        # Mapping for "Enable" and "Disable" to 1 and 0 respectively
        value_mapping = {"Enable": 1, "Disable": 0}
        value = value_mapping.get(value, value)

        # return all buttons to their default color
        for all_widgets in button_list.values():
            all_widgets.configure(fg_color=("#636363", "#222222"),
                                  hover_color=("#757474", "#3b3b3b"))

        hover_color = ryuConf.red_main_config("GlobalConfiguration", "hoverColor")
        hover_color_lighter = ryuConf.red_main_config("GlobalConfiguration", "hoverColorLighten")
        alert_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")

        return_value = ryuConf.edit_smail_config(key, name, value)
        if return_value:
            button_list[button_id].configure(fg_color=(hover_color, hover_color),
                                             hover_color=(hover_color_lighter, hover_color_lighter))
            print(f"Updated smail config: {name}, changed value is: {value}")
        else:
            print("Some error occurred.")
            button_list[button_id].configure(fg_color=(alert_color, alert_color),
                                             hover_color=(alert_color, alert_color))

    def update_entry_widgets(self, email_val, entry_type, button_id):
        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontSize"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))
        hv_col = ryuConf.red_main_config("GlobalConfiguration", "hoverColor")
        hv_col_light = ryuConf.red_main_config("GlobalConfiguration", "hoverColorLighten")
        hover_color = (hv_col, hv_col)
        hover_col_lighter = (hv_col_light, hv_col_light)
        # in progres rn.
        entry_value_mapping = {0: "username",
                               1: "password",
                               2: "guardian_email",
                               3: "Person",
                               }

        # reset back submit button color, if its red or green
        self.submit_entry_btn[button_id].configure(fg_color=("#636363", "#222222"),
                                                   hover_color=("#757474", "#3b3b3b"))

        if email_val is None:
            self.submit_entry_btn[button_id].configure(fg_color=("red", "red"),
                                                       hover_color=("red", "red"), )
            return

        if not entry_type == 1:  # regex check for all email inputs
            match = re.fullmatch(r'\b[\w.%+-]+(?<!\s)@[A-Za-z0-9.-]+\.[A-Za-zščřžýáíéúůďťňóŠČŘŽÝÁÍÉÚŮĎŤŇÓ]{2,7}\b',
                                 email_val)

            # email inputs for seniors email and caregiver email
            if match and not entry_type == 3 and not entry_type == 2:
                entry_type = entry_value_mapping.get(entry_type, entry_type)  # map the id to its correct name
                self.submit_entry_btn[button_id].configure(fg_color=hover_color, hover_color=hover_col_lighter)
                ryuConf.edit_smail_config("credentials", entry_type, email_val)

            elif match and entry_type == 2 and not entry_type == 3:
                entry_type = entry_value_mapping.get(entry_type, entry_type)  # map the id to its correct name
                self.submit_entry_btn[button_id].configure(fg_color=hover_color, hover_color=hover_col_lighter)
                ryuConf.edit_smail_config(None, entry_type, email_val)

            # add six emails:
            elif match and entry_type == 3 and not entry_type == 2:
                if self.person_counter < 6:
                    entry_type = entry_value_mapping.get(entry_type, entry_type)
                    ryuConf.edit_smail_config("emails", f"{entry_type}{self.person_counter}", email_val)
                    self.person_counter += 1
                    self.submit_entry_btn[button_id].configure(text=f"Add person{self.person_counter}")
                elif self.person_counter == 6:
                    entry_type = entry_value_mapping.get(entry_type, entry_type)
                    ryuConf.edit_smail_config("emails", f"{entry_type}{self.person_counter}", email_val)
                    self.person_counter = 1
                    self.submit_entry_btn[button_id].configure(text=f"Add person{self.person_counter}")

                self.entry_widgets[button_id].delete(0, customtkinter.END)
                self.entry_widgets[button_id].configure(placeholder_text=f"added: {email_val}, Add next email:",
                                                        font=font_value)
                self.entry_widgets[1].focus_set()
            else:
                self.submit_entry_btn[button_id].configure(fg_color=("red", "red"),
                                                           hover_color=("red", "red"), )
        # password
        else:
            entry_type = entry_value_mapping.get(entry_type, entry_type)  # map the id to its correct name
            ryuConf.edit_smail_config("credentials", entry_type, email_val)
            self.submit_entry_btn[button_id].configure(fg_color=hover_color, hover_color=hover_col_lighter)
            print("placeholder")

    def file_dialog(self):
        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontSize"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))
        home_dir = os.path.expanduser("~")
        self.filename_picture = filedialog.askopenfilename(initialdir=home_dir)
        if not self.filename_picture:  # check, if tuple is empty, if yes, return
            return
        self.choose_pictures[0].configure(text=self.filename_picture, font=font_value)

    def submit_filedialog(self):
        # todo: path check
        if not self.filename_picture:
            print("filename error <placeholder>")
            return
        if self.filedialog_counter < 6:
            ryuConf.edit_smail_config("images", f"Person{self.filedialog_counter}", self.filename_picture)
            self.filedialog_counter += 1
            self.choose_pictures[1].configure(text=f"Add person{self.filedialog_counter}")
        elif self.filedialog_counter == 6:
            ryuConf.edit_smail_config("images", f"Person{self.filedialog_counter}", self.filename_picture)
            self.filedialog_counter = 1
            self.choose_pictures[1].configure(text=f"Add person{self.filedialog_counter}")

    def create_widgets(self):
        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontSize"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))
        # global value_name

        rel_x = 1 * (2 / 5)
        rel_y = 0
        rel_x_btns = rel_x

        # Define the number of non-entry widgets
        number_of_non_entry_widgets = 3

        # Iterate over the label names to create entry widgets and submit buttons
        for entry_number in range(len(self.label_names) - number_of_non_entry_widgets):
            self.submit_entry_btn[entry_number] = customtkinter.CTkButton(self.master,
                                                                          font=font_value,
                                                                          width=self.width_frame * (1 / 5) - 2,
                                                                          height=self.widget_height - 2,
                                                                          border_width=0,
                                                                          corner_radius=0,
                                                                          fg_color=("#636363", "#222222"),
                                                                          hover_color=("#757474", "#3b3b3b"),
                                                                          text="Submit",
                                                                          command=lambda entry_id=entry_number:
                                                                          self.update_entry_widgets(
                                                                              self.entry_widgets[entry_id].get(),
                                                                              entry_id, entry_id)
                                                                          )
            self.entry_widgets[entry_number] = customtkinter.CTkEntry(self.master,
                                                                      font=("Halvetice", 100),
                                                                      width=self.width_frame * (2 / 5) - 2,
                                                                      height=self.widget_height - 2,
                                                                      border_width=0,
                                                                      corner_radius=0
                                                                      )

            if entry_number == 3:  # 3rd row
                self.combo_x = rel_x
                self.entry_widgets[entry_number].place(relx=rel_x, rely=rel_y * (10 / 11))
                rel_x += (2 / 5)
                self.submit_entry_btn[entry_number].place(relx=rel_x, rely=rel_y * (10 / 11))
                rel_y += (1 / len(self.label_names))
                self.combo_y = rel_y
                rel_x -= (2 / 5)
                rel_y += (1 / len(self.label_names))
            else:
                self.entry_widgets[entry_number].place(relx=rel_x, rely=rel_y * (10 / 11))
                rel_x += (2 / 5)
                self.submit_entry_btn[entry_number].place(relx=rel_x, rely=rel_y * (10 / 11))
                rel_x -= (2 / 5)
                rel_y += (1 / len(self.label_names))

        # Configure entry widget for password
        self.entry_widgets[1].configure(show='*')

        # Configure text for the first button
        self.submit_entry_btn[3].configure(text="Add Person1")

        for widget in range(2):
            self.choose_pictures[f"picture{widget}"] = customtkinter.CTkButton(master=self.master,
                                                                               height=self.widget_height - 2,
                                                                               corner_radius=0,
                                                                               fg_color=("#636363", "#222222"),
                                                                               hover_color=("#757474", "#3b3b3b"),
                                                                               font=font_value,
                                                                               )
        self.choose_pictures[f"picture{0}"].configure(text="Add picture for selected person →",
                                                      width=self.width_frame * (2 / 5) - 2,
                                                      command=lambda: self.file_dialog())

        self.choose_pictures[f"picture{1}"].configure(text=f"Add person{self.filedialog_counter}",
                                                      width=self.width_frame * (1 / 5) - 2,
                                                      command=lambda: self.submit_filedialog())

        self.choose_pictures[f"picture{0}"].place(relx=self.combo_x, rely=self.combo_y * (10 / 11))
        self.combo_x += (2 / 5)
        self.choose_pictures[f"picture{1}"].place(relx=self.combo_x, rely=self.combo_y * (10 / 11))

        # Define a list of options
        number_options = ["Enable", "Disable"]
        # Iterate over options to create buttons
        for value_name in number_options:
            self.caregiver_warning[value_name] = customtkinter.CTkButton(self.master,
                                                                         font=font_value,
                                                                         width=self.width_frame * (1 / 5) - 2,
                                                                         height=self.widget_height - 2,
                                                                         border_width=0,
                                                                         corner_radius=0,
                                                                         fg_color=("#636363", "#222222"),
                                                                         hover_color=("#757474", "#3b3b3b"),
                                                                         text=value_name,
                                                                         command=lambda value_id=value_name:
                                                                         self.update_buttons_widget(None,
                                                                                                    "resend_email",
                                                                                                    value_id, value_id,
                                                                                                    self.caregiver_warning))

            self.url_link[value_name] = customtkinter.CTkButton(self.master,
                                                                font=font_value,
                                                                width=self.width_frame * (1 / 5) - 2,
                                                                height=self.widget_height - 2,
                                                                border_width=0,
                                                                corner_radius=0,
                                                                fg_color=("#636363", "#222222"),
                                                                hover_color=("#757474", "#3b3b3b"),
                                                                text=value_name,
                                                                command=lambda value_id=value_name:
                                                                self.update_buttons_widget(None, "show_url", value_id,
                                                                                           value_id, self.url_link)
                                                                )
            # Place buttons
            self.caregiver_warning[value_name].place(relx=rel_x_btns, rely=rel_y * (10 / 11))
            rel_x_btns += (1 / 5)
            self.url_link[value_name].place(relx=rel_x, rely=(rel_y + 1 / len(self.label_names)) * (10 / 11))
            rel_x += (1 / 5)


class GlobalFrameWidgets:
    def __init__(self, frame_root, width, height_frame, restore, refresh):
        logger.info("Initiated widgets creation for Global frame.")
        self.master = frame_root
        self.width_frame = width
        self.label_names = ryuConf.red_main_config("careConf", "GlobalFrameLabels")
        self.hover_alert_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")
        self.action_widgets = {"restore_widget": restore, "refresh_widget": refresh}
        # create objects for widgets:
        self.error_label_arr = []
        self.screen_arr = []
        self.screen_num = {}  # choose which screen size scale to
        self.language_dict = {}  # language for applications array
        self.language_alert_dict = {}  # language alert dictionary
        self.colorscheme_dict = {}
        self.entry_dict = {}
        self.entry_buttons_dict = {}
        self.font_size = {}
        # for showing each buttons at one function and resize calculations ↓ ↓ ↓ ↓ ↓
        self.array_coranteng = [self.screen_num, self.language_dict, self.language_alert_dict, self.colorscheme_dict,
                                self.entry_dict, self.font_size]
        # ---------- CALS --------------
        resize_class = FrameElements(frame_root, width, height_frame, "GlobalFrameLabels")
        self.height_frame = resize_class.get_correct_size()
        self.labels = resize_class.create_labels(self.height_frame)
        self.buttons()
        self.highlight_configured_widgets()
        widget_list_array = [self.labels, self.screen_num, self.language_dict, self.language_alert_dict,
                             self.colorscheme_dict, self.entry_dict, self.font_size, self.entry_buttons_dict,
                             self.action_widgets]
        # resize events:
        resize_class.is_window_resized(widget_list_array)
        self.master.bind("<Configure>", lambda _: [resize_class.resize_font(widget_list_array),
                                                   resize_class.resize_widgets(widget_list_array)])

    @staticmethod
    def calculate_lighter_hover_color(input_value):
        hex_color = input_value.strip("#")
        # hex -> R G B
        red = int(hex_color[0:2], 16)
        green = int(hex_color[2:4], 16)
        blue = int(hex_color[4:6], 16)
        # lighten
        red = min(255, int(red * (1 + 35 / 100)))
        green = min(255, int(green * (1 + 35 / 100)))
        blue = min(255, int(blue * (1 + 35 / 100)))
        # back to hex
        new_hex_color = "#{:02x}{:02x}{:02x}".format(red, green, blue)
        print("new hex:", new_hex_color)
        # edit
        ryuConf.edit_main_config("GlobalConfiguration", "hoverColorLighten", new_hex_color)

    @staticmethod
    def update_config(key, name, value, button_id, button_list):
        # pokud se zadaří a nikde nebude value a button_id rozdílné, tak pak tyto proměnné sloučit
        print("name", name)
        print("value", value)

        language_mapping = {
            "Czech": "CZ",
            "English": "EN",
            "German": "DE"
        }
        value = language_mapping.get(value, value)

        # read json configs for hover color settings
        fg_col = ryuConf.red_main_config("GlobalConfiguration", "hoverColor")
        selected_button = (fg_col, fg_col)
        hov_col = ryuConf.red_main_config("GlobalConfiguration", "hoverColorLighten")
        sel_btn_hover = (hov_col, hov_col)

        # trying to update with visual notifications
        return_value = ryuConf.edit_main_config(key, name, value)
        for all_buttons in button_list:  # aka restore all buttons in that row to its original color
            button_list[all_buttons].configure(fg_color=("#636363", "#222222"), hover_color=("#757474", "#3b3b3b"))
        if return_value is True:
            button_list[button_id].configure(fg_color=selected_button, hover_color=sel_btn_hover)
        else:
            logger.error("There was an error while updating the value.")
            button_list[button_id].configure(fg_color=("red", "red"), hover_color=("#8B0000", "#8B0000"))

    def highlight_configured_widgets(self):
        fg_col = ryuConf.red_main_config("GlobalConfiguration", "hoverColor")
        fg_color_values = (fg_col, fg_col)
        hov_co = ryuConf.red_main_config("GlobalConfiguration", "hoverColorLighten")
        hover_color_values = (hov_co, hov_co)

        language = ryuConf.red_main_config("GlobalConfiguration", "language")
        language_alert = ryuConf.red_main_config("GlobalConfiguration", "alertSoundLanguage")

        language_mapping = {
            "CZ": "Czech",
            "EN": "English",
            "DE": "German"
        }
        language = language_mapping.get(language, language)
        language_alert = language_mapping.get(language_alert, language_alert)

        self.colorscheme_dict[ryuConf.red_main_config("GlobalConfiguration", "colorMode")].configure(
            fg_color=fg_color_values, hover_color=hover_color_values)
        self.language_alert_dict[language_alert].configure(
            fg_color=fg_color_values, hover_color=hover_color_values)
        self.language_dict[language].configure(
            fg_color=fg_color_values, hover_color=hover_color_values)
        self.screen_num[ryuConf.red_main_config("GlobalConfiguration", "numOfScreen")].configure(
            fg_color=fg_color_values, hover_color=hover_color_values)
        self.font_size[ryuConf.red_main_config("GlobalConfiguration", "fontThickness")].configure(
            fg_color=fg_color_values, hover_color=hover_color_values)

        for name in self.entry_dict:
            if name == "alertColor" or name == "hoverColor":
                self.entry_dict[name].configure(
                    placeholder_text=f'Select value. (default is: {ryuConf.red_main_config("GlobalConfiguration", name)})')
            elif name == "soundDelay":
                self.entry_dict[name].configure(
                    placeholder_text=f'Select value. (default is: {ryuConf.red_main_config("GlobalConfiguration", name)} s)')
            else:
                self.entry_dict[name].configure(
                    placeholder_text=f'Select value. (default is: {ryuConf.red_main_config("GlobalConfiguration", name)} px)')

        logger.info("Highlighted correct values that are in config file.")

    def show_entry_error(self, button_object, entry_object, label_id):
        window_height = self.master.winfo_height()
        window_width = self.master.winfo_width()

        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontSize"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))

        rel_entry_x = entry_object.winfo_x() / window_width
        rel_entry_y = entry_object.winfo_y() / window_height

        rel_button_x = button_object.winfo_x() / window_width
        rel_button_y = button_object.winfo_y() / window_height

        button_object.place_forget()
        entry_object.place_forget()

        self.error_label_arr.append(label_id)

        label_id = customtkinter.CTkLabel(self.master)
        label_id.configure(width=self.width_frame * (2 / 5) - 2.5,
                           height=self.height_frame * (1 / (len(self.label_names) + 1)) - 2.5,
                           fg_color=(self.hover_alert_color, self.hover_alert_color),
                           font=font_value,
                           text="There was an error in user input, for more info., please see Log.")
        label_id.place(relx=rel_entry_x, rely=rel_entry_y)

        label_id_btn = customtkinter.CTkButton(self.master)
        label_id_btn.configure(width=self.width_frame * (1 / 5) - 2.5,
                               height=self.height_frame * (1 / (len(self.label_names) + 1)) - 2.5,
                               border_width=0,
                               corner_radius=0,
                               fg_color=("#636363", "#222222"),
                               hover_color=("#757474", "#3b3b3b"),
                               text="Let me try again!",
                               font=font_value,
                               command=lambda entry_value=label_id, entry_button=label_id_btn:
                               [label_id.place_forget(), label_id_btn.place_forget(),
                                entry_object.place(relx=rel_entry_x, rely=rel_entry_y),
                                button_object.place(relx=rel_button_x, rely=rel_button_y)])
        label_id_btn.place(relx=rel_button_x, rely=rel_button_y)
        self.error_label_arr.append(label_id_btn)

    def update_config_entry(self, key, name, input_value, button_object, entry_object):
        # firstly read hover color settings, so it doesn't get mismatched when changing
        selected_button = ryuConf.red_main_config("GlobalConfiguration", "hoverColor")
        sel_btn_hover = ryuConf.red_main_config("GlobalConfiguration", "hoverColorLighten")

        if name == "alertColor" or name == "hoverColor":
            match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', input_value)
            if match and name == "hoverColor":  # only for hoverColor
                self.calculate_lighter_hover_color(input_value)  # calculate lighter hover color
                button_object.configure(fg_color=(selected_button, selected_button),
                                        hover_color=(sel_btn_hover, sel_btn_hover))
                ryuConf.edit_main_config(key, name, input_value)
                return
            elif match:  # for alertColor
                button_object.configure(fg_color=(selected_button, selected_button),
                                        hover_color=(sel_btn_hover, sel_btn_hover))
                ryuConf.edit_main_config(key, name, input_value)
                return
            else:  # else catch, when incorect type is given
                self.show_entry_error(button_object, entry_object, name)
                logger.error(f"Changed integer value was not in HEX format, user input was: '{input_value}'")
                return

        # number input regex section
        else:
            match = re.search(r'^\d+$', input_value)
            if match:
                button_object.configure(fg_color=(selected_button, selected_button),
                                        hover_color=(sel_btn_hover, sel_btn_hover))
                ryuConf.edit_main_config(key, name, int(input_value))
                return
            else:
                self.show_entry_error(button_object, entry_object, name)
                logger.error(f"Changed integer value was not number, user input was: {input_value}")
                return

    def buttons(self):
        # First config row:
        for screen_primary, monitor in enumerate(get_monitors()):
            if screen_primary >= 3:  # Only allow 3 monitors
                break
            self.screen_arr.append(screen_primary)
            self.screen_num[screen_primary] = customtkinter.CTkButton(master=self.master)
            self.screen_num[screen_primary].configure(text=f"Screen {screen_primary}",
                                                      command=lambda current_id=screen_primary: self.update_config(
                                                          "GlobalConfiguration",
                                                          "numOfScreen",
                                                          current_id,
                                                          current_id,
                                                          self.screen_num)
                                                      )

        # Second config row:
        language_arr = ryuConf.red_main_config("careConf", "LanguageOptions")
        for language in language_arr:
            self.language_dict[language] = customtkinter.CTkButton(master=self.master)
            self.language_dict[language].configure(text=language,
                                                   command=lambda lang_id=language: self.update_config(
                                                       "GlobalConfiguration",
                                                       "language",
                                                       lang_id,
                                                       lang_id,
                                                       self.language_dict)
                                                   )

        # Third config row:
        for language_alert in language_arr:
            self.language_alert_dict[language_alert] = customtkinter.CTkButton(master=self.master)
            self.language_alert_dict[language_alert].configure(text=language_alert,
                                                               command=lambda lang_id=language_alert:
                                                               self.update_config("GlobalConfiguration",
                                                                                  "alertSoundLanguage",
                                                                                  lang_id,
                                                                                  lang_id,
                                                                                  self.language_alert_dict)
                                                               )

        # Fourth config row:
        colorscheme_arr = ["Light", "Dark"]
        for option in colorscheme_arr:
            self.colorscheme_dict[option] = customtkinter.CTkButton(self.master)
            self.colorscheme_dict[option].configure(text=option,
                                                    command=lambda colorscheme_id=option:
                                                    self.update_config(
                                                        "GlobalConfiguration",
                                                        "colorMode",
                                                        colorscheme_id,
                                                        colorscheme_id,
                                                        self.colorscheme_dict)
                                                    )

        # Fifth config row:
        width_size = self.width_frame * (2 / 5) - 2.5
        height_size = self.height_frame - 2.5
        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontSize"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))

        entry_objects = ryuConf.red_main_config("careConf", "EntryOptions")
        for entry_buttons_counter, entry_name in enumerate(entry_objects):
            self.entry_buttons_dict[entry_buttons_counter] = customtkinter.CTkButton(self.master)
            self.entry_dict[entry_name] = customtkinter.CTkEntry(self.master)
            self.entry_dict[entry_name].configure(border_width=0,
                                                  corner_radius=0,
                                                  width=width_size,
                                                  height=height_size,
                                                  placeholder_text=entry_name,
                                                  font=font_value)

            self.entry_buttons_dict[entry_buttons_counter].configure(text="Submit",
                                                                     command=lambda stored_name=entry_name,
                                                                                    button_id=entry_buttons_counter,
                                                                                    entry_object=self.entry_dict[
                                                                                        entry_name]:
                                                                     self.update_config_entry("GlobalConfiguration",
                                                                                              stored_name,
                                                                                              self.entry_dict[
                                                                                                  stored_name].get(),
                                                                                              self.entry_buttons_dict[
                                                                                                  button_id],
                                                                                              entry_object)
                                                                     )

        # Sixth config row:
        font_size_arr = ["bold", "normal"]
        for option in font_size_arr:
            self.font_size[option] = customtkinter.CTkButton(self.master)
            self.font_size[option].configure(border_width=0,
                                             corner_radius=0,
                                             width=width_size,
                                             height=height_size,
                                             text=option,
                                             command=lambda picked_value=option: self.update_config(
                                                 "GlobalConfiguration",
                                                 "fontThickness", picked_value,
                                                 picked_value, self.font_size))

        # logic for showing buttons
        self.show_buttons()

    def show_buttons(self):
        """
        This very scary looking function does multiple things, it sets repetitive parameters for widgets and its place on frame
        """
        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontSize"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))

        # height_num = self.height_frame * (1 / (len(self.label_names) + 1)) - 2.5
        height_num = self.height_frame - 2
        width_num = self.width_frame * (1 / 5) - 2
        y_position = float(0)

        for widget_dictionary in self.array_coranteng:
            # place entry widgets to frame
            if widget_dictionary is self.entry_dict:
                x_position = 1 * (2 / 5)  # starting place
                entry_buttons_counter = 0
                for entry_object in widget_dictionary.values():
                    x_button_poss = x_position + (2 / 5)
                    self.entry_buttons_dict[entry_buttons_counter].configure(border_width=0,
                                                                             corner_radius=0,
                                                                             fg_color=("#636363", "#222222"),
                                                                             hover_color=("#757474", "#3b3b3b"),
                                                                             font=font_value,
                                                                             width=width_num,
                                                                             height=height_num)
                    entry_object.place(relx=x_position, rely=y_position)
                    self.entry_buttons_dict[entry_buttons_counter].place(relx=x_button_poss, rely=y_position)
                    y_position += 1 * (1 / (len(self.label_names) + 1))
                    entry_buttons_counter += 1
                y_position -= 1 * (1 / (len(self.label_names) + 1))
            # place other widgets that aren't anyhow bond to entry to frame
            else:
                x_position = 1 * (2 / 5)  # starting place for other dictionaries
                for button in widget_dictionary.values():
                    button.configure(border_width=0,
                                     corner_radius=0,
                                     fg_color=("#636363", "#222222"),
                                     hover_color=("#757474", "#3b3b3b"),
                                     font=font_value,
                                     width=width_num,
                                     height=height_num)
                    button.place(relx=x_position, rely=y_position)
                    x_position += 1 * (1 / 5)  # Standard size for other dictionaries
            y_position += 1 * (1 / (len(self.label_names) + 1))
        logger.info("Created buttons and entry widgets for GLOBAL frame")


class DefaultFrameWidgets:
    def __init__(self, frame_root):
        self.master = frame_root
        text_variable = ("Welcome to the Configuration Application for Senior-os\n"
                         "Each button in menubar has its own configuration frame.\n"
                         "\nMore information in documentation <link>")
        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "controlFontSize") * 1.1,
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))

        label = customtkinter.CTkLabel(master=frame_root, text=text_variable, font=font_value)
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


class Frames:
    """
    This class creates all the needed frames for configuration buttons.
    It also handles two "restore" and "Refresh" buttons.
    and lastly, it handles switching the frames.
    """

    def __init__(self, master, width, height, divisor, number_of_buttons, name_of_buttons):
        # -------------
        self.master = master
        self.width = width
        self.height_frame = height - (height / divisor)
        self.divisor = divisor
        self.number_of_buttons = number_of_buttons + 1  # adding default frame
        self.buttons_name = name_of_buttons
        self.height = height
        # ------------
        self.alive_frame = self.number_of_buttons  # default frame (highest number from button names array + 1)
        self.frame_array = []
        self.frame_dictionary = {}
        self.restore_configurations = None
        self.refresh_frame = None
        # calls:
        self.alocate_frames()
        DefaultFrameWidgets(self.frame_dictionary[self.number_of_buttons])
        self.frame_dictionary[self.number_of_buttons].pack()

    def get_new_values_for_refresh(self, button_id):
        # set global color:
        customtkinter.set_appearance_mode(ryuConf.red_main_config("GlobalConfiguration", "colorMode"))
        # refresh:
        self.choose_frame(button_id, True)

    def restore_config(self, button_id):
        # choose, which restore action is needed:
        if self.alive_frame == 1:
            ryuConf.restore_main_config()
        elif self.alive_frame == 2:
            ryuConf.restore_smail_config()
        elif self.alive_frame == 3:
            ryuConf.restore_sweb_config()

        # get new values, aka read json config again:
        self.get_new_values_for_refresh(button_id)

    def refresh_restore_buttons(self, button_id):
        # create buttons:
        self.restore_configurations = customtkinter.CTkButton(master=self.frame_dictionary[button_id],
                                                              text="Restore Settings",
                                                              command=lambda: self.restore_config(button_id),
                                                              )

        self.refresh_frame = customtkinter.CTkButton(master=self.frame_dictionary[button_id],
                                                     text="Refresh frame",
                                                     command=lambda: self.get_new_values_for_refresh(button_id))

        # place:
        self.restore_configurations.place(relx=0.5 - (1 * 2 / 5) - 0.001,
                                          rely=0.91)  # bro, I forgot why these numbers are here
        self.refresh_frame.place(relx=0.5 + 0.001, rely=0.91)

        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "controlFontSize"),
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))

        hovor_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")
        for widget in [self.restore_configurations, self.refresh_frame]:
            widget.configure(hover_color=(hovor_color, hovor_color),
                             font=font_value,
                             fg_color=("#D3D3D3", "#171717"),
                             text_color=("black", "white"),
                             height=self.height_frame * (1 / 11),
                             width=self.master.winfo_width() * (2 / 5),
                             border_width=2,
                             corner_radius=0,
                             anchor=customtkinter.CENTER)

    def choose_frame(self, button_id, refresh):
        if refresh:
            # Refresh frame
            for widget in self.frame_dictionary[self.alive_frame].winfo_children():
                widget.place_forget()
            self.alive_frame = button_id  # just making sure, that the frame is set as currently alive frame
            logger.info("Refreshing frame now.")

        # skip if frame alive is the same as next frame to show
        elif self.alive_frame == button_id:
            return

        # Pack the new frame and forget the old one
        elif self.alive_frame is not None:
            self.frame_dictionary[self.alive_frame].pack_forget()
            for widget in self.frame_dictionary[self.alive_frame].winfo_children():
                widget.place_forget()
            self.frame_dictionary[button_id].pack()
            self.alive_frame = button_id
            logger.info("Showing new frame, hiding the old one.")
        else:
            logger.error("There is no frame to show, even though there should be.")
            return

        # Show corresponding class with widgets to its frame
        frame_mapping = {
            "Global": GlobalFrameWidgets,
            "Mail": MailFrameWidgets,
            "Web": WebFrameWidgets,
            "Logs": LogsFrameWidgets
        }
        #
        # Search for frame name based on ID with button id:
        # AKA: button_id=1, Global frame ID=1 -> match -> show it
        #
        global_frame_names = ryuConf.red_main_config("careConf", "menuButtonsList")
        frame_name = global_frame_names[
            button_id - 1]  # Adjust button_id to match zero-based indexing (it starts from 0 and not 1)
        frame_class = frame_mapping.get(frame_name)  # frame mapping

        if frame_class:
            if frame_name == "Logs":
                frame_class(self.frame_dictionary[button_id], self.width, self.height_frame)
                logger.info(f"User picked frame '{frame_name}', creating frame now.")
                return
            else:
                self.refresh_restore_buttons(button_id)  # restore and reset buttons
                frame_class(self.frame_dictionary[button_id], self.width, self.height_frame,
                            self.restore_configurations, self.refresh_frame)
                logger.info(f"User picked frame '{frame_name}', creating frame now.")
                return
        else:
            logger.error("Button doesn't have its corresponding frame or it isn't present in config options")

    # create needed frames for config, based on config.json
    def create_frames(self, number):
        self.frame_dictionary[number] = customtkinter.CTkFrame(self.master)
        self.frame_dictionary[number].configure(fg_color=("white", "#1a1a1a"))
        self.frame_dictionary[number].pack_propagate(False)
        self.frame_dictionary[number].configure(width=self.width, height=self.height_frame)
        number += 1

    def alocate_frames(self):
        number = 1
        while number <= self.number_of_buttons:
            self.frame_array.append(number)
            number += 1
        for num_id in self.frame_array:
            self.create_frames(num_id)


class Toolbar:
    def __init__(self, master, width, height, divisor, toolbar_buttons_count, button_names):
        self.toolbar_frame = customtkinter.CTkFrame(master)
        self.toolbar_frame.pack_propagate(False)
        self.toolbar_frame.configure(width=width, height=height / divisor)
        self.toolbar_frame.pack(side=customtkinter.TOP)
        self.width = width
        self.height = height
        self.master = master
        self.button_selected = None
        self.hover_alert_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")

        # ---
        self.frame_height = height / divisor
        self.x_poss = 0
        # ---
        self.buttons_names = button_names  # name of configuration buttons from json
        self.toolbar_buttons_count = toolbar_buttons_count + 1  # adding one for exit
        self.button_dictionary = {}
        self.customBtnList = []
        # calls:
        self.alocate_number_of_buttons()
        # class calls:
        self.frame_class = Frames(self.master, self.width, self.height, divisor, toolbar_buttons_count, button_names)
        logger.info("Created toolbar subFrame")

    def alocate_number_of_buttons(self):
        print("allocating memory for creation")
        num = 1
        while num <= self.toolbar_buttons_count:
            self.customBtnList.append(num)
            num += 1
        for number in self.customBtnList:
            self.create_buttons(number)

    def create_buttons(self, id_num):
        self.button_dictionary[id_num] = customtkinter.CTkButton(self.toolbar_frame)
        font_value = (ryuConf.red_main_config("GlobalConfiguration", "fontFamily"),
                      ryuConf.red_main_config("GlobalConfiguration", "controlFontSize") * 1.20,
                      ryuConf.red_main_config("GlobalConfiguration", "fontThickness"))
        # EXIT button
        if id_num == self.toolbar_buttons_count:  # aka, the last button is the exit button
            self.button_dictionary[id_num].configure(text=f"EXIT", font=font_value)
            self.button_dictionary[id_num].configure(fg_color=("white", "#1a1a1a"),
                                                     hover_color=(self.hover_alert_color, self.hover_alert_color),
                                                     text_color=("black", "white"))
            # here lambda works, because it's inside a for loop, so it gets correct id of a number
            self.button_dictionary[id_num].configure(command=lambda: self.master.destroy())
        # The rest of buttons
        else:
            self.button_dictionary[id_num].configure(text=self.buttons_names[id_num - 1],
                                                     font=font_value)
            self.button_dictionary[id_num].configure(command=lambda: [self.frame_class.choose_frame(id_num, False),
                                                                      self.selected_button(id_num)])
            #  ("white_scheme", "dark_scheme")
            self.button_dictionary[id_num].configure(fg_color=("white", "#1a1a1a"),
                                                     hover_color=("#bebebe", "#2e2e2e"),
                                                     text_color=("black", "white"))

        self.button_dictionary[id_num].configure(width=self.width / self.toolbar_buttons_count,
                                                 height=self.frame_height)

        self.button_dictionary[id_num].configure(border_width=3, corner_radius=0)

        # relx or rely is between 0 and 1, 0 is left corner, 1 is right corner etc.
        if id_num == 1:
            self.button_dictionary[1].place(relx=0, rely=0)
        else:
            self.x_poss = self.x_poss + (1 / self.toolbar_buttons_count)
            self.button_dictionary[id_num].place(relx=self.x_poss, rely=0)

    def selected_button(self, id_num):
        fg_selected = ryuConf.red_main_config("GlobalConfiguration", "hoverColor")
        fg_hover = ryuConf.red_main_config("GlobalConfiguration", "hoverColorLighten")

        if self.button_selected is not None:
            self.button_dictionary[self.button_selected].configure(fg_color=("white", "#1a1a1a"),
                                                                   hover_color=("#bebebe", "#2e2e2e"))
            self.button_selected = id_num
            self.button_dictionary[id_num].configure(fg_color=(fg_selected, fg_selected),
                                                     hover_color=(fg_hover, fg_hover))
        else:
            self.button_dictionary[id_num].configure(fg_color=(fg_selected, fg_selected),
                                                     hover_color=(fg_hover, fg_hover))
            self.button_selected = id_num


class Core(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        screenNum = ryuConf.red_main_config("GlobalConfiguration", "numOfScreen")
        self.screenWidth = get_monitors()[screenNum].width  # screen width_frame
        self.screenHeight = get_monitors()[screenNum].height  # screen height
        self.heightDivisor = ryuConf.red_main_config("GUI_template", "height_divisor")
        self.buttons_names = ryuConf.red_main_config("careConf", "menuButtonsList")
        self.toolbar_buttons_count = len(ryuConf.red_main_config("careConf", "menuButtonsList"))
        # ---
        self.toolbar = Toolbar(self, self.screenWidth, self.screenHeight, self.heightDivisor,
                               self.toolbar_buttons_count, self.buttons_names)
        self.title(f"Caregiver configuration application -- Version:{Version}")
        # ---
        logger.info("Creating root window for application")
        # Fullscreen thingy:
        self.fullscreen_lock = False
        self.fullscreen_state = True
        self.esc_pressed = False
        self.f11_pressed = False

        self.attributes("-fullscreen", True)

        self.bind("<KeyPress>", self.on_key_press)
        self.bind("<KeyRelease>", self.on_key_release)

    def on_key_press(self, event):
        if not self.fullscreen_lock:
            if event.keysym == "Escape":
                self.toggle_fullscreen()
                self.fullscreen_lock = True
            elif event.keysym == "F11":
                self.toggle_fullscreen()
                self.fullscreen_lock = True

        ms_delay = 350
        if event.keysym == "Escape":
            self.esc_pressed = True
            self.after(ms_delay, self.check_long_press, "esc")
        elif event.keysym == "F11":
            self.f11_pressed = True
            self.after(ms_delay, self.check_long_press, "f11")

    def on_key_release(self, event):
        if event.keysym == "Escape":
            self.esc_pressed = False
        elif event.keysym == "F11":
            self.f11_pressed = False

    def check_long_press(self, key):
        if key == "esc" and self.esc_pressed:
            logger.info("Long press key detected on Esc, opinion rejected.")
        elif key == "f11" and self.f11_pressed:
            logger.info("Long press key detected on Esc, opinion rejected.")
        else:
            self.fullscreen_lock = False

    def toggle_fullscreen(self):
        self.fullscreen_state = not self.fullscreen_state
        if self.fullscreen_state:
            self.attributes("-fullscreen", True)
        else:
            self.attributes('-fullscreen', False)
            self.geometry(f"{int(self.screenWidth * 0.70)}x{int(self.screenHeight * 0.70)}+0+0")  # Nastaví původní
            self.minsize(int(self.screenWidth * 0.70), int(self.screenHeight * 0.70))  # width_frame, height
            self.maxsize(int(self.screenWidth), int(self.screenHeight))  # width_frame x height + x + y


def main():
    app = Core()
    app.mainloop()
