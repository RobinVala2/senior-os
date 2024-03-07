"""
Written by: RYUseless
"""
import tkinter
from tkinter import *
import smail.template.configActions as JS
from screeninfo import get_monitors


def getButtonConf():
    # collecting values for font and colors
    bg = JS.jsonRed('colors_info', "buttons_unselected")
    bg_active = JS.jsonRed('colors_info', "buttons_selected")
    # end of collecting values for font and colors
    return bg, bg_active


def resolutionMath():
     #TODO: do len(get_monitors()) when choosing which screen to get in caregiver app
    _numOfScreen = JS.jsonRed_upd('GlobalConfiguration', "numOfScreen")
    # this is from screen_info imported get_monitors to get always the first screen
    _screenWidth = get_monitors()[_numOfScreen].width
    _screenHeight = get_monitors()[_numOfScreen].height
    # upper frame (MenuFrame)width and height
    panelWidth = int(_screenWidth / JS.jsonRed_upd('GUI_template', "width_divisor"))
    panelHeight = int(_screenHeight / JS.jsonRed_upd('GUI_template', "height_divisor"))
    # lower frame (ApplicationFrame) width and height
    app_width = _screenWidth - panelWidth
    app_height = _screenHeight - panelHeight
    # return thing
    return _screenWidth, panelWidth, panelHeight, app_width, app_height


def executeCommandFromOPTButton(x: object):  # call def for opt1 commands
    if x == 1:
        print(f"id tlacitka jest:{x} | text je: EXIT")
    elif x == 2:
        print(f"id tlacitka jest:{x} | text je: opt#{x - 1}")
    elif x == 3:
        print(f"id tlacitka jest:{x} | text je: opt#{x - 1}")
    elif x == 4:
        print(f"id tlacitka jest:{x} | text je: opt#{x - 1}")
    elif x == 5:
        print(f"id tlacitka jest:{x} | text je: opt#{x - 1}")
    elif x == 6:
        print(f"id tlacitka jest:{x} | text je: opt#{x - 1}")
    elif x == 7:
        print(f"id tlacitka jest:{x} | text je: opt#{x - 1}")
    elif x == 8:
        print(f"id tlacitka je:{x} | text je: opt#{x - 1}")


class _MenuFrameTemplate:
    """
                            ↓↓↓ masterFrane ↓↓↓
    ┌───────────────────────────────────────────────────────────────────────────┐
    │ menuFrame │               optionsFrame                                    │
    └───────────────────────────────────────────────────────────────────────────┘
    """

    def __init__(self, root: tkinter.Tk, sixWidth: int, sixHeight: int):
        self.root = root
        bg_color = '#e5e5e5'

        # master frame
        masterFrame = Frame(root, height=sixHeight, bg=bg_color)
        # ↓ forbids frame to resize to button size
        masterFrame.pack_propagate(False)
        masterFrame.pack(side=TOP, fill=X)

        # menu frame
        self.menuFrame = Frame(masterFrame, width=sixWidth, bg=bg_color)
        self.menuFrame.pack_propagate(False)
        self.menuFrame.pack(side=LEFT, fill=Y)

        # options frame
        self.optionsFrame = Frame(masterFrame, bg=bg_color)
        self.optionsFrame.pack_propagate(False)
        self.optionsFrame.pack(expand=True, fill=BOTH)


class ApplicationFrameTemplate:
    def __init__(self, root: tkinter.Tk):
        self.exitButtonPokus = None
        bg_color = JS.jsonRed('colors_info', "app_frame")
        self.root = root
        self.app_frame_width = resolutionMath()[3]
        self.app_frame_height = resolutionMath()[4]
        self.master_frame = Frame(root, height=self.app_frame_height, bg=bg_color)
        self.master_frame.pack_propagate(False)
        self.master_frame.pack(fill=X)
        self.createExitButton()

    def changeColor(self):
        self.exitButtonPokus['bg'] = "#301934"
        self.exitButtonPokus['activebackground'] = "#301934"

    def createExitButton(self):
        self.exitButtonPokus = Button(self.master_frame, text="C L I C K  M E ", command=self.changeColor)
        self.exitButtonPokus['bg'] = "white"
        self.exitButtonPokus.pack(side=LEFT, expand=True, fill='both')

    """
END OF FRAME SECTION

START OF BUTTONS SECTION
    """


class menuButtonCRT:
    """Create Menu_Action_Buttons and Back_Action_Button.
    :param text_value: this class creates buttons for menu selection and going back option.
    """

    def __init__(self, menuBar: tkinter.Frame, optionsBar: tkinter.Frame, panelWidth: int, sixHeight: int):
        self.dummyPixel = PhotoImage(width=1, height=1)
        self.sixWidth = panelWidth  # ← get portion of the screen width
        self.optionsBar = optionsBar  # ← tkinter.Frame for options
        self.sixHeight = sixHeight  # ← get portion of the screen height
        self.menuBar = menuBar  # ← tkinter.Frame for menu buttons
        self.button_dict = {}  # ← this thing for creating menu and back buttons
        self.option = []  # ← array for specifying 'IDs' for buttons
        self.id_of_menu = 1  # ← value that keeps track of which ID is in use
        self.createOptArr()  # ← get number of men. and bac. buttons
        self.createButtons()  # ← def call
        self.dummyPixel = PhotoImage(width=1, height=1)
        # call for opt. class buttons:
        self.optButtons1 = optionsButtonsCRT1(optionsBar=optionsBar, panelWidth=panelWidth, panelHeight=sixHeight)
        self.optButtons2 = optionsButtonsCRT2(optionsBar=optionsBar, panelWidth=panelWidth, panelHeight=sixHeight)
        """
        TODO: možná by šlo zavolat self.optButtons1, ale pouze změnit finální x=i o +4 tak, aby pak def co si rozlišuje commandy věděl x
        tím by se ušetřila identická kopie třídy + exit tlačítko :)
        """

    def createOptArr(self):  # this reads values from conf.json and creates array based of length that was given
        _numberOfValues = JS.jsonRed('buttons_info', "num_of_menu_buttons")  # get values from conf.json
        _counter = 1
        while _counter <= _numberOfValues:
            self.option.append(_counter)
            _counter += 1

    def menuActionUp(self):  # this def goes up one menu button: menu_X -> menu_X+1
        if self.id_of_menu == 1:
            new_dict = self.optButtons1.button_dict
            for i in new_dict:
                new_dict[i].pack_forget()
        """
        if the number of the menu is lower than the length of self.option, it goes one button up and shows optButtons for that menu
        if the number of menuButton is equal to the length, it does a loop and goes back to menu1 with its optButtons
        """
        if self.id_of_menu < len(self.option):
            new_dict2 = self.optButtons2.button_dict
            for i in new_dict2:
                new_dict2[i].pack(side=LEFT, padx=JS.jsonRed('buttons_info', "padx_value"))
            self.button_dict[self.id_of_menu].pack_forget()
            self.button_dict[self.id_of_menu + 1].pack(side=LEFT, expand=True, fill='both')
            self.id_of_menu += 1

        elif self.id_of_menu == len(self.option):
            self.button_dict[self.id_of_menu].pack_forget()
            self.id_of_menu = 1
            self.button_dict[self.id_of_menu].pack(side=LEFT, expand=True, fill='both')
            # opt buttons actions:
            new_dict2 = self.optButtons2.button_dict  # hide secondary opt
            for i in new_dict2:
                new_dict2[i].pack_forget()
            new_dict = self.optButtons1.button_dict  # show again the first opt buttons
            for i in new_dict:
                new_dict[i].pack(side=LEFT, padx=JS.jsonRed('buttons_info', "padx_value"))

    def createButtons(self):  # this def creates menu and back action button
        # collecting values for font and colors from def
        getValues = getButtonConf()
        bg = getValues[0]
        bg_active = getValues[1]
        # end of collecting values for font and colors
        for i in self.option:
            self.button_dict[i] = Button(self.menuBar, text=f"MENU {i}", command=lambda: self.menuActionUp())
            # buttons configuration:
            self.button_dict[i]['activebackground'] = bg_active
            self.button_dict[i]['bg'] = bg
            self.button_dict[i]['font'] = JS.jsonRed('font_info', "font")
            self.button_dict[i]['borderwidth'] = 2
            self.button_dict[i]['relief'] = 'solid'
        self.button_dict[1].pack(side=LEFT, expand=True, fill='both')  # FIRST MENU


class optionsButtonsCRT1:
    def __init__(self, optionsBar: tkinter.Frame, panelWidth: int, panelHeight: int):
        self.dummyPixel = PhotoImage(width=1, height=1)
        self.optionsBar = optionsBar
        self.button_dict = {}  # this thing for creating menu and back buttons
        self.option = []  # array for specifying 'IDs' for buttons
        self.sixWidth = panelWidth  # get portion of the screen width
        self.sixHeight = panelHeight  # get portion of the screen height
        self.createOptArr()
        self.createOPT1Buttons()

    def createOptArr(self):  # this reads values from conf.json and creates array based of length that was given
        _numberOfValues = JS.jsonRed('buttons_info', "num_of_opt_on_frame")
        _counter = 1
        while _counter <= _numberOfValues:
            self.option.append(_counter)
            _counter += 1

    def createOPT1Buttons(self):
        # collecting values for font and colors from def
        getValues = getButtonConf()
        bg = getValues[0]
        bg_active = getValues[1]
        numOPT = JS.jsonRed('buttons_info', "num_of_opt_on_frame")
        padxValue = JS.jsonRed('buttons_info', "padx_value")
        # end of collecting values for font and colors
        # -------------------------------------------
        for i in self.option:
            def execCommand(x=i):  # this def stores current i of each button
                executeCommandFromOPTButton(x)

            if i == 1:  # make first button exit button
                self.button_dict[i] = Button(self.optionsBar, text='EXIT', image=self.dummyPixel, compound="c",
                                             command=exit)  # exit == exit(0)
            else:
                self.button_dict[i] = Button(self.optionsBar, text=f'OPT#{i - 1}', image=self.dummyPixel, compound="c",
                                             command=execCommand)
            self.button_dict[i]['activebackground'] = bg_active
            # 1/x of width - padX value from both sides * num of buttons ↓
            self.button_dict[i]['width'] = int(self.sixWidth - (2 * padxValue * numOPT))
            self.button_dict[i]['bg'] = bg
            self.button_dict[i]['font'] = JS.jsonRed('font_info', "font")
            self.button_dict[i]['height'] = self.sixHeight
            self.button_dict[i]['borderwidth'] = 2
            self.button_dict[i]['relief'] = 'solid'

            # show buttons:
            self.button_dict[i].pack(side=LEFT, padx=padxValue)


class optionsButtonsCRT2:
    def __init__(self, optionsBar: tkinter.Frame, panelWidth: int, panelHeight: int):
        self.dummyPixel = PhotoImage(width=1, height=1)
        self.optionsBar = optionsBar
        self.button_dict = {}  # this thing for creating menu and back buttons
        self.option = []  # array for specifying 'IDs' for buttons
        self.sixWidth = panelWidth  # get portion of the screen width
        self.sixHeight = panelHeight  # get portion of the screen height
        self.createOptArr()
        self.createOPT2Buttons()

    def createOptArr(self):  # this reads values from conf.json and creates array based of length that was given
        _numberOfValues = JS.jsonRed('buttons_info', "num_of_opt_on_frame")
        _counter = 1
        while _counter <= _numberOfValues:
            self.option.append(_counter)
            _counter += 1

    def createOPT2Buttons(self):
        # collecting values for font and colors from def
        getValues = getButtonConf()
        bg = getValues[0]
        bg_active = getValues[1]
        numOPT = JS.jsonRed('buttons_info', "num_of_opt_on_frame")
        padxValue = JS.jsonRed('buttons_info', "padx_value")
        # end of collecting values for font and colors
        # -------------------------------------------
        for i in self.option:
            def execCommand(x=i):  # this def stores current i of each button
                x = x + 4
                executeCommandFromOPTButton(x)

            self.button_dict[i] = Button(self.optionsBar, text=f'OPT#{i + 3}', image=self.dummyPixel, compound="c",
                                         command=execCommand)
            # button config:
            self.button_dict[i]['activebackground'] = bg_active
            # 1/x of width - padX value from both sides * num of buttons ↓
            self.button_dict[i]['width'] = int(self.sixWidth - (2 * padxValue * numOPT))
            self.button_dict[i]['bg'] = bg
            self.button_dict[i]['font'] = JS.jsonRed('font_info', "font")
            self.button_dict[i]['height'] = self.sixHeight
            self.button_dict[i]['borderwidth'] = 2
            self.button_dict[i]['relief'] = 'solid'


# this class creates root windows and calls needed classes
class App:
    def __init__(self, root: tkinter.Tk):
        sixWidth = resolutionMath()[1]  # get sixth of the resolution to make frame width
        sixHeight = resolutionMath()[2]  # get sixth of the resolution to make frame height
        root.title("SeniorOS interface app")
        root.attributes('-fullscreen', True)  # make app fullscreen
        # calling classes
        menuFrameTemp = _MenuFrameTemplate(root, sixWidth, sixHeight)
        self.menuFrameTempVal = menuFrameTemp.optionsFrame  # return class frame value
        menuFrameCreateButtons = menuButtonCRT(menuFrameTemp.menuFrame, menuFrameTemp.optionsFrame, sixWidth, sixHeight)
        self.menuFrameCreateButtonsVal = menuFrameCreateButtons