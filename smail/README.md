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
This program has been tested and optimized for use with Python versions 3.11 and 3.12. 

## Configuration requirement for Email Client
Before initiating the email client, it is essential to generate configuration files utilizing the SGIVE app. 
This process entails inserting an email address and password, ensuring seamless functionality.

### Password generation for Email Client
To connect to your Gmail account from a non-web environment, such as an SMAIL app, you'll need to generate an app password. 
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

4. Ensure that all necessary dependencies are installed ([Installation](##installation)).

5. Before executing the application, ensure that you have set up the necessary configurations and generated the required app password for connection, as outlined in the [previous section](##configuration-requirement-for-email-client).

6. Once everything is set up, run the application by clicking on the "Run" or "Play" button within your IDE.

It's important to note that for optimal functionality, it is recommended to run the application using an Integrated Development Environment (IDE) such as PyCharm rather than executing it directly through the command line. This ensures that all dependencies are properly managed and that the application environment is correctly configured.
