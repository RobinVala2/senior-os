import customtkinter
from screeninfo import get_monitors
import sgive.src.CaregiverApp.configurationActions as ryuConf
import logging
import os

"""
Author: RYUseless
Github: https://github.com/RYUseless
Version: 0.0.1(Alpha)
"""

logger = logging.getLogger(__file__)
logger.info("initiated logging")

colorScheme = ryuConf.red_main_config("GlobalConfiguration", "colorMode")
customtkinter.set_appearance_mode(colorScheme)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


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


class Frames:
    def __init__(self, master, width, height, divisor, number_of_buttons, name_of_buttons):
        self.master = master
        self.width = width
        self.height_frame = height - (height / divisor)
        self.divisor = divisor
        self.number_of_buttons = number_of_buttons + 1  # adding default frame
        self.buttons_name = name_of_buttons
        self.height = height
        # ---
        self.alive_frame = self.number_of_buttons  # default frame (highest number from button names array + 1)
        self.frame_array = []
        self.frame_dictionary = {}
        # calls:
        self.alocate_frames()
        FrameDefault(self.frame_dictionary[self.number_of_buttons])
        self.frame_dictionary[self.number_of_buttons].pack()

    def alocate_frames(self):
        number = 1
        while number <= self.number_of_buttons:
            self.frame_array.append(number)
            number += 1
        for num_id in self.frame_array:
            self.create_frames(num_id)

    def create_frames(self, number):
        self.frame_dictionary[number] = customtkinter.CTkFrame(self.master)
        self.frame_dictionary[number].configure(fg_color=("white", "#1a1a1a"))
        self.frame_dictionary[number].pack_propagate(False)
        self.frame_dictionary[number].configure(width=self.width, height=self.height_frame)
        number += 1

    def choose_frame(self, button_id, refresh):
        if refresh is True:  # only for refreshing, there is no need for .pack, because it was done once already
            for widget in self.frame_dictionary[self.alive_frame].winfo_children():  # this forgets all widgets inside a frame
                widget.pack_forget()
            self.frame_dictionary[self.alive_frame].pack_forget()  # this forgets frame itself
            self.frame_dictionary[button_id].pack_forget()

        elif self.alive_frame == button_id:  # single instance lock
            return

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

        # calling each frame classes for its widgets
        if button_id == 1 and self.buttons_name[button_id - 1] == "Global":
            FrameGlobal(self.frame_dictionary[button_id], self.width, self.height, self.height_frame, self.master)

        elif button_id == 2 and self.buttons_name[button_id - 1] == "Mail":
            MailGlobal(self.frame_dictionary[button_id], self.width, self.height, self.height_frame, self.master)

        elif button_id == 3 and self.buttons_name[button_id - 1] == "Web":
            WebGlobal(self.frame_dictionary[button_id])

        elif button_id == 4 and self.buttons_name[button_id - 1] == "LOGS":
            LogsGlobal(self.frame_dictionary[button_id], self.width, self.height_frame)

        else:
            logger.error("button doesnt have its corresponding frame or it isn't present in config options")
            exit("ryu.02")


class FrameDefault:
    def __init__(self, frame_root):
        self.master = frame_root

        label = customtkinter.CTkLabel(master=frame_root, text="DEFAULT FRAME :)", font=("Helvetica", 36, "bold"))
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


class FrameGlobal:
    def __init__(self, frame_root, width, height, height_frame, master):
        logger.info("Creating and showing frame for Global configuration.")
        self.master = frame_root
        self.height_frame = height_frame
        self.width = width
        self.label_names = ryuConf.red_main_config("careConf", "GlobalFrameLabels")
        self.font_name = ryuConf.red_main_config("GlobalConfiguration", "fontFamily")
        self.label_size = ryuConf.red_main_config("GlobalConfiguration", "labelFontSize")
        self.font_boldness = ryuConf.red_main_config("GlobalConfiguration", "fontThickness")
        self.hover_alert_color = ryuConf.red_main_config("GlobalConfiguration", "alertColor")
        self.label_dict = {}
        # -----------------
        # needed for refresh:
        self.height = height
        self.master_dummy = master
        # -----------------
        # call:
        self.create_labels()
        # -----------------
        # buttons:
        self.restore_configurations = customtkinter.CTkButton(master=frame_root, text="Restore Configurations",
                                                              command=lambda: [ryuConf.restore_main_config(),
                                                                               self.refresh()],
                                                              height=self.height_frame * (
                                                                      1 / (len(self.label_names) + 1)),
                                                              hover_color=(
                                                                  self.hover_alert_color, self.hover_alert_color),
                                                              width=self.width * (2 / 5),
                                                              font=(
                                                                  self.font_name, self.label_size + 17,
                                                                  self.font_boldness),
                                                              fg_color=("#D3D3D3", "#171717"),
                                                              text_color=("black", "white"),
                                                              anchor=customtkinter.CENTER)
        self.restore_configurations.place(relx=0.5 - (1 * 2 / 5) - 0.001, rely=0.91)

        self.refresh_frame = customtkinter.CTkButton(master=frame_root, text="Refresh frame",
                                                     command=lambda: self.refresh(),
                                                     height=self.height_frame * (1 / (len(self.label_names) + 1)),
                                                     hover_color=(self.hover_alert_color, self.hover_alert_color),
                                                     width=self.width * (2 / 5),
                                                     font=(
                                                         self.font_name, self.label_size + 17,
                                                         self.font_boldness),
                                                     fg_color=("#D3D3D3", "#171717"),
                                                     text_color=("black", "white"),
                                                     anchor=customtkinter.CENTER)
        self.refresh_frame.place(relx=0.5 + 0.001, rely=0.91)
        # -----------------
        # Bind the resize event
        self.master.bind("<Configure>", self.on_resize)
        # end ---------------------------

    def refresh(self):
        customtkinter.set_appearance_mode(ryuConf.red_main_config("GlobalConfiguration", "colorMode"))
        heightDivisor = ryuConf.red_main_config("GUI_template", "height_divisor")
        buttons_names = ryuConf.red_main_config("careConf", "menuButtonsList")
        toolbar_buttons_count = len(ryuConf.red_main_config("careConf", "menuButtonsList"))
        # call again class for frame generation
        Frames(self.master_dummy, self.width, self.height, heightDivisor, toolbar_buttons_count,
               buttons_names).choose_frame(1, True)

    def create_labels(self):
        y_position = 0
        for label_name in self.label_names:
            label = customtkinter.CTkLabel(self.master)
            label.configure(text=label_name,
                            font=(self.font_name, self.label_size + 17, self.font_boldness),
                            width=self.width * (2 / 5),
                            height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)),
                            # height=self.height_frame * (1 / 11),
                            fg_color=("#D3D3D3", "#171717"))  # whiteMode DarkMode
            label.place(relx=0, rely=y_position)
            self.label_dict[label_name] = label
            y_position += (1 / (len(self.label_names) + 1))

    def on_resize(self, event):
        # Update the width and height of the frame
        self.width = event.width
        # self.height_frame = event.height

        # Resize labels
        for label in self.label_dict.values():
            label.configure(width=self.width * (2 / 5),
                            height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)))
            # height=self.height_frame * (1 / 11))

        # Recalculate button height and width
        self.restore_configurations.configure(height=self.height_frame * (1 / (len(self.label_names) + 1)),
                                              width=self.width * (2 / 5))
        self.refresh_frame.configure(height=self.height_frame * (1 / (len(self.label_names) + 1)),
                                     width=self.width * (2 / 5))


class MailGlobal:
    def __init__(self, frame_root, width, height, height_frame, master):
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
        # needed for refresh:
        self.height = height
        self.master_dummy = master
        # -----------------
        # call:
        self.create_labels()
        # -----------------
        # lower buttons:
        self.restore_configurations = customtkinter.CTkButton(master=frame_root, text="Restore Configurations",
                                                              command=lambda: [ryuConf.restore_main_config(),
                                                                               self.refresh()],
                                                              height=self.master.winfo_height() * (
                                                                      1 / self.button_height_fract),
                                                              # 1/11, because I allow only 10 options on frame
                                                              width=self.width * (2 / 5),
                                                              font=(
                                                                  self.font_name, self.label_size + 17,
                                                                  self.font_boldness),
                                                              hover_color=(
                                                                  self.hover_alert_color, self.hover_alert_color),
                                                              fg_color=("#D3D3D3", "#171717"),
                                                              text_color=("black", "white"),
                                                              anchor=customtkinter.CENTER)
        self.restore_configurations.place(relx=0.5 - (1 * 2 / 5) - 0.001, rely=0.91)

        self.refresh_frame = customtkinter.CTkButton(master=frame_root, text="Refresh frame",
                                                     command=lambda: self.refresh(),
                                                     height=self.height_frame * (1 / self.button_height_fract),
                                                     width=self.width * (2 / 5),
                                                     font=(
                                                         self.font_name, self.label_size + 17,
                                                         self.font_boldness),
                                                     hover_color=(self.hover_alert_color, self.hover_alert_color),
                                                     fg_color=("#D3D3D3", "#171717"),
                                                     text_color=("black", "white"),
                                                     anchor=customtkinter.CENTER)
        self.refresh_frame.place(relx=0.5 + 0.001, rely=0.91)
        # -----------------
        # Bind the resize event
        self.master.bind("<Configure>", self.on_resize)
        # end ---------------------------

    def refresh(self):
        customtkinter.set_appearance_mode(ryuConf.red_main_config("GlobalConfiguration", "colorMode"))
        heightDivisor = ryuConf.red_main_config("GUI_template", "height_divisor")
        buttons_names = ryuConf.red_main_config("careConf", "menuButtonsList")
        toolbar_buttons_count = len(ryuConf.red_main_config("careConf", "menuButtonsList"))
        # call again class for frame generation
        Frames(self.master_dummy, self.width, self.height, heightDivisor, toolbar_buttons_count,
               buttons_names).choose_frame(2, True)

    def create_labels(self):
        y_position = 0
        for label_name in self.label_names:
            label = customtkinter.CTkLabel(self.master)
            label.configure(text=label_name,
                            font=(self.font_name, self.label_size + 17, self.font_boldness),
                            width=self.width * (2 / 5),
                            height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)),
                            # height=self.height_frame * (1 / 11),
                            fg_color=("#D3D3D3", "#171717"))  # whiteMode DarkMode
            label.place(relx=0, rely=y_position)
            self.label_dict[label_name] = label
            y_position += (1 / (len(self.label_names) + 1))

    def on_resize(self, event):
        # Update the width and height of the frame
        self.width = event.width
        # self.height_frame = event.height

        # Resize labels
        for label in self.label_dict.values():
            label.configure(width=self.width * (2 / 5),
                            height=self.master.winfo_height() * (1 / (len(self.label_names) + 1)))
            # height=self.height_frame * (1 / 11))

        # Recalculate button height and width
        self.restore_configurations.configure(height=self.master.winfo_height() * (1 / self.button_height_fract),
                                              width=self.width * (2 / 5))
        self.refresh_frame.configure(height=self.height_frame * (1 / self.button_height_fract),
                                     width=self.width * (2 / 5))


class WebGlobal:
    def __init__(self, frame_root):
        self.master = frame_root
        logger.info("Creating and showing frame for Web configuration.")
        label = customtkinter.CTkLabel(master=frame_root, text="WEB CONFIG FRAME SOON")
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


class LogsGlobal:
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
        print("todo")


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
                                                      width=self.width * 1/5)
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
                                                      width=self.width * 1/5)
        filter_options = ["INFO", "WARNING", "CRITICAL", "ERROR", "ALL"]
        pick_filter_btn.configure(values=filter_options)
        pick_filter_btn.place(relx=1 * (1/5), rely=0)
        pick_filter_btn.set("Choose LOG filter option")  # default showing value
        # ---------------------------------------------------------------------------
        # refresh button:
        button = customtkinter.CTkButton(master=self.options_toolbar_frame,
                                         height=self.height * 0.10,
                                         width=self.width * 1 / 5,
                                         text="Refresh",
                                         command=lambda: self.refresh())
        button.place(relx=1 * (4/5), rely=0)

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
        self.title("Caregiver configuration application -- Version: 0.0.1(Alpha)")
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
