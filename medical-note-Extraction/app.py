import extraction as extraction
import streamlit as st
from note_extraction.extraction import *
import requests
import json

state = st.cache_resource()


# Function to extract medical entities
def extract_entities(notes):
    api_url = "http://ec2-34-223-50-104.us-west-2.compute.amazonaws.com:5007/medical-entity"
    payload = {"notes": notes}
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"}
    response = requests.post(api_url, data=json.dumps(payload), headers=headers)
    respons_json = response.json()
    return respons_json['Output'].split(',')


def main():
    medial_note_output = ''
    if 'note' in st.session_state:
        medial_note_output = st.session_state.note
    st.set_page_config(page_title="Invoice Extraction Bot")
    st.title("Medical Entity Extraction 🗃️")
    pdf = st.file_uploader("Upload Progress note here, only PDF files allowed", type=["pdf"],
                           accept_multiple_files=True)
    if not pdf:
        if 'note' in st.session_state:
            st.session_state.pop('note')
            medial_note_output = None
    if pdf:
        question = st.text_area('Prompt: ', 'Pretend you as a expert in content extraction, Please extract HPI, '
                                            'Objective'
                                            ' and Assessment from below medical note.')
        submit = st.button("Extract Note")
        if submit and question:
            file_bytes = pdf[0]
            medial_note_output = extract_medical_note(file_bytes, question)
            st.session_state["note"] = medial_note_output
            print(medial_note_output["HPI"])
            print(medial_note_output is not None)

    if medial_note_output:
        # Display in Streamlit
        st.subheader("Progress Note")

        # Display HPI with Extract button
        hpi_text = st.text_area('HPI :', medial_note_output["HPI"])
        if st.button('Extract Medical Entities', key='hpi_extract'):
            # extracted_entities = extract_entities(hpi_text)
            st.text_area('Extracted Entities:', json.dumps(extract_entities(hpi_text), indent=2))

        # Display Objective with Extract button
        objective_text = st.text_area('Objective :', json.dumps(medial_note_output["Objective"], indent=2))
        if st.button('Extract Medical Entities', key='objective_extract'):
            # extracted_entities = extract_entities(objective_text)
            st.text_area('Extracted Entities:', json.dumps(extract_entities(objective_text), indent=2))

        # Display Assessment with Extract button
        assessment_text = st.text_area('Assessment :', json.dumps(medial_note_output["Assessment"], indent=2))
        if st.button('Extract Medical Entities', key='assessment_extract'):
            # extracted_entities = extract_entities(assessment_text)
            st.text_area('Extracted Entities:', json.dumps(extract_entities(assessment_text), indent=2))


# Invoking main function
if __name__ == '__main__':
    main()
