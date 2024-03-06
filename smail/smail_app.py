import logging
import os
import tkinter
from template import configActions as act
from layout import one_frame
from antiphishing.get_DB import get_DB


logging.basicConfig(
     level=logging.INFO,
     filename=os.path.join(os.getcwd().split("smail")[0], "sconf/logs/SMAILlog.log"),
     filemode="w",
     format="%(asctime)s:SMAIL-%(levelname)s-%(funcName)s: %(message)s",
     datefmt="%b %d %H:%M:%S",
)

if __name__ == '__main__':
    _currentVersionOfConfig = 0.3
    isExist = act.configExistCheck(_currentVersionOfConfig)
    # get phishing database
    get_DB()
    if isExist:
        root = tkinter.Tk()
        root.configure(bg="#FFFFFF")
        app = one_frame(root)
        root.mainloop()
    else:
        logging.critical("Could not start SMAIL app.")
