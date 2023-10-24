import json
import os
import logging
from getmac import get_mac_address as gmac

logger = logging.getLogger(__file__)
logger.info("initiated logging")


def temporaryGetPath():  # this is how i get to the sconf/ file, for now :)
    whereTheFuckAmI = os.getcwd()
    split = whereTheFuckAmI.split("sgive")
    path = split[0]
    configPath = os.path.join(path, "sconf")
    return configPath
def getLogFile():
    whereTheFuckAmI = os.getcwd()
    split = whereTheFuckAmI.split("sgive")
    path = split[0]
    configPath = os.path.join(path, "sconf")
    if os.path.exists(os.path.join(configPath, "logs")):
        return os.path.join(configPath, "logs")
    else:
        os.mkdir(os.path.join(configPath, "logs"))
        return os.path.join(configPath, "logs")

def readJsonConfig(key, value):
    path = temporaryGetPath()
    if os.path.exists(path) and os.path.isfile(
            os.path.join(temporaryGetPath(), 'config.json')):  # checks for the conf file, if there is any
        with open(os.path.join(path, 'config.json'), "r") as file:
            jsonData = json.load(file)
        return jsonData[key][value]
    else:
        logging.critical('There is no config.json or sconf/ file present in system, exiting program now.')
        exit(1)


def readLog(givenFilter,givenName):
    print(givenName)
    findPhrases = []
    if givenFilter is None:
        print("given value is NONE")
        findPhrases = ["INFO", "WARNING", "CRITICAL","ERROR"]
    else:
        findPhrases.append(givenFilter)
        print(f"filtering by:{givenFilter}")
    pickedValues = []
    path = getLogFile()
    if os.path.exists(path) and os.path.isfile(os.path.join(getLogFile(), f'{givenName}.log')):  # check if log and folder exists
        with open(os.path.join(path, f'{givenName}.log')) as f:  # open log file
            f = f.readlines()  # read
        for line in f:  # check each lines
            for phrase in findPhrases:  # check list
                if phrase in line:  # if its same
                    pickedValues.append(line)  # add to the pickedValues list
                    break  # bžum bžum bžum brekeke
        return pickedValues
    else:
        logging.error(f'There is no {givenName}.log in sconf/logs or the folder itself is missing.')
        #exit(1)


def editConfig(key, name, value):
    # this def edits name in conf.json to value
    path = temporaryGetPath()
    # checks for the conf file, if there is any
    if os.path.exists(path) and os.path.isfile(os.path.join(temporaryGetPath(), 'config.json')):
        with open(os.path.join(path, 'config.json'), 'r') as file:
            data = json.load(file)
            data[key][name] = value
        with open(os.path.join(path, 'config.json'), 'w') as f:
            json.dump(data, f, indent=4)
    logging.info(f'successfully edited value: "{value}" at key: "{name}".')


def getMac():
    mac = gmac()
    return mac


def caregiverAppConfig(path):
    options = ["Global\nconfig", "Mail\nconfig", "Web\nconfig", "LOGS"]
    languageOPT = ["Czech", "English", "German"]
    dictionary = {
        'pathToConfig': {
            "path": path
        },
        'GlobalConfiguration': {
            "numOfScreen": 0,
            "language": "English",
            "colorMode": "light",
            "soundDelay": 5,
            "alertColor": "#AAFF00",
            "alertSoundLanguage": "English",
            "fontSize": 36,
            "labelFontSize": 12,
            "fontThickness": "bold",
            "fontFamily": "Helvetica",
            "macAddress": getMac(),
        },
        "GUI_template" : {
            "num_of_menu_buttons": 2,
            "num_of_opt_on_frame": 4,
            "padx_value": 5,
            "height_divisor": 4.5,
            "width_divisor": 5,
        },
        'careConf': {
            "fg": 5,
            "bg": 5,
            "heightDivisor": 7,
            "menuButtonsList": options.copy(),
            "LanguageOptions": languageOPT.copy()

        },
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(os.path.join(path, 'config.json'), "w+") as outfile:
        outfile.write(json_object)
