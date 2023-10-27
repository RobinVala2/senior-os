from PyQt5.QtWidgets import QMainWindow, QApplication, QStyle, QLabel, QVBoxLayout, QMessageBox
from PyQt5.QtWidgets import QLineEdit, QPushButton, QToolBar,QLineEdit, QWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QCursor
from urllib.parse import urlparse
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QEvent, QUrl, Qt, QTimer, QSize, pyqtSignal
import sys, os, tarfile, subprocess
from antiPhishing.URLBlocker import URLBlocker
from antiPhishing.URLLogger import URLLogger
from antiPhishing.UpdatePhishingTXT import TXTFileModificationChecker
from loadConfig import *
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
        self.url_bar_height = screen_height - self.button_height
        self.url_bar_width = screen_width/2
        # Number of button on menu = numberOfOptions + 1
        total_padding = (num_option_on_frame)*padding
        # Calculate width for button
        self.button_width = math.floor((screen_width-total_padding)/width_divisor) - padding*(3/4)
    
    def get_height_button(self):
        return self.button_height
    
    def get_width_button(self):
        return self.button_width
    
    def get_url_bar_height(self):
        return self.url_bar_height
    
    def get_url_bar_width(self):
        return self.url_bar_width

# My main browser contains all GUI in this class (Toolbar, Buttons, URLbar)
class MyBrowser(QMainWindow):
    # Define the contructor for initialization 
    def __init__(self,config_data,my_config_data):
        super(MyBrowser,self).__init__()
        # Set window flags to customize window behavior
        # Remove standard window controls
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.lang_translator = Translator()
        self.get_height_and_width = GetHeightAndWidthFromScreen()
        #page = MyWebEnginePage(self.browser)
        #page.urlChangedSignal.connect(self.navigate_to_url)
        #self.browser.setPage(page)
        
        #settings = self.browser.settings()
        #settings.setFontSize(QWebEngineSettings.DefaultFontSize, 50) 

        # Load URL blocker and logger
        file_to_phishing = my_config_data["phishing_database"]["path"]
        self.url_blocker = URLBlocker(file_to_phishing)
        self.logger = URLLogger()
        
        # Check if SWEB_PHISH_1.txt is up to date
        phishing_checker = TXTFileModificationChecker(my_config_data,self.logger)
        phishing_checker.check_and_update_if_needed()
        
        # Initialization pygame mixer 
        pygame.mixer.init()
        # Sound control attribute
        self.sound_for_button = None
        
        self.path_to_alert_phishing_music = my_config_data["audio"]["sweb_cz_alert_phishing"]
        self.path_to_url_music = my_config_data["audio"]["sweb_cz_url"]
        
        # Get parameter from file sconf/TEMPLATE.json
        self.font_family_info = config_data["GlobalConfiguration"]["fontFamily"]
        self.font_size_info = config_data["GlobalConfiguration"]["fontSize"]
        self.font_weight_info = config_data["GlobalConfiguration"]["fontThickness"]
        self.button_value_padd_info = config_data["GUI_template"]["padx_value"]
        self.time_hover_button = config_data["GlobalConfiguration"]["soundDelay"] * 1000
        
        # Get height and width from class GetHeightAndWidthInfo
        self.buttons_width_info = self.get_height_and_width.get_width_button()
        self.buttons_height_info = self.get_height_and_width.get_height_button()
        self.url_bar_height_info = self.get_height_and_width.get_url_bar_height()
        self.url_bar_width_info = self.get_height_and_width.get_url_bar_width()
        
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
        
        # Set a style for Menu 1 toolbar
        self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
        
        # Set a style for Menu 1 toolbar
        self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
        
        # Get number of menu and number of options in the menu from sconf/config.json
        num_menu_buttons = config_data['GUI_template']['num_of_menu_buttons']
        num_of_opt_on_menu = config_data['GUI_template']['num_of_opt_on_frame']

        if num_menu_buttons == 2 and num_of_opt_on_menu == 4:
            self.setup_initial_menu_1()
            self.setup_initial_menu_2()
        else:
            self.close()
            
        # Set disvisible for menu 2
        self.menu_2_toolbar.setVisible(False)
        
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create another flexible spacer widget
        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create toolbar for saving URL
        self.url_toolbar = QToolBar("URL Navigation")
        self.addToolBar(self.url_toolbar)
        self.url_toolbar.setMovable(False)
        
        
        self.url_toolbar.addWidget(left_spacer)
        # Create a URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setAlignment(Qt.AlignCenter)
        # Change the parameter of URL bar
        self.url_bar.setStyleSheet(f"""
        QToolBar {{
                background-color: {self.color_info_menu};
        }}
        QLineEdit {{
            width: {self.url_bar_width_info}px;
            height: {self.url_bar_height_info}px;
            font-family: {self.font_family_info};
            font-size: {int(self.buttons_height_info/3)}px;
            font-weight: {self.font_weight_info};
            background-color: {self.color_info_app};         
        }}        
        """)
        
        # When text of URL is changed, check for URL Phishing
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.url_toolbar.addWidget(self.url_bar)
        self.url_toolbar.addWidget(right_spacer)
        
        # Initially make URL toolbar visible
        # This method is used for Address option -> hide and show url bar
        self.url_toolbar.setVisible(False)
        
        # Configure audio and for hovering buttons, menus and options
        # Run this methods for the set Current language in Translator
        self.update_ui_text()
        self.update_ui_audio()
        self.browser.setUrl(QUrl("https://edition.cnn.com"))
        self.browser.urlChanged.connect(self.security_again_phishing)
        self.browser.loadFinished.connect(self.onLoadFinished)
        
    def onLoadFinished(self, success):
        url_in_browser = self.browser.url()
        print()
        if success:
            if "homepage" not in url_in_browser.toString():
                self.browser.setZoomFactor(1.5)
            else:
                return
        
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
        self.menu1_button.clicked.connect(self.toggle_toolbar)
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
        self.back_btn.clicked.connect(self.browser.back)
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
        self.menu2_button.clicked.connect(self.toggle_toolbar)
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
        self.menu2_addres_new_text_label = QLabel("Address", self.menu2_button)
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
        
    # Show full screen without Minimizing or Moving
    def show_app_fullscreen(self):
        self.showFullScreen()
        
    # Method use for disable menu when click to another menu
    def toggle_toolbar(self):
        # Toggle visibility of toolbars
        if self.menu_1_toolbar.isVisible():
            self.menu_1_toolbar.setVisible(False)
            self.menu_2_toolbar.setVisible(True)
        else:
            self.menu_2_toolbar.setVisible(False)
            self.menu_1_toolbar.setVisible(True)
        
    # Method for get current language and update default language in app
    # If translate button is clicked, change to other language and audio
    def toggle_language(self):
        self.lang_translator.toggle_language()
        self.update_ui_text()
        self.update_ui_audio()
    
    # Function for updating text on Browser when user clicked to button Translate
    # Default value is "cz" -> "en" -> "de"
    def update_ui_text(self):
            self.menu1_new_text_label.setText(self.lang_translator.get_text("menu1"))
            self.menu2_new_text_label.setText(self.lang_translator.get_text("menu2"))
            self.menu2_addres_new_text_label.setText(self.lang_translator.get_text("menu2Address"))

    # Function for updating audio on Browser when user clicked to button Translate
    # Default value is "cz" -> "en" -> "de"
    def update_ui_audio(self):
            self.setup_hover_sound(self.menu1_button,self.time_hover_button,self.lang_translator.get_audio("menu1"))
            self.setup_hover_sound(self.menu1Exit,self.time_hover_button,self.lang_translator.get_audio("menu1Exit"))
            self.setup_hover_sound(self.back_btn,self.time_hover_button,self.lang_translator.get_audio("menu1Back"))
            self.setup_hover_sound(self.menu1WWW1,self.time_hover_button,self.lang_translator.get_audio("menu1WWW1"))
            self.setup_hover_sound(self.menu1WWW2,self.time_hover_button,self.lang_translator.get_audio("menu1WWW2"))
            self.setup_hover_sound(self.menu2_button,self.time_hover_button,self.lang_translator.get_audio("menu2"))
            self.setup_hover_sound(self.menu2WWW3,self.time_hover_button,self.lang_translator.get_audio("menu2WWW3"))
            self.setup_hover_sound(self.menu2WWW4,self.time_hover_button,self.lang_translator.get_audio("menu2WWW4"))
            self.setup_hover_sound(self.menu2WWW5,self.time_hover_button,self.lang_translator.get_audio("menu2WWW5"))
            self.setup_hover_sound(self.menu2Address,self.time_hover_button,self.lang_translator.get_audio("menu2Address"))
            self.path_to_alert_phishing_music = self.lang_translator.get_audio("alert_phishing")
            self.path_to_url_music = self.lang_translator.get_audio("url")

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
        self.play_sound_for_button(self.path_to_url_music)
        self.browser.setUrl(QUrl("about:blank"))
        self.url_toolbar.setVisible(not self.url_toolbar.isVisible())

    # This method is used for navigation URL bar
    def navigate_to_url(self):
        # Get url from URL toobal
        url_in_bar = self.url_bar.text().strip()
        #If "." is not contained in URL
        if "." not in url_in_bar:
            url_in_bar = "https://www.google.com/search?q=" + url_in_bar
        # If in URl not http or https, connect with HTTPS
        if "://" not in url_in_bar:
            url_in_bar = "https://" + url_in_bar
        
        # Set default style for toolbar
        self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
        self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
          
        # Set visible after navitigation
        self.url_toolbar.setVisible(False)
        # Set url bar as clean
        self.url_bar.clear()
        # Connect to URL after entering
        self.browser.setUrl(QUrl(url_in_bar))
        
    def security_again_phishing(self,qurl):
        # Get url from QURL
        url_in_browser = qurl.toString()
        if not url_in_browser.endswith('/'):
            #url_in_browser = url_in_browser[:-1]
            if "about:blank" in url_in_browser:
                return
            elif "google.com" not in url_in_browser:
                # Check that if URL is from URL
                if self.url_blocker.is_url_blocked(url_in_browser):
                    self.show_blocked_message(url_in_browser)
                    # Log with level 5 when connected to phishing
                    self.logger.log_blocked_url('WEBBROWSER', 5, 'main <security>', f'Connection to Phishing server {url_in_browser}')
                    
                    # Set red colour for connect to phishing
                    self.menu_1_toolbar.setStyleSheet(self.phishing_style_toolbar())
                    self.menu_2_toolbar.setStyleSheet(self.phishing_style_toolbar())
                    
                    # Set visible after navitigation
                    self.url_toolbar.setVisible(False)
                    # Set url bar as clean
                    self.url_bar.clear()
                    # Connect to URL after entering
                    self.browser.setUrl(QUrl(url_in_browser))
                else:
                    self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                    self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                    # Log with level 6 INFORMATIONAL
                    self.logger.log_blocked_url('WEBBROWSER', 6, 'main <security>', f'Connection to {url_in_browser}')
                    # Connect to URL after entering
                    self.browser.setUrl(QUrl(url_in_browser))
            else:
                self.menu_1_toolbar.setStyleSheet(self.default_style_toolbar())
                self.menu_2_toolbar.setStyleSheet(self.default_style_toolbar())
                # Log with LEVEL 6 INFORMATIONAL
                self.logger.log_blocked_url('WEBBROWSER', 6, 'main <security>', f'Connection to {url_in_browser}')
                # Connect to URL after entering
                self.browser.setUrl(QUrl(url_in_browser))
        else:
            return
        
    # Show block message when User connect to web from Phishing list
    def show_blocked_message(self, url):
        #msg = QMessageBox()
        #msg.setIcon(QMessageBox.Warning)
        #msg.setText(f"Blocked Phishing URL: {url}")
        #msg.setWindowTitle("Blocked URL Warning")
        #msg.exec_()
        self.play_sound_for_button(self.path_to_alert_phishing_music)
        
    # Method for updating title
    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle(title)
        
    # Method for connect to the second www2 ct24.ceskatelevize.cz
    def navigate_www1(self):
        self.browser.setUrl(QUrl("https://ct24.ceskatelevize.cz"))
        
    # Method for connect to the irozhlas.cz
    def navigate_www2(self):
        self.browser.setUrl(QUrl("https://irozhlas.cz"))

    # Method for connect to the idnes.cz
    def navigate_www3(self):
        # Define the Home Page for the Web Browser
        # !!! using .html but still don't have good Home Page
        html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'homepage.html')
        self.browser.load(QUrl.fromLocalFile(html_path))

    # Method for connect to the aktualne.cz
    def navigate_www4(self):
        self.browser.setUrl(QUrl("https://www.aktualne.cz"))

    # Method for connect to the denik.cz
    def navigate_www5(self):
        self.browser.setUrl(QUrl("https://www.denik.cz"))
    
# Definuje funkci Main
if __name__ == "__main__":
    try:
        qApplication = QApplication(sys.argv)
        # Load config data from JSON file
        sweb_config = load_sweb_config_json()
        config = load_template_config_json()
        mainWindow = MyBrowser(config,sweb_config)
        mainWindow.show_app_fullscreen()
        sys.exit(qApplication.exec_())
    except Exception as exp:
        # Load URL blocker and logger
        sweb_config = load_sweb_config_json()
        file_to_phishing = sweb_config["phishing_database"]["path"]
        url_blocker = URLBlocker(file_to_phishing)
        logger = URLLogger()
        # Log with level 2
        logger.log_blocked_url('WEBBROWSER', 2, 'main <security>', f'Application did not work')
        # Exit with an error code
        sys.exit(1)
