import streamlit as st
#from dotenv import load_dotenv
from utils import *
from pypdf import PdfReader
from io import BytesIO


def main():
    #load_dotenv()

    st.set_page_config(page_title="Invoice Extraction Bot")
    st.title("Invoice Extraction Bot...💁 ")
    st.subheader("I can help you in extracting invoice data")


    # Upload the Invoices (pdf files)
    pdf = st.file_uploader("Upload invoices here, only PDF files allowed", type=["pdf"],accept_multiple_files=True)
    #-------------------------------------------------------------------------------------
    submit = st.button("Extract Data")
    if submit:
        # print(pdf)
        file_bytes = pdf[0]
        # file_contents = file_bytes.read()
        pdf_reader = PdfReader(file_bytes)
        print(pdf_reader)
        text = ""
        for page in pdf_reader.pages:
            print(pdf_reader.pages)
            print('page')
            print(page.extract_text())
            text += page.extract_text()
        return text
        print(text)

    #_____________________________________________________________________________________

    #submit=st.button("Extract Data")

    # if submit:
    #     with st.spinner('Wait for it...'):
    #         df=create_docs(pdf)
    #         st.write(df.head())
    #
    #         data_as_csv= df.to_csv(index=False).encode("utf-8")
    #         st.download_button(
    #             "Download data as CSV",
    #             data_as_csv,
    #             "benchmark-tools.csv",
    #             "text/csv",
    #             key="download-tools-csv",
    #         )
    #     st.success("Hope I was able to save your time❤️")


#Invoking main function
if __name__ == '__main__':
    main()