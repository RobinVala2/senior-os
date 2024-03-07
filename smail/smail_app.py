import logging
import os
import tkinter
from sgive.src.CaregiverApp.configurationActions import main_config_default, smail_config_default
from layout import one_frame
from antiphishing.get_DB import get_DB
from template import configActions as act


logging.basicConfig(
     level=logging.INFO,
     filename=os.path.join(os.getcwd().split("smail")[0], "sconf/logs/SMAILlog.log"),
     filemode="w",
     format="%(asctime)s:SMAIL-%(levelname)s-%(funcName)s: %(message)s",
     datefmt="%b %d %H:%M:%S",
)

if __name__ == '__main__':

    config_path = os.path.join(os.getcwd().split("smail")[0], "sconf/")

    try:

        # Generating old configuration file for template
        config_old = act.configExistCheck("0")

        # Check if configuration files exist
        if not os.path.exists(os.path.join(config_path, "config.json")):
            main_config_default(os.path.join(config_path))
            logging.info("Generating global configuration file.")

        if not os.path.exists(os.path.join(config_path, "SMAIL_config.json")):
            smail_config_default(os.path.join(config_path))
            logging.info("Generating SMAIL configuration file.")

        # Getting phishing database
        get_DB()

        root = tkinter.Tk()
        root.configure(bg="#FFFFFF")
        app = one_frame(root)
        root.mainloop()
    except Exception as e:
        logging.critical("Could not start SMAIL app, error loading configuration." + e)
