import sys
from subprocess import CREATE_NO_WINDOW

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

username = sys.argv[1]
password = sys.argv[2]

options = webdriver.ChromeOptions()
options.add_argument('ignore-certificate-errors')
options.add_experimental_option("detach", True)
services = Service(executable_path=ChromeDriverManager().install())
services.creationflags = CREATE_NO_WINDOW
driver = webdriver.Chrome(service=services, options=options)


URL = "https://10.2.1.11"    # -- Link to URL page that you want to automate.

def workflow(driver):
    """Edit Workflow to automate."""

    # === Start automation zone ===

    elem = driver.find_element(By.NAME, "username")
    elem.clear()
    elem.send_keys(username)
    elem = driver.find_element(By.NAME, "password")
    elem.clear()
    elem.send_keys(password)
    elem = driver.find_element(By.XPATH, '//*[@id="login-page"]/div[1]/table/tbody/tr/td[2]/div/div/form/div[1]/fieldset/div[3]/button')
    elem.click()

    # === End automation zone ===

if __name__ == '__main__':
    driver.get(URL)
    workflow(driver)
    