import streamlit as st
import os

def process_files(folder_path):
    file_contents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                content = file.read()
                file_contents.append((filename, content))
    return file_contents


def execute_main():
    st.title("PDF Upload, Display, and Save App")

    # Upload PDF through Streamlit
    folder_path = st.sidebar.selectbox("Select Folder", os.listdir())
    folder_path = os.path.join(os.getcwd(), folder_path)
    # Display selected folder
    st.write(f"Selected Folder: {folder_path}")
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            save_path = save_pdf(uploaded_file)
            pdf2img.pdf2img(save_path)
            doc_name = save_path.split("/")[-1].split(".")[0]
            table_coordinates(document_name=doc_name)
            whiten.whiten_table_region(doc_name=doc_name)

            main.main(doc_name=doc_name)
            export_pdf.output_pdf(doc_name=doc_name)

            output_path = "utils_table/out/" + doc_name + "/"
            if os.path.exists(output_path):
                output_path_dirs = os.listdir(output_path)
                i = 0
                for dirs in output_path_dirs:
                    files = os.listdir(output_path + dirs)
                    for file in files:
                        if file.endswith(".pdf"):
                            displayPDF(output_path + dirs + "/" + file)

                # if file.endswith(".pdf"):
                #     displayPDF(output_path + file)

                st.success(f"All PDFs have been displayed!")
            else:
                st.error(f"No PDFs were generated")




# Streamlit app
def main():
    st.title("File Processor App")

    # Select a folder
    folder_path = st.sidebar.selectbox("Select Folder", os.listdir())
    folder_path = os.path.join(os.getcwd(), folder_path)

    # Display selected folder
    st.write(f"Selected Folder: {folder_path}")

    # Button to process files
    if st.button("Process Files"):
        file_contents = process_files(folder_path)

        # Display file contents
        st.subheader("File Contents:")
        for filename, content in file_contents:
            st.write(f"### {filename}")
            st.code(content, language='text')

if __name__ == "__main__":
    main()