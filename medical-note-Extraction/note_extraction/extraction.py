from note_extraction.pdf_extraction import *
from note_extraction.llm_note_summarization import *


def extract_medical_note(pdf, question):
    medical_note = pdf_extraction(pdf)
    extracted_note = llm_note_extraction(medical_note, question)
    return extracted_note
