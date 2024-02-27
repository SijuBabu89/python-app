import csv

from PIL.PdfParser import pdf_repr
from langchain.docstore.document import Document
import re
import os
import csv
from PyPDF2 import PdfReader


def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text


def extract_medical_entities(pdf_content):
    medical_codes = {}
    procedures = extract_procedures(pdf_content)
    assessment = extract_assessment(pdf_content)
    medical_codes['procedures'] = procedures
    medical_codes['assessment'] = assessment
    return medical_codes


def extract_procedures(pdf_content):
    # Remove new line and unwanted sppace
    if 'Procedure Codes' not in pdf_content:
        return ""
    pdf_content = re.sub(r'\s+', ' ', pdf_content.replace('\r\n', ' '))
    # Find the index where 'Subjective:' occurs
    subjective_header_index = pdf_content.find('Subjective:')
    # Extract the text starting from 'Subjective:'
    pdf_content = pdf_content[subjective_header_index:]
    # Define the pattern to match
    pattern = re.compile(r'Provider:.*?eCW', re.DOTALL)
    pdf_content = re.sub(pattern, '', pdf_content)
    pattern = re.compile(r'\(Aveta, Bot \).*?DOS: (\d{2}/\d{2}/\d{4})', re.DOTALL)
    pdf_content = re.sub(pattern, '', pdf_content)
    pattern = re.compile(r'Electronically signed by.*?Sign off status: Completed', re.DOTALL)
    pdf_content = re.sub(pattern, '', pdf_content)
    pattern = re.compile(r'Provider:.*?Lookup\.jsp', re.DOTALL)
    pdf_content = re.sub(pattern, '', pdf_content)
    pattern = re.compile(r'Provider:.*?Date: (\d{2}/\d{2}/\d{4})', re.DOTALL)
    pdf_content = re.sub(pattern, '', pdf_content)
    # Define a regular expression pattern to match the plan section
    pattern = re.compile(r'Plan:(.*?)(?:Follow Up:.*?(?=(?:Subjective:|$)))', re.DOTALL)
    # Find all matches in the progress notes
    matches = re.search(pattern, pdf_content)
    pdf_content = matches.group(1).strip() if matches else ""
    # Define a regular expression pattern to match and remove the content between "Treatment" and "Procedure Codes"
    pattern = re.compile(r'Treatment:(.*?)(?=Procedure Codes:|$)', re.DOTALL)
    # Replace the matched content with an empty string
    pdf_content = pattern.sub('', pdf_content)
    pdf_content = pdf_content.replace("Procedure Codes: ", "")
    return pdf_content


def extract_assessment(pdf_content):
    # Remove new line and unwanted sppace
    pdf_content = re.sub(r'\s+', ' ', pdf_content.replace('\r\n', ' '))
    # Find the index where 'Subjective:' occurs
    subjective_header_index = pdf_content.find('Subjective:')
    # Extract the text starting from 'Subjective:'
    pdf_content = pdf_content[subjective_header_index:]
    # Define the pattern to match
    pattern = re.compile(r'Provider:.*?eCW', re.DOTALL)
    pdf_content = re.sub(pattern, '', pdf_content)
    pattern = re.compile(r'\(Aveta, Bot \).*?DOS: (\d{2}/\d{2}/\d{4})', re.DOTALL)
    pdf_content = re.sub(pattern, '', pdf_content)
    pattern = re.compile(r'Electronically signed by.*?Sign off status: Completed', re.DOTALL)
    pdf_content = re.sub(pattern, '', pdf_content)
    pattern = re.compile(r'Provider:.*?Lookup\.jsp', re.DOTALL)
    pdf_content = re.sub(pattern, '', pdf_content)
    pattern = re.compile(r'Provider:.*?Date: (\d{2}/\d{2}/\d{4})', re.DOTALL)
    pdf_content = re.sub(pattern, '', pdf_content)
    # Extracting the Assessment part from the progress note.
    assessment_pattern = re.compile(r'Assessment:(.*?)Plan:', re.DOTALL)
    matches = re.search(assessment_pattern, pdf_content)
    pdf_content = matches.group(1).strip() if matches else ""
    pdf_content = pdf_content.replace('Assessment: ', '')
    return pdf_content


def format_assessment(assessment):
    # Use regular expression to extract ICD descriptions
    icd_pattern = re.compile(r'\d+\.\s(.*?)\s-\s[\w\d\.]+')

    icd_matches = re.findall(icd_pattern, assessment)
    if icd_matches:
        assessment = ', '.join([f"{i}. {desc}" for i, desc in enumerate(icd_matches, start=1)])
    return assessment


def parse_segment(segment):
    try:
        # Extract the code (first 5 digits)
        code_match = re.match(r'\d{5}', segment)
        if code_match:
            code = code_match.group(0)
        else:
            return None

        # Attempt to split the segment into description and modifiers parts
        description_modifiers_split = segment[len(code):].split(", Modifiers: ")
        description = description_modifiers_split[0].strip()

        # Initialize modifiers as an empty list by default
        modifiers = []

        # If modifiers are present, convert them to a list of integers
        if len(description_modifiers_split) == 2:
            modifiers_str = description_modifiers_split[1]
            modifiers = [int(mod.strip()) for mod in modifiers_str.split(',') if mod.strip()]

        return {'code': code, 'description': description, 'modifiers': modifiers}
    except ValueError:
        print(f"Error converting modifiers to integers in segment: {segment}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e} in segment: {segment}")
        return None


def format_procedure(text):
    print('format_procedure -------------------------->' + text)
    if len(text) == 0:
        return ""
    professional_cpt = []
    facility_cpt = []
    result = {}
    segments = re.split(r'(?=\b\d{5}\b)', text)
    for segment in segments:
        if segment.strip():
            parsed_segment = parse_segment(segment)
            if parsed_segment:
                print(parsed_segment)
                code_description = parsed_segment['description']
                if 'OPERATING' in code_description:
                    facility_cpt.append(code_description)
                else:
                    professional_cpt.append(code_description)
    professional = ', '.join(professional_cpt)
    facility = ', '.join(facility_cpt)
    professional = professional.replace(',,', ',')
    facility = facility.replace(',,', ',')
    result['Professional'] = professional
    result['Facility'] = facility
    return result


def extractRecordAsDocument(file_path):
    docs = []
    with open(file_path, mode='r') as file:
        csvFile = csv.DictReader(file)
        for row in csvFile:
            met = {}
            met['id'] = row['Id']
            met['ICD Codes'] = row['ICD Code']
            met['CPT Codes'] = row['CPT Code']
            met['File Name'] = row['File Name']
            docs.append(Document(
                page_content=" Progress Note : " + row['PDF Content'] + ", ICD Code : " + row[
                    'CPT Code'] + ", CPT Code : " + row['CPT Code'],
                metadata=met
            )
            )
    return docs
