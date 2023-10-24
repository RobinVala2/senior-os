import json
import os


def temporaryGetPath():
    whereTheFuckAmI = os.getcwd()
    split = whereTheFuckAmI.split("sgive")
    path = split[0]
    configPath = os.path.join(path, "sconf")
    return configPath


def configExistCheck(givenVersion):
    pathToJsonConf = temporaryGetPath()
    print(pathToJsonConf)
    if os.path.exists(pathToJsonConf):
        if os.path.isfile(os.path.join(pathToJsonConf, 'OLDconfig.json')):
            print(os.path.isfile(os.path.join(pathToJsonConf, 'configOLD.json')))
            currentVersion = jsonRed('Version', "configVersion")
            if not currentVersion == givenVersion:
                _jsonWrite(givenVersion)
                print("LOG: updating conf.json")
                return True
            print("LOG: conf.json is already there, skipping")
            return True
        else:
            _jsonWrite(givenVersion)
            return True
    else:
        print("LOG: there is no path to the configuration file")
        return False


def _jsonWrite(currentVersion):
    # default json config
    dictionary = {
        'Version': {
            "configVersion": currentVersion
        },
        'buttons_info': {
            "num_of_menu_buttons": 2,
            "num_of_opt_on_frame": 4,
            "num_of_opt_buttons": 18,
            "padx_value": 5,
        },
        'colors_info': {
            "menu_frame": "#e5e5e5",
            "app_frame": "#FFFFFF",
            "buttons_unselected": "#e5e5e5",
            "buttons_selected": "#00ff00",
        },
        'font_info': {
            "font": "Helvetica 36 bold",
        },
        'resolution_info': {
            "numOfScreen": 0,
            "height_divisor": 4.5,
            "width_divisor": 5,
        }
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(f"{temporaryGetPath()}/OLDconfig.json", "w+") as outfile:
        outfile.write(json_object)


def jsonRed(key, value):
    path = temporaryGetPath()
    if os.path.exists(path):  # checks for the conf file, if there is any
        with open(os.path.join(path, 'OLDconfig.json'), "r") as file:
            jsonData = json.load(file)
        return jsonData[key][value]
    else:
        print("LOG: there is no path to the configuration file")
        return
