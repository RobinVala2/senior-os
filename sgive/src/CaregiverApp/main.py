from tkinter import *
import configurationActions as ryuconf
import os
import CaregiverGUI as ryuGUI
import logging

logging.basicConfig(
    filename=os.path.join(ryuconf.temporaryGetPath(), 'ConfigurationApp.log'),
    level=logging.INFO,
    format="%(asctime)s : %(module)s %(levelname)s - %(funcName)s at line %(lineno)s : %(message)s",
    filemode='w+',
)

if __name__ == '__main__':
    whereTheFuckAmI = os.getcwd()
    split = whereTheFuckAmI.split("sgive")
    path = split[0]
    configPath = os.path.join(path, "sconf")
    # create config, only if there is not any config.json already
    if os.path.exists(configPath) and not os.path.isfile(os.path.join(configPath, 'config.json')):
        ryuconf.caregiverAppConfig(configPath)
        logging.error("No config was found, generating new one.")

    root = Tk()
    ryuGUI.AppBase(root)
    root.mainloop()
