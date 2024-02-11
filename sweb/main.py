# Frameworks from PyQt5 libraries
from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QLabel, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QToolBar, QWidget, QAction
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QEvent, QUrl, Qt, QTimer, QSize, pyqtSignal
from PyQt5.QtGui import QIcon
# Library for parsing URL value
from urllib.parse import urlparse
# Library for getting information about user's monitor
from screeninfo import get_monitors
# Created own class for logging and blocking phishing URL
from antiPhishing.URLBlocker import URLBlocker
from antiPhishing.URLLogger import URLLogger
from antiPhishing.UpdatePhishingTXT import PhishingDatabaseModificationChecker
from loadConfig import *
# Own class for translating
from languge_Translator import Translator
import pygame, math
import sys, os

class MyWebEnginePage(QWebEnginePage):
    # Define a signal that will carry a URL as its argument
    urlChangedSignal = pyqtSignal(QUrl)

    def __init__(self, parent=None):
        super().__init__(parent)
        
    def acceptNavigationRequest(self, url, _type, isMainFrame):
        # Ensure only modifying behavior for clicked links
        if _type == QWebEnginePage.NavigationTypeLinkClicked and isMainFrame:
            # Navigate to the url
            self.urlChangedSignal.emit(url)
            # Tell the view that handled this navigation request
            return False
        # Return True for all other navigation requests
        return True

    def createWindow(self, _type):
        # Create a new instance of MyWebEnginePage for the new window request
        new_page = MyWebEnginePage(self)
        new_page.urlChangedSignal.connect(self.urlChangedSignal.emit)
        return new_page
    
class GetMonitorHeightAndWidth:
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
        total_padding = (num_option_on_frame)*padding
        # Calculate width for button
        self.button_width = math.floor((screen_width-total_padding)/width_divisor) - padding*(3/4)
    
    def get_height_button(self):
        return self.button_height
    
    def get_width_button(self):
        return self.button_width

# My main browser contains all GUI in this class (Toolbar, Buttons, URLbar)
class MyBrowser(QMainWindow):
    # Define the contructor for initialization 
    def __init__(self,template_config_data,my_config_data):
        super(MyBrowser,self).__init__()
        # Set window flags to customize window behavior
        # Remove standard window controls
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.main_browser = QWebEngineView()
        # Set cutstom page to open new page in the same browser
        self.my_custom_page = MyWebEnginePage(self.main_browser)
        self.my_custom_page.urlChangedSignal.connect(self.on_url_changed_my_custom_page)
        # Add my custom page to browser
        self.main_browser.setPage(self.my_custom_page)
        self.setCentralWidget(self.main_browser)
        # Default page is configured as seznam.cz
        # Check if input URL is contained HTTP or HTTPS
        if input_url_from_terminal.startswith("https") or input_url_from_terminal.startswith("http"):
            self.main_browser.setUrl(QUrl(input_url_from_terminal))
        else:
            self.main_browser.setUrl(QUrl("http://" + input_url_from_terminal)) 
        self.language_translator = Translator()
        self.get_monitor_height_and_width = GetMonitorHeightAndWidth()

        # Load URL blocker and logger
        path_to_phishing_database = my_config_data["phishing_database"]["path"]
        self.url_blocker = URLBlocker(path_to_phishing_database)
        self.url_logger = URLLogger()
        
        # Check if phishing database is up to date
        phishing_database_check_update = PhishingDatabaseModificationChecker(my_config_data,self.url_logger)
        phishing_database_check_update.check_and_update_if_needed()
        
        # Initialization pygame mixer  for play sounds
        pygame.mixer.init()
        # Sound control attribute
        self.sound_mixer_control_for_button = None
        
        self.path_to_alert_phishing_music = my_config_data["audio"]["sweb_cz_alert_phishing"]
        self.path_to_url_music = my_config_data["audio"]["sweb_cz_url"]
        
        # Get parameter from file sconf/TEMPLATE.json
        self.font_family_info = template_config_data["GlobalConfiguration"]["fontFamily"]
        self.font_size_info = template_config_data["GlobalConfiguration"]["fontSize"]
        self.font_weight_info = template_config_data["GlobalConfiguration"]["fontThickness"]
        self.button_value_padd_info = template_config_data["GUI_template"]["padx_value"]
        self.time_hover_button = template_config_data["GlobalConfiguration"]["soundDelay"] * 1000
        
        # Get height and width from class GetHeightAndWidthInfo
        self.buttons_width_info = self.get_monitor_height_and_width.get_width_button()
        self.buttons_height_info = self.get_monitor_height_and_width.get_height_button()
        
        # Get my parametr from file
        self.color_info_menu = my_config_data["colors_info"]["menu_frame"]
        self.color_info_app = my_config_data["colors_info"]["app_frame"]
        self.color_info_button_unselected = my_config_data["colors_info"]["buttons_unselected"]
        self.color_info_button_selected = my_config_data["colors_info"]["buttons_selected"]
        
        # Get path for images
        self.path_to_image_exit = my_config_data["image"]["sweb_image_exit"]
        self.path_to_image_www1 = my_config_data["image"]["sweb_image_www1"]
        self.path_to_image_www2 = my_config_data["image"]["sweb_image_www2"]
        self.path_to_image_www3 = my_config_data["image"]["sweb_image_www3"]
        self.path_to_image_www4 = my_config_data["image"]["sweb_image_www4"]
        self.path_to_image_www5 = my_config_data["image"]["sweb_image_www5"]
        
        # Create a toolbar for saving menu and buttons
        self.menu_1_toolbar = QToolBar("Menu 1")
        self.addToolBar(self.menu_1_toolbar)
        self.menu_1_toolbar.setMovable(False)
        
        # Create a toolbar for saving menu and buttons
        self.menu_2_toolbar = QToolBar("Menu 2")
        self.addToolBar(self.menu_2_toolbar)
        self.menu_2_toolbar.setMovable(False)
        
        self.addToolBarBreak()
        
        self.toolbar_space = QToolBar("Spacer")
        # Set the spacer height
        self.toolbar_space.setFixedHeight(int(self.buttons_height_info))
        self.toolbar_space.setStyleSheet(f"""
        QToolBar {{
                background-color: #fff;
        }}
        """)
        self.addToolBar(self.toolbar_space)
        self.toolbar_space.setMovable(False)
        self.toolbar_space.setVisible(False)
        self.addToolBarBreak()
        
        # Set a style for Menu 1 toolbar
        self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
        
        # Set a style for Menu 1 toolbar
        self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
        
        # Get number of menu and number of options in the menu from sconf/config.json
        num_menu_buttons = template_config_data['GUI_template']['num_of_menu_buttons']
        num_of_opt_on_menu = template_config_data['GUI_template']['num_of_opt_on_frame']

        if num_menu_buttons == 2 and num_of_opt_on_menu == 4:
            self.setup_initial_menu_1()
            self.setup_initial_menu_2()
        else:
            self.close()
            
        # Set disvisible for menu 2
        self.menu_2_toolbar.setVisible(False)
        
        # Create toolbar for saving URL
        self.url_toolbar = QToolBar("URL Navigation")
        self.addToolBar(self.url_toolbar)
        self.url_toolbar.setMovable(False)
        
        # Create a URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setAlignment(Qt.AlignCenter)
        # Change the parameter of URL bar
        self.url_bar.setStyleSheet(f"""
        QToolBar {{
                background-color: {self.color_info_menu};
        }}
        QLineEdit {{
            border: 2px solid black;
            height: {self.buttons_height_info}px;
            font-family: {self.font_family_info};
            font-size: {int(self.buttons_height_info/3)}px;
            font-weight: {self.font_weight_info};
            background-color: {self.color_info_app};         
        }}        
        """)
        
        # When text of URL is changed, check for URL Phishing
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_toolbar.addWidget(self.url_bar)
        
        # Initially make URL toolbar visible
        # This method is used for Address option -> hide and show url bar
        self.url_toolbar.setVisible(False)
        
        # Configure audio and for hovering buttons, menus and options
        # Run this methods for the set Current language in Translator
        self.update_ui_text()
        self.update_ui_audio()
        self.main_browser.urlChanged.connect(self.security_against_phishing)
        # Apply changing text after finishing load
        #self.main_browser.loadFinished.connect(self.finished_load_web_page)
    
    def on_url_changed_my_custom_page(self, url):
        # Load the new URL in the existing browser window
        self.main_browser.setUrl(url)
        
    def setup_initial_menu_1(self):
        # Create first Menu
        self.menu1_button = QPushButton(self)
        # Create Menu QvBoxLayout
        menu1_news_layout = QVBoxLayout(self.menu1_button)
        self.menu1_new_text_label = QLabel("Menu 1", self.menu1_button)
        menu1_news_layout.addWidget(self.menu1_new_text_label)
        # Align text in the center
        menu1_news_layout.setAlignment(self.menu1_new_text_label,Qt.AlignCenter)
        # Change to hand when click cursor
        self.menu1_button.setCursor(Qt.PointingHandCursor)
        self.menu1_button.clicked.connect(self.toggle_between_toolbar)
        self.menu_1_toolbar.addWidget(self.menu1_button)
        
        # Add a bliak space between two button
        spacer1 = QWidget()
        spacer1.setFixedWidth(self.button_value_padd_info)
        self.menu_1_toolbar.addWidget(spacer1)

        # Add Exit button
        self.menu1Exit = QPushButton(self)
        # Create Home QvBoxLayout
        menu1Exit_layout = QVBoxLayout(self.menu1Exit)
        # Set Icon for Exit
        menu1Exit_icon = QIcon(self.path_to_image_exit)
        menu1Exit_label = QLabel(self.menu1Exit)
        menu1Exit_label.setPixmap(menu1Exit_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1Exit_layout.addWidget(menu1Exit_label)
        # Align text and icon in the center
        menu1Exit_layout.setAlignment(menu1Exit_label,Qt.AlignCenter)
        self.menu1Exit.clicked.connect(self.close)
        self.menu1Exit.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1Exit)
        
        # Add a bliak space between two button
        spacer2 = QWidget()
        spacer2.setFixedWidth(self.button_value_padd_info)
        self.menu_1_toolbar.addWidget(spacer2)
        
        # Add back button
        self.back_btn = QPushButton(self)
        back_layout = QVBoxLayout(self.back_btn)
        # Set icon for Language
        back_icon = self.style().standardIcon(QStyle.SP_ArrowBack)
        back_label = QLabel(self.back_btn)
        back_label.setPixmap(back_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        back_layout.addWidget(back_label)
        # Change to hand when click cursor
        self.back_btn.setCursor(Qt.PointingHandCursor)
        # Align text and icon in the center
        back_layout.setAlignment(back_label,Qt.AlignCenter)
        self.back_btn.clicked.connect(self.main_browser.back)
        self.menu_1_toolbar.addWidget(self.back_btn)
        
         # Add a blank space between two button
        spacer3 = QWidget()
        spacer3.setFixedWidth(self.button_value_padd_info)
        self.menu_1_toolbar.addWidget(spacer3)
        
        # Add Menu1_WWW1 button
        self.menu1WWW1 = QPushButton(self)
        menu1WWW1_layout = QVBoxLayout(self.menu1WWW1)
        # Icon for Ceska televize
        menu1WWW1_icon = QIcon(self.path_to_image_www1)
        menu1WWW1_label = QLabel(self.menu1WWW1)
        menu1WWW1_label.setPixmap(menu1WWW1_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1WWW1_layout.addWidget(menu1WWW1_label)
        # Align icon in the center
        menu1WWW1_layout.setAlignment(menu1WWW1_label,Qt.AlignCenter)
        self.menu1WWW1.clicked.connect(self.navigate_www1)
        self.menu1WWW1.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1WWW1)
        
        # Add a blank space between two button
        spacer4 = QWidget()
        spacer4.setFixedWidth(self.button_value_padd_info)
        self.menu_1_toolbar.addWidget(spacer4)
        
        # Add Menu1_WWW2 button
        self.menu1WWW2 = QPushButton(self)
        menu1WWW2_layout = QVBoxLayout(self.menu1WWW2)
        # Icon for Irozhlas
        menu1WWW2_icon = QIcon(self.path_to_image_www2)
        menu1WWW2_label = QLabel(self.menu1WWW2)
        menu1WWW2_label.setPixmap(menu1WWW2_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu1WWW2_layout.addWidget(menu1WWW2_label)
        # Align icon in the center
        menu1WWW2_layout.setAlignment(menu1WWW2_label,Qt.AlignCenter)
        self.menu1WWW2.clicked.connect(self.navigate_www2)
        self.menu1WWW2.setCursor(Qt.PointingHandCursor)
        self.menu_1_toolbar.addWidget(self.menu1WWW2)
    
    def setup_initial_menu_2(self):
        # Create second Menu
        self.menu2_button = QPushButton(self)
        # Create Home QvBoxLayout
        menu2_news_layout = QVBoxLayout(self.menu2_button)
        self.menu2_new_text_label = QLabel("Menu 2", self.menu2_button)
        menu2_news_layout.addWidget(self.menu2_new_text_label)
        # Align text and icon in the center
        menu2_news_layout.setAlignment(self.menu2_new_text_label,Qt.AlignCenter)
        # Change to hand when click cursor
        self.menu2_button.setCursor(Qt.PointingHandCursor)
        # Show menu 1 when clicked
        self.menu2_button.clicked.connect(self.toggle_between_toolbar)
        self.menu_2_toolbar.addWidget(self.menu2_button)
        
        # Add a bliak space between two button
        spacer5 = QWidget()
        spacer5.setFixedWidth(self.button_value_padd_info)
        self.menu_2_toolbar.addWidget(spacer5)
        
        # Add Menu2_WWW3 button
        self.menu2WWW3 = QPushButton(self)
        menu2WWW3_layout = QVBoxLayout(self.menu2WWW3)
        # Icon for idnes
        menu2WWW3_icon = QIcon(self.path_to_image_www3)
        menu2WWW3_label = QLabel(self.menu2WWW3)
        menu2WWW3_label.setPixmap(menu2WWW3_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu2WWW3_layout.addWidget(menu2WWW3_label)
        # Align text and icon in the center
        menu2WWW3_layout.setAlignment(menu2WWW3_label,Qt.AlignCenter)
        self.menu2WWW3.clicked.connect(self.navigate_www3)
        self.menu2WWW3.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW3)
        
        # Add a bliak space between two button
        spacer6 = QWidget()
        spacer6.setFixedWidth(self.button_value_padd_info)
        self.menu_2_toolbar.addWidget(spacer6)
        
        # Add Menu2_WWW4 button
        self.menu2WWW4 = QPushButton(self)
        menu2WWW4_layout = QVBoxLayout(self.menu2WWW4)
        # Icon for aktualne.cz
        menu2WWW4_icon = QIcon(self.path_to_image_www4)
        menu2WWW4_label = QLabel(self.menu2WWW4)
        menu2WWW4_label.setPixmap(menu2WWW4_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu2WWW4_layout.addWidget(menu2WWW4_label)
        # Align text and icon in the center
        menu2WWW4_layout.setAlignment(menu2WWW4_label,Qt.AlignCenter)
        self.menu2WWW4.clicked.connect(self.navigate_www4)
        self.menu2WWW4.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW4)
        
        # Add a bliak space between two button
        spacer7 = QWidget()
        spacer7.setFixedWidth(self.button_value_padd_info)
        self.menu_2_toolbar.addWidget(spacer7)
        
        # Add Menu2_WWW5 button
        self.menu2WWW5 = QPushButton(self)
        menu2WWW5_layout = QVBoxLayout(self.menu2WWW5)
        # Icon for denik.cz
        menu2WWW5_icon = QIcon(self.path_to_image_www5)
        menu2WWW5_label = QLabel(self.menu2WWW5)
        menu2WWW5_label.setPixmap(menu2WWW5_icon.pixmap(QSize(int(self.buttons_width_info/(1.5)),int(self.buttons_height_info/(1.5)))))
        menu2WWW5_layout.addWidget(menu2WWW5_label)
        # Align text and icon in the center
        menu2WWW5_layout.setAlignment(menu2WWW5_label,Qt.AlignCenter)
        self.menu2WWW5.clicked.connect(self.navigate_www5)
        self.menu2WWW5.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2WWW5)
        
        # Add a bliak space between two button
        spacer8 = QWidget()
        spacer8.setFixedWidth(self.button_value_padd_info)
        self.menu_2_toolbar.addWidget(spacer8)
        
        # Add Menu2_Address button
        self.menu2Address = QPushButton(self)
        # Create Home QvBoxLayout
        menu2Address_layout = QVBoxLayout(self.menu2Address)
        self.menu2_addres_new_text_label = QLabel("Page out of list", self.menu2_button)
        self.menu2_addres_new_text_label.setWordWrap(True)
        self.menu2_addres_new_text_label.setAlignment(Qt.AlignCenter)
        menu2Address_layout.addWidget(self.menu2_addres_new_text_label)
        # Align text and icon in the center
        menu2Address_layout.setAlignment(self.menu2_addres_new_text_label,Qt.AlignCenter)
        self.menu2Address.clicked.connect(self.toggle_url_toolbar)
        self.menu2Address.setCursor(Qt.PointingHandCursor)
        self.menu_2_toolbar.addWidget(self.menu2Address)
        
    
    # Set default style for Toolbar
    def default_style_toolbar(self):
        style_string = f"""
             QToolBar {{
                background-color: {self.color_info_menu};
            }}
            
            /* Changes parameters for button in Toolbar*/
            QPushButton {{
                border: 1px solid black;
                background-color: {self.color_info_button_unselected};                   
                font-size: {self.font_size_info}px;
                font-weight: {self.font_weight_info};
                font-family: {self.font_family_info};
                width: {self.buttons_width_info}px;
                height: {self.buttons_height_info}px;
            }}
            
            QPushButton:hover {{
                background-color: {self.color_info_button_selected}; 
            }}
            
            QPushButton QLabel {{
                font-size: {self.font_size_info}px;
                font-weight: {self.font_weight_info};
                font-family: {self.font_family_info};
            }}
        """
        
        return style_string
    
    # Set default style for Toolbar
    def phishing_style_toolbar(self):
        alert_style_string = f"""
             QToolBar {{
                background-color: {self.color_info_menu};
            }}
            
            /* Changes parameters for button in Toolbar*/
            QPushButton {{
                border: 1px solid black;
                background-color: red;                   
                font-size: {self.font_size_info}px;
                font-weight: {self.font_weight_info};
                font-family: {self.font_family_info};
                width: {self.buttons_width_info}px;
                height: {self.buttons_height_info}px;
            }}
            
            QPushButton:hover {{
                background-color: {self.color_info_button_selected}; 
            }}
            
            QPushButton QLabel {{
                font-size: {self.font_size_info}px;
                font-weight: {self.font_weight_info};
                font-family: {self.font_family_info};
            }}
        """
        
        return alert_style_string
    
    def finished_load_web_page(self):
        # Get url value from browser
        url_in_browser_value = self.main_browser.url()
        if True:
            # If it is home, do not change anything
            if "homepage.html" != url_in_browser_value.toString():
                self.main_browser.setZoomFactor(1.5)
                # Wait 1 second for loading, after 1 second, connect to change web content (HTML injection)
                QTimer.singleShot(1000, lambda: self.html_injection_to_web_content())
            else:
                return
    
    # This method is used for changing font in HTML content
    def html_injection_to_web_content(self):
        injection_javasript = """
        <!-- Change only paragraph, article, span and header elements with lower levels--> 
        var changed_tag = ['p', 'div', 'article', 'span', 'h3', 'h4', 'h5'];
        <!-- Create a function to change content style-->
        var change_content_style = function(element) {
            if (element.children.length === 0) {
                element.style.fontSize = '23px';
                element.style.lineHeight = '1.2';
                element.style.fontFamily = 'Arial';
            }
            Array.from(element.children).forEach(change_content_style);
        }
        <!-- Call created function with input html content-->
        change_content_style(document.body);
        """
        self.main_browser.page().runJavaScript(injection_javasript)
    
    # Show full screen without Minimizing or Moving
    def show_app_fullscreen(self):
        self.showFullScreen()
        
    # Method use for disable menu when click to another menu
    def toggle_between_toolbar(self):
        # Toggle visibility of toolbars
        if self.menu_1_toolbar.isVisible():
            self.menu_1_toolbar.setVisible(False)
            self.menu_2_toolbar.setVisible(True)
        else:
            self.menu_2_toolbar.setVisible(False)
            self.menu_1_toolbar.setVisible(True)
        
    # Method for get current language and update default language in app
    # If translate button is clicked, change to other language and audio
    def toggle_supported_language(self):
        self.language_translator.toggle_supported_language()
        self.update_ui_text()
        self.update_ui_audio()
    
    # Function for updating text on Browser when user clicked to button Translate
    # Default value is "cz" -> "en" -> "de"
    def update_ui_text(self):
            self.menu1_new_text_label.setText(self.language_translator.get_translated_text("menu1"))
            self.menu2_new_text_label.setText(self.language_translator.get_translated_text("menu2"))
            self.menu2_addres_new_text_label.setText(self.language_translator.get_translated_text("menu2Address"))

    # Function for updating audio on Browser when user clicked to button Translate
    # Default value is "cz" -> "en" -> "de"
    def update_ui_audio(self):
            self.setup_hover_sound_value(self.menu1_button,self.time_hover_button,self.language_translator.get_translated_audio("menu1"))
            self.setup_hover_sound_value(self.menu1Exit,self.time_hover_button,self.language_translator.get_translated_audio("menu1Exit"))
            self.setup_hover_sound_value(self.back_btn,self.time_hover_button,self.language_translator.get_translated_audio("menu1Back"))
            self.setup_hover_sound_value(self.menu1WWW1,self.time_hover_button,self.language_translator.get_translated_audio("menu1WWW1"))
            self.setup_hover_sound_value(self.menu1WWW2,self.time_hover_button,self.language_translator.get_translated_audio("menu1WWW2"))
            self.setup_hover_sound_value(self.menu2_button,self.time_hover_button,self.language_translator.get_translated_audio("menu2"))
            self.setup_hover_sound_value(self.menu2WWW3,self.time_hover_button,self.language_translator.get_translated_audio("menu2WWW3"))
            self.setup_hover_sound_value(self.menu2WWW4,self.time_hover_button,self.language_translator.get_translated_audio("menu2WWW4"))
            self.setup_hover_sound_value(self.menu2WWW5,self.time_hover_button,self.language_translator.get_translated_audio("menu2WWW5"))
            self.setup_hover_sound_value(self.menu2Address,self.time_hover_button,self.language_translator.get_translated_audio("menu2Address"))
            self.path_to_alert_phishing_music = self.language_translator.get_translated_audio("alert_phishing")
            self.path_to_url_music = self.language_translator.get_translated_audio("url")

    # QpushButton can be set HoverLeave and HoverEnter event with "widget"
    # Play sound when usesr hovers on button longer than 5 seconds
    def setup_hover_sound_value(self, input_widget, hover_time,path_to_sound):
        # Using Qtimer to set clock
        input_widget.hover_timer = QTimer()
        input_widget.hover_timer.setInterval(hover_time)
        # Run only one times when hover
        input_widget.hover_timer.setSingleShot(True)
        input_widget.hover_timer.timeout.connect(lambda: self.play_sound_for_button(path_to_sound))
        # Install event to widget -> Event is comefrom eventFilter
        input_widget.installEventFilter(self)
    
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
            self.sound_mixer_control_for_button = pygame.mixer.Sound(path_to_sound)
            self.sound_mixer_control_for_button.play()
        except Exception as exc:
            print(f"Failed to play sound: {str(exc)}")
            
    # Stop sound immediately when button is leaved hover
    def stop_sound_for_button(self):
        if self.sound_mixer_control_for_button:
            self.sound_mixer_control_for_button.stop()
            self.sound_mixer_control_for_button = None
        
    # This method is set for visible and invisible URL bar
    def toggle_url_toolbar(self):
        # Toggle visibility of the URL toolbar
        self.play_sound_for_button(self.path_to_url_music)
        self.main_browser.setUrl(QUrl("about:blank"))
        self.url_toolbar.setVisible(not self.url_toolbar.isVisible())
        self.toolbar_space.setVisible(not self.toolbar_space.isVisible())

    # This method is used for navigation URL bar
    def navigate_to_url(self):
        # Get url from URL toobal
        url_in_bar_value = self.url_bar.text().strip()
        #If "." is not contained in URL
        if "." not in url_in_bar_value:
            url_in_bar_value = "https://www.google.com/search?q=" + url_in_bar_value
        # If in URl not http or https, connect with HTTPS
        if "://" not in url_in_bar_value:
            url_in_bar_value = "https://" + url_in_bar_value
        
        # Set default style for toolbar
        self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
        self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
          
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
        # Set url bar as clean
        self.url_bar.clear()
        # Connect to URL after entering
        self.main_browser.setUrl(QUrl(url_in_bar_value))
    
    # Method for security against phishing    
    def security_against_phishing(self,qurl):
        # Get url from QURL
        url_in_browser_value = qurl.toString()
        if url_in_browser_value.endswith('/'):
            if self.url_blocker.is_url_blocked(url_in_browser_value):
                self.play_sound_for_button(self.path_to_alert_phishing_music)
                 # Log with level 5 when connected to phishing
                self.url_logger.log_blocked_url('WEBBROWSER', 5, 'main <security>', f'Connection to Phishing server {url_in_browser_value}')
                    
                # Set red colour for connect to phishing
                self.menu_1_toolbar.setStyleSheet(self.phishing_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.phishing_style_toolbar())
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
            else:
                # Set default style for toolbar
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                # Log with LEVEL 6 INFORMATIONAL
                self.url_logger.log_blocked_url('WEBBROWSER', 6, 'main <security>', f'Connection to {url_in_browser_value}')
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
        elif not url_in_browser_value.endswith('/'):
            if "about:blank" in url_in_browser_value:
                return
            elif "google.com" in url_in_browser_value:
                    self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                    self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                    # Log with level 6 INFORMATIONAL
                    self.url_logger.log_blocked_url('WEBBROWSER', 6, 'main <security>', f'Connection to {url_in_browser_value}')
                    # Connect to URL after entering
                    self.main_browser.setUrl(QUrl(url_in_browser_value))
            elif self.url_blocker.is_url_blocked(url_in_browser_value):
                self.play_sound_for_button(self.path_to_alert_phishing_music)
                # Log with level 5 when connected to phishing
                self.url_logger.log_blocked_url('WEBBROWSER', 5, 'main <security>', f'Connection to Phishing server {url_in_browser_value}')
                    
                # Set red colour for connect to phishing
                self.menu_1_toolbar.setStyleSheet(self.phishing_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.phishing_style_toolbar())
                # Connect to URL after entering
                self.main_browser.setUrl(QUrl(url_in_browser_value))
        else:
            self.main_browser.setUrl(QUrl(url_in_browser_value))
            self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
            self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
            #self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
            # Log with LEVEL 6 INFORMATIONAL
            #self.logger.log_blocked_url('WEBBROWSER', 6, 'main <security>', f'Connection to {url_in_browser_value}')
            # Connect to URL after entering
            #self.browser.setUrl(QUrl(url_in_browser_value))
        self.finished_load_web_page()
        
        
    # Method for connect to the second www2 ct24.ceskatelevize.cz
    def navigate_www1(self):
        self.main_browser.setUrl(QUrl("https://edition.cnn.com"))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
        
    # Method for connect to the irozhlas.cz
    def navigate_www2(self):
        self.main_browser.setUrl(QUrl("https://irozhlas.cz"))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)

    # Method for connect to the idnes.cz
    def navigate_www3(self):
        # Define the Home Page for the Web Browser
        # !!! using .html but still don't have good Home Page
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'homepage.html')
        self.main_browser.load(QUrl.fromLocalFile(html_path))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
        self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
        self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())

    # Method for connect to the aktualne.cz
    def navigate_www4(self):
        self.main_browser.setUrl(QUrl("https://www.aktualne.cz"))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)

    # Method for connect to the denik.cz
    def navigate_www5(self):
        self.main_browser.setUrl(QUrl("https://www.denik.cz"))
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        self.toolbar_space.setVisible(False)
    
# Define main function to call application
if __name__ == "__main__":
    try:
        qApplication = QApplication(sys.argv)
        # If browser is opened in command terminal
        input_url_from_terminal = sys.argv[1] if len(sys.argv) > 1 else "https://seznam.cz"
        # Load config data from JSON file
        sweb_config = load_sweb_config_json()
        template_config = load_template_config_json()
        main_window = MyBrowser(template_config,sweb_config) # Set parametr for main browser window
        main_window.show_app_fullscreen() # Call main browser window
        sys.exit(qApplication.exec_())
    except Exception as excep:
        url_logger = URLLogger()
        # Log with level 2 - CRITICAL
        url_logger.log_blocked_url('WEBBROWSER', 2, 'main <security>', f'Application did not work')
        # Exit with an error code
        sys.exit(1)
