"""
From the spreadsheet, yield urls for documents tabs that we should scrape from
"""

import os
import csv

input_csv = os.path.abspath(os.path.join(os.getcwd(), "..", "input_data.csv"))



def get_doc_page_urls():
    with open(input_csv, newline='') as csvfile:
        filereader = csv.reader(csvfile)
        for row in filereader:
            la = row[1]
            affordable = row[6]
            url = row[2]
            if la == 'Manchester' and affordable == 'n/a':
                return_url = url.replace('activeTab=summary', 'activeTab=documents')
                yield return_url


