import os
import fitz


def extract_text_from_pdf(pdf_path):
    with fitz.open(pdf_path) as doc:   # open the PDF document
        text = ''
        for page in doc:   # iterate over the pages
            text += page.get_text()   # get the text of each page
    return text


def save_text_to_txt(text, txt_path):
    with open(txt_path, 'w', encoding='utf-8') as file:   # use utf-8 encoding to avoid garbled characters
        file.write(text)


def convert_pdfs_to_txt(folder_path):
    # Create a directory to store the TXT files
    output_folder = folder_path
    os.makedirs(output_folder, exist_ok=True)

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and filename.endswith('.pdf'):
            # Extract text from the PDF
            text = extract_text_from_pdf(file_path)

            # Generate the corresponding output file path
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(output_folder, txt_filename)

            # Save the extracted text to a TXT file
            save_text_to_txt(text.replace("\n", ""), txt_path)

    print('Conversion completed. TXT files saved in:', output_folder)

