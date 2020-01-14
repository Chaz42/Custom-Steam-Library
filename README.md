# Custom Steam Library

A custom tool to edit certain features of the new Steam Library UI
Note that Exiting steam and restarting will reset the Library UI back to default
Future feature will auto detect Steam launching & update the UI

## Features
- Remove cartridge tilt on hover
- Custom cartridge tilt on hover
- Custom cartridge zoom level on hover
- Remove cartridge shine
- Round cartridge corners
- Custom cartridge hover contrast, brightness, & saturation
- Custom date last played label colors

## Todo
- [ ] Detect steam launch or library file change & update the library UI
- [ ] Add config file to save/ load user settings
- [ ] Add logging
- [ ] Add example comparison pictures for each option (Could do this with pages containing pics for each)
- [ ] Utilize tkinter grid & not pack

- Can non hovered cartridges be darkened?
- Can 'Whats new' be removed?
- Can Recent friend activity be rounded?
- Can friends playing portraits be moved? (Or fix Z level) https://i.imgur.com/SSpxmxi.png
- Can Info box on hover be resized, rounded, removed, or timing changed?


## Configuration
- config.json file is located in ~\AppData\Roaming\Custom-Steam-Library
- Default config gets created on app startup if no config file already exists

## Building
1.) Ensure pyinstaller is installed:
```
pyinstaller --version
```
2.) Run the following command in the main directory:
```
pyinstaller --noconsole --onefile ConfigTool.py
```
3.) Locate ConfigTool.exe in the \dist\ folder
