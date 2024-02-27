from flask import Flask, request, abort
import json
from pinecone_impl import *
from llm_icd_cpt_app import *
from llm_progress_note_code_prediction import *
from data_extraction import *
from jiffy_connector import *
import ast

app = Flask(__name__)


@app.route('/')
def progress_note_icd_code():
    return 'ECW Insurance Mapping!'


@app.route('/llm/predict_icd', methods=['POST'])
def get_icd_code():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    insurance_result = ''
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    progress_note = request.get_json().get('description')
    progress_note = "" if progress_note is None else progress_note
    if progress_note is not None:
        result = predict_icd_code(progress_note)
        json_output = json.dumps(result)
        parsed_json = json.loads(json_output)
    print(parsed_json)
    api_response = {
        "Output": result
    }
    return result


@app.route('/llm/predict_cpt', methods=['POST'])
def get_cpt_code():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    insurance_result = ''
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    progress_note = request.get_json().get('description')
    progress_note = "" if progress_note is None else progress_note
    if progress_note is not None:
        result = predict_cpt_code(progress_note)
        json_output = json.dumps(result)
        parsed_json = json.loads(json_output)
    print(parsed_json)
    api_response = {
        "Output": result
    }
    return result


@app.route('/llm/predict_medical_code', methods=['POST'])
def get_medical_code():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    insurance_result = ''
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    progress_note = ""
    file_path = request.get_json().get('pdf_path')
    file_path = "" if file_path is None else file_path
    if len(file_path) > 0:
        progress_note = extract_pfd_content(file_path)
    progress_note = "" if progress_note is None else progress_note
    print('progress_note : ')
    print(progress_note)
    if progress_note is not None:
        llm_cpt_result = ""
        pg_icd_codes = extract_assessment(progress_note)
        pg_cpt_codes = extract_procedures(progress_note)
        formated_icd_code = format_assessment(pg_icd_codes)
        formated_cpt_code = format_procedure(pg_cpt_codes)
        if len(formated_cpt_code) > 0:
            professional_cpt = predict_cpt_code(formated_cpt_code['Professional'])
            facility_cpt = predict_cpt_code(formated_cpt_code['Facility'])
            llm_cpt_result = professional_cpt + ", " + facility_cpt
        llm_icd_result = predict_icd_code(formated_icd_code)
    api_response = {
        "LLMICDCode": llm_icd_result,
        "LLMCPTCode": llm_cpt_result,
        "PGICDCode": pg_icd_codes,
        "PGCPTCode": pg_cpt_codes
    }
    return api_response


@app.route('/llm/extract_medical_entities', methods=['POST'])
def get_medical_entities():
    result = {}
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    insurance_result = ''
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    progress_note = request.get_json().get('progress_notes')
    progress_note = "" if progress_note is None else progress_note
    if progress_note is not None:
        result = extract_medical_entities(progress_note)
    return result


@app.route('/icd_code/full_result', methods=['POST'])
def extract_full_result():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    insurance_result = ''
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    print('-------------------------------------------------------------------------------------')
    print('REQUEST : ')
    print(request)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST FORM : ')
    print(request.form)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST HEADERS : ')
    print(request.headers)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST ARGS : ')
    print(request.args)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST JSON : ')
    print(request.get_json())
    print('-------------------------------------------------------------------------------------')
    print('AUTHENTICATION')
    print(request.authorization)
    print('-------------------------------------------------------------------------------------')

    progress_note = request.get_json().get('progress_note')
    gpt_model = request.get_json().get('gpt_model')
    progress_note = "" if progress_note is None else progress_note
    gpt_model = "gpt-3.5-turbo" if gpt_model is None else gpt_model
    query = progress_note
    if query is not None:
        result = get_answer(query, gpt_model)
        # Convert the list to JSON format
        json_output = json.dumps(result)
        # Load the JSON string back to a Python object
        parsed_json = json.loads(json_output)
    return result


@app.route('/icd_code/result', methods=['POST'])
def extract_result():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    insurance_result = ''
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    print('-------------------------------------------------------------------------------------')
    print('REQUEST : ')
    print(request)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST FORM : ')
    print(request.form)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST HEADERS : ')
    print(request.headers)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST ARGS : ')
    print(request.args)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST JSON : ')
    print(request.get_json())
    print('-------------------------------------------------------------------------------------')
    print('AUTHENTICATION')
    print(request.authorization)
    print('-------------------------------------------------------------------------------------')

    progress_note = request.get_json().get('progress_note')
    gpt_model = request.get_json().get('gpt_model')
    progress_note = "" if progress_note is None else progress_note
    gpt_model = "gpt-3.5-turbo" if gpt_model is None else gpt_model
    query = progress_note
    if query is not None:
        result = get_answer(query, gpt_model)
        result = json.loads(result)
        result.pop('query', None)
    api_response = {
        "Output": result
    }
    return api_response


@app.route('/extract_code', methods=['POST'])
def extract_progressnote_code():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    insurance_result = ''
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    print('-------------------------------------------------------------------------------------')
    print('REQUEST : ')
    print(request)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST FORM : ')
    print(request.form)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST HEADERS : ')
    print(request.headers)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST ARGS : ')
    print(request.args)
    print('-------------------------------------------------------------------------------------')
    print('REQUEST JSON : ')
    print(request.get_json())
    print('-------------------------------------------------------------------------------------')
    print('AUTHENTICATION')
    print(request.authorization)
    print('-------------------------------------------------------------------------------------')

    progress_note = request.get_json().get('progress_note')
    progress_note = "" if progress_note is None else progress_note
    query = progress_note
    if query is not None:
        result = get_progress_note_result(query)
    api_response = {
        "Output": result
    }
    return api_response


if __name__ == '__main__':
    print("---- Into the main Function ----")
    app.run(debug=True, host='0.0.0.0', port=5005)
