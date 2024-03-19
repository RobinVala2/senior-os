# Application for senior caregiver
- Goal of this section (sgive) is to make a fully working application, that lets senior's
 caregiver configure application specifically for seniors needs.
- Application is written in python, for FrontEnd element of the caregiver app I am using custimTkinter.

- There is also a UserInterface template, Currently it has two versions.
   - Tkinter app is less modular, but little bit more responsive.
   - CustomTkinter on the other hand is more modular, has more UI elements and is resizable.

- More background work is about generating, reading and correctly editing .json configuration files for each application (SGIVE, SWEB, SMAIL, GLOBAL)
- Lastly, there is some implementation of Machine Learning, ML has three datasets. On first start, all three models and vectorizers gets trained, but for detection is used only that model, that corespond to current language in global config.

## How to install:
> TODO:

## Caregiver Application:
- [Link to folder here](src/CaregiverApp/) <br>
- Only for caregiver, not meant for senior
- Is resizable, so caregiver can look at other stuff too, for example at config itself.
- UI is strongly influenced by my UI template, but is newer version, so it is little better. <br>
<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/CaregiverApp_GLOBAL.png" alt="App_screenshot_not_showing" style="width:50%;"></br>
> will add more screenshots


## User interface template:
[Both versions are here](src/gui_template/) <br>
- simple module in python, used as a tamplate for senior-os application that needs front end UI.
- its configurable through json file.
- can be edited through configuration application for caregiver.
- every element is dynamic (etc. buttons are) or its in progress to be dynamic.

<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/newGuiTemp-white.png" alt="App_screenshot_not_showing" style="width:50%;"></br>

> will add more screenshots



### TODO:
- [ ] SWEB configuration
- [ ] Optimalization
- [ ] Testing


