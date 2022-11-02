import os
import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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


def get_url_content(url):
    """
    Cache locally once downloaded
    """
    folder = os.path.join(os.getcwd(), "scrape_data", "manchester")
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
        time.sleep(2)
        data = page.text
        print("writing to {}".format(local_filepath))
        with open(local_filepath, 'w') as f:
            f.write(data)
        return data


def get_pdf(path, url):
    print(url)
    time.sleep(2)
    if not os.path.exists(path):
        os.makedirs(path)
    doc_name = url.split('/')[-1]
    if doc_name in os.listdir(path):
        print('pdf already exists')
        # file already exists
        return
    print('getting pdf {}'.format(doc_name))
    response = requests.get(url)    
    filepath = os.path.join(path, doc_name)
    with open(filepath, 'wb') as f:
        f.write(response.content)
    time.sleep(2)
    

def get_manchester_doc_page(ref, url):
    url = url.replace('activeTab=summary', 'activeTab=documents')
    if 'activeTab=documents' not in url:
        print('')
        print('not the right tab!')
        print(url)
        print('')
    html = get_url_content(url)
    soup = BeautifulSoup(html, 'html.parser')
    return {'ref': ref, 'page': soup, 'url': url}


def get_manchester_doc_pages():
    results = []
    filepath = os.path.join(os.getcwd(), "data.csv")
    with open(filepath, newline='') as csvfile:
        filereader = csv.reader(csvfile)
        for i, row in enumerate(filereader):
            ref = row[0]
            LA = row[1]
            portal_url = row[2]
            if LA == 'Manchester':
                results.append(get_manchester_doc_page(ref, portal_url))
    return results


def download_manchester_docs(url, ref, page):
    links = page.find_all("a", {"title": "View Document"})
    if not links:
        print("No links for {}".format(ref))
    for link in links:
        get_pdf(url, ref, link.get('href'))
        doc_url = '{}{}'.format('https://pa.manchester.gov.uk', link.get('href'))
        local_path = os.path.join(os.getcwd(), "manchester_docs", ref.replace("/", '%2F'))
        # get_pdf(local_path, doc_url)

def get_pdf(url, ref, input_href):
    filename = input_href.split('/')[-1].split('.')[0]
    download_path = f"/home/hector/molly-web-scrape/manchester_docs/{ref.replace('/', '%2F')}/{filename}"
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if os.listdir(download_path):
        if not os.listdir(download_path)[0].endswith('.crdownload'):
            print("file already exists: {}".format(filename))
            return
        else:
            print("failed download: {}".format(filename))
            return
            for f in os.listdir(download_path):
                os.remove(os.path.join(download_path, f))
    print('getting pdf: {} {}'.format(ref, filename))
    browser = get_browser(download_path)
    browser.get(url)
    input = browser.find_element(By.XPATH, "//a[@href='" + input_href + "']")
    input.click()
    time.sleep(2)


def download_files():
    doc_pages = get_manchester_doc_pages()
    for page_info in doc_pages:
        ref = page_info['ref']
        page = page_info['page']
        url = page_info['url']
        download_manchester_docs(url, ref, page)

count = 8128

if __name__ == '__main__':
    download_files()