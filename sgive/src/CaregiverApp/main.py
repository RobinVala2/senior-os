from tkinter import *
import configurationActions as ryuconf
import os
#  import CaregiverGUI as ryuFrontEnd
import FrontEnd as ryuFrontEnd
import logging

logging.basicConfig(
    filename=os.path.join(ryuconf.get_log(), 'ConfigurationApp.log'),
    level=logging.INFO,
    format="%(asctime)s : %(module)s %(levelname)s - %(funcName)s at line %(lineno)s : %(message)s",
    filemode='w+',
)

if __name__ == '__main__':
    url = ['https://www.google.com/', 'https://www.youtube.cum/']
    ryuconf.MLcheck(url)

    whereTheFuckAmI = os.getcwd()
    split = whereTheFuckAmI.split("sgive")
    path = split[0]
    configPath = os.path.join(path, "sconf")
    # create config, only if there is not any config.json already
    if os.path.exists(configPath) and not os.path.isfile(os.path.join(configPath, 'config.json')):
        ryuconf.main_config_default(configPath)
        logging.error("No config was found, generating new one.")

    # root = Tk()
    # ryuFrontEnd.AppBase(root)
    # root.mainloop()
    ryuFrontEnd.main()  # FRONTEND CALL
