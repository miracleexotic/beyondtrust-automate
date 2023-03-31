import sys, os, multiprocessing, urllib3
from time import sleep
from appium import webdriver
from selenium.webdriver import ActionChains
import pyautogui


class DevMode:

    DEVMODE_ON = ("reg", "add", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock", "/t", "REG_DWORD", "/f", "/v", "AllowDevelopmentWithoutDevLicense", "/d", "1")
    DEVMODE_OFF = ("reg", "add", "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock", "/t", "REG_DWORD", "/f", "/v", "AllowDevelopmentWithoutDevLicense", "/d", "0")

    def __init__(self, debug=False) -> None:
        self.debug = debug
        self._is_admin = False

    @property
    def is_admin(self):
        return self._is_admin

    def isUserAdmin(self):
        self._os_name = os.name

        if self._os_name == 'nt':
            import ctypes
            # WARNING: requires Windows XP SP2 or higher!
            try:
                self._is_admin = ctypes.windll.shell32.IsUserAnAdmin()
            except Exception as e:
                print("Error [DevMode]:", e)
                print("\t- Admin check failed, assuming not an admin.")
            
        elif self._os_name == 'posix':
            # Check for root on Posix
            return os.getuid() == 0
        
        else:
            raise RuntimeError(f"Unsupported operating system for this module: {self._os_name}")
        
        return self._is_admin

    def runAsAdmin(self, cmdLine=None, wait=True):
        self._os_name = os.name

        if self._os_name != 'nt':
            raise RuntimeError("This function is only implemented on Windows.")

        import win32con, win32event, win32process
        from win32com.shell.shell import ShellExecuteEx
        from win32com.shell import shellcon

        python_exe = sys.executable

        if cmdLine is None:
            cmdLine = [python_exe] + sys.argv

        elif not (isinstance(cmdLine, tuple) or 
                  isinstance(cmdLine, list)):
            raise ValueError("cmdLine is not a sequence.")
        
        cmd = f'"{cmdLine[0]}"'
        params = " ".join([f'"{x}"' for x in cmdLine[1:]])
        cmdDir = ''
        showCmd = win32con.SW_HIDE
        lpVerb = 'runas'  # causes UAC elevation prompt.

        procInfo = ShellExecuteEx(nShow=showCmd,
                                fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                lpVerb=lpVerb,
                                lpDirectory=cmdDir,
                                lpFile=cmd,
                                lpParameters=params)
        if self.debug: print("\t-", procInfo)

        if wait:
            procHandle = procInfo['hProcess']    
            obj = win32event.WaitForSingleObject(procHandle, win32event.INFINITE)
            rc = win32process.GetExitCodeProcess(procHandle)
            if self.debug: print("\t- Process handle %s returned code %s" % (procHandle, rc))
        else:
            rc = None

        return rc

    @staticmethod
    def ON():
        print("Developer Mode: ON")
        return DevMode().runAsAdmin(DevMode.DEVMODE_ON)
    
    @staticmethod
    def OFF():
        print("Developer Mode: OFF")
        return DevMode().runAsAdmin(DevMode.DEVMODE_OFF)
    
    def __enter__(self):
        print("Running with Enable Developer Mode...")
        if self.isUserAdmin():
            self.runAsAdmin(DevMode.DEVMODE_ON)
        else:
            print("\t- Not Admin user: access is denied.")
        
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.isUserAdmin():
            self.runAsAdmin(DevMode.DEVMODE_OFF)

class WinAppDriver:

    def __init__(self, debug=False) -> None:
        self.debug = debug
        self._stop = multiprocessing.Event()

    def _run(self, event):

        import win32con, win32process
        from win32com.shell.shell import ShellExecuteEx
        from win32com.shell import shellcon

        cmd = '"WinAppDriver.exe"'
        cmdDir = r'C:\Program Files\Windows Application Driver'
        showCmd = win32con.SW_HIDE

        if self.debug: print("Start process [WinAppDriver]:", end=" ")
        try:
            procInfo = ShellExecuteEx(nShow=showCmd,
                                    fMask=shellcon.SEE_MASK_NOCLOSEPROCESS,
                                    lpDirectory=cmdDir,
                                    lpFile=cmd)
            if self.debug: print(procInfo)
        except Exception as e:
            print("Failed: WinAppDriver can't Running. \n\t-", e)
        procHandle = procInfo['hProcess'] 

        event.wait()
        if event.is_set():
            if self.debug: print("End process [WinAppDriver]:", procHandle)

            try:
                win32process.TerminateProcess(procHandle, 0)
            except Exception as e:
                if self.debug: print("Failed: WinAppDriver can't terminate. \n\t-", e)

    def run(self):
        self.proc = multiprocessing.Process(target=self._run, args=(self._stop,))
        self.proc.start()

    def close(self):
        self._stop.set()
        self.proc.join()

    def __enter__(self):
        self.run()

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()


def kill_app(name):
    try:
        os.system(f"taskkill /f /im  \"{name}\"")
    except Exception as e:
        print(f"Error: Can't Terminate current app[{name}] \n\t-", e)

def clear_text():
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")

def replaceText(msg):
    clear_text()
    pyautogui.write(msg)

def loopTab(number):
    for _ in range(number):
        pyautogui.press('tab')


ip_address = sys.argv[1]
port = sys.argv[2]
username = sys.argv[3]
password = sys.argv[4]

APP_EXE_PATH = r"C:\Program Files\Quest Software\Toad Edge\ToadEdge.exe"  # -- Path to .exe file that you want to automate.

def workflow(driver: webdriver.Remote):
    """Edit Workflow to automate."""

    # === Start automation zone ===
    
    driver.find_element_by_xpath('//*[@Name="MySQL"][@LocalizedControlType="check box"]').click()
    replaceText(ip_address)
    loopTab(1)
    sleep(1)
    replaceText(port)
    loopTab(2)
    sleep(1)
    replaceText(username)
    loopTab(1)
    sleep(1)
    replaceText(password)
    sleep(1)
    driver.find_element_by_xpath('//*[@Name="Connect"][@LocalizedControlType="button"]').click()

    # === End automation zone ===

if __name__ == '__main__':

    driver = None
    is_complete = False
    failed_count = 0

    with DevMode() as dm:
        while not (is_complete or failed_count >= 3) and dm.is_admin:
            with WinAppDriver(debug=True):
                try:
                    driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities= {
                        "app": APP_EXE_PATH
                    })
                except Exception as e:
                    print("Error:", e)
                    failed_count += 1

                    desktopSession = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities= {
                        "app": "Root"
                    })
                    desktopSession.find_element_by_xpath(f'//*[@Name="Toad Edge - 1 running window"]').click()
                    TopLevelWindow = desktopSession.find_element_by_xpath(f'//*[@Name="Toad Edge"][@LocalizedControlType="window"]')
                    TopLevelWindowHandle = hex(int(TopLevelWindow.get_attribute("NativeWindowHandle")));
                    driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', desired_capabilities= {
                        "appTopLevelWindow": TopLevelWindowHandle
                    })

                try:
                    workflow(driver)
                    is_complete = True
                except urllib3.exceptions.MaxRetryError:
                    print("Connection refused: \n\t- Please check dev-mode are Enable in windows.")
                    failed_count += 1

    

    
