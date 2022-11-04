import zipfile
import xml.etree.ElementTree as ET


def docx_contains_text(filepath, text_string):
    try:
        doc = zipfile.ZipFile(filepath).read('word/document.xml')
        if text_string in str(doc):
            return True
        return False
    except Exception:
        return None

