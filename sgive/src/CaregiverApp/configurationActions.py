import json
import os
import logging
from getmac import get_mac_address as gmac
from sgive.src.CaregiverApp import threatDetect

logger = logging.getLogger(__file__)
logger.info("initiated logging")


def get_path():  # this is how i get to the sconf/ file, for now :)
    whereTheFuckAmI = os.getcwd()
    split = whereTheFuckAmI.split("sgive")
    path = split[0]
    configPath = os.path.join(path, "sconf")
    return configPath


# LOG FILES ACTIONS: ---------------------------------------------------------------------------------------------------
def get_log():
    whereTheFuckAmI = os.getcwd()
    split = whereTheFuckAmI.split("sgive")
    path = split[0]
    configPath = os.path.join(path, "sconf")
    if os.path.exists(os.path.join(configPath, "logs")):
        return os.path.join(configPath, "logs")
    else:
        os.mkdir(os.path.join(configPath, "logs"))
        return os.path.join(configPath, "logs")


def read_log(givenFilter, givenName):
    if givenName is None:
        return
    findPhrases = []
    if givenFilter is None:
        findPhrases = ["INFO", "WARNING", "CRITICAL", "ERROR"]
    else:
        findPhrases.append(givenFilter)
        print(f"filtering by:{givenFilter}")
    pickedValues = []
    path = get_log()
    if os.path.exists(path) and os.path.isfile(
            os.path.join(get_log(), givenName)):  # check if log and folder exists
        with open(os.path.join(path, givenName)) as f:  # open log file
            f = f.readlines()  # read
        for line in f:  # check each lines
            for phrase in findPhrases:  # check list
                if phrase in line:  # if its same
                    pickedValues.append(line)  # add to the pickedValues list
                    break  # bžum bžum bžum brekeke
        return pickedValues
    else:
        logging.error(f"There is no {givenName}.log in sconf/logs or the folder itself is missing.")


# CHECK FOR ML LEARNING ------------------------------------------------------------------------------------------------
def MLcheck(URL):
    print("Checking for /ML-SAVED dir...")
    path = os.path.join(os.getcwd(), "ML-saved")

    if os.path.exists(path):
        threatDetect.Main(URL)
        print(os.listdir(path))


# MAIN (GLOBAL) CONFIG ACTIONS: ----------------------------------------------------------------------------------------
def red_main_config(key, value):  # this reads only main config
    path = get_path()
    if os.path.exists(path) and os.path.isfile(
            os.path.join(get_path(), 'config.json')):  # checks for the conf file, if there is any
        with open(os.path.join(path, 'config.json'), "r") as file:
            jsonData = json.load(file)
        return jsonData[key][value]
    else:
        logging.critical('There is no config.json or sconf/ file present in system, exiting program now.')
        exit(1)


def edit_main_config(key, name, value):
    # this def edits name in conf.json to value
    path = get_path()
    # checks for the conf file, if there is any
    if os.path.exists(path) and os.path.isfile(os.path.join(get_path(), 'config.json')):
        with open(os.path.join(path, 'config.json'), 'r') as file:
            data = json.load(file)
            data[key][name] = value
        with open(os.path.join(path, 'config.json'), 'w') as f:
            json.dump(data, f, indent=4)
    logging.info(f'successfully edited value: "{value}" at key: "{name}".')


def restore_main_config():
    print("Restoring config")
    path = red_main_config("pathToConfig", "path")
    main_config_default(path)


def main_config_default(path):
    options = ["Global", "Mail", "Web", "LOGS"]
    languageOPT = ["Czech", "English", "German"]
    GLobalFramesOptions = ["Choose primary display:", "Choose OS language:", "Choose alert language:",
                           "Choose colorscheme:", "Choose alert color (hex):", "Choose alert delay:",
                           "Choose font size:", "Choose label size:", "Choose boldness:", "add later:"]
    SMailLabelOptions = ["Senior's email:", "Senior's password:", "Add emails:", "Activation for care. email",
                         "Caregiver email:"]
    dictionary = {
        'pathToConfig': {
            "path": path
        },
        'GlobalConfiguration': {
            "numOfScreen": 0,
            "language": "English",
            "colorMode": "light",
            "light_color": "white",
            "dark_color": "gray",
            "soundDelay": 5,
            "alertColor": "#8B0000",
            "alertSoundLanguage": "English",
            "fontSize": 36,
            "labelFontSize": 12,
            "fontThickness": "bold",
            "fontFamily": "Helvetica",
        },
        "GUI_template": {
            "num_of_menu_buttons": 2,
            "num_of_opt_on_frame": 4,
            "num_of_opt_buttons": 18,
            "padx_value": 5,
            "height_divisor": 4.5,
            "width_divisor": 5,
        },
        'careConf': {
            "fg": 5,
            "bg": 5,
            "heightDivisor": 7,
            "menuButtonsList": options.copy(),
            "LanguageOptions": languageOPT.copy(),
            "GlobalFrameLabels": GLobalFramesOptions.copy(),
            "SMailFrameLabels": SMailLabelOptions.copy(),
        },
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(os.path.join(path, 'config.json'), "w+") as outfile:
        outfile.write(json_object)
