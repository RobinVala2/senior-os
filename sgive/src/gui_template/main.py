from tkinter import *
import guiTemplate as temp
import configActions as act

import tkinter
from tkinter import *
import sgive.src.gui_template.configActions as JS
from screeninfo import get_monitors

from sgive.src.guiTemplateCustomTkinter import guiTempCTK


def deprecated_tkinter(old_root):
    old_root.destroy()

    _currentVersionOfConfig = 0.3
    isExist = act.configExistCheck(_currentVersionOfConfig)
    if isExist:
        root = Tk()
        temp.App(root)
        AppResolution = temp.resolutionMath()
        print(f"resolution of the app is:{AppResolution[3]}x{AppResolution[4]}")
        root.mainloop()
    else:
        print("LOG: there is no conf.json present in the system")
        exit(1)


def customTkinter(old_root):
    old_root.destroy()
    guiTempCTK.main()


def app():
    menu_root = Tk()  # create a root widget
    menu_root.title("Which GUI")
    menu_root.configure(background="gray")

    _numOfScreen = JS.jsonRed('resolution_info', "numOfScreen")
    _screen_width = get_monitors()[_numOfScreen].width
    _screen_height = get_monitors()[_numOfScreen].height
    _app_width = int(get_monitors()[_numOfScreen].width / 2)
    _app_height = int(get_monitors()[_numOfScreen].height / 2)

    # width, height
    menu_root.minsize(int(_screen_width / 7), int(_screen_height / 7))  # smallest possible window size
    menu_root.maxsize(_screen_width, _screen_height)  # biggest possible window size
    # window size and position
    menu_root.geometry(
        f"{_app_width}x{_app_height}+{int((_screen_width / 2) - _app_width / 2)}+{int((_screen_height / 2) - _app_height / 2)}")
    # width x height + x + y

    _widget_height = _app_height * 0.25

    f3 = Frame(menu_root, bd=1, bg="blue", relief=SUNKEN)
    f3.place(height=_widget_height, width=_app_width, x=0, y=_app_height - _app_height * 0.25)

    option_1 = tkinter.Button(f3, text="Old Tkinter", command=lambda: deprecated_tkinter(menu_root))
    option_1.place(x=0, y=0, height=_widget_height, width=_app_width * 0.339)

    option_2 = tkinter.Button(f3, text="New CustomTkinter", command=lambda: customTkinter(menu_root))
    option_2.place(x=_app_width * 0.339, y=0, height=_widget_height, width=_app_width * 0.339)

    option_3 = tkinter.Button(f3, text="New Tkinter")
    option_3.place(x=2 * _app_width * 0.339, y=0, height=_widget_height, width=_app_width * 0.339)

    menu_root.mainloop()


if __name__ == '__main__':
    app()
