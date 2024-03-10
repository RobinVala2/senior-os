# Web browser for seniors

## Application Overview
This application is a senior-friendly web browser using PyQt5, focusing on accessibility, ease of use, and security. His mission is to make more  accessible place for seniors, with enhanced text readability, intuitive navigation, , audio, multi-language support and security features to protect against phishing website.
Here's the design concept for web browser:
- Menu 1
![SWEB_MENU_1](https://github.com/forsenior/senior-os/blob/main/sweb/screens/SWEB_MENU_1.png)
- Menu 2
![SWEB_MENU_2](https://github.com/forsenior/senior-os/blob/main/sweb/screens/SWEB_MENU_2.png)
- Warning when connect to phishing webpage these are installed from phishing database
![SWEB_MENU_ALERT](https://github.com/forsenior/senior-os/blob/main/sweb/screens/SWEB_MENU_ALERT.png)

## Our Design
- We believe the Internet should be accessible to everyone, regardless of age. Our browser empowers seniors with user-friendly tools, making the online world an enjoyable space to explore.
- Věříme, že by Internet měl být přístupný všem bez ohledu na věk. Náš prohlížeč poskytuje seniorům uživatelské přívětivé nástroje, díky nimž je online svět příjemným prostorem k objevování.
- Wir glauben, dass das Internet für jeden zugänglich sein sollte, unabhängig vom Alter. Unser Browser stellt Senioren benutzerfreundliche Tools zur Verfügung und macht die Online-Welt zu einem angenehmen Ort zum Erkunden.

### Key Features
- Clear and Large Buttons: Easy navigation with large for essential functions.
- Readable Text: Enhanced text size not only in the buttons but also in the content of webpage.
- Audible support: Sound support for button interactions whenever users hover on the buttons longer than 5s.
- Support multiple languages: Available in English, Czech, and Deutsch.
- Security Against Phishing Webpage: Identify and alert users about potential phishing websites.
- Activity Logging: Logs browsing activity to a text file for security purposes.

### Installation
!!!Ensure you have Python3 or pip installed on your system.
Follow these steps to set up Web Browser in FEDORA operating system:
```bash
# Clone the project repository
git clone https://github.com/forsenior/senior-os

# Navigate to the project directory
cd sweb

# Install required Python packages with dnf if using Fedora
sudo dnf install python3
sudo dnf install python3-qt5
sudo dnf install python3-qt5-webengine
sudo dnf install python3-pygame
pip3 install screeninfo
pip3 install yagmail

# Run the browser
python3 sweb.py
```

Follow these steps to set up Web Browser in WINDOWS operating system:
```bash
# Clone the project repository
git clone https://github.com/forsenior/senior-os

# Navigate to the project directory
cd sweb

# Install required Python packages in command prompt
pip install PyQt5
pip install PyQtWebEngine
pip install screeninfo
pip install PyQt5Designer
pip install pygame
pip install requests
pip install yagmail

# Run the browser from terminal
python sweb.py [Your visited website]
```

### Usage
Upon launching the browser, you are greeted with an intuitive interface designed for ease of use. Enjoy a safer browsing experience.

### Contributing
FACULTY OF ELECTRICAL ENGINEERING AND COMMUNICATION
![SWEB_FEKT](https://github.com/forsenior/senior-os/blob/main/sconf/images/SWEB_FEKT_VUT_LOGO.jpg)
