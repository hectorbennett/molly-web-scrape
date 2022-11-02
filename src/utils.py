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

def download_document(case_number, index, url, referer):
    case_number_folder = case_number.replace("/", "_")
    output_folder = os.path.abspath(os.path.join(os.getcwd(), "..", "output", "docs", case_number_folder, str(index)))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if os.listdir(output_folder):
        #something already in there.
        return
    filename = url.split('/')[-1]
    download_path = os.path.join(output_folder, filename)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.5",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "JSESSIONID=Az97YQFNmGOISbxsWMewsxOcmjKosn4onKsY3V79.shpdmzm003",
        "Host": "pa.manchester.gov.uk",
        "Pragma": "no-cache",
        "Referer": referer,
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"
    }

    print(url)
    response = requests.get(url, headers=headers)
    # Save the PDF
    if response.status_code == 200:
        with open(download_path, "wb") as f:
            f.write(response.content)
    else:
        print(response.status_code)
    time.sleep(5)

def download_document_with_selenium(case_number, index, url):
    print(f'download {case_number} {index} {url}')
    case_number_folder = case_number.replace("/", "_")
    output_folder = os.path.abspath(os.path.join(os.getcwd(), "..", "output", "docs", case_number_folder, str(index)))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if os.listdir(output_folder):
        #something already in there.
        return
    # filename = url.split('/')[0]
    browser = get_selenium_browser(output_folder)
    time.sleep(1)
    browser.get(url)
    time.sleep(1)
    print(browser.page_source)
    time.sleep(1)
    # download_path = os.path.join(output_folder, filename)



if __name__ == '__main__':
    get_html_from_url('https://www.google.com')