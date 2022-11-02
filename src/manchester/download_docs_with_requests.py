import os
from bs4 import BeautifulSoup
from utils import get_html_from_url, download_document
from .get_doc_page_urls import get_doc_page_urls


def download_docs_with_requests(url):
    print(url)
    html = get_html_from_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a", {"title": "View Document"})
    case_number = soup.find("input", {"name": "caseNumber"})
    if not links:
        print(f"No links for {url}")
        return
    for index, link in enumerate(links):
        href = link.get('href')
        href = f"https://pa.manchester.gov.uk{href}"
        download_document(case_number.get("value"), index, href, url)


def download_all_docs_with_requests():
    doc_page_urls = get_doc_page_urls()
    for url in doc_page_urls:
        download_docs_with_requests(url)
        # download_docs_with_requests()