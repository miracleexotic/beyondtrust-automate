# Automation

- Windows App automation.
- Web App automation.

## Features
- **Windows App** example script.
    1. DBeaver
    2. sqldeveloper
    3. Studio3T
    4. ToadEdge
- **Web** - Mostly Web can manage via selenium.
---
## Prerequisite
##### Windows
- Need ***Administrator*** to run script.
- Using [Appium](https://github.com/appium/python-client) require version 1.3.0
- Using [PyAutoGUI](https://pyautogui.readthedocs.io/en/latest/) require version 0.9.53
- Using [pywin32](https://pypi.org/project/pywin32/) require version 305
- Using [selenium](https://selenium-python.readthedocs.io/index.html) require version 3.14.1
- Other **Tools**
    1. [Inspect](https://learn.microsoft.com/en-us/windows/win32/winauto/inspect-objects) - Tool for inspect elements in Windows Application.
        **Download:** [Windows SDK for Windows 11 (10.0.22621.1778) - Install SDK](https://developer.microsoft.com/en-us/windows/downloads/sdk-archive/)
        **Path:** C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\inspect.exe
    2. [WinAppDriver](https://github.com/microsoft/WinAppDriver) - Tool for run Application Driver.
        **Download:** [ WindowsApplicationDriver_1.2.1.msi ](https://github.com/Microsoft/WinAppDriver/releases)
        **Path:** C:\Program Files (x86)\Windows Application Driver\WinAppDriver.exe
##### Web
- Using [selenium](https://selenium-python.readthedocs.io/index.html) require version 4.5.0
- Using [webdriver-manager](https://pypi.org/project/webdriver-manager/) require version 3.8.5

## Installation

Automation requires [Python3](https://www.python.org/downloads/) v3.9.x to run.
Install the dependencies and devDependencies.
#### Git clone
```sh
git clone https://github.com/miracleexotic/beyondtrust-automate.git
```
#### Python package
**Note:** Selenium is not use in the same version. if you need to run both environments you need to use virtual environment such as [venv](https://docs.python.org/3/library/venv.html) or [conda](https://docs.conda.io/en/latest/) etc.
- Windows Application
```sh
pip install -r beyondtrust-automate\win\requirements-win.txt
```
- Web Application
```sh
pip install -r beyondtrust-automate\win\requirements-web.txt
```


## License

MIT

**Free Software, Hell Yeah!**
