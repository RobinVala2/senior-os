from tkinter import *  # gui framework
import configurationActions as ryuconf  # mine thing for json actions
from screeninfo import get_monitors  # get all monitors
from configurationActions import readJsonConfig  # mine thing for json actions
import logging  # loging
import re  # regex

"""
Author: RYUseless
Github: https://github.com/RYUseless
Version: 0.0.9(Alpha)
"""

logger = logging.getLogger(__file__)
logger.info("initiated logging")


class menuBarButtons:
    def __init__(self, menuFrame: Frame, root: Tk, heightDivisor: int, height: int, width: int):
        self.height = height
        self.width = width
        self.root = root
        self.menuFrame = menuFrame
        self.heightDivisor = heightDivisor
        self.xValue = 0
        self.options = ryuconf.readJsonConfig("careConf", "menuButtonsList")
        self.buttonDictionary = {}
        # calls section
        self.buttons()
        self.CallConfigFrame = configurationFramesCreate(self.root, self.height, self.width)
        self.lastSelectedButton = None
        self.pickedButton = None

    def selectedButton(self, x):
        selectedColor = "#9e9d99"  # TODO: lehce teplejší šedou než jest tato
        if self.lastSelectedButton is None:
            self.buttonDictionary[x]['activebackground'] = selectedColor  # selected
            self.buttonDictionary[x]['bg'] = selectedColor  # selected
            self.lastSelectedButton = x
        else:
            self.buttonDictionary[self.lastSelectedButton]['activebackground'] = "#ebe9e4"  # normal
            self.buttonDictionary[self.lastSelectedButton]['bg'] = "#C7C6C1"  # normal
            self.lastSelectedButton = x
            self.buttonDictionary[x]['activebackground'] = selectedColor  # selected
            self.buttonDictionary[x]['bg'] = selectedColor  # selected

    def buttons(self):
        counter = 0
        self.options.append("EXIT")  # add exit as a last button
        for i in self.options:
            def getButtonNum(y=counter, name=i):
                self.selectedButton(y)
                if name == "Global\nconfig":
                    self.CallConfigFrame.GlobalConfigCall(y + 1)
                elif name == "Mail\nconfig":
                    self.CallConfigFrame.SmailConfigCall(y + 1)
                elif name == "Web\nconfig":
                    self.CallConfigFrame.swebConfigCall(y + 1)
                elif name == "LOGS":
                    self.CallConfigFrame.logConfigCall(y + 1)
                elif name == "EXIT":
                    exit(0)

            self.buttonDictionary[counter] = Button(self.menuFrame)
            self.buttonDictionary[counter]['text'] = i
            self.buttonDictionary[counter]['bg'] = '#C7C6C1'
            self.buttonDictionary[counter]['activebackground'] = '#ebe9e4'
            self.buttonDictionary[counter]['relief'] = 'solid'
            self.buttonDictionary[counter]['command'] = getButtonNum
            self.buttonDictionary[counter]['font'] = "Helvetica 36 bold"
            self.buttonDictionary[counter]['borderwidth'] = 1.5
            self.buttonDictionary[counter]['highlightbackground'] = "black"

            if counter == 0:
                self.buttonDictionary[counter].place(x=0, y=0, width=self.width / len(self.options),
                                                     height=self.height / self.heightDivisor)
            else:
                self.xValue = self.xValue + int(self.width / len(self.options)) + 5
                self.buttonDictionary[counter].place(x=self.xValue, y=0,
                                                     width=self.width / len(self.options),
                                                     height=self.height / self.heightDivisor)
            counter += 1
        logger.info("created buttons")


class configurationFramesCreate:
    def __init__(self, root: Tk, height: int, width: int):
        self.whichFrameIsON = None
        self.globalLock = False
        self.smailLock = False
        self.swebLock = False
        self.width = width
        self.height = height
        self.root = root
        self.heightDivisor = ryuconf.readJsonConfig("careConf", "heightDivisor")
        self.numberOfFrames = ryuconf.readJsonConfig("careConf", "menuButtonsList")
        self.crtFrameHeight = self.height - (self.height / self.heightDivisor)  # screen height - appFrame height
        self.frameDictionary = {}
        self.createFrame()

    def createFrame(self):
        valueOfI = 1
        while valueOfI <= len(self.numberOfFrames) + 1:
            self.frameDictionary[valueOfI] = Frame(self.root)
            self.frameDictionary[valueOfI].pack_propagate(False)
            self.frameDictionary[valueOfI]['bg'] = "white"  # TODO: read color from frame
            self.frameDictionary[valueOfI]['width'] = self.width
            self.frameDictionary[valueOfI]['height'] = self.crtFrameHeight
            valueOfI += 1
        logger.info("Created all needed frames.")

    def GlobalConfigCall(self, x):  # first frame
        print("-----------------GLOBAL FRAME-------------------")
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDictionary[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDictionary[x].pack()
        elif self.whichFrameIsON == x:
            pass
        else:
            self.whichFrameIsON = x
            self.frameDictionary[x].pack()

        showGlobalConfigFrame(self.frameDictionary[x], self.width, self.height)

    def SmailConfigCall(self, x):  # second frame
        print("-----------------SMAIL FRAME-------------------")
        self.frameDictionary[x].configure(bg="green")
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDictionary[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDictionary[x].pack()
        elif self.whichFrameIsON == x:
            pass
        else:
            self.whichFrameIsON = x
            self.frameDictionary[x].pack()

        if not self.smailLock:
            self.smailLock = True
            logger.info("created smailFrameConfig")

    def swebConfigCall(self, x):
        print("-----------------SWEB FRAME-------------------")
        self.frameDictionary[x].configure(bg="blue")
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            self.frameDictionary[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDictionary[x].pack()
        elif self.whichFrameIsON == x:
            pass
        else:
            self.whichFrameIsON = x
            self.frameDictionary[x].pack()

        if not self.swebLock:
            self.swebLock = True
            logger.info("created swebFrameConfig")

    def logConfigCall(self, x):
        print("-----------------LOG FRAME-------------------")
        if not self.whichFrameIsON is None and self.whichFrameIsON != x:
            for widgets in self.frameDictionary[x].winfo_children():
                widgets.destroy()
            self.frameDictionary[self.whichFrameIsON].pack_forget()
            self.whichFrameIsON = x
            self.frameDictionary[x].pack()
        elif self.whichFrameIsON == x:
            pass
        else:
            self.whichFrameIsON = x
            self.frameDictionary[x].pack()

        showLogConfigFrame(self.frameDictionary[x], self.height, self.width)


class showLogConfigFrame:
    def __init__(self, logFrame: Frame, height, width):
        self.height = height
        self.width = width
        self.logFrame = logFrame
        self.filterOptionValue = None
        self.logButtons()
        self.viewLogs()
        logger.info("Opening Log frame.")

    def refreshLogFrame(self):  # F5 ON FRAME THAT SHOWS LOGS
        for widgets in self.logFrame.winfo_children():
            widgets.destroy()
        self.logButtons()
        self.viewLogs()

    def logButtons(self):
        frameHeight = self.height / 20
        labelWidth = self.width / 6
        buttonWidth = self.width / 15
        spacer = self.width / 900
        getNewX = labelWidth + spacer
        buttonsList = ["INFO", "WARNING", "ERROR", "CRITICAL"]
        buttonsDict = {}
        filterFrame = Frame(self.logFrame, width=self.width, height=frameHeight, bg="white")
        filterFrame.pack_propagate(False)
        filterFrame.pack()

        logLaleb = Label(filterFrame, text="filter options:")
        logLaleb.place(x=0,y=0,width=labelWidth,height=frameHeight)

        filterButtonsC = 0
        for filterOption in buttonsList:
            def getCurrentNumID(x=filterButtonsC,value=filterOption):
                print(f"šmekši id:{x},value to filter is:{value}")
                self.filterOptionValue = value
                self.refreshLogFrame()
            buttonsDict[filterOption] = Button(filterFrame, text=filterOption, command=getCurrentNumID)
            if filterButtonsC == 0:
                buttonsDict[filterOption].place(x=getNewX, y=0, width=buttonWidth, height=frameHeight)
            else:
                getNewX = getNewX + buttonWidth + spacer
                buttonsDict[filterOption].place(x=getNewX, y=0, width=buttonWidth, height=frameHeight)
            filterButtonsC += 1

        getNewX = getNewX + buttonWidth + 2*spacer

        pickLogFileLabel = Label(filterFrame, text="choose log file:")
        pickLogFileLabel.place(x=getNewX, y=0, width=labelWidth, height=frameHeight)

        B = Button(filterFrame, text="REFRESH", command=lambda: self.refreshLogFrame())
        # half of the screen width↓     ↓ this is half of the button width
        centerPosX = (self.width/2) - (self.width/20)/2
        # B.place(x=centerPosX, y=0, width=self.width/20, height=frameHeight)

    def viewLogs(self):
        print("epicko value is",self.filterOptionValue)
        textThing = Text(self.logFrame, height=self.height - (self.height / 7),
                         width=self.width,
                         bg="white")
        scroll = Scrollbar(orient=VERTICAL, )
        scroll.config(command=textThing.yview, )
        textThing["yscrollcommand"] = scroll.set
        textThing.pack()
        file = ryuconf.readLog(self.filterOptionValue)
        for f in file:
            textThing.insert(END, f)
        textThing.config(state=DISABLED)  # disable editing


class showGlobalConfigFrame:
    def __init__(self, frame: Frame, width, height):
        self.frame = frame
        self.changeLanguageDict = {}
        self.changeLanguageAlertDict = {}
        self.width = width
        self.height = height
        self.widthLabel = width / 2
        self.widthButton = width / 10
        self.heightDivisor = ryuconf.readJsonConfig("careConf", "heightDivisor")
        self.spacer = 10
        self.heightWidgets = ((height - (height / self.heightDivisor)) / 11) - self.spacer
        self.Xposition = 0
        self.Yposition = self.spacer
        self.activeColor = "#5c6447"
        self.normalColor = "#D3D3D3"
        self.options = ryuconf.readJsonConfig("careConf", "LanguageOptions")
        self.fontGet = (f"{ryuconf.readJsonConfig('GlobalConfiguration', 'fontFamily')} "  # font family
                        f"{ryuconf.readJsonConfig('GlobalConfiguration', 'labelFontSize')} "  # font size
                        f"{ryuconf.readJsonConfig('GlobalConfiguration', 'fontThickness')}")  # font thicc?
        self.fontInputThing = (f"{ryuconf.readJsonConfig('GlobalConfiguration', 'fontFamily')} "
                               f"{ryuconf.readJsonConfig('GlobalConfiguration', 'fontSize')} "
                               f"{ryuconf.readJsonConfig('GlobalConfiguration', 'fontThickness')}")
        # some None things:
        self.inputError = Label(frame, bg="#D2042D")  # TODO: change to reading thing from json
        self.errorLabel = Label(frame, bg="#D2042D")  # TODO: change to reading thing from json
        self.colorButtonSelected = None
        self.delaySubmit = None
        self.pickedButton = None
        self.pickedButton2 = None
        self.thicknessButtonSelected = None

        # calls:
        self.OSpickScreen()  # choose which screen res you want
        self.OSlanguage()  # choose language for applications
        self.OSalertSound()  # choose alert language for apps
        self.OScolorScheme()  # light or dark scheme
        self.OSalertColor()  # color of widget, when selected
        self.OSdelayTime()  # delay before notification starts
        self.OSfontSize()  # size of text
        self.OSlabelFontSize()  # size of text, but label
        self.OSfontThicckness()  # t h i c c
        self.OSfontFamily()  # family name
        self.OSresetButton()  # r e s e t

    """
    OS screen -------------------------------------------------------------------------------------------------------
    """

    def OSpickScreen(self):
        # TODO: dodělat reset, barvu picku a při vícero jak 3 monitorech to spawne label co řekne ať si to člověk edituje přímo v jsonu
        colorModeLabel = Label(self.frame, text="pick Screen: ")
        colorModeLabel['font'] = self.fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.Xposition = self.Xposition + self.widthLabel + self.spacer

        buttonThing = {}
        buttonDict = []
        monitors = get_monitors()
        counter = 0
        while counter < len(monitors):
            buttonDict.append(counter)
            counter += 1
        self.radioVarScreens = IntVar(value=ryuconf.readJsonConfig("GlobalConfiguration", "numOfScreen"))
        for id in buttonDict:
            def getNum(i=id):
                print(i)
                ryuconf.editConfig("GlobalConfiguration", "numOfScreen", i)

            buttonThing[id] = Radiobutton(self.frame, text=f"monitor č.{id + 1}", variable=self.radioVarScreens,
                                          value=id)
            buttonThing[id]['font'] = self.fontGet
            buttonThing[id]['command'] = getNum
            if id == 0:
                buttonThing[id].place(x=self.Xposition, y=self.Yposition,
                                      width=self.widthButton, height=self.heightWidgets)
            else:
                self.Xposition = self.Xposition + self.widthButton + self.spacer
                buttonThing[id].place(x=self.Xposition, y=self.Yposition,
                                      width=self.widthButton, height=self.heightWidgets)

    """
    OS screen END------------------------------------------------------------------------------------------------------
    OS language -------------------------------------------------------------------------------------------------------
    """

    def changeColorLanguage(self, idLanButton):  # LANGUAGE SELECTION
        buttonSelectedColor = "#5c6447"
        if not self.pickedButton is None:
            self.changeLanguageDict[self.pickedButton].configure(bg="#D3D3D3", activebackground="#bdbbbb")
            self.changeLanguageDict[idLanButton].configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.pickedButton = idLanButton
        else:
            self.changeLanguageDict[idLanButton].configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.pickedButton = idLanButton

    def OSlanguage(self):
        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + self.spacer

        languageLabel = Label(self.frame, text="OS language:")
        languageLabel['font'] = self.fontGet
        languageLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.Xposition = self.Xposition + self.widthLabel + self.spacer

        counterLangCount = 1
        self.radioVar = StringVar(value=ryuconf.readJsonConfig("GlobalConfiguration", "language"))
        for name in self.options:
            def getName(n=name, c=counterLangCount):
                self.changeColorLanguage(c)
                self.radioVar.get()  # needs to be here to show picked selection
                ryuconf.editConfig("GlobalConfiguration", "language", n)

            self.changeLanguageDict[counterLangCount] = Radiobutton(self.frame, text=name, variable=self.radioVar,
                                                                    value=name)
            self.changeLanguageDict[counterLangCount]['font'] = self.fontGet
            self.changeLanguageDict[counterLangCount].configure(bg="#D3D3D3", activebackground="#bdbbbb")
            self.changeLanguageDict[counterLangCount]['command'] = getName
            if counterLangCount == 1:
                self.changeLanguageDict[counterLangCount].place(x=self.Xposition, y=self.Yposition,
                                                                width=self.widthButton, height=self.heightWidgets)
            else:
                self.Xposition = self.Xposition + self.widthButton + self.spacer
                self.changeLanguageDict[counterLangCount].place(x=self.Xposition, y=self.Yposition,
                                                                width=self.widthButton, height=self.heightWidgets)
            counterLangCount += 1

    """
    OS language END-----------------------------------------------------------------------------------------------------
    
    OS Color scheme------------------------------------------------------------------------------------------------------
    """

    def changeColorColorschemeSelection(self, buttonID):  # COLOR SCHEME SELECTION
        buttonSelectedColor = "#5c6447"
        if not self.colorButtonSelected is None:
            self.colorButtonSelected.configure(bg="#D3D3D3", activebackground="#bdbbbb")
            buttonID.configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.colorButtonSelected = buttonID
        else:
            buttonID.configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.colorButtonSelected = buttonID

    def OScolorScheme(self):
        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + self.spacer

        colorModeLabel = Label(self.frame, text="System color scheme:")
        colorModeLabel['font'] = self.fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.radioVar2 = StringVar(value=ryuconf.readJsonConfig("GlobalConfiguration", "colorMode"))
        # light mode
        whiteColorButton = Radiobutton(self.frame, text="Light", variable=self.radioVar2, value="Light")
        whiteColorButton['command'] = lambda: [
            ryuconf.editConfig("GlobalConfiguration", "colorMode", self.radioVar2.get()),
            self.changeColorColorschemeSelection(whiteColorButton)]
        whiteColorButton['font'] = self.fontGet
        self.Xposition = self.Xposition + self.widthLabel + self.spacer
        whiteColorButton.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)
        # dark mode
        BlackColorButton = Radiobutton(self.frame, text="Dark", variable=self.radioVar2, value="Dark")
        BlackColorButton['command'] = lambda: [
            ryuconf.editConfig("GlobalConfiguration", "colorMode", self.radioVar2.get()),
            self.changeColorColorschemeSelection(BlackColorButton)]
        BlackColorButton['font'] = self.fontGet
        self.Xposition = self.Xposition + self.widthButton + self.spacer
        BlackColorButton.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

    """
    OS Color END-----------------------------------------------------------------------------------------------------
    
    OS delay time------------------------------------------------------------------------------------------------------
    """

    def checkIfInputIsNumber(self, givenInput, xPos, yPos, whichConfig):
        global inputInt
        try:
            inputInt = int(givenInput)
        except ValueError:
            if whichConfig == 1:
                self.delaySubmit.configure(bg=self.normalColor,
                                           activebackground=self.normalColor)  # change submit button color barch
            elif whichConfig == 2:
                self.fontSubmit.configure(bg=self.normalColor,
                                          activebackground=self.normalColor)  # change submit button color barch
            elif whichConfig == 3:
                self.labelSubmit.configure(bg=self.normalColor,
                                           activebackground=self.normalColor)  # change submit button color barch
            iks = xPos + self.widthButton + self.spacer
            self.inputError['text'] = f"'{givenInput}' is not a number, value must be number!"
            errorLabelWidth = self.width - (2 * self.widthButton + self.widthLabel + 3*self.spacer)
            self.inputError.place(x=iks, y=yPos, width=errorLabelWidth, height=self.heightWidgets)
            logger.error(f"Value '{givenInput}' is not a number, value must be number!")
            return
        # 1 - soundDelay
        # 2 - fontSize
        if whichConfig == 1:
            ryuconf.editConfig("GlobalConfiguration", "soundDelay", inputInt)
            self.delaySubmit.configure(bg=self.activeColor, activebackground=self.activeColor)
        elif whichConfig == 2:
            ryuconf.editConfig("GlobalConfiguration", "fontSize", inputInt)
            self.fontSubmit.configure(bg=self.activeColor, activebackground=self.activeColor)
        elif whichConfig == 3:
            ryuconf.editConfig("GlobalConfiguration", "labelFontSize", inputInt)
            self.labelSubmit.configure(bg=self.activeColor, activebackground=self.activeColor)

        self.inputError.place_forget()

    def OSdelayTime(self):
        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + self.spacer

        soundDelayLabel = Label(self.frame,
                                text="Alert delay (in seconds):")
        soundDelayLabel['font'] = self.fontGet
        soundDelayLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.inputText = Text(self.frame)
        self.inputText['font'] = self.fontInputThing
        defalultDelayValue = ryuconf.readJsonConfig("GlobalConfiguration", "soundDelay")
        self.inputText.insert(1.0, defalultDelayValue)
        self.Xposition = self.Xposition + self.widthLabel + self.spacer
        self.inputText.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        self.delaySubmit = Button(self.frame, text="submit")
        self.delaySubmit['font'] = self.fontGet
        self.Xposition = self.Xposition + self.widthButton + self.spacer
        self.delaySubmit.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        getCurrentX = self.Xposition
        getCurrentY = self.Yposition

        self.delaySubmit['command'] = lambda: self.checkIfInputIsNumber(self.inputText.get(1.0, 'end-1c'), getCurrentX,
                                                                        getCurrentY, 1)

    """
    OS DELAY END-----------------------------------------------------------------------------------------------------

    OS Alert color------------------------------------------------------------------------------------------------------
    """

    def hexCheck(self, hexInput, xPos, yPos):
        # TODO: dodělat oddělaní error labelu, když se pak zadá znovu dobře value
        if not len(hexInput) == 7:  # hex needs (?) to have 7 characters
            self.colorSubmit.configure(bg=self.normalColor, activebackground=self.normalColor)
            self.errorLabel['text'] = f"'{hexInput}' needs to have 7 characters"
            logger.error(f"'{hexInput}' needs to have 7 characters")
            iks = xPos + self.widthButton + self.spacer
            errorLabelWidth = self.width - (self.widthButton + (self.widthLabel / 3) + self.widthLabel + 30)
            self.errorLabel.place(x=iks, y=yPos, width=errorLabelWidth, height=self.heightWidgets)
            return

        match = re.search(r'^#(?:[0-9a-fA-F]{1,2}){3}$', hexInput)  # regex check

        if match:
            self.errorLabel.place_forget()
            ryuconf.editConfig("GlobalConfiguration", "alertColor", hexInput)
            self.colorSubmit.configure(bg=self.activeColor, activebackground=self.activeColor)
        else:
            self.colorSubmit.configure(bg=self.normalColor, activebackground=self.normalColor)
            self.errorLabel['text'] = f"'{hexInput}' is not a HEX value in format '#123456'"
            logger.error(f"'{hexInput}' is not a HEX value in format '#123456'")
            iks = xPos + self.widthButton + self.spacer
            errorLabelWidth = self.width - (self.widthButton + (self.widthLabel / 3) + self.widthLabel + 30)
            self.errorLabel.place(x=iks, y=yPos, width=errorLabelWidth, height=self.heightWidgets)

    def OSalertColor(self):
        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + self.spacer

        colorModeLabel = Label(self.frame, text="Alert color in hex (#12345): ")
        colorModeLabel['font'] = self.fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.inputHex = Text(self.frame)
        self.inputHex['font'] = self.fontInputThing
        defaultHexValue = ryuconf.readJsonConfig("GlobalConfiguration", "alertColor")
        self.inputHex.insert(1.0, defaultHexValue)
        self.Xposition = self.Xposition + self.widthLabel + self.spacer
        self.inputHex.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel / 3, height=self.heightWidgets)

        self.colorSubmit = Button(self.frame, text="submit")
        self.colorSubmit['font'] = self.fontGet
        self.Xposition = self.Xposition + (self.widthLabel / 3) + self.spacer
        self.colorSubmit.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        getCurrentXforHex = self.Xposition
        getCurrentYforHex = self.Yposition

        self.colorSubmit['command'] = lambda: self.hexCheck(self.inputHex.get(1.0, 'end-1c'), getCurrentXforHex,
                                                            getCurrentYforHex)

    """
    OS DELAY END-----------------------------------------------------------------------------------------------------

    OS alertSoundLanguage------------------------------------------------------------------------------------------------------
    """

    def changeColorLanguageAlert(self, idLanButton):  # LANGUAGE SELECTION
        buttonSelectedColor = "#5c6447"
        if not self.pickedButton2 is None:
            self.changeLanguageAlertDict[self.pickedButton2].configure(bg="#D3D3D3", activebackground="#bdbbbb")
            self.changeLanguageAlertDict[idLanButton].configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.pickedButton2 = idLanButton
        else:
            self.changeLanguageAlertDict[idLanButton].configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.pickedButton2 = idLanButton

    def OSalertSound(self):
        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + self.spacer

        colorModeLabel = Label(self.frame, text="Alert sound language: ")
        colorModeLabel['font'] = self.fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.Xposition = self.Xposition + self.widthLabel + self.spacer

        counterLangCount = 1
        self.soundVar = StringVar(value=ryuconf.readJsonConfig("GlobalConfiguration", "alertSoundLanguage"))
        for name in self.options:
            def getName(n=name, c=counterLangCount):
                self.soundVar.get()  # needs to be here to show picked selection
                self.changeColorLanguageAlert(c)
                ryuconf.editConfig("GlobalConfiguration", "alertSoundLanguage", n)

            self.changeLanguageAlertDict[counterLangCount] = Radiobutton(self.frame, text=name, variable=self.soundVar,
                                                                         value=name)
            self.changeLanguageAlertDict[counterLangCount]['font'] = self.fontGet
            self.changeLanguageAlertDict[counterLangCount].configure(bg="#D3D3D3", activebackground="#bdbbbb")
            self.changeLanguageAlertDict[counterLangCount]['command'] = getName
            if counterLangCount == 1:
                self.changeLanguageAlertDict[counterLangCount].place(x=self.Xposition, y=self.Yposition,
                                                                     width=self.widthButton, height=self.heightWidgets)
            else:
                self.Xposition = self.Xposition + self.widthButton + self.spacer
                self.changeLanguageAlertDict[counterLangCount].place(x=self.Xposition, y=self.Yposition,
                                                                     width=self.widthButton, height=self.heightWidgets)
            counterLangCount += 1

    """
    OS alertSoundLanguage END-----------------------------------------------------------------------------------------------------

    OS fontSizer------------------------------------------------------------------------------------------------------
    """

    def OSfontSize(self):
        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + self.spacer

        fontSizeLabel = Label(self.frame, text="Font size: ")
        fontSizeLabel['font'] = self.fontGet
        fontSizeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.inputFont = Text(self.frame)
        self.inputFont['font'] = self.fontInputThing
        defalultDelayValue = ryuconf.readJsonConfig("GlobalConfiguration", "fontSize")
        self.inputFont.insert(1.0, defalultDelayValue)
        self.Xposition = self.Xposition + self.widthLabel + self.spacer
        self.inputFont.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        self.fontSubmit = Button(self.frame, text="submit")
        self.fontSubmit['font'] = self.fontGet
        self.Xposition = self.Xposition + self.widthButton + self.spacer
        self.fontSubmit.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        getCurrentX = self.Xposition
        getCurrentY = self.Yposition

        self.fontSubmit['command'] = lambda: self.checkIfInputIsNumber(self.inputFont.get(1.0, 'end-1c'), getCurrentX,
                                                                       getCurrentY, 2)

    """
    OS fontSize END-----------------------------------------------------------------------------------------------------

    OS labelFontSize------------------------------------------------------------------------------------------------------
    """

    def OSlabelFontSize(self):
        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + self.spacer

        colorModeLabel = Label(self.frame, text="Label font size: ")
        colorModeLabel['font'] = self.fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.inputlabelFontSize = Text(self.frame)
        self.inputlabelFontSize['font'] = self.fontInputThing
        defalultDelayValue = ryuconf.readJsonConfig("GlobalConfiguration", "labelFontSize")
        self.inputlabelFontSize.insert(1.0, defalultDelayValue)
        self.Xposition = self.Xposition + self.widthLabel + self.spacer
        self.inputlabelFontSize.place(x=self.Xposition, y=self.Yposition, width=self.widthButton,
                                      height=self.heightWidgets)

        self.labelSubmit = Button(self.frame, text="submit")
        self.labelSubmit['font'] = self.fontGet
        self.Xposition = self.Xposition + self.widthButton + self.spacer
        self.labelSubmit.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        getCurrentX = self.Xposition
        getCurrentY = self.Yposition

        self.labelSubmit['command'] = lambda: self.checkIfInputIsNumber(self.inputlabelFontSize.get(1.0, 'end-1c'),
                                                                        getCurrentX, getCurrentY, 3)

    """
    OS labelFontSize END-----------------------------------------------------------------------------------------------------

    OS fontThickness------------------------------------------------------------------------------------------------------
    """

    def changedColor(self, buttonID):
        buttonSelectedColor = "#5c6447"
        if not self.thicknessButtonSelected is None:
            self.thicknessButtonSelected.configure(bg="#D3D3D3", activebackground="#bdbbbb")
            buttonID.configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.thicknessButtonSelected = buttonID
        else:
            buttonID.configure(bg=buttonSelectedColor, activebackground=buttonSelectedColor)
            self.thicknessButtonSelected = buttonID

    def OSfontThicckness(self):
        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + self.spacer

        colorModeLabel = Label(self.frame, text="Text thickness: ")
        colorModeLabel['font'] = self.fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.thicknessVar = StringVar(value=ryuconf.readJsonConfig("GlobalConfiguration", "fontThickness"))
        # light mode
        boldButton = Radiobutton(self.frame, text="bold", variable=self.thicknessVar, value="bold")
        boldButton['command'] = lambda: [ryuconf.editConfig("GlobalConfiguration",
                                                            "fontThickness", self.thicknessVar.get()),
                                         self.changedColor(boldButton)]
        boldButton['font'] = self.fontGet
        self.Xposition = self.Xposition + self.widthLabel + self.spacer
        boldButton.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)
        # dark mode
        slimButton = Radiobutton(self.frame, text="slim", variable=self.thicknessVar, value="")
        slimButton['command'] = lambda: [ryuconf.editConfig("GlobalConfiguration", "fontThickness",
                                                            self.thicknessVar.get()),
                                         self.changedColor(slimButton)]
        slimButton['font'] = self.fontGet
        self.Xposition = self.Xposition + self.widthButton + self.spacer
        slimButton.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

    """
    OS fontThickness END-----------------------------------------------------------------------------------------------------

    OS fontFamily------------------------------------------------------------------------------------------------------
    """

    def OSfontFamily(self):
        self.Xposition = 0
        self.Yposition = self.Yposition + self.heightWidgets + self.spacer

        colorModeLabel = Label(self.frame, text="Font family: ")
        colorModeLabel['font'] = self.fontGet
        colorModeLabel.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel, height=self.heightWidgets)

        self.inputFontFamily = Text(self.frame)
        self.inputFontFamily['font'] = self.fontInputThing
        defaultHexValue = ryuconf.readJsonConfig("GlobalConfiguration", "fontFamily")
        self.inputFontFamily.insert(1.0, defaultHexValue)
        self.Xposition = self.Xposition + self.widthLabel + self.spacer
        self.inputFontFamily.place(x=self.Xposition, y=self.Yposition, width=self.widthLabel / 3, height=self.heightWidgets)

        self.fontFamilySubmit = Button(self.frame, text="submit")
        self.fontFamilySubmit['font'] = self.fontGet
        self.Xposition = self.Xposition + (self.widthLabel / 3) + self.spacer
        self.fontFamilySubmit.place(x=self.Xposition, y=self.Yposition, width=self.widthButton, height=self.heightWidgets)

        getCurrentXforHex = self.Xposition
        getCurrentYforHex = self.Yposition

        self.fontFamilySubmit['command'] = lambda: print( "workey")

    # ------------------------------------------------------------------------------------------------------------------

    def restoreColors(self):  # RESTORES ALL SELECTED BUTTONS
        getWhereConfigIs = ryuconf.readJsonConfig("pathToConfig", "path")
        ryuconf.caregiverAppConfig(getWhereConfigIs)  # generates default config.json
        self.delaySubmit.configure(bg=self.normalColor, activebackground=self.normalColor)
        self.fontSubmit.configure(bg=self.normalColor, activebackground=self.normalColor)
        self.labelSubmit.configure(bg=self.normalColor, activebackground=self.normalColor)
        self.colorSubmit.configure(bg=self.normalColor, activebackground=self.normalColor)
        if not self.pickedButton is None:
            self.changeLanguageDict[self.pickedButton].configure(bg=self.normalColor, activebackground=self.normalColor)
        if not self.pickedButton2 is None:
            self.changeLanguageAlertDict[self.pickedButton2].configure(bg=self.normalColor, activebackground=self.normalColor)
        if not self.colorButtonSelected is None:
            self.colorButtonSelected.configure(bg=self.normalColor, activebackground=self.normalColor)
        if not self.thicknessButtonSelected is None:
            self.thicknessButtonSelected.configure(bg=self.normalColor, activebackground=self.normalColor)
        else:
            return

    def resetActions(self):
        self.errorLabel.place_forget()
        self.radioVar.set(ryuconf.readJsonConfig("GlobalConfiguration", "language"))
        self.radioVar2.set(ryuconf.readJsonConfig("GlobalConfiguration", "colorMode"))
        self.soundVar.set(ryuconf.readJsonConfig("GlobalConfiguration", "alertSoundLanguage"))
        self.thicknessVar.set(value=ryuconf.readJsonConfig("GlobalConfiguration", "fontThickness"))
        self.inputText.delete("1.0", "end")
        self.inputText.insert(1.0, ryuconf.readJsonConfig("GlobalConfiguration", "soundDelay"))
        self.inputHex.delete(1.0, "end")
        self.inputHex.insert(1.0, ryuconf.readJsonConfig("GlobalConfiguration", "alertColor"))
        self.inputlabelFontSize.delete(1.0, "end")
        self.inputlabelFontSize.insert(1.0, ryuconf.readJsonConfig("GlobalConfiguration", "labelFontSize"))
        self.inputFont.delete(1.0, "end")
        self.inputFont.insert(1.0, ryuconf.readJsonConfig("GlobalConfiguration", "fontSize"))
        # final action
        logger.info("resetting config")

    def OSresetButton(self):
        self.Xposition = (self.width / 2) - ((self.width / 5) / 2)
        self.Yposition = self.Yposition + self.heightWidgets + self.spacer
        restore = Button(self.frame, text="RESTORE TO DEFAULT SETTINGS")
        restore.place(x=self.Xposition, y=self.Yposition, width=self.width / 5, height= self.heightWidgets - self.spacer)
        restore['command'] = lambda: [self.restoreColors(), self.resetActions()]


class AppBase:
    def __init__(self, root: Tk):
        self.root = root
        self.heightDivisor = 7
        self.screenWidth = get_monitors()[readJsonConfig("GlobalConfiguration", "numOfScreen")].width  # screen width
        self.screenHeight = get_monitors()[readJsonConfig("GlobalConfiguration", "numOfScreen")].height  # screen height
        self.rootSetup()  # def for root window
        self.menuBarFrameSetup()  # def for creating menu bar frame

    def rootSetup(self):
        self.root.title("Caregiver Configuration v:0.0.1")
        self.root.attributes('-fullscreen', True)
        self.root.configure(background="white")
        logger.info("created root window")

    def menuBarFrameSetup(self):
        masterFrame = Frame(self.root)  # creating menu bar frame (tkinter.Frame)
        masterFrame.pack_propagate(False)
        masterFrame['width'] = self.screenWidth
        masterFrame['height'] = self.screenHeight / self.heightDivisor
        masterFrame['bg'] = 'white'
        masterFrame.pack(side=TOP)
        logger.info("created menuFrame")
        # calling class for creating objects
        menuBarButtons(masterFrame, self.root, self.heightDivisor, self.screenHeight, self.screenWidth)
