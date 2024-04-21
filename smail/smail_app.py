import logging
import os
import tkinter
from layout import one_frame
from antiphishing.get_DB import get_DB
from template import configActions as act
from configuration import smail_config_default, check_logfile


if __name__ == '__main__':

    check_logfile()
    config_path = os.path.join(os.getcwd().split("smail")[0], "sconf/")

    try:
        # Generating global configuration file
        config = act.configExistCheck()

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
