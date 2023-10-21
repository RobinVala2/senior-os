from loadConfig import *

class Translator:
    def __init__(self):
        self.langConfigDB = load_sweb_config_json()
        self.language_keys = ["cz","en","de"]
        self.current_language = self.langConfigDB["language"]["default_language"]
        # Set current language is CZ =0 , EN = 1, DE = 2
        if(self.current_language) == "cz":
            self.current_language_index = 0
        elif self.current_language == "en":
            self.current_language_index = 1
        else:
            self.current_language_index = 2

    def toggle_language(self):
        # Increase the index to change the language
        self.current_language_index += 1
        # If we reached the end of the list, go back
        if self.current_language_index >= len(self.language_keys):
            self.current_language_index = 0
        # Change current language after this function called
        self.current_language = self.language_keys[self.current_language_index]

    # Get text from .json acroding Key value
    def get_text(self, nameButton):
        key = f"sweb_{self.current_language}_{nameButton}"
        return self.langConfigDB["text"].get(key, f"No translation found for {key}")
    
    # Get audio from .json acroding Key value
    def get_audio(self, nameButton):
        key = f"sweb_{self.current_language}_{nameButton}"
        return self.langConfigDB["audio"].get(key, f"No translation found for {key}")

    # Get state of current language
    def get_current_language(self):
        return self.language_keys[self.current_language_index]