import os
import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options



def get_selenium_browser(download_directory):
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


def get_html_from_url(url):
    """
    Cache html in the scrape_cache
    """
    folder = os.path.abspath(os.path.join(os.getcwd(), "..", "scrape_cache"))
    if not os.path.exists(folder):
        os.makedirs(folder)
    local_filepath = os.path.join(folder, url.replace('/', '_'))
    if os.path.isfile(local_filepath):
        with open(local_filepath, 'r') as file:
            data = file.read()
            return data
    else:
        print("getting {}".format(url))
        page = requests.get(url)
        print("success!")
        time.sleep(0.5)
        data = page.text
        print("writing to {}".format(local_filepath))
        with open(local_filepath, 'w') as f:
            f.write(data)
        return data

def download_document():
    pass

if __name__ == '__main__':
    get_html_from_url('https://www.google.com')