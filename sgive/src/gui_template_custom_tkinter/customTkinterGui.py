
import customtkinter
from screeninfo import get_monitors
from sgive.src.CaregiverApp import configurationActions as ryuConf

colorScheme = ryuConf.readJsonConfig("GlobalConfiguration", "colorMode")
customtkinter.set_appearance_mode(colorScheme)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class menuButtonsCreate:
    def __init__(self, masterFrame, width, frameHeight):
        self.width = width
        self.frameHeight = frameHeight
        self.masterFrame = masterFrame
        self.numOfMenuButtons = 2
        self.numOfCustomButtons = 8
        self.howManyCustomButtonsOnFrame = 4
        self.menuButtonValue = None
        # subframes
        self.menuButtonFrame = customtkinter.CTkFrame(master=self.masterFrame)
        self.customButtonsFrame = customtkinter.CTkFrame(master=self.masterFrame)
        # calls
        self.createSubFrames()
        self.createMenuButtons()

    def createSubFrames(self):
        menuBtnWidth = self.width / (1+self.howManyCustomButtonsOnFrame)
        customBtnWidth = self.width - menuBtnWidth

        # frame for menu buttons
        self.menuButtonFrame.configure(width=menuBtnWidth)
        self.menuButtonFrame.pack_propagate(False)
        self.menuButtonFrame.configure(height=self.frameHeight)
        self.menuButtonFrame.pack(side=customtkinter.LEFT)

        # frame for custom buttons
        self.customButtonsFrame.configure(width=customBtnWidth)
        self.customButtonsFrame.pack_propagate(False)
        self.customButtonsFrame.configure(height=self.frameHeight)
        self.customButtonsFrame.pack(side=customtkinter.LEFT)

    def createMenuButtons(self):
        menuList = []
        menuDict = {}
        num = 1
        while num <= self.numOfMenuButtons:
            menuList.append(num)
            num += 1
        for number in menuList:
            def storeEachButtonsNum(savedNum=number):
                # TODO: call custom buttons
                print(f"ID kliknutého  tlacitka jest :{savedNum}")
                if not savedNum == len(menuList):
                    menuDict[savedNum].pack_forget()
                    menuDict[savedNum + 1].pack(padx=10)
                    self.menuButtonValue = savedNum
                else:
                    menuDict[savedNum].pack_forget()
                    menuDict[1].pack(padx=10)
                    self.menuButtonValue = savedNum


            menuDict[number] = customtkinter.CTkButton(self.menuButtonFrame)
            menuDict[number].configure(text=f"MENU {number}", font=("Helvetica", 36, "bold"))
            menuDict[number].configure(border_width=3, corner_radius=0)
            menuDict[number].configure(width=(self.width / (1+self.howManyCustomButtonsOnFrame)), height=self.frameHeight)
            menuDict[number].configure(command=storeEachButtonsNum)
            if customtkinter.get_appearance_mode() == "Dark":

                menuDict[number].configure(fg_color="#1e1f22")  # , hover_color="#1e1f22"
            else:
                menuDict[number].configure(fg_color="white", text_color="black")

        menuDict[1].pack(padx=10) #show only first


        print("create menu shit thing thing")

class gui:
    def __init__(self, root):
        self.root = root
        # TODO: change screen number to conf.json read
        self.screenWidth = get_monitors()[0].width  # screen width
        self.screenHeight = get_monitors()[0].height  # screen height
        # TODO: change divisor to conf.json read
        self.heightDivisor = 7
        # calls for root window setup etc
        self.rootWindowSetup()
        self.appMenuFrameSetup()

    def rootWindowSetup(self):
        self.root.title("custom tkinter gui template")
        self.root.attributes('-fullscreen', True)
        self.root.configure(background="white")

    def appMenuFrameSetup(self):
        menuFrame = customtkinter.CTkFrame(self.root)
        menuFrame.pack_propagate(False)
        menuFrame.configure(width=self.screenWidth, height=self.screenHeight / self.heightDivisor)
        menuFrame.pack(side=customtkinter.TOP)
        # calling class for menuFrame actions
        menuButtonsCreate(menuFrame, self.screenWidth, self.screenHeight / self.heightDivisor)


if __name__ == '__main__':
    root = customtkinter.CTk()
    gui(root)
    root.mainloop()
