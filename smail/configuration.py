import json
import os


def smail_config_default(path):
    dictionary = {
        'pathToConfig': {
            "path": path
        },
        'credentials': {
            "username": "ts1bp2023@gmail.com",
            "password": "ajoliddkigtswdpe",
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
    with open(os.path.join(path, 'SMAIL_config.json'), "w+", encoding='utf-8') as f:
        f.write(json_object)

def global_config_default(path):
    dictionary = {
        "pathToConfig": {
            "path": "/home/robinvala/BP/senior-os/sconf/"
        },
        "GlobalConfiguration": {
            "numOfScreen": 0,
            "language": "EN",
            "alertSoundLanguage": "EN",
            "colorMode": "Light",
            "alertColor": "#f20c1f",
            "hoverColor": "#03ff03",
            "hoverColorLighten": "#7c8e76",
            "soundDelay": 5,
            "fontSize": 36,
            "controlFontSize": 70,
            "fontThickness": "bold",
            "fontFamily": "Helvetica"
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
            "buttons_selected": "#00ff00"
        },
        "careConf": {
            "fg": 5,
            "bg": 5,
            "heightDivisor": 7,
            "menuButtonsList": [
                "Global",
                "Mail",
                "Web",
                "Logs"
            ],
            "LanguageOptions": [
                "Czech",
                "English",
                "German"
            ],
            "GlobalFrameLabels": [
                "Display",
                "Language",
                "Sound language",
                "Colorscheme",
                "Alert color (in hex)",
                "Highlight color (in hex)",
                "Sound delay (in s)",
                "Toolbar font (in px)",
                "Widget font (in px)",
                "Font weight"
            ],
            "SMailFrameLabels": [
                "Senior email",
                "Senior password",
                "Email contacts (six)",
                "Pictures (six)",
                "Caregiver warning",
                "Caregiver email",
                "URL links in email"
            ],
            "SwebFrameLabels": [
                "Sender email",
                "Sender password",
                "Receiver email"
            ],
            "EntryOptions": [
                "alertColor",
                "hoverColor",
                "soundDelay",
                "controlFontSize",
                "fontSize"
            ]
        }
    }
    json_object = json.dumps(dictionary, indent=4)
    with open(os.path.join(path, 'config.json'), "w+", encoding='utf-8') as f:
        f.write(json_object)