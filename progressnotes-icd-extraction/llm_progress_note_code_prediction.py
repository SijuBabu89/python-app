icd_template = """**Prompt for Medical Coding from Progress Notes**

**Objective:** Utilize the provided progress notes to extract relevant medical conditions. Then, accurately assign the corresponding ICD-10 based on the identified information.

**Instructions:**

1. **Read the Progress Notes Carefully:** Begin by thoroughly reading the provided progress notes. Pay close attention to any diagnoses, symptoms.

2. **Identify Key Medical Conditions:** Extract key medical conditions mentioned in the notes. Look for both primary concerns and any secondary conditions or complications.

3. **Assign ICD-10 Codes:**
   - For each identified medical condition, assign the appropriate ICD-10 code.
   - Ensure to specify if a condition is the primary reason for the visit or a secondary condition.
   - Use the format "Condition - ICD-10 Code (Primary/Secondary)" for clarity.

5. **Format Your Response:** Organize your findings into a structured format as shown below. Ensure all codes are accurate and correctly matched with the conditions or procedures.

6. **Make sure the output is in JSON format and should not contain any other details, so that the output will be consistent in all requests.

**Desired Output Format:**

```json

    "ICD Code": {{[
        "Condition 1 - ICD-10 Code (Primary/Secondary)",
        "Condition 2 - ICD-10 Code",
        "Condition 3 - ICD-10 Code"
    ]}}
```

**Example Progress Notes:**

- Patient presents for screening of colon cancer.
- Noted presence of melanosis coli during examination.
- Patient reports mild discomfort due to internal hemorrhoids.

**Example Response:**

```json

    "ICD Code": {{[
        "Screening for colon cancer - Z12.11 (Primary)",
        "Melanosis coli - K63.89",
        "Internal hemorrhoids - K64.8"
    ]}}

```
Answer the question based only on the following context:
{context}

The text of the progress note is given below:
{progressnote}
."""

cpt_template = """**Prompt for Medical Coding from Progress Notes**

**Objective:** Utilize the provided progress notes to extract relevant procedures. Then, accurately assign the corresponding CPT codes based on the identified information.

**Instructions:**

1. **Read the Progress Notes Carefully:** Begin by thoroughly reading the provided progress notes. Pay close 
attention to procedures.

2. **Identify Procedures:** Extract procedures mentioned in the notes based on the context given.

3. **Assign CPT Codes and Modifiers:**
  - For each procedure or treatment mentioned, assign the corresponding CPT code.
  - If multiple procedures are mentioned, list each CPT code separately.
  - Include any relevant CPT modifiers as needed.
  - Show the duplicate modifiers if any.

5. **Format Your Response:** Organize your findings into a structured format as shown below. Ensure all codes are accurate and correctly matched with the procedures.

6. **Make sure the output is in JSON format and should not contain any other details, so that the output will be consistent in all requests.

    **Desired Output Format:**

    ```json

     "CPT Code": {{['Code': 'CPT Code 1', 'Description':'CPT Description 1', 'Modifiers'=['Modifier1', 'Modifier2'],
     'Code': "CPT Code 2", 'Description':'CPT Description 2', 'Modifiers'=['Modifier3']]}}

```

**Example Progress Notes:**

- Patient presents for screening of colon cancer.
- Noted presence of melanosis coli during examination.
- Patient reports mild discomfort due to internal hemorrhoids.

**Example Response:**
    ```json

    "CPT Code": {{["Code":"45380", "Description":"Patient presents for screening of colon cancer", "Modifiers":['22','44'],
    "Code":"45381", "Description":"Noted presence of melanosis coli during examination", "Modifiers":['33']]}}

```
    
Answer the question based only on the following context:
{context}

The text of the progress note is given below:
{progressnote}
."""


import os
from langchain.vectorstores import Pinecone as PineconeStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import json

vector_index = "medical-note-icd-code"
embedding_model = "text-embedding-ada-002"
openai_key = "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"
openai_model = "gpt-4-turbo-preview"

embeddings = OpenAIEmbeddings(model=embedding_model)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or openai_key

chat_model = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model=openai_model
)
vector_store = PineconeStore.from_existing_index(vector_index, embeddings)


def predict_icd_code(icd_descriptions):
    if len(icd_descriptions) < 1:
        return ""
    retriever = vector_store.as_retriever(search_kwargs={'filter': {'Type': 'ICDCode'}})
    prompt = ChatPromptTemplate.from_template(icd_template)
    chain = (
            {"context": retriever,  "progressnote": RunnablePassthrough()}
            | prompt
            | chat_model
            | StrOutputParser()
    )
    result = chain.invoke(icd_descriptions)
    print(result)
    result = result.replace("\n", "").replace("```", "").replace("json", "").replace("'", "")
    json_data = json.loads(result)
    output_string = " | ".join(json_data["ICD Code"])
    return output_string


def predict_cpt_code(cpt_descriptions):
    if len(cpt_descriptions) < 1:
        return ""
    retriever = vector_store.as_retriever(search_kwargs={'filter': {'Type': 'CPTCode'}})
    prompt = ChatPromptTemplate.from_template(cpt_template)
    chain = (
            {"context": retriever, "progressnote": RunnablePassthrough()}
            | prompt
            | chat_model
            | StrOutputParser()
    )
    result = chain.invoke(cpt_descriptions)
    result = result.replace("\n", "").replace("```", "").replace("json", "").replace("'", "")
    print(result)
    json_data = json.loads(result)
    output_list = []
    output_string = ""
    if json_data:
        for entry in json_data["CPT Code"]:
            code = entry["Code"]
            description = entry["Description"]
            modifiers = entry["Modifiers"]
            output_list.append(f"{code} - {description} , Modifiers - {modifiers}")
        output_string = ' | '.join(output_list)
    return output_string
