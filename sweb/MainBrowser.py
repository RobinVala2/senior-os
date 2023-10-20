from math import log
from PyQt5.QtWidgets import QMainWindow, QApplication, QMenu, QStyle, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtWidgets import QLineEdit, QPushButton, QAction, QToolBar,QLineEdit, QHBoxLayout, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QCursor
from urllib.parse import urlparse
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QEvent, QUrl, Qt, QTimer, QSize, pyqtSignal
import sys, os, tarfile, subprocess
import logging
from datetime import datetime
from loadConfig import *
from functools import partial
from languge_Translator import Translator
import pygame, math
from PyQt5.QtWebChannel import QWebChannel
from screeninfo import get_monitors

class MyWebEnginePage(QWebEnginePage):
    # Define a signal that will carry a URL as its argument
    urlChangedSignal = pyqtSignal(str)
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        if _type == QWebEnginePage.NavigationTypeLinkClicked:
            # This check ensures you're only modifying behavior for clicked links.
            if isMainFrame:  # you might want to navigate only if it's the main frame
                self.load(url)  # navigate to the url
                return False  # return False here to tell the view we've handled this navigation request
        return True  # return True for all other navigation requests you haven't explicitly handled
    
    def createWindow(self, _type):
        # Instead of creating a new window, navigate to the requested URL in the current window
        page = MyWebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    def on_url_changed(self, url):
        # Emit the signal with the URL
        self.urlChangedSignal.emit(url.toString())
        
class GetHeightAndWidthFromScreen:
    def __init__(self):
        template_config = load_template_config_json()
        num_of_monitor = template_config["GlobalConfiguration"]["numOfScreen"]
        padding = template_config["GUI_template"]["padx_value"]
        height_divisor = template_config["GUI_template"]["height_divisor"]
        width_divisor = template_config["GUI_template"]["width_divisor"]
        num_option_on_frame = template_config["GUI_template"]["num_of_opt_on_frame"]
        
        # Get monitor size
        # 0 = Get the first monitor
        monitor = get_monitors()[num_of_monitor]
        screen_width, screen_height = monitor.width, monitor.height
        self.button_height = screen_height / height_divisor
        
        # Number of button on menu = numberOfOptions + 1
        total_padding = (num_option_on_frame+1)*padding
        # Calculate width for button
        self.button_width = math.floor((screen_width-total_padding)/width_divisor) - padding
    
    def GetHeightButton(self):
        return self.button_height
    
    def GetWidthButton(self):
        return self.button_width

# Call class URL Logger for logging Phishing url to file
# Cisco log: seq no:timestamp: %facility-severity-MNEMONIC:description
class URLLogger:
    def __init__(self, log_file="logPhishing.txt"):
        self.log_file = log_file
        # Ensure the name for log file
        # If the name of file does not exist, create the new file
        # Sequence number initialization
        self.seq_no = 0
        # Ensure that the file is exist
        self._init_txt()

    # Method for creating and opening file .txt
    def _init_txt(self):
        try:
            # Read file with file name
            with open(self.log_file, 'r') as f:
                f.readline()
        except FileNotFoundError:
            # If file does not exist, show use w to create new and write parameter
            with open(self.log_file, 'w') as f:
                f.write("Logging phishing URL from Browser\n")
                
    # Show the the block message to window
    def log_blocked_url(self, url, facility, severity, mnemonic, description):
        logging.warning(f'Blocked URL accessed: {url}. This URL is Phishing')
        self.log_to_txt(url, facility, severity, mnemonic, description)

    # When the URL is blocked from log_blocked_url, save to file .txt
    def log_to_txt(self, url, facility, severity, mnemonic, description):
        self.seq_no += 1
        # Set current time 
        current_time = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        # seq no:timestamp: %facility-severity-MNEMONIC:description
        log_entry = f"{self.seq_no}\t{current_time}\t{facility}-{severity}-{mnemonic}\t{description}-{url}\n"
        # Write to exising file txt
        with open(self.log_file, 'a') as f:
            f.write(log_entry)
        
# Class for blocking Phishing URL. Using tarfile to extract from file .tar.gz
# Go through all domain in the file
# If the domain is match, take a blocking
class URLBlocker:
    def __init__(self, paths_to_db):
        self.blocked_urls = set()
        # Load file from file path
        for filepath in paths_to_db:
            self.load_urls_from_tar_gz(filepath)
        
    # Read all member in that Domain file
    def load_urls_from_tar_gz(self,path):
        with tarfile.open(path, "r:gz") as tar:
            for member in tar.getmembers():
                # Real all member from the file until the file is None
                url_file = tar.extractfile(member)
                if url_file is not None:
                    content  = url_file.read().decode('utf-8')
                    urls = content.strip().split('\n')
                    self.blocked_urls.update(urls)

    # Control that if the url is Block
    def is_url_blocked(self, url):
        return url in self.blocked_urls

# My main browser contains all GUI in this class (Toolbar, Buttons, URLbar)
class MyBrowser(QMainWindow):
    # Define the contructor for initialization 
    def __init__(self,config_data,my_config_data):
        super(MyBrowser,self).__init__()
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.lang_translator = Translator()
        self.get_height_and_width = GetHeightAndWidthFromScreen()
        #page = MyWebEnginePage(self.browser)
        #page.urlChangedSignal.connect(self.navigate_to_url)
        #self.browser.setPage(page)
        
        # Initialization pygame mixer 
        pygame.mixer.init()
        # Sound control attribute
        self.sound_for_button = None
        
        # Disable all native parameter for Tooltip to set my own type
        QApplication.setEffectEnabled(Qt.UI_FadeTooltip, False)
        QApplication.setEffectEnabled(Qt.UI_AnimateTooltip, False)
        
        # Define the Home Page for the Web Browser
        # !!! using .html but still don't have good Home Page
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'homepage.html')
        self.browser.setUrl(QUrl.fromLocalFile(html_path))
        
        # Get parameter from file sconf/TEMPLATE.json
        font_family_info = config_data["GlobalConfiguration"]["fontFamily"]
        font_size_info = config_data["GlobalConfiguration"]["fontSize"]
        font_weight_info = config_data["GlobalConfiguration"]["fontThickness"]
        self.button_value_padd_info = config_data["GUI_template"]["padx_value"]
        self.time_hover_button = config_data["GlobalConfiguration"]["soundDelay"] * 1000
        
        # Get height and width from class GetHeightAndWidthInfo
        self.buttons_width_info = self.get_height_and_width.GetWidthButton()
        self.buttons_height_info = self.get_height_and_width.GetHeightButton()
        
        # Get my parametr from file
        color_info_menu = my_config_data["colors_info"]["menu_frame"]
        color_info_app = my_config_data["colors_info"]["app_frame"]
        color_info_button_unselected = my_config_data["colors_info"]["buttons_unselected"]
        color_info_button_selected = my_config_data["colors_info"]["buttons_selected"]
        self.buttons_icon_width_info = my_config_data["sweb_buttons_add_info"]["sweb_button_icon_width"]
        self.buttons_icon_height_info = my_config_data["sweb_buttons_add_info"]["sweb_button_icon_height"]
        
        # Get path for images
        self.path_to_image_https = my_config_data["image"]["sweb_image_https"]
        self.path_to_image_http = my_config_data["image"]["sweb_image_http"]
        self.path_to_image_exit = my_config_data["image"]["sweb_image_exit"]
        self.path_to_image_translate = my_config_data["image"]["sweb_image_translate"]
        self.path_to_image_www2 = my_config_data["image"]["sweb_image_www2"]
        self.path_to_image_www3 = my_config_data["image"]["sweb_image_www3"]
        self.path_to_image_www4 = my_config_data["image"]["sweb_image_www4"]
        self.path_to_image_www5 = my_config_data["image"]["sweb_image_www5"]
        self.path_to_image_www6 = my_config_data["image"]["sweb_image_www6"]
        self.path_to_image_menu = my_config_data["image"]["sweb_image_menu"]

        # Function for URL bar
        self.browser.urlChanged.connect(self.update_url)
        self.browser.titleChanged.connect(self.update_title)
        
        # Create toolbar for saving URL
        self.url_toolbar = QToolBar("URL Navigation")
        self.addToolBar(self.url_toolbar)
        self.addToolBarBreak()
        
        # Create a toolbar for saving menu and buttons
        self.buttons_toolbar = QToolBar("Buttons Navigation")
        self.addToolBar(self.buttons_toolbar)
        
        # Set a style for button toolbar
        self.buttons_toolbar.setStyleSheet(f"""
             QToolBar {{
                background-color: {color_info_menu};
            }}
            
            /* Changes parameters for button in Toolbar*/
            QPushButton {{
                border: 1px solid black;
                background-color: {color_info_button_unselected};                  
                font-size: {font_size_info}px;
                font-weight: {font_weight_info};
                font-family: {font_family_info};
                width: {self.buttons_width_info}px;
                height: {self.buttons_height_info}px;
                margin-right: {self.button_value_padd_info}px;
            }}
            
            QPushButton:hover {{
                background-color: {color_info_button_selected}; 
            }}
            
            QPushButton QLabel {{
                font-size: {font_size_info}px;
                font-weight: {font_weight_info};
                font-family: {font_family_info};
            }}
        """)
        # Set parameter to save Text label of buttons when change language
        self.menu1_text_label = "Menu 1"
        self.menu1Exit_text_label = "Exit"
        self.menu1WWW1_text_label = "WWW 1"
        self.menu1WWW2_text_label = "WWW 2"
        self.menu1WWW3_text_label = "WWW 3"
        self.menu2_text_label = "Menu 2"
        self.menu2WWW4_text_label = "WWW 4"
        self.menu2WWW5_text_label = "WWW 5"
        self.menu2WWW6_text_label = "WWW 6"
        self.menu2Address_text_label = "Address"
        
        # Get number of menu and number of options in the menu from sconf/config.json
        num_menu_buttons = config_data['GUI_template']['num_of_menu_buttons']
        num_of_opt_on_menu = config_data['GUI_template']['num_of_opt_on_frame']

        if num_menu_buttons == 2 and num_of_opt_on_menu == 4:
            self.setup_initial_menu_1()
        else:
            self.close()
        
        # Create a URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setAlignment(Qt.AlignCenter)
        # Change the parameter of URL bar
        self.url_bar.setStyleSheet(f"""
        QLineEdit {{
            font-family: {font_family_info};
            font-size: {font_size_info}px;
            font-weight: {font_weight_info};
            background-color: {color_info_app};         
        }}        
        """)
        self.url_bar.setClearButtonEnabled(True)
        # Load URL blocker and logger
        filepaths = ["Phishing.Database-master/ALL-phishing-domains.tar.gz","Phishing.Database-master/ALL-phishing-links.tar.gz"]
        self.url_blocker = URLBlocker(filepaths)
        self.logger = URLLogger()
        # Navitigate URL when press enter
        # When text of URL is changed, check for URL Phishing
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_bar.textChanged.connect(self.check_url)
        # Update URL address to URL bar
        self.browser.urlChanged.connect(self.update_url)
        # Green when connect with https, red for connection with http
        self.url_bar.security_icon_action = self.url_bar.addAction(QIcon(),QLineEdit.TrailingPosition)
        self.url_toolbar.addWidget(self.url_bar)
        
        # Initially make URL toolbar visible
        # This method is used for Address option -> hide and show url bar
        self.url_toolbar.setVisible(False)

        # Configure audio and for hovering buttons, menus and options
        # Run this methods for the set Current language in Translator
        self.CurrentMenu = 1
        self.update_ui_text()
        
    def setup_initial_menu_1(self):
        # Clear existing buttons
        self.buttons_toolbar.clear()
        self.CurrentMenu = 1
        # Create first Menu
        self.menu1_button = QPushButton(self)
        # Create Home QvBoxLayout
        menu1_news_layout = QVBoxLayout(self.menu1_button)
        menu1_news_icon = QIcon(self.path_to_image_menu)
        menu1_news_label = QLabel(self.menu1_button)
        menu1_news_label.setPixmap(menu1_news_icon.pixmap(QSize(int(self.buttons_width_info/2),int(self.buttons_height_info/2))))
        menu1_news_layout.addWidget(menu1_news_label)
        self.menu1_new_text_label = QLabel(self.menu1_text_label, self.menu1_button)
        menu1_news_layout.addWidget(self.menu1_new_text_label)
        # Align text and icon in the center
        menu1_news_layout.setAlignment(menu1_news_label,Qt.AlignCenter)
        menu1_news_layout.setAlignment(self.menu1_new_text_label,Qt.AlignCenter)
        # Change to hand when click cursor
        self.menu1_button.setCursor(Qt.PointingHandCursor)
        self.menu1_button.clicked.connect(self.setup_initial_menu_2)
        self.buttons_toolbar.addWidget(self.menu1_button)

        # Add Exit button
        self.menu1Exit = QPushButton(self)
        # Create Home QvBoxLayout
        menu1Exit_layout = QVBoxLayout(self.menu1Exit)
        # Set Icon for Exit
        menu1Exit_icon = QIcon(self.path_to_image_exit)
        menu1Exit_label = QLabel(self.menu1Exit)
        menu1Exit_label.setPixmap(menu1Exit_icon.pixmap(QSize(int(self.buttons_width_info/2),int(self.buttons_height_info/2))))
        menu1Exit_layout.addWidget(menu1Exit_label)
        self.menu1_new_Exit_text_label = QLabel(self.menu1Exit_text_label, self.menu1Exit)
        menu1Exit_layout.addWidget(self.menu1_new_Exit_text_label)
        # Align text and icon in the center
        menu1Exit_layout.setAlignment(menu1Exit_label,Qt.AlignCenter)
        menu1Exit_layout.setAlignment(self.menu1_new_Exit_text_label,Qt.AlignCenter)
        self.menu1Exit.clicked.connect(self.close)
        self.menu1Exit.setCursor(Qt.PointingHandCursor)
        self.buttons_toolbar.addWidget(self.menu1Exit)
        
        # Add language button
        self.translate_btn = QPushButton(self)
        translate_layout = QVBoxLayout(self.translate_btn)
        # Set icon for Language
        translate_icon = QIcon(self.path_to_image_translate)
        translate_label = QLabel(self.translate_btn)
        translate_label.setPixmap(translate_icon.pixmap(QSize(int(self.buttons_width_info/2),int(self.buttons_height_info/2))))
        translate_layout.addWidget(translate_label)
        # Text fo reload button
        translate_text_label = QLabel("EN/CZ/DE",self.translate_btn)
        translate_layout.addWidget(translate_text_label)
        # Change to hand when click cursor
        self.translate_btn.setCursor(Qt.PointingHandCursor)
        # Align text and icon in the center
        translate_layout.setAlignment(translate_label,Qt.AlignCenter)
        translate_layout.setAlignment(translate_text_label,Qt.AlignCenter)
        self.translate_btn.clicked.connect(self.toggle_language)
        self.buttons_toolbar.addWidget(self.translate_btn)
        
        # Add Menu1_WWW2 button
        self.menu1WWW2 = QPushButton(self)
        menu1WWW2_layout = QVBoxLayout(self.menu1WWW2)
        # Icon for Ceska televize
        menu1WWW2_icon = QIcon(self.path_to_image_www2)
        menu1WWW2_label = QLabel(self.menu1WWW2)
        menu1WWW2_label.setPixmap(menu1WWW2_icon.pixmap(QSize(int(self.buttons_width_info/2),int(self.buttons_height_info/2))))
        menu1WWW2_layout.addWidget(menu1WWW2_label)
        self.menu1_new_WWW2_text_label = QLabel(self.menu1WWW2_text_label, self.menu1WWW2)
        menu1WWW2_layout.addWidget(self.menu1_new_WWW2_text_label)
        # Align text and icon in the center
        menu1WWW2_layout.setAlignment(menu1WWW2_label,Qt.AlignCenter)
        menu1WWW2_layout.setAlignment(self.menu1_new_WWW2_text_label,Qt.AlignCenter)
        self.menu1WWW2.clicked.connect(self.navigate_www2)
        self.menu1WWW2.setCursor(Qt.PointingHandCursor)
        self.buttons_toolbar.addWidget(self.menu1WWW2)
        
        # Add Menu1_WWW3 button
        self.menu1WWW3 = QPushButton(self)
        menu1WWW3_layout = QVBoxLayout(self.menu1WWW3)
        # Icon for Irozhlas
        menu1WWW3_icon = QIcon(self.path_to_image_www3)
        menu1WWW3_label = QLabel(self.menu1WWW3)
        menu1WWW3_label.setPixmap(menu1WWW3_icon.pixmap(QSize(int(self.buttons_width_info/2),int(self.buttons_height_info/2))))
        menu1WWW3_layout.addWidget(menu1WWW3_label)
        self.menu1_new_WWW3_text_label = QLabel(self.menu1WWW3_text_label, self.menu1WWW3)
        menu1WWW3_layout.addWidget(self.menu1_new_WWW3_text_label)
        # Align text and icon in the center
        menu1WWW3_layout.setAlignment(menu1WWW3_label,Qt.AlignCenter)
        menu1WWW3_layout.setAlignment(self.menu1_new_WWW3_text_label,Qt.AlignCenter)
        self.menu1WWW3.clicked.connect(self.navigate_www3)
        self.menu1WWW3.setCursor(Qt.PointingHandCursor)
        self.buttons_toolbar.addWidget(self.menu1WWW3)
        
        self.update_ui_audio()
    
    def setup_initial_menu_2(self):
        # Clear existing buttons
        self.buttons_toolbar.clear()
        self.CurrentMenu = 2
        # Create second Menu
        self.menu2_button = QPushButton(self)
        # Create Home QvBoxLayout
        menu2_news_layout = QVBoxLayout(self.menu2_button)
        menu2_news_icon = QIcon(self.path_to_image_menu)
        menu2_news_label = QLabel(self.menu2_button)
        menu2_news_label.setPixmap(menu2_news_icon.pixmap(QSize(int(self.buttons_width_info/2),int(self.buttons_height_info/2))))
        menu2_news_layout.addWidget(menu2_news_label)
        self.menu2_new_text_label = QLabel(self.menu2_text_label, self.menu2_button)
        menu2_news_layout.addWidget(self.menu2_new_text_label)
        # Align text and icon in the center
        menu2_news_layout.setAlignment(menu2_news_label,Qt.AlignCenter)
        menu2_news_layout.setAlignment(self.menu2_new_text_label,Qt.AlignCenter)
        # Change to hand when click cursor
        self.menu2_button.setCursor(Qt.PointingHandCursor)
        # Show menu 1 when clicked
        self.menu2_button.clicked.connect(self.setup_initial_menu_1)
        self.buttons_toolbar.addWidget(self.menu2_button)
        
        # Add Menu2_WWW4 button
        self.menu2WWW4 = QPushButton(self)
        menu2WWW4_layout = QVBoxLayout(self.menu2WWW4)
        # Icon for idnes
        menu2WWW4_icon = QIcon(self.path_to_image_www4)
        menu2WWW4_label = QLabel(self.menu2WWW4)
        menu2WWW4_label.setPixmap(menu2WWW4_icon.pixmap(QSize(int(self.buttons_width_info/2),int(self.buttons_height_info/2))))
        menu2WWW4_layout.addWidget(menu2WWW4_label)
        self.menu2_new_WWW4_text_label = QLabel(self.menu2WWW4_text_label, self.menu2WWW4)
        menu2WWW4_layout.addWidget(self.menu2_new_WWW4_text_label)
        # Align text and icon in the center
        menu2WWW4_layout.setAlignment(menu2WWW4_label,Qt.AlignCenter)
        menu2WWW4_layout.setAlignment(self.menu2_new_WWW4_text_label,Qt.AlignCenter)
        self.menu2WWW4.clicked.connect(self.navigate_www4)
        self.menu2WWW4.setCursor(Qt.PointingHandCursor)
        self.buttons_toolbar.addWidget(self.menu2WWW4)
        
        # Add Menu2_WWW5 button
        self.menu2WWW5 = QPushButton(self)
        menu2WWW5_layout = QVBoxLayout(self.menu2WWW5)
        # Icon for aktualne.cz
        menu2WWW5_icon = QIcon(self.path_to_image_www5)
        menu2WWW5_label = QLabel(self.menu2WWW5)
        menu2WWW5_label.setPixmap(menu2WWW5_icon.pixmap(QSize(int(self.buttons_width_info/2),int(self.buttons_height_info/2))))
        menu2WWW5_layout.addWidget(menu2WWW5_label)
        self.menu2_new_WWW5_text_label = QLabel(self.menu2WWW5_text_label, self.menu2WWW5)
        menu2WWW5_layout.addWidget(self.menu2_new_WWW5_text_label)
        # Align text and icon in the center
        menu2WWW5_layout.setAlignment(menu2WWW5_label,Qt.AlignCenter)
        menu2WWW5_layout.setAlignment(self.menu2_new_WWW5_text_label,Qt.AlignCenter)
        self.menu2WWW5.clicked.connect(self.navigate_www5)
        self.menu2WWW5.setCursor(Qt.PointingHandCursor)
        self.buttons_toolbar.addWidget(self.menu2WWW5)
        
        # Add Menu2_WWW6 button
        self.menu2WWW6 = QPushButton(self)
        menu2WWW6_layout = QVBoxLayout(self.menu2WWW6)
        # Icon for denik.cz
        menu2WWW6_icon = QIcon(self.path_to_image_www6)
        menu2WWW6_label = QLabel(self.menu2WWW6)
        menu2WWW6_label.setPixmap(menu2WWW6_icon.pixmap(QSize(int(self.buttons_width_info/2),int(self.buttons_height_info/2))))
        menu2WWW6_layout.addWidget(menu2WWW6_label)
        self.menu2_new_WWW6_text_label = QLabel(self.menu2WWW6_text_label, self.menu2WWW6)
        menu2WWW6_layout.addWidget(self.menu2_new_WWW6_text_label)
        # Align text and icon in the center
        menu2WWW6_layout.setAlignment(menu2WWW6_label,Qt.AlignCenter)
        menu2WWW6_layout.setAlignment(self.menu2_new_WWW6_text_label,Qt.AlignCenter)
        self.menu2WWW6.clicked.connect(self.navigate_www6)
        self.menu2WWW6.setCursor(Qt.PointingHandCursor)
        self.buttons_toolbar.addWidget(self.menu2WWW6)
        
        # Add Menu2_Address button
        self.menu2Address = QPushButton(self)
        # Create Home QvBoxLayout
        menu2Address_layout = QVBoxLayout(self.menu2Address)
        menu2Address_icon = self.style().standardIcon(QStyle.SP_FileDialogContentsView)
        menu2Address_label = QLabel(self.menu2Address)
        menu2Address_label.setPixmap(menu2Address_icon.pixmap(QSize(int(self.buttons_width_info/2),int(self.buttons_height_info/2))))
        menu2Address_layout.addWidget(menu2Address_label)
        self.menu2_new_Address_text_label = QLabel(self.menu2Address_text_label, self.menu2Address)
        menu2Address_layout.addWidget(self.menu2_new_Address_text_label)
        # Align text and icon in the center
        menu2Address_layout.setAlignment(menu2Address_label,Qt.AlignCenter)
        menu2Address_layout.setAlignment(self.menu2_new_Address_text_label,Qt.AlignCenter)
        #self.menu1WWW2.clicked.connect(self.navigate_home)
        self.menu2Address.setCursor(Qt.PointingHandCursor)
        self.buttons_toolbar.addWidget(self.menu2Address)
        
        self.update_ui_audio()
        
    # Method for get current language and update default language in app
    # If translate button is clicked, change to other language and audio
    def toggle_language(self):
        self.lang_translator.toggle_language()
        self.update_ui_text()
        self.update_ui_audio()
    
    # Function for updating text on Browser when user clicked to button Translate
    # Default value is "en" -> "cz" -> "de"
    def update_ui_text(self):
        if self.CurrentMenu == 1:
            self.menu1_text_label = self.lang_translator.get_text("menu1")
            self.menu1_new_text_label.setText(self.menu1_text_label)
            self.menu1Exit_text_label = self.lang_translator.get_text("menu1Exit")
            self.menu1_new_Exit_text_label.setText(self.menu1Exit_text_label)
            # Menu 1 still not exist
            self.menu1WWW1_text_label = self.lang_translator.get_text("menu1WWW1")
            self.menu1WWW2_text_label = self.lang_translator.get_text("menu1WWW2")
            self.menu1_new_WWW2_text_label.setText(self.menu1WWW2_text_label)
            self.menu1WWW3_text_label = self.lang_translator.get_text("menu1WWW3")
            self.menu1_new_WWW3_text_label.setText(self.menu1WWW3_text_label)
        else:
            # Do nothing
            pass
        self.menu2_text_label = self.lang_translator.get_text("menu2")
        self.menu2WWW4_text_label = self.lang_translator.get_text("menu2WWW4")
        self.menu2WWW5_text_label = self.lang_translator.get_text("menu2WWW5")
        self.menu2WWW6_text_label = self.lang_translator.get_text("menu2WWW6")
        self.menu2Address_text_label = self.lang_translator.get_text("menu2Address")

    # Function for updating audio on Browser when user clicked to button Translate
    # Default value is "en" -> "cz" -> "de"
    def update_ui_audio(self):
        if self.CurrentMenu == 1:
            self.setup_hover_sound(self.menu1_button,self.time_hover_button,self.lang_translator.get_audio("menu1"))
            self.setup_hover_sound(self.menu1Exit,self.time_hover_button,self.lang_translator.get_audio("menu1Exit"))
            self.setup_hover_sound(self.translate_btn,self.time_hover_button,self.lang_translator.get_audio("translateButton"))
            self.setup_hover_sound(self.menu1WWW2,self.time_hover_button,self.lang_translator.get_audio("menu1WWW2"))
            self.setup_hover_sound(self.menu1WWW3,self.time_hover_button,self.lang_translator.get_audio("menu1WWW3"))
        else:
            self.setup_hover_sound(self.menu2_button,self.time_hover_button,self.lang_translator.get_audio("menu2"))
            self.setup_hover_sound(self.menu2WWW4,self.time_hover_button,self.lang_translator.get_audio("menu2WWW4"))
            self.setup_hover_sound(self.menu2WWW5,self.time_hover_button,self.lang_translator.get_audio("menu2WWW5"))
            self.setup_hover_sound(self.menu2WWW6,self.time_hover_button,self.lang_translator.get_audio("menu2WWW6"))
            self.setup_hover_sound(self.menu2Address,self.time_hover_button,self.lang_translator.get_audio("menu2Address"))

    # QpushButton can be set HoverLeave and HoverEnter event with "widget"
    def setup_hover_sound(self, widget, hover_time,path_to_sound):
        # Using Qtimer to set clock
        widget.hover_timer = QTimer()
        widget.hover_timer.setInterval(hover_time)
        # Run only one times when hover
        widget.hover_timer.setSingleShot(True)
        widget.hover_timer.timeout.connect(lambda: self.play_sound_for_button(path_to_sound))
        # Install event to widget -> Event is comefrom eventFilter
        widget.installEventFilter(self)
    
    # Set event for leave and enter button -> Using only with QpushButton
    def eventFilter(self, watched, event):
        if event.type() == QEvent.HoverEnter:
            watched.hover_timer.start()
        elif event.type() == QEvent.HoverLeave:
            watched.hover_timer.stop()
            # Stop sound immediately
            self.stop_sound_for_button()
        return super().eventFilter(watched, event)
    
    # Play a sound, which is stored on SWEB_config.json
    def play_sound_for_button(self, path_to_sound):
        # Ensure the file exists before playing it
        if not os.path.exists(path_to_sound):
            print(f"Sound file not found: {path_to_sound}")
            return
        try:
            # Load and play the sound file
            self.sound_for_button = pygame.mixer.Sound(path_to_sound)
            self.sound_for_button.play()
        except Exception as exc:
            print(f"Failed to play sound: {str(exc)}")
            
    # Stop sound immediately when button is leaved hover
    def stop_sound_for_button(self):
        if self.sound_for_button:
            self.sound_for_button.stop()
            self.sound_for_button = None
        
    # This method is set for visible and invisible URL bar
    def toggle_url_toolbar(self):
        # Toggle visibility of the URL toolbar
        self.url_toolbar.setVisible(not self.url_toolbar.isVisible())

    # This method is used for navigation URL bar
    def navigate_to_url(self):
        # Get url from URL toobal
        url_in_bar = self.url_bar.text().strip()
        # Check that if URL is from URL
        if self.url_blocker.is_url_blocked(url_in_bar):
            self.show_blocked_message(url_in_bar)
            self.logger.log_blocked_url(url_in_bar,'BROWSER', 'LOG_EMERG', 'CONN', 'Phishing connection refused')
            return
        # If "." is not contained in URL
        if "." not in url_in_bar:
            url_in_bar = "https://www.google.com/search?q=" + url_in_bar
        else:
            # Top Level Domain is not available
            if not any(url_in_bar.endswith(tld) for tld in [".com", ".org", ".net", ".gor", ".cz"]):
                url_in_bar = "https://www.google.com/search?q=" + url_in_bar
        # If in URl not http or https, connect with HTTPS
        if "://" not in url_in_bar:
            url_in_bar = "https://" + url_in_bar

        self.browser.setUrl(QUrl(url_in_bar))
    
    # This method is first security in Browser
    # Check if connection is under HTTP or HTTPS
    def check_url(self,url):
        if url.startswith("https://"):
            self.url_bar.security_icon_action.setIcon(QIcon(self.path_to_image_https))
        else:
            self.url_bar.security_icon_action.setIcon(QIcon(self.path_to_image_http))
        
    # Show block message when User connect to web from Phishing list
    def show_blocked_message(self, url):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(f"Blocked Phishing URL: {url}")
        msg.setWindowTitle("Blocked URL Warning")
        msg.exec_()

    # Method for updating URL
    def update_url(self, inputURL):
        # Change text in url Bar
        self.url_bar.setText(inputURL.toString())
        self.url_bar.setCursorPosition(0)
        
    # Method for updating title
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(title)
        
    # Method for connect to the second www2 ct24.ceskatelevize.cz
    def navigate_www2(self):
        self.browser.setUrl(QUrl("https://ct24.ceskatelevize.cz"))
        
    # Method for connect to the third irozhlas.cz
    def navigate_www3(self):
        self.browser.setUrl(QUrl("https://irozhlas.cz"))

    # Method for connect to the fourth idnes.cz
    def navigate_www4(self):
        self.browser.setUrl(QUrl("https://www.idnes.cz"))

    # Method for connect to the fifth aktualne.cz
    def navigate_www5(self):
        self.browser.setUrl(QUrl("https://www.aktualne.cz"))

    # Method for connect to the sixth denik.cz
    def navigate_www6(self):
        self.browser.setUrl(QUrl("https://www.denik.cz"))
    
# Definuje funkci Main
if __name__ == "__main__":
    qApplication = QApplication(sys.argv)
    qApplication.setApplicationName("Web Browser for senior")
    sweb_config = load_sweb_config_json()
    # Nastavit styl pro vsechny ToolTip (Vymenit styl jako CSS)
    qApplication.setStyleSheet("""
    """)
    # Load config data from JSON file
    config = load_template_config_json()
    mainWindow = MyBrowser(config,sweb_config)
    mainWindow.show()
    sys.exit(qApplication.exec_())
