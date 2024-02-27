import requests
import fitz  # PyMuPDF

url = "https://trial.jiffy.ai/auth/realms/aveta/protocol/openid-connect/token"
name = 'apexuser2@yopmail.com'
key = 'Welcome'
clientId = 'cb04118f-f5c1-4914-95e7-d233966a05d9'
pdf_file_path = "https://health-central.develop.aveta.trial.jiffy.ai/platform/drive/v1/objects/"


def get_auth_token():
    s = requests.Session()
    authPayload = 'grant_type=password&scope=openid email profile&username={}&password={}&client_id={}'
    payload = authPayload.format(name, key, clientId)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = s.post(url, headers=headers, data=payload)
    return response.json()["access_token"]


def extract_pfd_content(pdf_file):
    file_path_url = pdf_file_path + pdf_file
    print('File Path : '+file_path_url)
    payload = {}
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': 'Bearer ' + get_auth_token(),
    }
    response = requests.request("GET", file_path_url, headers=headers, data=payload)
    pdf_text_content = ""
    print(response.status_code)
    if response.status_code == 200:
        pdf_document = fitz.open(stream=response.content, filetype="pdf")
        # Iterate through each page
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            pdf_text_content += page.get_text()
    return pdf_text_content
