from tkinter import *
import tkinter
import tkinter.font as tkFont
from screeninfo import get_monitors

import sgive.src.gui_template.Tkinter_UI as temp
import sgive.src.gui_template.CustomTkinter_UI as guiTempCTK
import sgive.src.gui_template.configActions as JS


def deprecated_tkinter(old_root):
    old_root.destroy()

    _currentVersionOfConfig = 0.3
    isExist = JS.configExistCheck(_currentVersionOfConfig)
    if isExist:
        root = tkinter.Tk()
        temp.App(root)
        AppResolution = temp.resolutionMath()
        print(f"resolution of the app is:{AppResolution[3]}x{AppResolution[4]}")
        root.mainloop()
    else:
        print("LOG: there is no conf.json present in the system")
        exit(1)


def customTkinter(old_root):
    JS.restore_main_config()
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
    custom_font = tkFont.Font(family="Helvetica", size=16, weight="bold")  # Můžete změnit na jiný font podle potřeby

    option_1 = tkinter.Button(menu_root, text="Old Tkinter", font=custom_font,
                              command=lambda: deprecated_tkinter(menu_root))
    option_1.place(x=0, y=0, height=_app_height, width=_app_width * 0.5)

    option_2 = tkinter.Button(menu_root, text="New CustomTkinter",font=custom_font,
                              command=lambda: customTkinter(menu_root))
    option_2.place(x=_app_width * 0.5, y=0, height=_app_height, width=_app_width * 0.5)

    menu_root.mainloop()

def main():
    JS.restore_main_config()
    path = JS.temporaryGetPath()
    JS._jsonWrite(path)
    app()


if __name__ == '__main__':
    main()

