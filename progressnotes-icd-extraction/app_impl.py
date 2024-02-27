from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import OpenAI
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Pinecone
import json
from pinecone_impl import *

query = """I want to find the ICD codes in the below progress notes, based on the data you have in the vector store.
Following is the Progress Note : 

"""
embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

progressnotes ="""2/4/24, 11:00 AM eCW (Aveta, Bot )
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

def get_response(progress_note):
    query + " progress_note"
    # llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.0)
    # llm = ChatOpenAI(model='gpt-4-1106-preview', temperature=1)
    vector_store = get_existing_index()
    #vector_store = Pinecone.from_existing_index("medical-note-icd-code", embeddings)
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={'k': 2})
    # retriever = vector_store.as_retriever(search_type='mmr', search_kwargs={'k':1})
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever,
                                     return_source_documents=True)
    # qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
    # chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    # answer = chain.run(query)
    answer = qa({"query": query})
    # print('_____________________________ OPEN AI RESULT _______________________________')
    # print(answer)
    # print('__________________________________ END _____________________________________')


def get_answer(progress_note):
    answer = get_response(progress_note)

    # Assuming the 'source_documents' list contains instances of a 'Document' class
    class Document:
        def __init__(self, page_content, metadata):
            self.page_content = page_content
            self.metadata = metadata

    # Convert to JSON
    json_result = json.dumps(answer, default=lambda obj: obj.__dict__, indent=2)

    # Print the JSON
    json_result

get_answer(progressnotes)