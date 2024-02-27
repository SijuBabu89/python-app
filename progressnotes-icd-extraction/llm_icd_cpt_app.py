import os
from operator import itemgetter
import json
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain_community.vectorstores import Pinecone

template = """**Prompt for Medical Coding from Progress Notes**

**Objective:** Utilize the provided progress notes to extract relevant medical conditions and procedures. Then, accurately assign the corresponding ICD-10 and CPT codes based on the identified information.

**Instructions:**

1. **Read the Progress Notes Carefully:** Begin by thoroughly reading the provided progress notes. Pay close attention to any diagnoses, symptoms, procedures, and treatments mentioned.

2. **Identify Key Medical Conditions and Procedures:** Extract key medical conditions and procedures mentioned in the notes. Look for both primary concerns and any secondary conditions or complications.

3. **Assign ICD-10 Codes:**
   - For each identified medical condition, assign the appropriate ICD-10 code. 
   - Ensure to specify if a condition is the primary reason for the visit or a secondary condition.
   - Use the format "Condition - ICD-10 Code (Primary/Secondary)" for clarity.

4. **Assign CPT Codes:**
   - For each procedure or treatment mentioned, assign the corresponding CPT code.
   - If multiple procedures are mentioned, list each CPT code separately.

5. **Format Your Response:** Organize your findings into a structured format as shown below. Ensure all codes are accurate and correctly matched with the conditions or procedures.

**Desired Output Format:**

```json

    "ICD Code": [
        "Condition 1 - ICD-10 Code (Primary/Secondary)",
        "Condition 2 - ICD-10 Code",
        "Condition 3 - ICD-10 Code"
    ],
    "CPT Code": [
        "CPT Code 1",
        "CPT Code 2"
    ]

```

**Example Progress Notes:**

- Patient presents for screening of colon cancer.
- Noted presence of melanosis coli during examination.
- Patient reports mild discomfort due to internal hemorrhoids.

**Example Response:**

```json

    "ICD Code": [
        "Screening for colon cancer - Z12.11 (Primary)",
        "Melanosis coli - K63.89",
        "Internal hemorrhoids - K64.8"
    ],
    "CPT Code": [
        "A4550",
        "J7040"
    ]

```
Answer the question based only on the following context:
{context}

The text of the progress note is given below:
{progressnote}
."""

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY") or "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"
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

chat_model = ChatOpenAI(
    openai_api_key=os.environ["OPENAI_API_KEY"],
    model='gpt-4-turbo-preview'
)


def get_progress_note_result(progressnote):
    prompt = ChatPromptTemplate.from_template(template)
    vector_store = Pinecone.from_existing_index("medical-note-icd-code", embeddings)
    retriever = vector_store.as_retriever()
    chain = (
            {"context": retriever, "progressnote": RunnablePassthrough()}
            | prompt
            | chat_model
            | StrOutputParser()
    )
    result = chain.invoke(progressnote)
    result = result.replace("json", "").replace("```", "")
    json_data = json.loads(result)
    return json_data
