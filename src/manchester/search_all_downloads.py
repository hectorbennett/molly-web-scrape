"""
From the spreadsheet, yield urls for documents tabs that we should scrape from
"""
import os
import csv
from utils import file_contains_text

input_csv = os.path.abspath(os.path.join(os.getcwd(), "..", "input_data.csv"))
output_csv_filepath =  os.path.abspath(os.path.join(os.getcwd(), "..", "output", "manchester_output.csv"))

def get_case_numbers():
    case_numbers = []
    with open(input_csv, newline='') as csvfile:
        filereader = csv.reader(csvfile)
        for row in filereader:
            case_number = row[0]
            la = row[1]
            affordable = row[6]
            if la == 'Manchester' and affordable == 'n/a':
                case_numbers.append(case_number)
    return case_numbers

def get_download_information():
    for case_number in get_case_numbers():
        folder = os.path.abspath(os.path.join(os.getcwd(), '..', 'output', 'docs', case_number.replace('/', '_')))
        for (dirpath, dirnames, filenames) in os.walk(folder):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                yield {
                    'case_number': case_number,
                    'filename': filename,
                    'contains_affordable': file_contains_text(filepath, "affordable")
                }


def search_all_downloads():
    with open(output_csv_filepath, "w") as csvfile:
        writer = csv.DictWriter(
            csvfile, fieldnames=["case_number", "filename", "contains_affordable"]
        )
        writer.writeheader()
        csvfile.flush()
        for row in get_download_information():
            writer.writerow({"case_number": row['case_number'], "filename": row['filename'], "contains_affordable": row['contains_affordable']})
            csvfile.flush()

    # print('search all downloads')

# def get_doc_page_urls():
#     urls = []
#     with open(input_csv, newline='') as csvfile:
#         filereader = csv.reader(csvfile)
#         for row in filereader:
#             la = row[1]
#             affordable = row[6]
#             url = row[2]
#             if la == 'Manchester' and affordable == 'n/a':
#                 urls.append(url.replace('activeTab=summary', 'activeTab=documents'))
#     return urls

# # import required module
# import os
# import csv
# import PyPDF2
# from utils import pdf_contains_text



# directory = os.path.join(os.getcwd(), "manchester_docs")


# with open(output_csv_filepath, "w") as csvfile:
#     writer = csv.DictWriter(
#         csvfile, fieldnames=["reference", "filename", "status"]
#     )
#     writer.writeheader()
#     for folder in os.listdir(directory):
#         # reference_folder = os.path.join(directory, folder)
#         # for folder in os.listdir(reference_folder):
#         #     path = os.path.join(reference_folder, folder)
#         #     if not os.listdir(path):
#         #         continue
#         #     file = os.listdir(path)[0]
#         #     # for file in os.listdir(path):
#         #     #     print(file)
#         #     reference = folder.replace('%2F', '/').strip()
#         #     print(f'{reference}: {file}')
#         #     filepath = os.path.join(path, file)
#         #     if file_contains_text(filepath, "affordable"):
#         #         writer.writerow({"reference": reference, "filename": file, "status": "match"})
#         #         print('\nTRUE\n')
#         #         csvfile.flush()
#         #     else:
#         #         writer.writerow({"reference": reference, "filename": file, "status": "no match"})
#         #         csvfile.flush()
#             # except Exception:
#             #     writer.writerow({"reference": reference, "filename": file, "status": "error"})
