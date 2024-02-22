# Application for senior caregiver
- Goal of this section (sgive) is to make a fully working application, that lets senior's
 caregiver configure application specifically for seniors needs.
- Application is written in python, for FrontEnd element, I am using custimTkinter.

- There is also a UserInterface template, there are to be specific two versions.
   - Tkinter and customTkinter version.

- Next main part is about config files (json) and collection log files.
- Lastly there is ML detection, that runs as a service, it gets called once a day or week and it checks all suspicious address that other application collected.


## Caregiver Application:
- [Link to folder here](src/CaregiverApp/) <br>
- Only for caregiver, not meant for senior
- Is resizable, so caregiver can look at other stuff too, for example at config itself.
- UI is strongly influenced by my UI template, but is newer version, so it is little better. <br>
<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/CaregiverApp_GLOBAL.png" alt="App_screenshot_not_showing" style="width:50%;">


## User interface template:
[UI tkinter](src/gui_template/) <br>
[UI customTkinter](src/guiTemplateCustomTkinter/) <br>
- simple module in python, used as a tamplate for senior-os application that needs front end UI.
- its configurable through json file.
- can be edited through configuration application for caregiver.
- every element is dynamic (etc. buttons are) or its in progress to be dynamic.

<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/newGuiTemp-white.png" alt="App_screenshot_not_showing" style="width:50%;">


### TODO:
- [ ] SMAIL configuration
- [ ] SWEB configuration
- [ ] fix logs rescaling issues
- [ ] better ML dataset implementation and other ML fixes


