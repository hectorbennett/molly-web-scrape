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


directory = os.path.join(os.getcwd(), "manchester_docs")
output_csv_filepath =  os.path.join(os.getcwd(), "manchester_search_results.csv")

with open(output_csv_filepath, "w") as csvfile:
    writer = csv.DictWriter(
        csvfile, fieldnames=["reference", "filename", "status"]
    )
    writer.writeheader()
    for folder in os.listdir(directory):
        reference_folder = os.path.join(directory, folder)
        for folder in os.listdir(reference_folder):
            path = os.path.join(reference_folder, folder)
            if not os.listdir(path):
                continue
            file = os.listdir(path)[0]
            # for file in os.listdir(path):
            #     print(file)
            reference = folder.replace('%2F', '/').strip()
            print(f'{reference}: {file}')
            filepath = os.path.join(path, file)
            if file_contains_text(filepath, "affordable"):
                writer.writerow({"reference": reference, "filename": file, "status": "match"})
                print('\nTRUE\n')
                csvfile.flush()
            else:
                writer.writerow({"reference": reference, "filename": file, "status": "no match"})
                csvfile.flush()
            # except Exception:
            #     writer.writerow({"reference": reference, "filename": file, "status": "error"})
