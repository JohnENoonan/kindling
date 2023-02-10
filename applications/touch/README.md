# Kindling Interactive App
The TouchDesigner implementation of the interactive experience

## Installation

### Touchdesigner
* [Install Touchdesigner 2022.31030](https://derivative.ca/release/202231030/67006)
* Apply a license

### Python
Make sure to have a python installation on the machine. Run `pip install pyqrcode` and then set *Edit->Preferences* "External Python to Search Path" to `C:/**python_version_path**/Lib/site-packages`.

### Audio
TODO

### Configuration

#### Environment
Environment variables are set in the file `.env` at the repo's root. To create this file run:
```bash
cd etc
python mergeEnvFile.py
```

## Startup

### Production
TODO

#### Startup Task
Using the [task scheduler](https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page):
1. create a task named `kindling-startup`
	* optimized for Windows 10
	* trigger set to log on of any user with a 3 min delay
	* the action set to Start a Program, and run the script `[ repo ]\applications\touch\etc\startup-apps.bat`. 
	* For conditions, uncheck the box for needing AC power, and Settings uncheck the box for Stop the task if it runs longer than X. The rest of the defaults are correct. 
2. Create a task named `kindling-reboot`
	* optimized for Windows 10, 
	* trigger set to on a schedule set to Daily at 2:00:00 AM
	* set the action set to Start a Program, and run the script `[ repo ]\applications\touch\etc\reboot.bat.`
	* For conditions, uncheck the box for needing AC power, and Settings uncheck the box for Stop the task if it runs longer than X. The rest of the defaults are correct.

### Development
To start in development you can just launch the touchdesigner file `kindling-viz.toe`.

## Closing The App
TODO

## Hotkeys
During development there are several hot keys 

| Keys                     | Effect                                     |
|--------------------------|--------------------------------------------|
| **ctrl+alt+d**           | toggle the perform mode debug window       |
