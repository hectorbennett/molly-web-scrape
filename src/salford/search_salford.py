# import required module
import os
import csv
import PyPDF2



def file_contains_text(filepath, text_string):
    reader = PyPDF2.PdfFileReader(filepath)
    for page_number in range(0, reader.numPages):
        page = reader.getPage(page_number)
        page_content = page.extractText()
        if text_string.lower() in page_content.lower():
            return True
    return False


directory = os.path.join(os.getcwd(), "salford_docs")
output_csv_filepath =  os.path.join(os.getcwd(), "salford_search_results.csv")

with open(output_csv_filepath, "w") as csvfile:
    writer = csv.DictWriter(
        csvfile, fieldnames=["reference", "filename", "status"]
    )
    writer.writeheader()
    for folder in os.listdir(directory):
        reference_folder = os.path.join(directory, folder)
        for file in os.listdir(reference_folder):
            reference = folder.replace('%2F', '/')
            print(f'{reference}: {file}')
            filepath = os.path.join(reference_folder, file)
            try:
                if file_contains_text(filepath, "affordable"):
                    writer.writerow({"reference": reference, "filename": file, "status": "match"})
                    print('\nTRUE\n')
                    csvfile.flush()
                else:
                    writer.writerow({"reference": reference, "filename": file, "status": "no match"})
                    csvfile.flush()
            except Exception:
                writer.writerow({"reference": reference, "filename": file, "status": "error"})
