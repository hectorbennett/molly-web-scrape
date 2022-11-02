import os
from bs4 import BeautifulSoup
from utils import get_html_from_url, download_document
from .get_doc_page_urls import get_doc_page_urls


def download_docs_with_requests(url):
    html = get_html_from_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a", {"title": "View Document"})
    if not links:
        print(f"No links for {url}")
        return
    for link in links:
        os.path.abspath(os.path.join(os.getcwd(), "..", "scrape_cache"))
        output_path = os.path.join(os.getcwd(), "salford_docs")
        href = link.get('href')
        print(href)
        # download_file(output_path, href)


def download_all_docs_with_requests():
    doc_page_urls = get_doc_page_urls()
    for url in doc_page_urls:
        download_docs_with_requests(url)
        # download_docs_with_requests()