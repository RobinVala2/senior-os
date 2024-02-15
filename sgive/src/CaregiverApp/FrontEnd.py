import customtkinter
from screeninfo import get_monitors
import sgive.src.CaregiverApp.configurationActions as ryuConf
import logging
import os

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
        # func calls:
        self.find_log_files()

        self.options_toolbar()
        self.log_textbox(None)

    def refresh(self):
        print("refreshing???")
        for widget in self.master.winfo_children():
            # this forgets all widgets inside a frame
            widget.pack_forget()
        self.master.pack_forget()  # this forgets frame itself
        self.master.pack()
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
        textbox.configure(height=self.height - (self.height * 0.10), width=self.width, fg_color=("#D3D3D3", "#171717"),
                          scrollbar_button_color=("black", "white"),
                          scrollbar_button_hover_color=("#3b3b3b", "#636363"))
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
        self.screen_width_diff = 0  # for checkin, if the screen width is correct
        self.restore_configurations = restore
        self.refresh_frame = refresh
        # create objects for widgets:
        self.screen_arr = []
        self.screen_num = {}
        self.label_dict = {}
        self.language_dict = {}
        # for showing each buttons at one function and resize calculations ↓ ↓ ↓ ↓ ↓
        self.mega_array = [self.screen_num, self.language_dict]
        # ---------- CALS --------------
        self.master.winfo_width()
        self.master.bind("<Configure>", self.on_resize)
        self.create_labels()
        self.buttons()
        self.show_buttons()
        # E N D of constructor

    @staticmethod
    def update_config(key, name, value, button_id, button_list):
        # pokud se zadaří a nikde nebude value a button_id rozdílné, tak pak tyto proměnné sloučit
        return_value = ryuConf.edit_main_config(key, name, value)
        print("button object is:", button_id)
        for all_buttons in button_list:  # aka restore all buttons in that row to its original color
            button_list[all_buttons].configure(fg_color=("#636363", "#222222"), hover_color=("#757474", "#3b3b3b"))

        if return_value is True:
            button_list[button_id].configure(fg_color=("#4b5946", "#4b5946"), hover_color=("#7c8e76", "#7c8e76"))
        else:
            button_list[button_id].configure(fg_color=("red", "red"), hover_color=("#8B0000", "#8B0000"))
            print("oh fuck")

    def buttons(self):
        # ryuConf.edit_main_config(key,name,value),
        # first config row: ------------------------------------------------------------
        screen_primary = 0
        while screen_primary < len(get_monitors()):
            self.screen_arr.append(screen_primary)
            screen_primary += 1
        for id_value in self.screen_arr:
            self.screen_num[id_value] = customtkinter.CTkButton(master=self.master)
            self.screen_num[id_value].configure(border_width=0,
                                                corner_radius=0,
                                                fg_color=("#636363", "#222222"),
                                                hover_color=("#757474", "#3b3b3b"),
                                                width=self.master.winfo_width() * (1 / 5),
                                                height=self.master.winfo_height() * (
                                                        1 / (len(self.label_names) + 1)),
                                                text=f"Screen {id_value}",
                                                command=lambda current_id=id_value: self.update_config(
                                                    "GlobalConfiguration",
                                                    "numOfScreen",
                                                    current_id,
                                                    current_id,
                                                    self.screen_num))
        # -------------------------------------------------------------------------------
        # second config row: ------------------------------------------------------------
        language_arr = ryuConf.red_main_config("careConf", "LanguageOptions")
        for language in language_arr:
            self.language_dict[language] = customtkinter.CTkButton(master=self.master)
            self.language_dict[language].configure(border_width=0,
                                                    corner_radius=0,
                                                    fg_color=("#636363", "#222222"),
                                                    hover_color=("#757474", "#3b3b3b"),
                                                    width=self.master.winfo_width() * (1 / 5),
                                                    height=self.master.winfo_height() * (
                                                               1 / (len(self.label_names) + 1)),
                                                    text=language,
                                                    command=lambda lang_id=language: self.update_config(
                                                                                                    "GlobalConfiguration",
                                                                                                    "language",
                                                                                                    lang_id,
                                                                                                    lang_id,
                                                                                                    self.language_dict))

            # -------------------------------------------------------------------------------
            # third config row: ------------------------------------------------------------
            x_position = 1 * (2 / 5)  # reset X position
            # y_position = y_position + 1 * (1 / (len(self.label_names) + 1))
            # lower Y position by one button height down

    def show_buttons(self):
        y_position = 0
        for array in self.mega_array:
            x_position = 1 * (2 / 5)
            for button in array:
                array[button].place(relx=x_position, rely=y_position)
                x_position = x_position + (1 * (1 / 5))
            y_position = y_position + (1 * (1 / (len(self.label_names) + 1)))


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

    def on_resize(self, event):
        width_new = event.width * (2 / 5)

        # for loop for labels
        for label in self.label_dict.values():
            label.configure(width=width_new,
                            height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)))

        # recalculate sizes for all buttons that are 2/5 of the size
        for btn in [self.restore_configurations, self.refresh_frame]:
            btn.configure(height=self.height_frame * (1 / 11),
                          width=self.master.winfo_width() * (2 / 5),
                          anchor=customtkinter.CENTER)

        # recalculate sizes for all buttons that are 1/5 of the size
        for array in self.mega_array:
            for widget in array:
                array[widget].configure(width=self.master.winfo_width() * (1 / 5),
                                                     height=self.master.winfo_height() * (
                                                             1 / (len(self.label_names) + 1)))


class Frames:
    def __init__(self, master, width, height, divisor, number_of_buttons, name_of_buttons):
        self.label_names = ryuConf.red_main_config("careConf", "GlobalFrameLabels")
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
        self.get_screen_dimensions()

    def get_screen_dimensions(self):
        ctk_screenwidth = self.master.winfo_screenwidth()
        print("\n------------------------------")
        print("expected screen width:", ctk_screenwidth)
        print("true screen width:", self.width)
        print("frame width with ctk shit:", self.master.winfo_width())
        print("------------------------------\n")

    def get_new_values_for_refresh(self, button_id):
        # set global color:
        customtkinter.set_appearance_mode(ryuConf.red_main_config("GlobalConfiguration", "colorMode"))
        # reread once again all configs
        self.label_names = ryuConf.red_main_config("careConf", "GlobalFrameLabels")
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
        # refresh frame
        if refresh is True:
            for widget in self.frame_dictionary[self.alive_frame].winfo_children():
                # this forgets all widgets inside a frame
                widget.pack_forget()
            self.frame_dictionary[self.alive_frame].pack_forget()  # this forgets frame itself
            self.frame_dictionary[button_id].pack_forget()
            # huh?
            self.frame_dictionary[button_id].pack()

        # check if frame isn't already running
        elif self.alive_frame == button_id:
            return

        # pack_forget old frame and pack new one
        elif not self.alive_frame is None and refresh is False:  # forget showing frame, show new
            for widget in self.frame_dictionary[self.alive_frame].winfo_children():
                widget.pack_forget()
            self.frame_dictionary[self.alive_frame].pack_forget()
            self.frame_dictionary[button_id].pack()
            self.alive_frame = button_id

        else:
            # shouldn't ever happen, because there should always be the last frame, if no configuration is opened
            # it gets called in constructor
            logger.error("There is no frame to show, even there should be.")
            return

        # some ryu:tm: autism stuff for showing corresponding class with widgets to its frame
        name_counter = 1
        for name in self.frame_names:
            if button_id == name_counter:
                if button_id < (self.number_of_buttons - 1):  # - log frame
                    self.refresh_restore_buttons(button_id)
                # manual work for now:
                # later, maybe add array for frame widgets classes and go through it
                if name == "Global":
                    GlobalFrameWidgets(self.frame_dictionary[button_id], self.width, self.height_frame,
                                       self.restore_configurations, self.refresh_frame)
                    return
                elif name == "Mail":
                    MailFrameWidgets(self.frame_dictionary[button_id], self.width, self.height_frame)
                    return
                elif name == "Web":
                    WebFrameWidgets(self.frame_dictionary[button_id], self.width, self.height_frame)
                    return
                elif name == "LOGS":
                    LogsFrameWidgets(self.frame_dictionary[button_id], self.width, self.height_frame)
                    return
                else:
                    logger.error("button doesnt have its corresponding frame or it isn't present in config options")
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
        if id_num == self.toolbar_buttons_count:  # aka, the last button is the exit button
            self.button_dictionary[id_num].configure(text=f"EXIT", font=("Helvetica", 36, "bold"))
            self.button_dictionary[id_num].configure(fg_color=("white", "#1a1a1a"),
                                                     hover_color=(self.hover_alert_color, self.hover_alert_color),
                                                     text_color=("black", "white"))
            # here lambda works, because its inside of a for loop, so it gets correct id of a number
            self.button_dictionary[id_num].configure(command=lambda: self.master.destroy())
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
            print("selected button is ", self.button_selected)
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
        # ---
        # toolbar class call:
        self.toolbar = Toolbar(self, self.screenWidth, self.screenHeight, self.heightDivisor,
                               self.toolbar_buttons_count, self.buttons_names)


def main():
    app = Core()
    app.mainloop()


if __name__ == '__main__':
    main()
