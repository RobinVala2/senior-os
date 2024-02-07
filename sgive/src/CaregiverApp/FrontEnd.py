import customtkinter
from screeninfo import get_monitors
import sgive.src.CaregiverApp.configurationActions as ryuConf

colorScheme = ryuConf.readJsonConfig("GlobalConfiguration", "colorMode")
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
        self.frame_height = height/divisor
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
        print("alocating memory for creation")
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
            self.button_dictionary[id_num].configure(text=self.buttons_names[id_num - 1], font=("Helvetica", 36, "bold"))
            self.button_dictionary[id_num].configure(command=lambda: self.frame_class.choose_frame(id_num))

        self.button_dictionary[id_num].configure(width=self.width / self.toolbar_buttons_count, height=self.frame_height)

        if colorScheme == "light":
            self.button_dictionary[id_num].configure(fg_color="white", hover_color="#D3D3D3", text_color="black")  # white
        else:
            self.button_dictionary[id_num].configure(fg_color="#1a1a1a",hover_color="#2e2e2e", text_color="white")  # dark

        self.button_dictionary[id_num].configure(border_width=3, corner_radius=0)

        if id_num == 1:
            self.button_dictionary[1].place(x=0, y=0)
        else:
            self.x_poss = self.x_poss + int(self.width / self.toolbar_buttons_count)
            self.button_dictionary[id_num].place(x=self.x_poss, y=0)



    def frame_pic(self, id_num):
        if id_num == 1:
            print("global config frame")
            self.frame_class.choose_frame(id_num)
        elif id_num == 2:
            print("smail config frame")
            self.frame_class.choose_frame(id_num)
        elif id_num == 3:
            print("sweb config frame")
            self.frame_class.choose_frame(id_num)
        elif id_num == 4:
            print("log frame")
            self.frame_class.choose_frame(id_num)
        else:
            print("error, ending program...")
            exit(404)


class Frames:
    def __init__(self, master, width, height, divisor, number_of_buttons, name_of_buttons):
        self.master = master
        self.width = width
        self.height_frame = height - (height / divisor)
        self.divisor = divisor
        self.number_of_buttons = number_of_buttons + 1  # adding default frame
        self.buttons_name = name_of_buttons
        # -----
        self.alive_frame = None
        self.frame_array = []
        self.frame_dictionary = {}
        # calls:
        self.alocate_frames()

    def alocate_frames(self):
        number = 1
        while number <= self.number_of_buttons:
            self.frame_array.append(number)
            number += 1
        for num_id in self.frame_array:
            self.create_frames(num_id)

    def create_frames(self, number):
        self.frame_dictionary[number] = customtkinter.CTkFrame(self.master)
        if colorScheme == "light":
            self.frame_dictionary[number].configure(fg_color="red")
        else:
            self.frame_dictionary[number].configure(fg_color="#1a1a1a")
        self.frame_dictionary[number].pack_propagate(False)
        self.frame_dictionary[number].configure(width=self.width, height=self.height_frame)
        number += 1


    def choose_frame(self, button_id):
        if self.alive_frame is None:
            self.frame_dictionary[button_id].pack()
            self.alive_frame = button_id
            print(f"frame naživu je: {button_id}")
        else:
            self.frame_dictionary[self.alive_frame].pack_forget()
            print(f"zaviram frame: {self.alive_frame}")
            self.frame_dictionary[button_id].pack()
            self.alive_frame = button_id
            print(f"frame naživu je: {button_id}")

        if button_id == 1 and self.buttons_name[button_id-1] == "Global":
            FrameGlobal(self.frame_dictionary[1])
        elif button_id == 2 and self.buttons_name[button_id - 1] == "Mail":
            MailGlobal(self.frame_dictionary[2])
        elif button_id == 3 and self.buttons_name[button_id - 1] == "Web":
            WebGlobal(self.frame_dictionary[3])
        elif button_id == 4 and self.buttons_name[button_id - 1] == "LOGS":
            LogsGlobal(self.frame_dictionary[4])


class FrameGlobal:
    def __init__(self, frame_root):
        self.master = frame_root

        label = customtkinter.CTkLabel(master=frame_root, text="GLOBAL CONFIG FRAME SOON")
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


class MailGlobal:
    def __init__(self, frame_root):
        self.master = frame_root

        label = customtkinter.CTkLabel(master=frame_root, text="MAIL CONFIG FRAME SOON")
        label.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)


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
        # needed values:
        screenNum = ryuConf.readJsonConfig("GlobalConfiguration", "numOfScreen")
        self.screenWidth = get_monitors()[screenNum].width  # screen width
        self.screenHeight = get_monitors()[screenNum].height  # screen height
        self.heightDivisor = ryuConf.readJsonConfig("GUI_template", "height_divisor")
        self.buttons_names = ryuConf.readJsonConfig("careConf", "menuButtonsList")
        self.toolbar_buttons_count = len(ryuConf.readJsonConfig("careConf", "menuButtonsList"))
        # root configs: --------
        self.title("Caregiver configuration application -- alpha:0.0.1")
        # width, height
        self.minsize(int(self.screenWidth * 0.80), int(self.screenHeight * 0.80))
        self.maxsize(self.screenWidth, self.screenHeight)
        # width x height + x + y
        self.geometry(f"{self.screenWidth}x{self.screenHeight}+0+0")
        # toolbar:
        self.toolbar = Toolbar(self, self.screenWidth, self.screenHeight, self.heightDivisor, self.toolbar_buttons_count, self.buttons_names)

        # frames:
        # self.frame = Frames(self, self.screenWidth, self.screenHeight, self.heightDivisor, self.toolbar_buttons_count)


def main():
    app = Core()
    app.mainloop()


if __name__ == '__main__':
    main()
