import customtkinter
from screeninfo import get_monitors
import sgive.src.CaregiverApp.configurationActions as ryuConf
import logging

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
        if id_num == self.toolbar_buttons_count:
            self.button_dictionary[id_num].configure(text=f"EXIT", font=("Helvetica", 36, "bold"))
            self.button_dictionary[id_num].configure(command=lambda: self.master.destroy())
        else:
            self.button_dictionary[id_num].configure(text=self.buttons_names[id_num - 1],
                                                     font=("Helvetica", 36, "bold"))
            self.button_dictionary[id_num].configure(command=lambda: self.frame_class.choose_frame(id_num, False))

        self.button_dictionary[id_num].configure(width=self.width / self.toolbar_buttons_count,
                                                 height=self.frame_height)

        if colorScheme == "light":
            self.button_dictionary[id_num].configure(fg_color="white", hover_color="#D3D3D3",
                                                     text_color="black")  # white
        else:
            self.button_dictionary[id_num].configure(fg_color="#1a1a1a", hover_color="#2e2e2e",
                                                     text_color="white")  # dark

        self.button_dictionary[id_num].configure(border_width=3, corner_radius=0)

        # relx or rely is between 0 and 1, 0 is left corner, 1 is right corner etc.
        if id_num == 1:
            self.button_dictionary[1].place(relx=0, rely=0)
        else:
            self.x_poss = self.x_poss + (1 / self.toolbar_buttons_count)
            self.button_dictionary[id_num].place(relx=self.x_poss, rely=0)


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
        print("Frame that is alive:", self.alive_frame, "\nFrame that should be loaded next:", button_id)
        if refresh is True:  # only for refreshing, there is no need for .pack, because it was done once already
            self.frame_dictionary[self.alive_frame].pack_forget()
            self.frame_dictionary[button_id].pack_forget()
        elif self.alive_frame == button_id:  # single instance lock
            return
        elif not self.alive_frame is None and refresh is False:  # forget showing frame, show new
            self.frame_dictionary[self.alive_frame].pack_forget()
            self.frame_dictionary[button_id].pack()
            self.alive_frame = button_id
        else:  # shouldn't ever happen, there is no frame showing
            self.frame_dictionary[button_id].pack()
            self.alive_frame = button_id

        # calling each frame classes for its widgets
        if button_id == 1 and self.buttons_name[button_id - 1] == "Global":
            FrameGlobal(self.frame_dictionary[button_id], self.width, self.height, self.height_frame, self.master)

        elif button_id == 2 and self.buttons_name[button_id - 1] == "Mail":
            MailGlobal(self.frame_dictionary[button_id], self.width, self.height, self.height_frame, self.master)

        elif button_id == 3 and self.buttons_name[button_id - 1] == "Web":
            WebGlobal(self.frame_dictionary[button_id])

        elif button_id == 4 and self.buttons_name[button_id - 1] == "LOGS":
            LogsGlobal(self.frame_dictionary[button_id])

        else:
            exit("ryu.02")


class FrameDefault:
    def __init__(self, frame_root):
        self.master = frame_root

        label = customtkinter.CTkLabel(master=frame_root, text="DEFAULT FRAME :)", font=("Helvetica", 36, "bold"))
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


class FrameGlobal:
    def __init__(self, frame_root, width, height, height_frame, master):
        self.master = frame_root
        self.height_frame = height_frame
        self.width = width
        self.label_names = ryuConf.red_main_config("careConf", "GlobalFrameLabels")
        self.font_name = ryuConf.red_main_config("GlobalConfiguration", "fontFamily")
        self.label_size = ryuConf.red_main_config("GlobalConfiguration", "labelFontSize")
        self.font_boldness = ryuConf.red_main_config("GlobalConfiguration", "fontThickness")
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
                                                              command=lambda: [ryuConf.restore_main_config(), self.refresh()],
                                                              height=self.height_frame * (1 / (len(self.label_names)+1)),
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
                                                     height=self.height_frame * (1 / (len(self.label_names)+1)),
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
                            height=self.master.winfo_height() * (1 / (len(self.label_names)+1)),
                            # height=self.height_frame * (1 / 11),
                            fg_color=("#D3D3D3", "#171717"))  # whiteMode DarkMode
            label.place(relx=0, rely=y_position)
            self.label_dict[label_name] = label
            y_position += (1 / (len(self.label_names)+1))

    def on_resize(self, event):
        # Update the width and height of the frame
        self.width = event.width
        # self.height_frame = event.height

        # Resize labels
        for label in self.label_dict.values():
            label.configure(width=self.width * (2 / 5),
                            height=self.master.winfo_height() * (1 / (len(self.label_names)+1)))
            # height=self.height_frame * (1 / 11))

        # Recalculate button height and width
        self.restore_configurations.configure(height=self.height_frame * (1 / (len(self.label_names)+1)),
                                              width=self.width * (2 / 5))
        self.refresh_frame.configure(height=self.height_frame * (1 / (len(self.label_names)+1)),
                                     width=self.width * (2 / 5))


class MailGlobal:
    def __init__(self, frame_root, width, height, height_frame, master):
        self.master = frame_root
        self.height_frame = height_frame
        self.width = width
        self.label_names = ryuConf.red_main_config("careConf", "SMailFrameLabels")
        self.font_name = ryuConf.red_main_config("GlobalConfiguration", "fontFamily")
        self.label_size = ryuConf.red_main_config("GlobalConfiguration", "labelFontSize")
        self.font_boldness = ryuConf.red_main_config("GlobalConfiguration", "fontThickness")
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
                                                              command=lambda: [ryuConf.restore_main_config(), self.refresh()],
                                                              height=self.master.winfo_height() * (1 / self.button_height_fract),
                                                              # 1/11, because I allow only 10 options on frame
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
                                                     height=self.height_frame * (1 / self.button_height_fract),
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
               buttons_names).choose_frame(2, True)

    def create_labels(self):
        y_position = 0
        for label_name in self.label_names:
            label = customtkinter.CTkLabel(self.master)
            label.configure(text=label_name,
                            font=(self.font_name, self.label_size + 17, self.font_boldness),
                            width=self.width * (2 / 5),
                            height=self.master.winfo_height() * (1 / (len(self.label_names)+1)),
                            # height=self.height_frame * (1 / 11),
                            fg_color=("#D3D3D3", "#171717"))  # whiteMode DarkMode
            label.place(relx=0, rely=y_position)
            self.label_dict[label_name] = label
            y_position += (1 / (len(self.label_names)+1))

    def on_resize(self, event):
        # Update the width and height of the frame
        self.width = event.width
        # self.height_frame = event.height

        # Resize labels
        for label in self.label_dict.values():
            label.configure(width=self.width * (2 / 5),
                            height=self.master.winfo_height() * (1 / (len(self.label_names)+1)))
            # height=self.height_frame * (1 / 11))

        # Recalculate button height and width
        self.restore_configurations.configure(height=self.master.winfo_height() * (1 / self.button_height_fract),
                                              width=self.width * (2 / 5))
        self.refresh_frame.configure(height=self.height_frame * (1 / self.button_height_fract),
                                     width=self.width * (2 / 5))


class WebGlobal:
    def __init__(self, frame_root):
        self.master = frame_root

        label = customtkinter.CTkLabel(master=frame_root, text="WEB CONFIG FRAME SOON")
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


class LogsGlobal:
    def __init__(self, frame_root):
        self.master = frame_root

        label = customtkinter.CTkLabel(master=frame_root, text="LOG FRAME SOON")
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


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
        self.title("Caregiver configuration application -- alpha:0.0.1")
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
