import logging
import json
import pygame
import PIL
from PIL import Image, ImageTk
from smail.template.guiTemplate import resolutionMath

logger = logging.getLogger(__file__)


def load_json_file(file_path):

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return 0
    except Exception as error:
        logging.error(f"An unexpected error occurred while loading data from {file_path}", exc_info=True)
        return -1


def load_credentials(path):

    data = load_json_file(path)
    credentials = data["credentials"]
    login = credentials["username"]
    password = credentials["password"]
    smtp_server = credentials["smtp_server"]
    smtp_port = credentials["smtp_port"]
    imap_server = credentials["imap_server"]
    imap_port = credentials["imap_port"]

    return login, password, smtp_server, smtp_port, imap_server, imap_port

def load_show_url(path):

    data = load_json_file(path)
    show = data["show_url"]
    return show

def font_config():

    # Reading font configuration
    data = load_json_file("../sconf/config_old.json")
    font_info = data["font_info"]["font"]
    return font_info

def app_color():

    # Reading background color configuration
    data = load_json_file("../sconf/config_old.json")
    bg = data["colors_info"]["app_frame"]
    return bg

def images():

    # Reading image configuration
    data = load_json_file("../sconf/SMAIL_config.json")
    images = data["images"]
    return images


def image_config(name, btn_height):

    data = images()
    path = data[name]
    original_image = Image.open(path)
    height_ratio = btn_height / original_image.height
    new_height = int(original_image.height * height_ratio)
    resized_image = original_image.resize((int(original_image.width * height_ratio), new_height), PIL.Image.LANCZOS)
    image = ImageTk.PhotoImage(resized_image)
    return image


def search_mail(id):

    # Searching email address of a person
    data = load_json_file("../sconf/SMAIL_config.json")
    emails = data["emails"]
    email = emails[f"Person{id}"]
    return email


def get_language():

    # Checks selected language
    data = load_json_file("../sconf/SMAIL_config.json")
    language = data["lang"]
    text = data["text"]
    return language, text


# audio session
def get_audio():

    # Reads configuration from json file
    data = load_json_file("../sconf/SMAIL_config.json")
    language = data["lang"]
    audio = data["audio"]
    timer = data["timer"]
    return language, audio, timer


def play_sound(button_name):

    pygame.mixer.init()
    language, audio, timer = get_audio()
    # Loads the audio file corresponding to the button_name.
    pygame.mixer.music.load(audio[f"smail_{language}_{button_name}"])
    # Plays the loaded audio.
    pygame.mixer.music.play()


def button_hover(button, button_name, enter_time):

    # Function is called when the mouse cursor hovers over a button.
    language, audio, timer = get_audio()
    # Scheduling playing sound after a specified time delay.
    # Storing the scheduled time event ID in enter_time[0].
    enter_time[0] = button.after(timer, lambda: play_sound(button_name))


def button_leave(button, enter_time):

    # Function is called when the mouse cursor leaves the button.
    # It checks if there is a scheduled event and cancels it if it exists.
    # This ensures that the sound won't play if the mouse leaves the button
    # before the specified delay.
    if enter_time[0]:
        button.after_cancel(enter_time[0])

# end of audio session


def height_config(parent):

    # Getting a height usable for text area and listbox
    font_base = font_config()

    # Pt to pixels
    font = font_base.split(" ")
    font_size = int(font[1])
    font_size_in_pixels = font_size / 0.75

    # Resolution info
    parent_height = parent.winfo_screenheight()
    area_of_upper_widget = resolutionMath()[2]
    usable_height = parent_height - area_of_upper_widget

    # Calculating widget height
    number_of_lines_listbox = int((usable_height - font_size_in_pixels * 3) / font_size_in_pixels)
    number_of_lines_textarea = int((usable_height - font_size_in_pixels * 6) / font_size_in_pixels)

    return number_of_lines_listbox, number_of_lines_textarea

def get_email_sender(email_string):

    start_index = email_string.find(": ") + 2

    # Check if the string is in format: "Od: <email@seznam.cz>"
    if start_index < len(email_string) - 1 and email_string[start_index] == "<":
        end_index = email_string.find(">", start_index)
        if end_index != -1:
            email_address = email_string[start_index + 1:end_index].strip()
            sender_name = email_address.split("@")[0]
            return sender_name
    end_index = email_string.find("<")

    # Check if the string is in format: "Od: Name Surname <email@seznam.cz>"
    if start_index != -1 and end_index != -1:
        sender_name = email_string[start_index:end_index].strip()
        return sender_name

    # If the format is "Od: email@seznam.cz" , extract name differently
    else:
        tokens = email_string.split(" ")
        if len(tokens) > 1:
            extracted_name = tokens[1]
            name = extracted_name.split("@")[0]
            return name


def get_guardian_email():

    # Reading configuration
    data = load_json_file("../sconf/SMAIL_config.json")
    mail = data["guardian_email"]
    return mail

def resend_active():

    # Reading configuration
    data = load_json_file("../sconf/SMAIL_config.json")
    active = data["resend_email"]
    smail = data["credentials"]["username"]
    gmail = data["guardian_email"]
    return active ==1, smail, gmail

def get_guardian_email():

    data = load_json_file("../sconf/SMAIL_config.json")
    gmail = data["guardian_email"]
    return gmail