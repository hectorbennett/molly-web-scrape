import PyPDF2



def file_contains_text(filepath, text_string):
    reader = PyPDF2.PdfFileReader(filepath)
    for page_number in range(0, reader.numPages):
        page = reader.getPage(page_number)
        page_content = page.extractText()
        if text_string.lower() in page_content.lower():
            return True
    return False

filepath = "/home/hector/molly-web-scrape/docs/14%2F65186%2FFUL/30080 Complete FRA 140731.pdf"
search_text = "affordable"
print(file_contains_text(filepath, search_text))