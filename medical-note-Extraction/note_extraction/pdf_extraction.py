from pypdf import PdfReader


def pdf_extraction(pdf_file_bytes):
    if pdf_file_bytes:
        pdf_reader = PdfReader(pdf_file_bytes)
        text = ""
        for page in pdf_reader.pages:
            #print(pdf_reader.pages)
            #print('page')
            #print(page.extract_text())
            text += page.extract_text()
        return text

