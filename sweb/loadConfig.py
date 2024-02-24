import json

# Load file json for inputing language text and audio of web browser
def load_sweb_config_json():
    # Exit when error occurs and print notification to log
    try:
        with open("../sconf/SWEB_config.json", "r",encoding='utf-8') as open_file:
            language_database = json.load(open_file)
        open_file.close()
        return language_database
    except FileNotFoundError:
        print(f"Configuration file not found /sconf/SWEB_config.json")
    except json.JSONDecodeError:
        print(f"Error parsing JSON file: /sconf/SWEB_config.json")
        
# Load Template config
def load_template_config_json():
    # Exit when error occurs and print notification to log
    try:
        with open("../sconf/TEMPLATE.json", "r",encoding='utf-8') as open_file:
            config_data = json.load(open_file)
        open_file.close()
        return config_data
    except FileNotFoundError:
        print(f"Configuration file not found /sconf/TEMPLATE.json")
    except json.JSONDecodeError:
        print(f"Error parsing JSON file: /sconf/TEMPLATE.json")

def load_config_in_same_directory(file_name):
    # Exit when error occurs and print notification to log
    try:
        with open(file_name, 'r',encoding='utf-8') as open_file:
            data = json.load(open_file)
        open_file.close
        return data
    except FileNotFoundError:
        print(f"Configuration file not found: {file_name}")
    except json.JSONDecodeError:
        print(f"Error parsing JSON file: {file_name}")
        
def load_permitted_website_from_sgive():
    permitted_website_list = set()
    # Exit when error occurs and print notification to log
    try:
        with open("../sgive/SWEB_Permitted_Websites.txt", 'r') as open_file:
            content  = open_file.read()
            reading_website = content.strip().split('\n')
            permitted_website_list.update(reading_website)
        open_file.close
        return permitted_website_list
    except FileNotFoundError:
        print(f"Configuration file not found: {open_file}")