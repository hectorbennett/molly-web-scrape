import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



def get_browser(download_directory):
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": download_directory,
        "directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    # Set path to chromedriver as per your configuration
    homedir = os.path.expanduser("~")
    webdriver_service = Service(f"{homedir}/chromedriver/stable/chromedriver")
    return webdriver.Chrome(service=webdriver_service, options=chrome_options)
