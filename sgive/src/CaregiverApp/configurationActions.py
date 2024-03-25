import json
import os
import logging
from getmac import get_mac_address as gmac
from sgive.src.CaregiverApp import threatDetect

logger = logging.getLogger(__file__)
logger.info("initiated logging")


def get_path():
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
    path = os.path.join(os.getcwd(), "ML-saved")
    if os.path.exists(path):
        threatDetect.Main(URL)


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
            json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info(f'successfully edited value: "{value}" at key: "{name}".')
    return True


def restore_main_config():
    print("Restoring GLOBAL config")
    path = red_main_config("pathToConfig", "path")
    main_config_default(path)


def main_config_default(path):
    options = ["Global", "Mail", "Web", "Logs"]
    languageOPT = ["Czech", "English", "German"]
    GLobalFramesOptions = ["Display",
                           "Language",
                           "Sound language",
                           "Colorscheme",
                           "Alert color (in hex)",
                           "Highlight color (in hex)",
                           "Sound delay (in s)",
                           "Menu font size (in px)",
                           "Text font size (in px)",
                           "Font weight"]
    SMailLabelOptions = ["Senior email",
                         "Senior password",
                         "Caregiver email",
                         "Email contacts (up to six)",
                         "Email pictures (up to six)",
                         "Send phishing warning",
                         "Show URL links in email"]
    SWebLabelOptions = ["URLs for websites",
                        "Pictures for websites",
                        "Send phising warning",
                        "Phishing formular",
                        "Senior website posting",
                        "Allowed website posting"]
    EntryOptions = ["alertColor", "hoverColor", "soundDelay", "controlFontSize", "fontSize"]

    # I removed from GlobalConfiguration these two:
    # "light_color": "white",
    # "dark_color": "gray",

    dictionary = {
        'pathToConfig': {
            "path": path
        },
        'GlobalConfiguration': {
            "numOfScreen": 0,
            "language": "EN",
            "alertSoundLanguage": "EN",
            "colorMode": "Light",
            "alertColor": "#8B0000",
            "hoverColor": "#4b5946",
            "hoverColorLighten": "#7c8e76",
            "soundDelay": 5,
            "fontSize": 36,
            "controlFontSize": 70,
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
            "menu_frame": "#e5e5e5",
            "app_frame": "#FFFFFF",
            "buttons_unselected": "#e5e5e5",
            "buttons_selected": "#00ff00",
        },
        'careConf': {
            "fg": 5,
            "bg": 5,
            "heightDivisor": 7,
            "menuButtonsList": options.copy(),
            "LanguageOptions": languageOPT.copy(),
            "GlobalFrameLabels": GLobalFramesOptions.copy(),
            "SMailFrameLabels": SMailLabelOptions.copy(),
            "SwebFrameLabels": SWebLabelOptions.copy(),
            "EntryOptions": EntryOptions.copy(),
        },
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(os.path.join(path, 'config.json'), "w+", encoding='utf-8') as outfile:
        outfile.write(json_object)


# ------------


def smail_config_default(path):
    dictionary = {
        'pathToConfig': {
            "path": path
        },
        'credentials': {
            "username": "ts1bp2023@gmail.com",
            "password": "snfshqlirranyvwe",
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "imap_server": "imap.gmail.com",
            "imap_port": 993,
            "max": 20
        },
        "emails": {
            "Person1": "croce.rosay@gmail.com",
            "Person2": "robin.valu@seznam.cz",
            "Person3": "241124@vut.cz",
            "Person4": "email4@gmail.com",
            "Person5": "email5@gmail.com",
            "Person6": "email6@gmail.com"
        },
        "images": {
            "exit": "../sconf/images/SMAIL_EXIT_1.png",
            "Person1": "../sconf/images/SMAIL_PERSON_1.png",
            "Person2": "../sconf/images/SMAIL_PERSON_2.png",
            "Person3": "../sconf/images/SMAIL_PERSON_3.png",
            "Person4": "../sconf/images/SMAIL_PERSON_4.png",
            "Person5": "../sconf/images/SMAIL_PERSON_5.png",
            "Person6": "../sconf/images/SMAIL_PERSON_6.png"
        },
        "resend_email": 0,
        "show_url": 1,
        "guardian_email": "241124@vut.cz",
        "lang": "cz",
        "timer": 5000,
        "text": {
            "smail_en_sendToButton": "Send To",
            "smail_en_inboxLabel": "Inbox:",
            "smail_en_recipientLabel": "To: ",
            "smail_en_subjectLabel": "Subject: ",
            "smail_en_messageLabel": "Message: ",
            "smail_en_from": "From: ",
            "smail_en_date": "Date: ",
            "smail_cz_sendToButton": "Komu",
            "smail_cz_inboxLabel": "Doručené: ",
            "smail_cz_recipientLabel": "Příjemce: ",
            "smail_cz_subjectLabel": "Předmět: ",
            "smail_cz_messageLabel": "Zpráva: ",
            "smail_cz_from": "Od: ",
            "smail_cz_date": "Datum: ",
            "smail_de_sendToButton": "Senden An",
            "smail_de_inboxLabel": "Posteingang: ",
            "smail_de_recipientLabel": "An: ",
            "smail_de_subjectLabel": "Betreff: ",
            "smail_de_messageLabel": "Nachricht: ",
            "smail_de_from": "Von: ",
            "smail_de_date": "Datum: "
        },
        "audio": {
            "smail_en_exitButton": "../sconf/audio/SMAIL_EN_EXIT_1.mp3",
            "smail_en_alert": "../sconf/audio/SMAIL_EN_ALERT_1.mp3",
            "smail_en_person1": "../sconf/audio/SMAIL_EN_PERSON_1.mp3",
            "smail_en_person2": "../sconf/audio/SMAIL_EN_PERSON_2.mp3",
            "smail_en_person3": "../sconf/audio/SMAIL_EN_PERSON_3.mp3",
            "smail_en_person4": "../sconf/audio/SMAIL_EN_PERSON_4.mp3",
            "smail_en_person5": "../sconf/audio/SMAIL_EN_PERSON_5.mp3",
            "smail_en_person6": "../sconf/audio/SMAIL_EN_PERSON_6.mp3",
            "smail_en_sendToButton": "../sconf/audio/SMAIL_EN_SENDTO_1.mp3",
            "smail_en_menu1": "../sconf/audio/SMAIL_EN_MENU_1.mp3",
            "smail_en_menu2": "../sconf/audio/SMAIL_EN_MENU_2.mp3",
            "smail_cz_exitButton": "../sconf/audio/SMAIL_CZ_EXIT_1.mp3",
            "smail_cz_alert": "../sconf/audio/SMAIL_CZ_ALERT_1.mp3",
            "smail_cz_person1": "../sconf/audio/SMAIL_CZ_PERSON_1.mp3",
            "smail_cz_person2": "../sconf/audio/SMAIL_CZ_PERSON_2.mp3",
            "smail_cz_person3": "../sconf/audio/SMAIL_CZ_PERSON_3.mp3",
            "smail_cz_person4": "../sconf/audio/SMAIL_CZ_PERSON_4.mp3",
            "smail_cz_person5": "../sconf/audio/SMAIL_CZ_PERSON_5.mp3",
            "smail_cz_person6": "../sconf/audio/SMAIL_CZ_PERSON_6.mp3",
            "smail_cz_sendToButton": "../sconf/audio/SMAIL_CZ_SENDTO_1.mp3",
            "smail_cz_menu1": "../sconf/audio/SMAIL_CZ_MENU_1.mp3",
            "smail_cz_menu2": "../sconf/audio/SMAIL_CZ_MENU_2.mp3",
            "smail_de_exitButton": "../sconf/audio/SMAIL_DE_EXIT_1.mp3",
            "smail_de_alert": "../sconf/audio/SMAIL_DE_ALERT_1.mp3",
            "smail_de_person1": "../sconf/audio/SMAIL_DE_PERSON_1.mp3",
            "smail_de_person2": "../sconf/audio/SMAIL_DE_PERSON_2.mp3",
            "smail_de_person3": "../sconf/audio/SMAIL_DE_PERSON_3.mp3",
            "smail_de_person4": "../sconf/audio/SMAIL_DE_PERSON_4.mp3",
            "smail_de_person5": "../sconf/audio/SMAIL_DE_PERSON_5.mp3",
            "smail_de_person6": "../sconf/audio/SMAIL_DE_PERSON_6.mp3",
            "smail_de_sendToButton": "../sconf/audio/SMAIL_DE_SENDTO_1.mp3",
            "smail_de_menu1": "../sconf/audio/SMAIL_DE_MENU_1.mp3",
            "smail_de_menu2": "../sconf/audio/SMAIL_DE_MENU_2.mp3",

            "smail_en_inbox": "../sconf/audio/SMAIL_EN_INBOX_1.mp3",
            "smail_en_recipient": "../sconf/audio/SMAIL_EN_RECIPIENT_1.mp3",
            "smail_en_subject": "../sconf/audio/SMAIL_EN_SUBJECT_1.mp3",
            "smail_en_read_message": "../sconf/audio/SMAIL_EN_READ_1.mp3",
            "smail_en_write_message": "../sconf/audio/SMAIL_EN_WRITE_1.mp3",
            "smail_cz_inbox": "../sconf/audio/SMAIL_CZ_INBOX_1.mp3",
            "smail_cz_recipient": "../sconf/audio/SMAIL_CZ_RECIPIENT_1.mp3",
            "smail_cz_subject": "../sconf/audio/SMAIL_CZ_SUBJECT_1.mp3",
            "smail_cz_read_message": "../sconf/audio/SMAIL_CZ_READ_1.mp3",
            "smail_cz_write_message": "../sconf/audio/SMAIL_CZ_WRITE_1.mp3",
            "smail_de_inbox": "../sconf/audio/SMAIL_DE_INBOX_1.mp3",
            "smail_de_recipient": "../sconf/audio/SMAIL_DE_RECIPIENT_1.mp3",
            "smail_de_subject": "../sconf/audio/SMAIL_DE_SUBJECT_1.mp3",
            "smail_de_read_message": "../sconf/audio/SMAIL_DE_READ_1.mp3",
            "smail_de_write_message": "../sconf/audio/SMAIL_DE_WRITE_1.mp3"
        }
    }
    json_object = json.dumps(dictionary, indent=4, ensure_ascii=False)
    with open(os.path.join(path, 'SMAIL_config.json'), "w+", encoding='utf-8') as outfile:
        outfile.write(json_object)


def restore_smail_config():
    path = read_smail_config("pathToConfig", "path")
    smail_config_default(path)


def read_smail_config(key, value):
    path = get_path()
    if os.path.exists(path) and os.path.isfile(
            os.path.join(get_path(), 'SMAIL_config.json')):  # checks for the conf file, if there is any
        with open(os.path.join(path, 'SMAIL_config.json'), "r") as file:
            jsonData = json.load(file)
        if key == '' or key is None:
            return jsonData[value]
        else:
            return jsonData[key][value]
    else:
        logging.critical('There is no SMAIL_config.json or sconf/ file present in system, exiting program now.')
        exit(1)


def edit_smail_config(key, name, value):
    # this def edits name in conf.json to value
    path = get_path()
    # checks for the conf file, if there is any
    if os.path.exists(path) and os.path.isfile(os.path.join(get_path(), 'config.json')):
        with open(os.path.join(path, 'SMAIL_config.json'), 'r', encoding='utf-8') as file:
            data = json.load(file)
            if key is None:
                data[name] = value
            else:
                data[key][name] = value
        with open(os.path.join(path, 'SMAIL_config.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)  # Ensure_ascii=False zajistí zachování ne-ASCII znaků
    logging.info(f'successfully edited value: "{value}" at key: "{name}".')
    return True


# -------------------------------------


def sweb_config_default(path):
    dictionary = {
        "phishing_database": {
            "path": "../sconf/phish/SWEB_PHISH_1.txt",
            "path_to_tar_github": "https://github.com/mitchellkrogza/Phishing.Database/raw/master/ALL-phishing-domains.tar.gz/"
        },
        "credentials": {
            "sender_mail": "ninhtestmagisterwork11111@gmail.com",
            "sender_password": "txhs bgkh aiga jnjc",
            "receiver_mail": "nguoiyeuvtv@gmail.com",
            "subject": "User's filling data",
            "smpt_server": "smtp.gmail.com",
            "smtp_port": 587
        },
        "language": {
            "default_language": "en"
        },
        "image": {
            "sweb_image_exit": "../sconf/images/SWEB_EXIT.png",
            "sweb_image_www1": "../sconf/images/SWEB_WWW1.png",
            "sweb_image_www2": "../sconf/images/SWEB_WWW2.png",
            "sweb_image_www3": "../sconf/images/SWEB_WWW3.jpg",
            "sweb_image_www4": "../sconf/images/SWEB_WWW4.png",
            "sweb_image_www5": "../sconf/images/SWEB_WWW5.png"
        },
        "colors_info": {
            "menu_frame": "#e5e5e5",
            "app_frame": "#FFFFFF",
            "buttons_unselected": "#e5e5e5",
            "buttons_selected": "#00ff00"
        },
        "text": {
            "sweb_en_menu1": "Menu 1",
            "sweb_en_menu2": "Menu 2",
            "sweb_en_menu2Address": "My page",
            "sweb_cz_menu1": "Menu 1",
            "sweb_cz_menu2": "Menu 2",
            "sweb_cz_menu2Address": "Moje stránka",
            "sweb_de_menu1": "Menü 1",
            "sweb_de_menu2": "Menü 2",
            "sweb_de_menu2Address": "Meine Seite"
        },
        "audio": {
            "sweb_en_menu1": "../sconf/audio/SWEB_EN_MENU_1.mp3",
            "sweb_en_menu1Exit": "../sconf/audio/SWEB_EN_EXIT.mp3",
            "sweb_en_menu1Back": "../sconf/audio/SWEB_EN_BACK.mp3",
            "sweb_en_menu1WWW1": "../sconf/audio/SWEB_EN_WWW_1.mp3",
            "sweb_en_menu1WWW2": "../sconf/audio/SWEB_EN_WWW_2.mp3",
            "sweb_en_menu2WWW3": "../sconf/audio/SWEB_EN_WWW_3.mp3",
            "sweb_en_menu2": "../sconf/audio/SWEB_EN_MENU_2.mp3",
            "sweb_en_menu2WWW4": "../sconf/audio/SWEB_EN_WWW_4.mp3",
            "sweb_en_menu2WWW5": "../sconf/audio/SWEB_EN_WWW_5.mp3",
            "sweb_en_menu2Address": "../sconf/audio/SWEB_EN_ADDRESS.mp3",
            "sweb_en_alert_phishing": "../sconf/audio/SWEB_EN_ALERT_PHISHING.mp3",
            "sweb_en_url": "../sconf/audio/SWEB_EN_URL.mp3",
            "sweb_cz_menu1": "../sconf/audio/SWEB_CZ_MENU_1.mp3",
            "sweb_cz_menu1Exit": "../sconf/audio/SWEB_CZ_EXIT.mp3",
            "sweb_cz_menu1Back": "../sconf/audio/SWEB_CZ_BACK.mp3",
            "sweb_cz_menu1WWW1": "../sconf/audio/SWEB_CZ_WWW_1.mp3",
            "sweb_cz_menu1WWW2": "../sconf/audio/SWEB_CZ_WWW_2.mp3",
            "sweb_cz_menu2WWW3": "../sconf/audio/SWEB_CZ_WWW_3.mp3",
            "sweb_cz_menu2": "../sconf/audio/SWEB_CZ_MENU_2.mp3",
            "sweb_cz_menu2WWW4": "../sconf/audio/SWEB_CZ_WWW_4.mp3",
            "sweb_cz_menu2WWW5": "../sconf/audio/SWEB_CZ_WWW_5.mp3",
            "sweb_cz_menu2Address": "../sconf/audio/SWEB_CZ_ADDRESS.mp3",
            "sweb_cz_alert_phishing": "../sconf/audio/SWEB_CZ_ALERT_PHISHING.mp3",
            "sweb_cz_url": "../sconf/audio/SWEB_CZ_URL.mp3",
            "sweb_de_menu1": "../sconf/audio/SWEB_DE_MENU_1.mp3",
            "sweb_de_menu1Back": "../sconf/audio/SWEB_DE_BACK.mp3",
            "sweb_de_menu1Exit": "../sconf/audio/SWEB_DE_EXIT.mp3",
            "sweb_de_menu1WWW1": "../sconf/audio/SWEB_DE_WWW_1.mp3",
            "sweb_de_menu1WWW2": "../sconf/audio/SWEB_DE_WWW_2.mp3",
            "sweb_de_menu2WWW3": "../sconf/audio/SWEB_DE_WWW_3.mp3",
            "sweb_de_menu2": "../sconf/audio/SWEB_DE_MENU_2.mp3",
            "sweb_de_menu2WWW4": "../sconf/audio/SWEB_DE_WWW_4.mp3",
            "sweb_de_menu2WWW5": "../sconf/audio/SWEB_DE_WWW_5.mp3",
            "sweb_de_menu2Address": "../sconf/audio/SWEB_DE_ADDRESS.mp3",
            "sweb_de_alert_phishing": "../sconf/audio/SWEB_DE_ALERT_PHISHING.mp3",
            "sweb_de_url": "../sconf/audio/SWEB_DE_URL.mp3"
        },
        "template": {
            "num_of_menu_buttons": 2,
            "num_of_opt_on_frame": 4,
            "padx_value": 5,
            "height_divisor": 4.5,
            "width_divisor": 5,
            "numOfScreen": 0,
            "language": "English",
            "colorMode": "Light",
            "soundDelay": 5,
            "alertColor": "#AAFF00",
            "alertSoundLanguage": "english",
            "fontSize": 36,
            "fontThickness": "bold",
            "fontFamily": "Helvetica"
        }

    }
    json_object = json.dumps(dictionary, indent=4, ensure_ascii=False)
    with open(os.path.join(path, 'SWEB_config.json'), "w+", encoding='utf-8') as outfile:
        outfile.write(json_object)


def restore_sweb_config():
    path = get_path()
    sweb_config_default(path)


def read_sweb_config(key, value):
    path = get_path()
    if os.path.exists(path) and os.path.isfile(
            os.path.join(get_path(), 'SWEB_config.json')):  # checks for the conf file, if there is any
        with open(os.path.join(path, 'SWEB_config.json'), "r") as file:
            jsonData = json.load(file)
        if key == '' or key is None:
            return jsonData[value]
        else:
            return jsonData[key][value]
    else:
        logging.critical('There is no SWEB_config.json or sconf/ file present in system, exiting program now.')
        exit(1)


def edit_sweb_config(key, name, value):
    # this def edits name in conf.json to value
    path = get_path()
    # checks for the conf file, if there is any
    if os.path.exists(path) and os.path.isfile(os.path.join(get_path(), 'config.json')):
        with open(os.path.join(path, 'SWEB_config.json'), 'r', encoding='utf-8') as file:
            data = json.load(file)
            if key is None:
                data[name] = value
            else:
                data[key][name] = value
        with open(os.path.join(path, 'SWEB_config.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)  # Ensure_ascii=False zajistí zachování ne-ASCII znaků
    logging.info(f'successfully edited value: "{value}" at key: "{name}".')
    return True
