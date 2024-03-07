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
    url = ['https://xhamster.com/', 'https://www.seznamzpravy.cz/clanek/zahranicni-stredni-evropa-policek-pro-slovensko-vlada-rusi-spolecna-jednani-247254#dop_ab_variant=0&dop_source_zone_name=zpravy.sznhp.box&source=hp&seq_no=1&utm_campaign=abtest241_shrnuti_llm_varB&utm_medium=z-boxiku&utm_source=www.seznam.cz']
    ryuconf.MLcheck(url)

    whereTheFuckAmI = os.getcwd()
    split = whereTheFuckAmI.split("sgive")
    path = split[0]
    configPath = os.path.join(path, "sconf")
    # create config, only if there is not any config.¨json already
    if os.path.exists(configPath) and not os.path.isfile(os.path.join(configPath, 'config.json')):
        ryuconf.main_config_default(configPath)
        logging.error("No global config was found, generating new one.")
    elif os.path.exists(configPath) and not os.path.isfile(os.path.join(configPath, 'SMAIL_config.json')):
        ryuconf.smail_config_default(configPath)
        logging.error("No SMAIL config was found, generating new one.")


    # root = Tk()
    # ryuFrontEnd.AppBase(root)
    # root.mainloop()
    ryuFrontEnd.main()  # FRONTEND CALL
