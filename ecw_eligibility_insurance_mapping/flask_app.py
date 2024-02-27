from flask import Flask, request, abort
import json
from milvus_impl import *

app = Flask(__name__)

@app.route('/')
def ecw_insurance_mapping():
    return 'ECW Insurance Mapping!'


@app.route('/insurance_similarity-search', methods=['POST'])
def similarity_search():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    insurance_result = ''
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    payer_name = request.get_json().get('payer_name')
    plan_name = request.get_json().get('plan_name')
    insurance_type = request.get_json().get('insurance_type')
    payer_name = "" if payer_name is None else payer_name
    plan_name = "" if plan_name is None else plan_name
    insurance_type = "" if insurance_type is None else insurance_type
    query = payer_name + ' ' + plan_name + ' ' + insurance_type
    return get_ecw_insurance(query)


@app.route('/insurance_search_result', methods=['POST'])
def similarity_search_result():
    app_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICIwcmZ2ajh6X2hSTjFpMFpLeXplZ2pUdERTNXA5dkRORkE5RWFsbTFnQ0RBIn0"
    auth_token = request.headers.get('Authorization')
    insurance_result = ''
    if auth_token is not None:
        auth_token = auth_token.split(" ")[1]
    if app_token != auth_token:
        abort(401, "Unauthorized access")
    payer_name = request.get_json().get('payer_name')
    plan_name = request.get_json().get('plan_name')
    insurance_type = request.get_json().get('insurance_type')
    payer_name = "" if payer_name is None else payer_name
    plan_name = "" if plan_name is None else plan_name
    insurance_type = "" if insurance_type is None else insurance_type
    query = payer_name + ' ' + plan_name + ' ' + insurance_type
    result = get_ecw_insurance_list(query)
    print(result)
    return result

if __name__ == '__main__':
    print("---- Into the main Function ----")
    app.run(debug=True, host='0.0.0.0', port=5010)