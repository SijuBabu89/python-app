import streamlit as st
import json
import re

# Sample API output
api_output = '''
{
    "Output": {
        "result": "{    "result": {        "ICD Code": ["Screening for colon cancer - Z12.11 (Primary)", "Melanosis coli - K63.89", "Internal hemorrhoids - K64.8"],         "CPT Code": ["A4550", "5656"]    }}",
        "source_documents": [
            {
                "metadata": {
                    "CPT Codes": "99214",
                    "File Name": "291139.pdf",
                    "ICD Codes": "1. Obesit y - E66.9 2. Bloating - R14.0 (Primary) 3. Gastric intestinal metaplasia, unspecified - K31.A0 4. Gastritis - K29.70",
                    "id": "1"
                },
                "page_content": " Progress Note : Subjective:\nChief Complaints:\n 1. *EGD R esults.\nHPI:\n New S ymptom : \n 47 y/o patient with h/o incomplete defecation, chronic constipation, gastric ulcer is here for a follow up after\nan EGD . EGD show LA gr ade A esophagitis, gastritis, and a normal duodenum. P ath report shows stomach antrum\nfocal intestinal metaplasia. P atient advised to repeat EGD in 3 y ears for surv eillance. R esults discussed with\npatient. Significance of findings and importance of surv eillance explained to patient. Anti reflux measures including\nincrease ph ysical activit y explained to patient. All patient questions were answered. P atient understand and agrees\nto plan.\n R equesting refill on metoclopr amide. Uses it prn bloating. C/o constipation at times. Has mir alax at home she\nwill use PRN.\nROS: \n Gener al/Constitutional : \n Denies Change in appetite. Denies Chills. Denies Fatigue. Denies Fever. \n ENT: \n Denies Decreased hearing. Denies Decreased sense of smell. Denies Difficult y swallowing. Denies Dry\nmouth. Denies Ear pain. \n Respiratory: \n Denies Chest pain. Denies Cough. Denies Shortness of breath at rest. Denies Shortness of breath with\nexertion. Denies Wheezing. \n Cardio vascular : \n Denies Chest pain at rest. Denies Chest pain with ex ertion. Denies Dizziness. Denies Dyspnea on\nexertion. Denies Palpitations. \n Gastrointestinal : \n Denies Abdominal pain. Denies Blood in stool. Denies Change in bowel habits. Denies Constipation. \nDenies Decreased appetite. Denies Diarrhea. Denies Difficult y swallowing. Denies Heartburn. \nDenies Hematemesis. Denies Nausea. Denies Rectal bleeding. Denies Vomiting. Denies Weight loss. \n Hematology : \n Denies Easy bruising. Denies Swollen glands. \n Genitourinary : \n Denies Blood in urine. Denies Difficult y urinating. Denies Frequent urination. \n Musculosk eletal : \n Denies Joint stiffness. Denies Leg cr amps. Denies Muscle aches. \n Skin: \n Denies Discolor ation. Denies Dry skin. \n Neurologic : \n Denies Balance difficult y. Denies Coordination. Denies Difficult y speaking. Denies Dizziness. \nDenies Fainting. \n \nMedical History: Hypertension, Hypoth yroidism.\nSurgical History: had skin mass remo val 2019, h ysterectom y 2002.\nProvider: David C. Chua, M.D. Date: 08/04/20232/4/24, 11:00 AM eCW (Aveta, Bot )\nhttps://ilasdlapp.ecwcloud.com/mobiledoc/jsp/webemr/index.jsp#/mobiledoc/jsp/webemr/webpm/claimLookup.jsp 2/3DOMINGUEZ, Beatriz DOB: 10/20/1975 (47 yo F) Acc No. 66303 DOS: 08/04/2023\nHospitalization/Major Diagnostic Procedure: Denies P ast Hospitalization.\nFamily History: \nNo family history of cancer .\nSocial History: \n Tobacco Use: Tobacco Use/Smoking Are y ou a nonsmok er. Tobacco use other than smoking Are y ou an other\ntobacco user? No . \n Drugs/Alcohol: Alcohol Screen Did you ha ve a drink containing alcohol in the past y ear? No , Points\n 0, Interpretation Negativ e. \nMedications: Taking Aspirin , Notes to Pharmacist: 81mg, T aking Lev othyroxine Sodium 50 MCG T ablet 1 tablet in\nthe morning on an empt y stomach Or ally Once a da y , Taking Losartan P otassium 100 MG T ablet 1 tablet Or ally\nOnce a da y , Taking Metoclopr amide HCl 10 MG T ablet 1 tablet Or ally Bedtime , T aking Omepr azole 40 MG Capsule\nDelayed Release T AKE 1 CAPSULE BY MOUTH TWICE DAIL Y 1 HOUR BEFORE BREAKF AST AND DINNER , Not -\nTaking/PRN Magnesium Citr ate 1.745 GM/30ML Solution as directed Or ally 6 hours before procedure , Not -\nTaking/PRN Golytely 236 GM Solution R econstituted as directed Or ally As Directed , Not -Taking/PRN Dulcolax 5 MG\nTablet Dela yed Release 4 tablet as needed Or ally Da y before procedure , Not -Taking/PRN Milk of Magnesia 400\nMG/5ML Suspension 45 ml Or ally 3 T ablespoonsful once a da y at bedtime , Not -Taking/PRN Dulcolax 5 MG T ablet\nDelayed Release 4 tablet as needed Or ally Da y before procedure , Medication List reviewed and reconciled with the\npatient\nAllergies: N.K.D .A.\nObjective:\nVitals: Temp: 98.2 F, HR: 88 /min, BP: 138/89 mm Hg, Ht: 5ft 3in , Wt: 185.8 lbs, BMI: 32.91 Index.\nExamination:\n gi physical examination:\n GENERAL APPEARANCE: in no acute distress , well dev eloped, well nourished . \n HEAD: normocephalic , atraumatic . \n EYES: no icterus . \n NECK/THYROID: neck supple, full r ange of motion , no cervical lymphadenopath y. \n SKIN: no suspicious lesions , warm and dry . \n HEAR T: no murmurs , regular r ate and rh ythm, S1, S2 normal . \n LUNGS: clear to auscultation bilater ally. \n ABDOMEN: normal , bowel sounds present , soft, nontender , nondistended . . \n EXTREMITIES: no clubbing, cy anosis, or edema . \n NEUROL OGIC: nonfocal , motor strength normal upper and lower extremities , sensory exam intact . \nAssessment:\nAssessment:\n1. Obesit y - E66.9 \n2. Bloating - R14.0 (Primary) \n3. Gastric intestinal metaplasia, unspecified - K31.A0 \n4. Gastritis - K29.70 \nPlan:\nTreatment:\n1. Bloating \nStart Metoclopr amide HCl T ablet, 10 MG, 1 tablet, Or ally, as needed for bloating, 30 da ys, 30, R efills 3 . \nNotes: Can use mir alax daily for constipation/bloating. Use metoclopr amide prn. W ays to impro ve constipation\ndiscussed with patient including increasing dietary fiber , water, exercise and weight reduction. R ecommended\nmiralax daily and milk of magnesia 2-3 times per week if needed. \n2. Obesity \nNotes: Long discussion with patient about how weight loss will help patients constipation and acid reflux. Advised\npt to start ex ercising and eating healither . Decrease portion siz es. \nProvider: David C. Chua, M.D. Date: 08/04/20232/4/24, 11:00 AM eCW (Aveta, Bot )\nhttps://ilasdlapp.ecwcloud.com/mobiledoc/jsp/webemr/index.jsp#/mobiledoc/jsp/webemr/webpm/claimLookup.jsp 3/3DOMINGUEZ, Beatriz DOB: 10/20/1975 (47 yo F) Acc No. 66303 DOS: 08/04/2023\n3. Gastric intestinal metaplasia, unspecified \nNotes: R epeat EGD in 3 yrs. for surviellance. \nPreventive Medicine: \n Counseling: Care goal follow -up plan: Abo ve Normal BMI F ollow-up Dietary management education, guidance,\nand counseling, Below Normal BMI F ollow-up Dietary education for weight gain, Nutrition/Dietary Counseling\nprovided Y es. \nFollow Up: 6 Months\n \nElectr onically signed by DA VID CHUA , MD, 036069933 on 08/17/2023 at 09:17 PM CDT\nSign off status: Completed\nProvider: David C. Chua, M.D. Date: 08/04/2023, The ICD Codes for this progress note are : 1. Obesit y - E66.9 2. Bloating - R14.0 (Primary) 3. Gastric intestinal metaplasia, unspecified - K31.A0 4. Gastritis - K29.70, The CPT Codes for this progress note are : 99214",
                "type": "Document"
            }
        ]
    }
}
'''

# Parse JSON output
api_output = re.sub(r'[^a-zA-Z0-9 {}:\[\],.-]', '', api_output)
# print(api_output)
# api_output = re.search(r'"result":\s*{(.*?)}', api_output, re.DOTALL).group(1)

api_output = json.loads(api_output)
inner_result = json.loads(api_output["Output"]["result"])

# Extract relevant information
icd_codes = inner_result["ICD Code"]
cpt_codes = inner_result["CPT Code"]
file_name = api_output["Output"]["source_documents"][0]["metadata"]["File Name"]

# Create Streamlit app
st.title("Progress Note API Output")

# Add text area for user input
user_input = st.text_area("Enter your text here:")

# Add dropdown for user selection
options = ["Option 1", "Option 2", "Option 3"]
selected_option = st.selectbox("Select an option:", options)

# Display file name
st.subheader(f"File Name: {file_name}")

# Display ICD Codes
st.subheader("ICD Codes:")
for icd_code in icd_codes:
    st.write(f"- {icd_code}")

# Display CPT Codes
st.subheader("CPT Codes:")
for cpt_code in cpt_codes:
    st.write(f"- {cpt_code}")

# Display user input and selected option after submission
if st.button("Submit"):
    st.subheader("User Input:")
    st.write(user_input)

    st.subheader("Selected Option:")
    st.write(selected_option)