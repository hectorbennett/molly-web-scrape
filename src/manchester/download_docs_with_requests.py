import os
import time
from bs4 import BeautifulSoup
from utils import get_html_from_url, download_document
from .get_doc_page_urls import get_doc_page_urls
import requests

def perform_referer_request(url):
    print(f'perform_referer_request: {url}')
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.5",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "JSESSIONID=Az97YQFNmGOISbxsWMewsxOcmjKosn4onKsY3V79.shpdmzm003",
        "Host": "pa.manchester.gov.uk",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0"
    }
    response = requests.get(url, headers=headers)
    # Save the PDF
    if response.status_code != 200:
        raise Exception(f"{response.status_code}: f{url}")
    time.sleep(1)


def download_docs_with_requests(url):
    html = get_html_from_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    case_number = soup.find("input", {"name": "caseNumber"})
    document_urls = get_document_urls(url)
    if not document_urls:
        print(f"No links for {url}")
        return
    perform_referer_request(url)
    for index, link in enumerate(document_urls):
        download_document(case_number.get("value"), index, link, referer=url)

def get_document_urls(doc_page_url):
    html = get_html_from_url(doc_page_url)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a", {"title": "View Document"})
    return [f"https://pa.manchester.gov.uk{link.get('href')}" for link in links]


def download_all_docs_with_requests():
    count = 0

    doc_page_urls = get_doc_page_urls()
    print(f'{len(doc_page_urls)} case_numbers')
    for url in doc_page_urls:
        count += len(get_document_urls(url))
    print(f'{count} documents')
    for url in doc_page_urls:
        download_docs_with_requests(url)
        # download_docs_with_requests()