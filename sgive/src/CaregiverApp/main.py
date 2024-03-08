from tkinter import *
import configurationActions as ryuconf
import os
from sgive.src.CaregiverApp import FrontEnd
import logging

logging.basicConfig(
    filename=os.path.join(ryuconf.get_log(), 'ConfigurationApp.log'),
    level=logging.INFO,
    format="%(asctime)s : %(module)s %(levelname)s - %(funcName)s at line %(lineno)s : %(message)s",
    filemode='w+',
)

if __name__ == '__main__':
    whereTheFuckAmI = os.getcwd()
    path_split = whereTheFuckAmI.split("sgive")
    config_folder = os.path.join(path_split[0], "sconf")

    configFilenames_arr = ["config.json", "SMAIL_config.json", "SWEB_config.json"]

    for file_name in configFilenames_arr:
        if not (os.path.exists(config_folder) and os.path.isfile(os.path.join(config_folder, file_name))):
            if file_name == "config.json":  # kind of redundant now, because frontend gets executed first...
                ryuconf.main_config_default(config_folder)
            elif file_name == "SMAIL_config.json":
                ryuconf.smail_config_default(config_folder)
            elif file_name == "SWEB_config.json":
                print("todo")

    # calling ML
    url = ['https://xhamster.com/', 'https://www.seznamzpravy.cz/clanek/zahranicni-stredni-evropa-policek-pro-slovensko-vlada-rusi-spolecna-jednani-247254#dop_ab_variant=0&dop_source_zone_name=zpravy.sznhp.box&source=hp&seq_no=1&utm_campaign=abtest241_shrnuti_llm_varB&utm_medium=z-boxiku&utm_source=www.seznam.cz']
    ryuconf.MLcheck(url)
    # calling Frontend
    FrontEnd.main()
