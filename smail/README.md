# SMAIL - Email client for late elderly users

This email client is adapted for seniors in the age group of 90 years and more. 
The developed email client is easy to use and contains only features that a senior may need. 
The implemented audio assistance allows seniors to navigate the application space more easily. 
Additionally, a security measure was implemented to alert the senior when they receive an email message with a link to
a fraudulent site.

## Environment for reading email messages
![menu1](https://github.com/forsenior/senior-os/blob/main/smail/screens/smail_reading_email_menu_1.png)

![menu2](https://github.com/forsenior/senior-os/blob/main/smail/screens/smail_reading_email_menu_2.png)

## Environment for writing email messages
![person](https://github.com/forsenior/senior-os/blob/main/smail/screens/smail_writing_email.png)

![custom](https://github.com/forsenior/senior-os/blob/main/smail/screens/smail_custom_writing_email.png)

## Warning when reading phishing email
![phishing](https://github.com/forsenior/senior-os/blob/main/smail/screens/smail_phishing_email.png)

## Installation
```bash
# Clone project repository
git clone https://github.com/forsenior/senior-os

cd smail

# Install requirements from the requirements.txt file
pip install -r requirements.txt
```
This program has been tested and optimized for use with Python versions 3.11 and 3.12, and is intended only for Linux distributions.
It is also required to have the **wget**
 tool installed to ensure full functionality.
## Configuration requirement for SMAIL
To ensure proper functioning of the SMAIL email client, it is crucial to first generate configuration files. This can be done either by utilizing the SGIVE app or by launching the SMAIL application. While there is an option to use default settings with a preset email, it is highly recommended that you enter your own email address and password during this process. 
### Password generation for SMAIL
To connect to your Gmail account from a non-web environment, such as SMAIL app, you'll need to generate an app password. 
Follow these steps to obtain the app password:
1. Go to the Google account settings by visiting *Google Account*.

2. Navigate to the "Security" tab.

3. Under the "Signing in to Google" section, locate and select "Two-step verification".

4. After authenticating your identity, scroll down to the "App passwords" section.

5. Choose the option to generate a new app password.

6. Select the app or device for which you're generating the password.

7. Follow the prompts to generate the app password.

8. Copy the generated app password and use it in the SGIVE app to connect your email client to your Gmail account securely.

## Starting the SMAIL

To launch the application, follow these steps:

1. Open your preferred IDE such as PyCharm or any other suitable development environment.

2. Navigate to the smail directory

3. Open the smail_app.py file of the application.

4. Ensure that all necessary dependencies are installed ([Installation](#installation)).

5. Before executing the application, ensure that you have set up the necessary configurations and generated the required app password for connection, as outlined in the [previous section](#configuration-requirement-for-email-client).

6. Once everything is set up, run the application by clicking on the "Run" button within your IDE or execute the following commands:

```bash
cd smail
python smail_app.py
```

