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
- **Requirements:** Linux distro (better with Gnome or KDE plasma), Tkinter (``pacman -S tk`` for example)
- clone the repo:``git clone git@github.com:RYUseless/senior-os.git``.
- cd into `senior-os/sgive/`
- run command: `sh CaregiverApplication.sh` or you can don: `sudo chmod +x CaregiverApplication.sh  && ./CaregiverApplication.sh`
> Application should start after installing all dependecies and configuring venv (if started for the first time)


## Caregiver Application:
- [Link to folder here](src/CaregiverApp/) <br>
- Only for caregiver, not meant for senior
- Is resizable, so caregiver can look at other stuff too, for example at config itself.
- UI is strongly influenced by my UI template, but is newer version, so it is little better. <br>
<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/CaregiverApp_GLOBAL.png" alt="App_screenshot_not_showing" style="width:50%;"></br>
<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/CaregiverApp_SMAIL.png" alt="App_screenshot_not_showing" style="width:50%;"></br>
<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/CaregiverApp_SWEB.png" alt="App_screenshot_not_showing" style="width:50%;"></br>
<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/CaregiverApp_LOGS.png" alt="App_screenshot_not_showing" style="width:50%;"></br>

- Application can be resized to its 70% size (% value may change).</br>
<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/CaregiverApp_resize_event.png" alt="App_screenshot_not_showing" style="width:50%;"></br>

- Application was tested personally on this HW.
- Screens:
    + 1920x1080, 27inch, 100% scaling
    + 1920x1080, +-30inch, 100% scaling
    + 2560x1440, 13inch, 200% scaling
    + 3840x2160, 13inch, 300% scaling
- OS:
    + Arch linux, Gnome 46.0, 6.6.23-1-lts
    + EnedeavourOS, KDE 6.0, 6.6.23-1-lts
 
 - Testing HW by other testers:
    + Yet to come sadly.
 
 - Known issues:
    + some visual bugs when resizing window.
    + Shinanigans with indexing primary monitor by zero and not the most left one by layout (more like linux issue tho)



## User interface template:
[Both versions are here](src/gui_template/) <br>
- simple module in python, used as a tamplate for senior-os application that needs front end UI.
- its configurable through json file.
- can be edited through configuration application for caregiver.
- every element is dynamic (etc. buttons are) or its in progress to be dynamic.

<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/newGuiTemp-white.png" alt="App_screenshot_not_showing" style="width:50%;"></br>
<img src="https://github.com/RYUseless/senior-os/blob/dev/sgive/screenshots/newGuiTemp-black.png" alt="App_screenshot_not_showing" style="width:50%;"></br>

## How to use:
> TODO:

### TODO:
- [ ] Optimalization
- [ ] Testing


