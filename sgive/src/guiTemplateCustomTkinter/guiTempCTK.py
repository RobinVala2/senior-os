import customtkinter
from screeninfo import get_monitors
import sgive.src.CaregiverApp.configurationActions as ryuConf

# if there are any issues, install "packaging"

colorScheme = ryuConf.readJsonConfig("GlobalConfiguration", "colorMode")
customtkinter.set_appearance_mode(colorScheme)  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


# Ǚ
class MenuBar:
    def __init__(self, masterFrame: customtkinter.CTkFrame, width: int, frameHeight: int, root: customtkinter.CTk):
        self.root = root
        self.width = width
        self.frameHeight = frameHeight
        self.masterFrame = masterFrame
        self.numOfCustomButtons = ryuConf.readJsonConfig("GUI_template", "num_of_opt_buttons")
        self.howManyCustomButtonsOnFrame = ryuConf.readJsonConfig("GUI_template", "num_of_opt_on_frame")
        # menuButtons needed things:
        self.menuList: list = []
        self.menuDict: dict = {}
        self.menuButtonValue = None
        # switching customButtons
        self.lowestID: int = 1
        self.highestID: int = 1
        # end of menuButtons section
        # subframes
        self.menuButtonFrame = customtkinter.CTkFrame(master=self.masterFrame)
        self.customButtonsFrame = customtkinter.CTkFrame(master=self.masterFrame)
        # custom buttons:
        self.customBtnDict = {}
        # calls
        self.createSubFrames()
        self.createCustomButtons()
        self.createMenuButtons()

    def createSubFrames(self):
        menuBtnWidth = self.width / (1 + self.howManyCustomButtonsOnFrame)
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

    def getHowManyMenuButtons(self):
        moduloThing = self.numOfCustomButtons % self.howManyCustomButtonsOnFrame
        if moduloThing == 0:
            numOfMenuButtons = self.numOfCustomButtons / self.howManyCustomButtonsOnFrame
            return numOfMenuButtons
        else:
            numOfMenuButtons = int(self.numOfCustomButtons / self.howManyCustomButtonsOnFrame)
            return numOfMenuButtons + 1

    def switchingCustomButtons(self):  # this thing handle switching buttons on its subframe
        if self.highestID < self.numOfCustomButtons:
            print("\nPRVOTNI ROLL  ---")
            counterDown = self.lowestID
            while counterDown <= self.highestID - 1:
                print("ID tlacitka na smazani je:", counterDown)
                self.customBtnDict[counterDown].pack_forget()
                counterDown += 1
            self.lowestID = self.highestID
            counter = 1
            while counter <= self.howManyCustomButtonsOnFrame:
                print("ID tlacitka NA ZOBRAZENI:", self.highestID)
                self.customBtnDict[self.highestID].pack(side=customtkinter.LEFT, padx=2, pady=2)
                if self.highestID > self.numOfCustomButtons - 1:
                    break
                self.highestID += 1
                counter += 1
        elif self.highestID >= self.numOfCustomButtons:
            print("\nEND ROLL  ---")
            counterDown = self.lowestID
            while counterDown <= self.highestID:
                print("ID tlacitka na smazani je:", counterDown)
                self.customBtnDict[counterDown].pack_forget()
                counterDown += 1
            self.lowestID = 1
            self.highestID = 1
            counterUP = 1
            while counterUP <= self.howManyCustomButtonsOnFrame:
                print("ID tlacitka NA ZOBRAZENI:", self.highestID)
                self.customBtnDict[self.highestID].pack(side=customtkinter.LEFT, padx=2, pady=2)
                if self.highestID > self.numOfCustomButtons - 1:
                    break
                self.highestID += 1
                counterUP += 1

    def menuButtonsSwitching(self, number):
        self.switchingCustomButtons()
        if not number == len(self.menuList):
            self.menuDict[number].pack_forget()
            self.menuDict[number + 1].pack(padx=5, pady=2)
            self.menuButtonValue = number
        else:
            self.menuDict[number].pack_forget()
            self.menuDict[1].pack(padx=5, pady=2)
            self.menuButtonValue = number

    def MenuButtons(self, number):
        self.menuDict[number] = customtkinter.CTkButton(self.menuButtonFrame)
        self.menuDict[number].configure(text=f"MENU {number}", font=("Helvetica", 36, "bold"))
        self.menuDict[number].configure(command=lambda: self.menuButtonsSwitching(number))
        self.menuDict[number].configure(border_width=3, corner_radius=0)
        self.menuDict[number].configure(width=(self.width / (1 + self.howManyCustomButtonsOnFrame)),
                                   height=self.frameHeight)
        if customtkinter.get_appearance_mode() == "Dark":

            self.menuDict[number].configure(fg_color="#1e1f22")  # , hover_color="#1e1f22"
        else:
            self.menuDict[number].configure(fg_color="white", text_color="black")

    def createMenuButtons(self):
        num: int = 1
        numberOfButtons = self.getHowManyMenuButtons()
        while num <= numberOfButtons:
            self.menuList.append(num)
            num += 1
        for number in self.menuList:
            self.MenuButtons(number)


        self.menuDict[1].pack(padx=5, pady=2)  # show only first menu Button
        self.switchingCustomButtons()
    """
    # CUSTOM BUTTONS SECTION #########################################
    """
    def customButtonCall(self, number):
        print(f"pressed button is: {number}")
        # zde se konfigurují akce pro dané tlačítko atd

    def customButton(self, number):
        self.customBtnDict[number] = customtkinter.CTkButton(self.customButtonsFrame)
        if number == 1:
            self.customBtnDict[number].configure(text="EXIT", font=("Helvetica", 36, "bold"))
            self.customBtnDict[number].configure(command=self.root.destroy)
        else:
            self.customBtnDict[number].configure(text=f"OPT_{number}", font=("Helvetica", 36, "bold"))
            self.customBtnDict[number].configure(command=lambda: self.customButtonCall(number))
        self.customBtnDict[number].configure(width=(self.width / (1 + self.howManyCustomButtonsOnFrame)),
                                             height=self.frameHeight)
        self.customBtnDict[number].configure(border_width=3, corner_radius=0)
        if customtkinter.get_appearance_mode() == "Dark":
            self.customBtnDict[number].configure(fg_color="#1e1f22")
        else:
            self.customBtnDict[number].configure(fg_color="white", text_color="black")

    def createCustomButtons(self):
        customBtnList = []
        self.customBtnDict = {}
        num = 1
        while num <= self.numOfCustomButtons:
            customBtnList.append(num)
            num += 1
        for number in customBtnList:
            self.customButton(number)


class App:
    def __init__(self, root: customtkinter.CTk):
        self.root = root
        screenNum = ryuConf.readJsonConfig("GlobalConfiguration", "numOfScreen")
        self.screenWidth = get_monitors()[screenNum].width  # screen width
        self.screenHeight = get_monitors()[screenNum].height  # screen height
        self.heightDivisor = ryuConf.readJsonConfig("GUI_template", "height_divisor")
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
        MenuBar(menuFrame, self.screenWidth, self.screenHeight / self.heightDivisor, self.root)


if __name__ == '__main__':
    root = customtkinter.CTk()
    App(root)
    root.mainloop()
