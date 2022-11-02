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
    # print(f'get url {url}')
    local_filepath = os.path.join(os.getcwd(), "scrape_data", "salford", url.replace('/', '_'))
    if os.path.isfile(local_filepath):
        with open(local_filepath, 'r') as file:
            data = file.read()
            return data
    else:
        page = requests.get(url)
        data = page.text
        with open(local_filepath, 'w') as f:
            f.write(data)
        return data


def get_salford_doc_page(ref, url):
    html = get_url_content(url)
    soup = BeautifulSoup(html, 'html.parser')
    docs_tab_url = soup.find(id="tab_externalDocuments").get("href")
    docs_tab_url = 'https://publicaccess.salford.gov.uk{}'.format(docs_tab_url)
    docs_tab_html = get_url_content(docs_tab_url)
    docs_tab_soup = BeautifulSoup(docs_tab_html, 'html.parser')
    docs_page_url = docs_tab_soup.find("p", {"class": "externalDocumentsLink"}).find('a').get('href')
    docs_page_html = get_url_content(docs_page_url)
    return {'ref': ref, 'page': BeautifulSoup(docs_page_html, 'html.parser'), 'url': docs_page_url}




def download_salford_docs(reference_number, url, input_ids):
    for id in input_ids:
        get_pdf(url, reference_number, id)
        

        
def get_pdf(url, ref, input_id):
    download_path = f"/home/hector/molly-web-scrape/salford_docs/{ref.replace('/', '%2F')}/{input_id}"
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if os.listdir(download_path):
        filename = os.listdir(download_path)[0]
        if not filename.endswith('.crdownload'):
            print("file already exists: {}".format(filename))
            return
        else:
            print("failed download: {}".format(filename))
            for f in os.listdir(download_path):
                os.remove(os.path.join(download_path, f))
    print('getting pdf: {} {}'.format(ref, input_id))
    browser = get_browser(download_path)
    browser.get(url)
    input = browser.find_element(By.ID, input_id)
    input.click()
    time.sleep(2)








def get_salford_doc_pages():
    results = []
    filepath = os.path.join(os.getcwd(), "data.csv")
    with open(filepath, newline='') as csvfile:
        filereader = csv.reader(csvfile)
        for i, row in enumerate(filereader):
            ref = row[0]
            LA = row[1]
            portal_url = row[2]
            if LA == 'Salford':
                results.append(get_salford_doc_page(ref, portal_url))
    return results

def download_files():
    doc_pages = get_salford_doc_pages()
    for page_info in doc_pages:
        ref = page_info['ref']
        page = page_info['page']
        url = page_info['url']
        doc_links = page.find_all("input", {"value": "View document"})
        download_salford_docs(ref, url, (l.get('id') for l in doc_links))


def validate_files():
    doc_pages = get_salford_doc_pages()
    for page_info in doc_pages:
        ref = page_info['ref']
        page = page_info['page']
        # assert the correct number of files have been downloaded.
        doc_count = len(page.find_all("input", {"value": "View document"}))
        local_folder = os.path.join(os.getcwd(), 'salford_docs', ref.replace('/', '%2F'))
        local_file_count = len(os.listdir(local_folder))
        if doc_count != local_file_count:
            print('{} has {} docs, it should have {}'.format(ref, local_file_count, doc_count))


directory = os.path.join(os.getcwd(), "salford_docs")

for folder in os.listdir(directory):
    reference_folder = os.path.join(directory, folder)

if __name__ == '__main__':
    # validate_files()
    download_files()
