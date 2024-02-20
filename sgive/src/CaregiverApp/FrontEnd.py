import customtkinter
from screeninfo import get_monitors
import sgive.src.CaregiverApp.configurationActions as ryuConf
import logging
import os
import re  # regex

"""
Author: RYUseless
Github: https://github.com/RYUseless
"""
Version = "0.0.3(Alpha)"

logger = logging.getLogger(__file__)
logger.info("initiated logging")

colorScheme = ryuConf.red_main_config("GlobalConfiguration", "colorMode")
customtkinter.set_appearance_mode(colorScheme)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


class DefaultFrameWidgets:
    def __init__(self, frame_root):
        self.master = frame_root
        text_variable = ("This is configuration application for caregiver only!\n"
                         "If you are senior yourself, you shouldn't be here.\n"
                         "\nTo leave, click \"EXIT\" in upper right corner.")

        label = customtkinter.CTkLabel(master=frame_root, text=text_variable, font=("Helvetica", 36, "bold"))
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


class LogsFrameWidgets:
    def __init__(self, frame_root, width, height):
        logger.info("Creating and showing frame for viewing Logs.")
        self.master = frame_root
        self.height = height
        self.width = width
        # ------
        self.log_filter = None
        self.log_file = None

        # -----
        # sub-frame, for buttons and stuff
        self.options_toolbar_frame = customtkinter.CTkFrame(frame_root)
        self.options_toolbar_frame.pack_propagate(False)
        self.options_toolbar_frame.configure(width=width, height=height * 0.10,  # aka XY% of whole frame height
                                             fg_color=("#dbd9d9", "#222222"))
        self.options_toolbar_frame.pack(side=customtkinter.TOP)
        self.log_file_choice = None
        self.log_files_names = []
        self.textbox = customtkinter.CTkTextbox(self.master)

        # func calls:
        self.find_log_files()

        self.options_toolbar()
        self.log_textbox(None)

    def refresh(self):
        for widget in self.master.winfo_children():
            # this forgets all widgets inside a frame
            widget.place_forget()
        for widget in self.master.winfo_children():
            widget.pack()

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
        # pick log folder:
        pick_folder_btn = customtkinter.CTkOptionMenu(master=self.options_toolbar_frame,
                                                      command=self.option_menu_call,
                                                      height=self.height * 0.10,
                                                      width=self.width * 1 / 5)
        dummy_values = []  # dummy array
        for name in self.log_files_names:
            dummy_values.append(name)  # add value to an array
        pick_folder_btn.configure(values=dummy_values)
        pick_folder_btn.place(relx=0, rely=0)
        pick_folder_btn.set("Choose LOG file")  # default showing value
        # -----------------------------------------------------------------------------
        # pick log folder:
        pick_filter_btn = customtkinter.CTkOptionMenu(master=self.options_toolbar_frame,
                                                      command=self.option_filter_call,
                                                      height=self.height * 0.10,
                                                      width=self.width * 1 / 5)
        filter_options = ["INFO", "WARNING", "CRITICAL", "ERROR", "ALL"]
        pick_filter_btn.configure(values=filter_options)
        pick_filter_btn.place(relx=1 * (1 / 5), rely=0)
        pick_filter_btn.set("Choose LOG filter option")  # default showing value
        # ---------------------------------------------------------------------------
        # refresh button:
        button = customtkinter.CTkButton(master=self.options_toolbar_frame,
                                         height=self.height * 0.10,
                                         width=self.width * 1 / 5,
                                         text="Refresh",
                                         command=lambda: self.refresh())
        button.place(relx=1 * (4 / 5), rely=0)

    def log_textbox(self, choice):
        textbox = customtkinter.CTkTextbox(self.master)
        textbox.configure(height=self.master.winfo_height() - (self.master.winfo_height() * 0.10), width=self.master.winfo_width(),
                          fg_color=("#D3D3D3", "#171717"),
                          scrollbar_button_color=("black", "white"),
                          scrollbar_button_hover_color=("#3b3b3b", "#636363"),
                          )
        textbox.place(relx=0, rely=1 * 0.10)
        file = ryuConf.read_log(self.log_filter, choice)
        if file is None:
            textbox.insert(customtkinter.END, "No log file was selected, nothing to show ...")
        else:
            for f in file:
                textbox.insert(customtkinter.END, f)
        textbox.configure(state="disabled")  # disable editing


class WebFrameWidgets:
    def __init__(self, frame_root, width, height_frame):
        self.master = frame_root
        self.height_frame = height_frame
        self.width = width
        # self.label_names = ryuConf.red_main_config("careConf", "SMailFrameLabels")
        self.font_name = ryuConf.red_main_config("GlobalConfiguration", "fontFamily")
        self.label_size = ryuConf.red_main_config("GlobalConfiguration", "labelFontSize")
        self.font_boldness = ryuConf.red_main_config("GlobalConfiguration", "fontThickness")
        self.hover_alert_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")
        # -----------------
        # Bind the resize event
        self.master.bind("<Configure>", self.on_resize)
        # E N D of constructor

    def on_resize(self, event):
        width_new = event.width * (2 / 5)

        # Recalculate button height and width (lower buttons, that are created in frame class)
        for widget in [self.master.children[child] for child in self.master.children]:
            if isinstance(widget, customtkinter.CTkButton):
                widget.configure(height=self.height_frame * (1 / 11),
                                 width=width_new)


class MailFrameWidgets:
    def __init__(self, frame_root, width, height_frame):
        logger.info("Creating and showing frame for Mail configuration.")
        self.master = frame_root
        self.height_frame = height_frame
        self.width = width
        self.label_names = ryuConf.red_main_config("careConf", "SMailFrameLabels")
        self.font_name = ryuConf.red_main_config("GlobalConfiguration", "fontFamily")
        self.label_size = ryuConf.red_main_config("GlobalConfiguration", "labelFontSize")
        self.font_boldness = ryuConf.red_main_config("GlobalConfiguration", "fontThickness")
        self.hover_alert_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")
        self.label_dict = {}
        self.button_height_fract = 11
        # -----------------
        # calls:
        self.master.bind("<Configure>", self.on_resize)
        self.create_labels()
        # E N D of constructor

    def create_labels(self):
        y_position = 0
        for label_name in self.label_names:
            label = customtkinter.CTkLabel(self.master)
            label.configure(text=label_name,
                            font=(self.font_name, self.label_size + 17, self.font_boldness),
                            width=self.master.winfo_width() * (2 / 5),
                            height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)),
                            # height=self.height_frame * (1 / 11),
                            fg_color=("#D3D3D3", "#171717"))  # whiteMode DarkMode
            label.place(relx=0, rely=y_position)
            self.label_dict[label_name] = label
            y_position += (1 / (len(self.label_names) + 1))

    def on_resize(self, event):
        width_new = event.width * (2 / 5)
        for label in self.label_dict.values():
            label.configure(width=width_new,
                            height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)))

        # Recalculate button height and width (lower buttons, that are created in frame class)
        for widget in [self.master.children[child] for child in self.master.children]:
            if isinstance(widget, customtkinter.CTkButton):
                widget.configure(height=self.height_frame * (1 / 11),
                                 width=width_new)


class GlobalFrameWidgets:
    def __init__(self, frame_root, width, height_frame, restore, refresh):
        logger.info("Creating and showing frame for Global configuration.")
        self.master = frame_root
        self.height_frame = height_frame
        self.width = width
        self.label_names = ryuConf.red_main_config("careConf", "GlobalFrameLabels")
        self.font_name = ryuConf.red_main_config("GlobalConfiguration", "fontFamily")
        self.label_size = ryuConf.red_main_config("GlobalConfiguration", "labelFontSize")
        self.font_boldness = ryuConf.red_main_config("GlobalConfiguration", "fontThickness")
        self.hover_alert_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")
        self.restore_configurations = restore
        self.refresh_frame = refresh
        # create objects for widgets:
        self.error_label_arr = []
        self.screen_arr = []
        self.screen_num = {}  # choose which screen size scale to
        self.label_dict = {}  # i forgor what dis :)
        self.language_dict = {}  # language for applications array
        self.language_alert_dict = {}  # language alert dictionary
        self.colorscheme_dict = {}
        self.entry_dict = {}
        self.entry_buttons_dict = {}
        self.font_size = {}
        # ---------
        # for showing each buttons at one function and resize calculations ↓ ↓ ↓ ↓ ↓
        self.array_coranteng = [self.screen_num, self.language_dict, self.language_alert_dict, self.colorscheme_dict,
                                self.entry_dict, self.font_size]
        # ---------- CALS --------------
        self.create_labels()  # creating labels for each lane
        self.buttons()  # creating objects for buttons
        self.show_buttons()  # logic for showing buttons
        self.highlight_configured_widgets()  # set default options
        self.master.bind("<Configure>", self.on_resize)
        # E N D of constructor



    def show_entry_error(self, button_object, entry_object, label_id):
        window_height = self.master.winfo_height()
        window_width = self.master.winfo_width()

        rel_entry_x = entry_object.winfo_x() / window_width
        rel_entry_y = entry_object.winfo_y() / window_height

        rel_button_x = button_object.winfo_x() / window_width
        rel_button_y = button_object.winfo_y() / window_height

        button_object.place_forget()
        entry_object.place_forget()

        self.error_label_arr.append(label_id)

        label_id = customtkinter.CTkLabel(self.master)
        label_id.configure(width=self.master.winfo_width() * (2 / 5) - 2.5,
                           height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)) - 2.5,
                           fg_color=(self.hover_alert_color, self.hover_alert_color),
                           text="There was an error in user input, for more info., please see Log.")
        label_id.place(relx=rel_entry_x, rely=rel_entry_y)

        label_id_btn = customtkinter.CTkButton(self.master)
        label_id_btn.configure(width=self.master.winfo_width() * (1 / 5) - 2.5,
                               height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)) - 2.5,
                               border_width=0,
                               corner_radius=0,
                               fg_color=("#636363", "#222222"),
                               hover_color=("#757474", "#3b3b3b"),
                               text="Let me try again!",
                               command=lambda entry_value=label_id, entry_button=label_id_btn:
                                [label_id.place_forget(), label_id_btn.place_forget(),
                                 entry_object.place(relx=rel_entry_x, rely=rel_entry_y),
                                 button_object.place(relx=rel_button_x, rely=rel_button_y)])
        label_id_btn.place(relx=rel_button_x, rely=rel_button_y)
        self.error_label_arr.append(label_id_btn)

    def check_value(self, key, name, input_value, button_object, entry_object):
        # hex color regex section
        if name == "alertColor" or name == "hoverColor":
            match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', input_value)
            if match:
                button_object.configure(fg_color=("#4b5946", "#4b5946"), hover_color=("#7c8e76", "#7c8e76"))
                ryuConf.edit_main_config(key, name, input_value)
                return
            else:
                # zde dodělat fucky wucky s error labelem atd
                self.show_entry_error(button_object, entry_object, name)
                logger.error(f"Changed integer value was not in HEX format, user input was: '{input_value}'")
                return
        # number input regex section
        else:
            match = re.search(r'^\d+$', input_value)
            if match:
                button_object.configure(fg_color=("#4b5946", "#4b5946"), hover_color=("#7c8e76", "#7c8e76"))
                ryuConf.edit_main_config(key, name, int(input_value))
                return
            else:
                self.show_entry_error(button_object, entry_object, name)
                logger.error(f"Changed integer value was not number, user input was: {input_value}")
                return

    @staticmethod
    def update_config(key, name, value, button_id, button_list):
        # ------------
        # pokud se zadaří a nikde nebude value a button_id rozdílné, tak pak tyto proměnné sloučit
        # ------------
        return_value = ryuConf.edit_main_config(key, name, value)
        for all_buttons in button_list:  # aka restore all buttons in that row to its original color
            button_list[all_buttons].configure(fg_color=("#636363", "#222222"), hover_color=("#757474", "#3b3b3b"))
        if return_value is True:
            button_list[button_id].configure(fg_color=("#4b5946", "#4b5946"), hover_color=("#7c8e76", "#7c8e76"))
        else:
            logger.error("There was an error while updating the value.")
            button_list[button_id].configure(fg_color=("red", "red"), hover_color=("#8B0000", "#8B0000"))

    def highlight_configured_widgets(self):
        fg_color_values = ("#4b5946", "#4b5946")
        hover_color_values = ("#7c8e76", "#7c8e76")

        self.colorscheme_dict[ryuConf.red_main_config("GlobalConfiguration", "colorMode")].configure(
            fg_color=fg_color_values, hover_color=hover_color_values)
        self.language_alert_dict[ryuConf.red_main_config("GlobalConfiguration", "alertSoundLanguage")].configure(
            fg_color=fg_color_values, hover_color=hover_color_values)
        self.language_dict[ryuConf.red_main_config("GlobalConfiguration", "language")].configure(
            fg_color=fg_color_values, hover_color=hover_color_values)
        self.screen_num[ryuConf.red_main_config("GlobalConfiguration", "numOfScreen")].configure(
            fg_color=fg_color_values, hover_color=hover_color_values)
        self.font_size[ryuConf.red_main_config("GlobalConfiguration", "fontThickness")].configure(
            fg_color=fg_color_values, hover_color=hover_color_values)

        time_unit = "s"
        for name in self.entry_dict:
            if name == "alertColor" or name == "hoverColor":
                self.entry_dict[name].configure(
                    placeholder_text=f'Select value. (default is: {ryuConf.red_main_config("GlobalConfiguration", name)})')
            else:
                self.entry_dict[name].configure(
                    placeholder_text=f'Select value. (default is: {ryuConf.red_main_config("GlobalConfiguration", name)}'
                                     f' {time_unit})')
        logger.info("Highlighted correct values that are in config file.")

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
        entry_objects = ryuConf.red_main_config("careConf", "EntryOptions")
        for entry_buttons_counter, entry_name in enumerate(entry_objects):
            self.entry_buttons_dict[entry_buttons_counter] = customtkinter.CTkButton(self.master)
            self.entry_dict[entry_name] = customtkinter.CTkEntry(self.master)
            self.entry_dict[entry_name].configure(border_width=0,
                                                  corner_radius=0,
                                                  width=self.master.winfo_width() * (2 / 5) - 2.5,
                                                  height=self.master.winfo_height() *
                                                         (1 / (len(self.label_names) + 1)) - 2.5,
                                                  placeholder_text=entry_name, )

            self.entry_buttons_dict[entry_buttons_counter].configure(text="Submit",
                                                                     command=lambda stored_name=entry_name,
                                                                                    button_id=entry_buttons_counter,
                                                                                    entry_object=self.entry_dict[
                                                                                        entry_name]:
                                                                     self.check_value("GlobalConfiguration",
                                                                                      stored_name,
                                                                                      self.entry_dict[
                                                                                          stored_name].get(),
                                                                                      self.entry_buttons_dict[
                                                                                          button_id], entry_object)
                                                                     )

        # Sixth config row:
        font_size_arr = ["bold", "normal"]
        for option in font_size_arr:
            self.font_size[option] = customtkinter.CTkButton(self.master)
            self.font_size[option].configure(border_width=0,
                                             corner_radius=0,
                                             width=self.master.winfo_width() * (
                                                     1 / 5) - 2.5,
                                             height=self.master.winfo_height() *
                                                    (1 / (len(self.label_names) + 1)) - 2.5,
                                             text=option,
                                             command=lambda picked_value=option: self.update_config(
                                                 "GlobalConfiguration",
                                                 "fontThickness", picked_value,
                                                 picked_value, self.font_size))

    def show_buttons(self):
        """
        This very scary looking function does multiple things, it sets repetitive parameters for widgets and its place on frame
        """
        y_position = 0.001
        for widget_dictionary in self.array_coranteng:
            # place entry widgets to frame
            if widget_dictionary is self.entry_dict:
                x_position = 1 * (2 / 5) + 0.001  # starting place
                entry_buttons_counter = 0
                for entry_object in widget_dictionary.values():
                    x_button_poss = x_position + (2 / 5)
                    self.entry_buttons_dict[entry_buttons_counter].configure(border_width=0,
                                                                             corner_radius=0,
                                                                             fg_color=("#636363", "#222222"),
                                                                             hover_color=("#757474", "#3b3b3b"),
                                                                             width=self.master.winfo_width() *
                                                                                   (1 / 5) - 2.5,
                                                                             height=self.master.winfo_height() * (1 / (
                                                                                     len(self.label_names) + 1)) - 2.5)
                    self.entry_buttons_dict[entry_buttons_counter].place(relx=x_button_poss, rely=y_position)
                    entry_object.place(relx=x_position, rely=y_position)
                    y_position += 1 * (1 / (len(self.label_names) + 1))
                    entry_buttons_counter += 1
                y_position -= 1 * (1 / (len(self.label_names) + 1))
            # place other widgets that aren't anyhow bond to entry to frame
            else:
                x_position = 1 * (2 / 5) + 0.001  # starting place for other dictionaries
                for button in widget_dictionary.values():
                    button.configure(border_width=0,
                                     corner_radius=0,
                                     fg_color=("#636363", "#222222"),
                                     hover_color=("#757474", "#3b3b3b"),
                                     width=self.master.winfo_width() * (1 / 5) - 2.5,
                                     height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)) - 2.5, )
                    button.place(relx=x_position, rely=y_position)
                    x_position += 1 * (1 / 5)  # Standard size for other dictionaries
            y_position += 1 * (1 / (len(self.label_names) + 1))
            logger.info("Created buttons and entry widgets for global frame")

    def create_labels(self):
        y_position = 0
        for label_name in self.label_names:
            label = customtkinter.CTkLabel(self.master)
            label.configure(text=label_name,
                            width=self.master.winfo_width() * (2 / 5),
                            height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)),
                            font=(self.font_name, self.label_size + 17, self.font_boldness),
                            fg_color=("#D3D3D3", "#171717"))  # whiteMode DarkMode
            label.place(relx=0, rely=y_position)
            self.label_dict[label_name] = label
            y_position += (1 / (len(self.label_names) + 1))
        logger.info("Created labels for global frame.")

    def on_resize(self, event):
        width_new = event.width * (2 / 5)

        # for loop for labels
        for label in self.label_dict.values():
            label.configure(width=width_new,
                            height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)))

        # recalculate sizes for all buttons that are 2/5 of the size:
        for btn in [self.restore_configurations, self.refresh_frame]:
            btn.configure(height=self.height_frame * (1 / 11),
                          width=self.master.winfo_width() * (2 / 5),
                          anchor=customtkinter.CENTER)

        for _, button_obj in self.entry_buttons_dict.items():
            button_obj.configure(width=self.master.winfo_width() * (1 / 5) - 2.5,
                                 height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)) - 2.5)

        # recalculates widgets in self.array_coranteng giga mega array:
        for item in self.array_coranteng:
            if item is self.entry_dict:
                for key, widget in item.items():
                    widget.configure(width=self.master.winfo_width() * (2 / 5) - 2.5,
                                     height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)) - 2.5)
            else:
                for key, widget in item.items():
                    widget.configure(width=self.master.winfo_width() * (1 / 5) - 2.5,
                                     height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)) - 2.5)
        logger.info("Calculating logic for frame widget to fit to new sized window.")


class Frames:
    def __init__(self, master, width, height, divisor, number_of_buttons, name_of_buttons):
        self.frame_names = ryuConf.red_main_config("careConf", "menuButtonsList")
        self.font_name = ryuConf.red_main_config("GlobalConfiguration", "fontFamily")
        self.label_size = ryuConf.red_main_config("GlobalConfiguration", "labelFontSize")
        self.font_boldness = ryuConf.red_main_config("GlobalConfiguration", "fontThickness")
        self.hover_alert_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")
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
        # reread once again all configs
        self.frame_names = ryuConf.red_main_config("careConf", "menuButtonsList")
        self.font_name = ryuConf.red_main_config("GlobalConfiguration", "fontFamily")
        self.label_size = ryuConf.red_main_config("GlobalConfiguration", "labelFontSize")
        self.font_boldness = ryuConf.red_main_config("GlobalConfiguration", "fontThickness")
        self.hover_alert_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")
        # refresh:
        self.choose_frame(button_id, True)

    def restore_config(self, button_id):
        ryuConf.restore_main_config()
        self.get_new_values_for_refresh(button_id)

    def refresh_restore_buttons(self, button_id):
        # create buttons:
        self.restore_configurations = customtkinter.CTkButton(master=self.frame_dictionary[button_id],
                                                              text="Restore Configurations",
                                                              border_width=2,
                                                              corner_radius=0,
                                                              command=lambda: self.restore_config(button_id),
                                                              )

        self.refresh_frame = customtkinter.CTkButton(master=self.frame_dictionary[button_id],
                                                     text="Refresh frame",
                                                     border_width=2,
                                                     corner_radius=0,
                                                     command=lambda: self.get_new_values_for_refresh(button_id))

        # place:
        self.restore_configurations.place(relx=0.5 - (1 * 2 / 5) - 0.001, rely=0.91)
        self.refresh_frame.place(relx=0.5 + 0.001, rely=0.91)

        # configure stats and size even when it's master frame resizes:
        for widget in [self.restore_configurations, self.refresh_frame]:
            widget.configure(hover_color=(self.hover_alert_color, self.hover_alert_color),
                             font=(
                                 self.font_name, self.label_size + 17,
                                 self.font_boldness),
                             fg_color=("#D3D3D3", "#171717"),
                             text_color=("black", "white"),
                             height=self.height_frame * (1 / 11),
                             width=self.master.winfo_width() * (2 / 5),
                             anchor=customtkinter.CENTER)

    def choose_frame(self, button_id, refresh):
        if refresh:
            # Refresh frame
            for widget in self.frame_dictionary[self.alive_frame].winfo_children():
                widget.place_forget()
            # self.frame_dictionary[self.alive_frame].pack_forget()  # Forget the frame itself
            # self.frame_dictionary[button_id].pack()  # Pack the new frame
            self.alive_frame = button_id  # just making sure, that the frame is set as currently alive frame
            logger.info("Refreshing frame now.")


        # skip if frame alive is the same as next frame to show
        elif self.alive_frame == button_id:
            return
        # Pack the new frame and forget the old one
        elif not self.alive_frame is None:
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
        name_counter = 1
        for name in self.frame_names:
            if button_id == name_counter:
                if button_id < (self.number_of_buttons - 1):  # - log frame
                    self.refresh_restore_buttons(button_id)

                if name == "Global":
                    GlobalFrameWidgets(self.frame_dictionary[button_id], self.width, self.height_frame,
                                       self.restore_configurations, self.refresh_frame)
                    logger.info(f"User picked frame '{name}', creating frame now.")
                    return
                elif name == "Mail":
                    MailFrameWidgets(self.frame_dictionary[button_id], self.width, self.height_frame)
                    logger.info(f"User picked frame '{name}', creating frame now.")
                    return
                elif name == "Web":
                    WebFrameWidgets(self.frame_dictionary[button_id], self.width, self.height_frame)
                    logger.info(f"User picked frame '{name}', creating frame now.")
                    return
                elif name == "Logs":
                    LogsFrameWidgets(self.frame_dictionary[button_id], self.width, self.height_frame)
                    logger.info(f"User picked frame '{name}', creating frame now.")
                    return
                else:
                    logger.error("Button doesn't have its corresponding frame or it isn't present in config options")
                    return
            else:
                name_counter += 1

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
        # EXIT button
        if id_num == self.toolbar_buttons_count:  # aka, the last button is the exit button
            self.button_dictionary[id_num].configure(text=f"EXIT", font=("Helvetica", 36, "bold"))
            self.button_dictionary[id_num].configure(fg_color=("white", "#1a1a1a"),
                                                     hover_color=(self.hover_alert_color, self.hover_alert_color),
                                                     text_color=("black", "white"))
            # here lambda works, because its inside of a for loop, so it gets correct id of a number
            self.button_dictionary[id_num].configure(command=lambda: self.master.destroy())
        # The rest of buttons
        else:
            self.button_dictionary[id_num].configure(text=self.buttons_names[id_num - 1],
                                                     font=("Helvetica", 36, "bold"))
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
        if not self.button_selected is None:
            self.button_dictionary[self.button_selected].configure(fg_color=("white", "#1a1a1a"),
                                                                   hover_color=("#bebebe", "#2e2e2e"))
            self.button_selected = id_num
            self.button_dictionary[id_num].configure(fg_color=("#d3d3d3", "#3b3b3b"),
                                                     hover_color=("#d3d3d3", "#3b3b3b"))
        else:
            self.button_dictionary[id_num].configure(fg_color=("#d3d3d3", "#3b3b3b"),
                                                     hover_color=("#d3d3d3", "#3b3b3b"))
            self.button_selected = id_num


class Core(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        screenNum = ryuConf.red_main_config("GlobalConfiguration", "numOfScreen")
        self.screenWidth = get_monitors()[screenNum].width  # screen width
        self.screenHeight = get_monitors()[screenNum].height  # screen height
        self.heightDivisor = ryuConf.red_main_config("GUI_template", "height_divisor")
        self.buttons_names = ryuConf.red_main_config("careConf", "menuButtonsList")
        self.toolbar_buttons_count = len(ryuConf.red_main_config("careConf", "menuButtonsList"))
        # ---
        # root window setup:
        self.title(f"Caregiver configuration application -- Version:{Version}")
        self.minsize(int(self.screenWidth * 0.80), int(self.screenHeight * 0.80))  # width, height
        self.maxsize(self.screenWidth, self.screenHeight)  # width x height + x + y
        self.geometry(f"{self.screenWidth}x{self.screenHeight}+0+0")
        logger.info("Creating root window for application")
        # ---
        # toolbar class call:
        self.toolbar = Toolbar(self, self.screenWidth, self.screenHeight, self.heightDivisor,
                               self.toolbar_buttons_count, self.buttons_names)


def main():
    app = Core()
    app.mainloop()


if __name__ == '__main__':
    main()
