import os
from pinecone import Pinecone, ServerlessSpec
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Pinecone as pine_cone
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAI
import json

os.environ["PINECONE_API_KEY"] = '39cbaf61-6cc2-4f1d-a90d-0d8b19e8d9ee'
os.environ["OPENAI_API_KEY"] = "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"
index_name = 'medical-note-icd-code'
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')


def create_index(index_name):
    pine_cone.create_index(
        name=index_name,
        dimension=384,
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )


def insert_vector_documents(docs):
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    docsearch = pine_cone.from_documents(docs, embeddings, index_name=index_name)
    # Pinecone.from_existing_index(index_name, embeddings)


def get_existing_index():
    pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
    return pine_cone.from_existing_index(index_name, embeddings)


progressnotes_temp = """2/4/24, 11:00 AM eCW (Aveta, Bot )
https://ilasdlapp.ecwcloud.com/mobiledoc/jsp/webemr/index.jsp#/mobiledoc/jsp/webemr/webpm/claimLookup.jsp 1/3DOMINGUEZ, Beatriz DOB: 10/20/1975 (47 yo F) Acc No. 66303 DOS: 08/04/2023
Progress Notes

Patient: Dominguez, Beatriz
Account Number: 66303Provider: David C. Chua, M.D .
DOB: 10/20/1975 Age: 47 Y Sex: Female Date: 08/04/2023
Phone: 708-983-4107
Address: 711 S 3rd A ve, Ma ywood, IL -60153
Pcp: Myrna M P atricio , MD
Subjective:
Chief Complaints:
 1. *EGD R esults.
HPI:
 New S ymptom :
 47 y/o patient with h/o incomplete defecation, chronic constipation, gastric ulcer is here for a follow up after
an EGD . EGD show LA gr ade A esophagitis, gastritis, and a normal duodenum. P ath report shows stomach antrum
focal intestinal metaplasia. P atient advised to repeat EGD in 3 y ears for surv eillance. R esults discussed with
patient. Significance of findings and importance of surv eillance explained to patient. Anti reflux measures including
increase ph ysical activit y explained to patient. All patient questions were answered. P atient understand and agrees
to plan.
 R equesting refill on metoclopr amide. Uses it prn bloating. C/o constipation at times. Has mir alax at home she
will use PRN.
ROS:
 Gener al/Constitutional :
 Denies Change in appetite. Denies Chills. Denies Fatigue. Denies Fever.
 ENT:
 Denies Decreased hearing. Denies Decreased sense of smell. Denies Difficult y swallowing. Denies Dry
mouth. Denies Ear pain.
 Respiratory:
 Denies Chest pain. Denies Cough. Denies Shortness of breath at rest. Denies Shortness of breath with
exertion. Denies Wheezing.
 Cardio vascular :
 Denies Chest pain at rest. Denies Chest pain with ex ertion. Denies Dizziness. Denies Dyspnea on
exertion. Denies Palpitations.
 Gastrointestinal :
 Denies Abdominal pain. Denies Blood in stool. Denies Change in bowel habits. Denies Constipation.
Denies Decreased appetite. Denies Diarrhea. Denies Difficult y swallowing. Denies Heartburn.
Denies Hematemesis. Denies Nausea. Denies Rectal bleeding. Denies Vomiting. Denies Weight loss.
 Hematology :
 Denies Easy bruising. Denies Swollen glands.
 Genitourinary :
 Denies Blood in urine. Denies Difficult y urinating. Denies Frequent urination.
 Musculosk eletal :
 Denies Joint stiffness. Denies Leg cr amps. Denies Muscle aches.
 Skin:
 Denies Discolor ation. Denies Dry skin.
 Neurologic :
 Denies Balance difficult y. Denies Coordination. Denies Difficult y speaking. Denies Dizziness.
Denies Fainting.

Medical History: Hypertension, Hypoth yroidism.
Surgical History: had skin mass remo val 2019, h ysterectom y 2002.
Provider: David C. Chua, M.D. Date: 08/04/20232/4/24, 11:00 AM eCW (Aveta, Bot )
https://ilasdlapp.ecwcloud.com/mobiledoc/jsp/webemr/index.jsp#/mobiledoc/jsp/webemr/webpm/claimLookup.jsp 2/3DOMINGUEZ, Beatriz DOB: 10/20/1975 (47 yo F) Acc No. 66303 DOS: 08/04/2023
Hospitalization/Major Diagnostic Procedure: Denies P ast Hospitalization.
Family History:
No family history of cancer .
Social History:
 Tobacco Use: Tobacco Use/Smoking Are y ou a nonsmok er. Tobacco use other than smoking Are y ou an other
tobacco user? No .
 Drugs/Alcohol: Alcohol Screen Did you ha ve a drink containing alcohol in the past y ear? No , Points
 0, Interpretation Negativ e.
Medications: Taking Aspirin , Notes to Pharmacist: 81mg, T aking Lev othyroxine Sodium 50 MCG T ablet 1 tablet in
the morning on an empt y stomach Or ally Once a da y , Taking Losartan P otassium 100 MG T ablet 1 tablet Or ally
Once a da y , Taking Metoclopr amide HCl 10 MG T ablet 1 tablet Or ally Bedtime , T aking Omepr azole 40 MG Capsule
Delayed Release T AKE 1 CAPSULE BY MOUTH TWICE DAIL Y 1 HOUR BEFORE BREAKF AST AND DINNER , Not -
Taking/PRN Magnesium Citr ate 1.745 GM/30ML Solution as directed Or ally 6 hours before procedure , Not -
Taking/PRN Golytely 236 GM Solution R econstituted as directed Or ally As Directed , Not -Taking/PRN Dulcolax 5 MG
Tablet Dela yed Release 4 tablet as needed Or ally Da y before procedure , Not -Taking/PRN Milk of Magnesia 400
MG/5ML Suspension 45 ml Or ally 3 T ablespoonsful once a da y at bedtime , Not -Taking/PRN Dulcolax 5 MG T ablet
Delayed Release 4 tablet as needed Or ally Da y before procedure , Medication List reviewed and reconciled with the
patient
Allergies: N.K.D .A.
Objective:
Vitals: Temp: 98.2 F, HR: 88 /min, BP: 138/89 mm Hg, Ht: 5ft 3in , Wt: 185.8 lbs, BMI: 32.91 Index.
Examination:
 gi physical examination:
 GENERAL APPEARANCE: in no acute distress , well dev eloped, well nourished .
 HEAD: normocephalic , atraumatic .
 EYES: no icterus .
 NECK/THYROID: neck supple, full r ange of motion , no cervical lymphadenopath y.
 SKIN: no suspicious lesions , warm and dry .
 HEAR T: no murmurs , regular r ate and rh ythm, S1, S2 normal .
 LUNGS: clear to auscultation bilater ally.
 ABDOMEN: normal , bowel sounds present , soft, nontender , nondistended . .
 EXTREMITIES: no clubbing, cy anosis, or edema .
 NEUROL OGIC: nonfocal , motor strength normal upper and lower extremities , sensory exam intact .
Assessment:
Assessment:
1. Obesit y - E66.9
2. Bloating - R14.0 (Primary)
3. Gastric intestinal metaplasia, unspecified - K31.A0
4. Gastritis - K29.70
Plan:
Treatment:
1. Bloating
Start Metoclopr amide HCl T ablet, 10 MG, 1 tablet, Or ally, as needed for bloating, 30 da ys, 30, R efills 3 .
Notes: Can use mir alax daily for constipation/bloating. Use metoclopr amide prn. W ays to impro ve constipation
discussed with patient including increasing dietary fiber , water, exercise and weight reduction. R ecommended
miralax daily and milk of magnesia 2-3 times per week if needed.
2. Obesity
Notes: Long discussion with patient about how weight loss will help patients constipation and acid reflux. Advised
pt to start ex ercising and eating healither . Decrease portion siz es.
Provider: David C. Chua, M.D. Date: 08/04/20232/4/24, 11:00 AM eCW (Aveta, Bot )
https://ilasdlapp.ecwcloud.com/mobiledoc/jsp/webemr/index.jsp#/mobiledoc/jsp/webemr/webpm/claimLookup.jsp 3/3DOMINGUEZ, Beatriz DOB: 10/20/1975 (47 yo F) Acc No. 66303 DOS: 08/04/2023
3. Gastric intestinal metaplasia, unspecified
Notes: R epeat EGD in 3 yrs. for surviellance.
Preventive Medicine:
 Counseling: Care goal follow -up plan: Abo ve Normal BMI F ollow-up Dietary management education, guidance,
and counseling, Below Normal BMI F ollow-up Dietary education for weight gain, Nutrition/Dietary Counseling
provided Y es.
Follow Up: 6 Months

Electr onically signed by DA VID CHUA , MD, 036069933 on 08/17/2023 at 09:17 PM CDT
Sign off status: Completed
Provider: David C. Chua, M.D. Date: 08/04/2023"""


def get_response(progress_note, model):
    progress_note = "" if len(progressnotes_temp) < 1 else progress_note
    # query = """Pretend you as a medical expert, Based on the data you have in the vector store. Please predict the ICD and CPT code from the below progress note.
    #
    # Output should be in below format :
    # result = ['Screening for colon cancer - Z12.11 (Primary)','Melanosis coli - K63.89 3','Internal hemorrhoids - K64.8']
    #
    # Following is the Progress Note :
    # """ + progress_note

    query = """"As a medical professional utilizing the information stored in the vector store, kindly forecast the corresponding ICD and CPT codes based on the provided progress note. The expected output json format is as follows:

    "result":{"ICD Code": ['Screening for colon cancer - Z12.11 (Primary)', 'Melanosis coli - K63.89', 'Internal hemorrhoids - K64.8'], "CPT Code": ['A4550','J7040']}

    The detailed progress note is provided below: """ + progress_note



    custm_query = """"**Prompt for Medical Coding from Progress Notes**

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
{
    "ICD Code": [
        "Condition 1 - ICD-10 Code (Primary/Secondary)",
        "Condition 2 - ICD-10 Code",
        "Condition 3 - ICD-10 Code"
    ],
    "CPT Code": [
        "CPT Code 1",
        "CPT Code 2"
    ]
}
```

**Example Progress Notes:**

- Patient presents for screening of colon cancer.
- Noted presence of melanosis coli during examination.
- Patient reports mild discomfort due to internal hemorrhoids.

**Example Response:**

```json
{
    "ICD Code": [
        "Screening for colon cancer - Z12.11 (Primary)",
        "Melanosis coli - K63.89",
        "Internal hemorrhoids - K64.8"
    ],
    "CPT Code": [
        "A4550",
        "J7040"
    ]
}
```

The text of the progress note is given below:
Subjective:
 Chief Complaints:
  1. CLN Results.
 HPI:
   New Symptom:
      65 y/o female patient is here for a follow up after a screening colonoscopy. Colonoscopy show six 2-3mm
 hyperplatic polyps in the rectum, internal hemorrhoids, diverticulosis, sigmoid colon. Results discussed with
 patient. Significance of findings and importance for surveillance explained to patient. Advise patient to repeat
 colonoscopy in 5 years for surveillance. All patient questions were answered. Patient understand and agrees to
 plan.
      Doing well today. Is a little distressed today - sister died a year ago from pancreatic cancer and was very
 scared about CLN results. Re assurance given. States was told many years ago by PCP that she has a fatty liver.
 ROS:
   General/Constitutional:
      Denies Change in appetite. Denies Chills. Denies Fatigue. Denies Fever.
   ENT:
      Denies Decreased hearing. Denies Decreased sense of smell. Denies Difficulty swallowing. Denies Dry
 mouth. Denies Ear pain.
   Respiratory:
      Denies Chest pain. Denies Cough. Denies Shortness of breath at rest. Denies Shortness of breath with
 exertion. Denies Wheezing.
   Cardiovascular:
      Denies Chest pain at rest. Denies Chest pain with exertion. Denies Dizziness. Denies Dyspnea on
 exertion. Denies Palpitations.
   Gastrointestinal:
      Denies Abdominal pain. Denies Blood in stool. Denies Change in bowel habits. Denies Constipation.
 Denies Decreased appetite. Denies Diarrhea. Denies Difficulty swallowing. Denies Heartburn.
 Denies Hematemesis. Denies Nausea. Denies Rectal bleeding. Denies Vomiting. Denies Weight loss.
   Hematology:
      Denies Easy bruising. Denies Swollen glands.
   Genitourinary:
      Denies Blood in urine. Denies Difficulty urinating. Denies Frequent urination.
   Musculoskeletal:
      Denies Joint stiffness. Denies Leg cramps. Denies Muscle aches.
   Skin:
      Denies Discoloration. Denies Dry skin.
   Neurologic:
      Denies Balance difficulty. Denies Coordination. Denies Difficulty speaking. Denies Dizziness.
 Denies Fainting.

 Medical History: PRE-DM, HTN.
 Surgical History: CLNX2 .
 Hospitalization/Major Diagnostic Procedure: Denies Past Hospitalization.

 Family History: Siblings: diagnosed with Cancer.
 SISTER- PANCREATICS CANCER.
 Social History:
   Tobacco Use: Tobacco Use/Smoking Are you a nonsmoker.
   Drugs/Alcohol: Alcohol Screen Did you have a drink containing alcohol in the past year? No, Points
 0, Interpretation Negative.
 Medications: Taking Valsartan , Taking metFORMIN HCl , Taking Atorvastatin Calcium , Medication List reviewed
 and reconciled with the patient
 Allergies: N.K.D.A.


Objective:
 Vitals: Temp: 96.6 F, HR: 106 /min, BP: 140/70 mm Hg, Ht: 5FT 6IN, Wt: 151.6 lbs, BMI: 24.47 Index.
 Examination:
   gi physical examination:
      GENERAL APPEARANCE: in no acute distress, well developed, well nourished.
      HEAD: normocephalic, atraumatic.
      EYES: no icterus.
      NECK/THYROID: neck supple, full range of motion, no cervical lymphadenopathy.
      SKIN: no suspicious lesions, warm and dry.
      HEART: no murmurs, regular rate and rhythm, S1, S2 normal.
      LUNGS: clear to auscultation bilaterally.
       ABDOMEN: normal, bowel sounds present, soft, nontender, nondistended. .
       EXTREMITIES: no clubbing, cyanosis, or edema.
       NEUROLOGIC: nonfocal, motor strength normal upper and lower extremities, sensory exam intact.

Plan:
 Treatment:
 1. Colon polyps
 Notes: Repeat in 5 years. Reassurance given about colon polyps.
 2. Fatty liver
 Notes: Patient ok to schedule FS in the future if she wants to.
Immunizations:
Immunization record has been reviewed and updated.
Preventive Medicine:
  Screening: Fall Risk Screenings Screening: No falls in the past year, Assessment: Performed, Balance-gait
assessment: Get Up & Go test performed.
 Follow Up: prn; per cln alert."""

    # embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    llm = ChatOpenAI(model=model, temperature=0.0)
    # llm = ChatOpenAI(model='gpt-4-1106-preview', temperature=1)
    vector_store = get_existing_index()
    # vector_store = Pinecone.from_existing_index("medical-note-icd-code", embeddings)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 1})
    #retriever = vector_store.as_retriever(search_type='mmr', search_kwargs={'k':2})
    #qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    # chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    # answer = chain.run(query)
    answer = qa({"query": custm_query})
    # print('_____________________________ OPEN AI RESULT _______________________________')
    # print(answer)
    # print('__________________________________ END _____________________________________')
    return answer


def get_answer(progress_note, model):
    answer = get_response(progress_note, model)
    print("Inside : " + " get_answer(progress_note) ")
    print(answer)

    # Assuming the 'source_documents' list contains instances of a 'Document' class
    class Document:
        def __init__(self, page_content, metadata):
            self.page_content = page_content
            self.metadata = metadata

    # Convert to JSON
    json_result = json.dumps(answer, default=lambda obj: obj.__dict__, indent=2)

    # Print the JSON
    return json_result




