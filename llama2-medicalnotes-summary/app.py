import torch
import transformers
from transformers import AutoTokenizer
from  langchain import LLMChain, HuggingFacePipeline, PromptTemplate
import os

text = """
Subjective:
Chief Complaints:
1. *f/u post CLN.
HPI:
New Symptom:
53 y/o male pt with a hx of adenomatous polyp of colon, hepatic steatosis, and high grade dysplasia in colonic
adenoma is here for a f/u after a CLN. CLN showed one fragment of hyperplastic polyp in the descending colon,
one hyperplastic polyp in the sigmoid colon, four fragments of hyperplastic polyps in the rectum, stool in entire
examined colon, and diverticulosis in sigmoid colon. Results discussed with patient. Significance of findings and
importance for surveillance explained to patient. Advise patient to repeat colonoscopy in 1 years for surveillance.
All patient questions were answered. Patient understand and agrees to plan. Pt did complain of bloating and gas.
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
Medical History: Diverticulosis, Dysplasia.
Surgical History: Colonoscopy 2021.
Hospitalization/Major Diagnostic Procedure: Denies Past Hospitalization.
Family History: Father: deceased, multiple maloma, diagnosed with Cancer. Mother: deceased, multiple
maloma, diagnosed with Cancer. Maternal Grand Mother: deceased, cancer.

9/13/23, 12:14 PM

Social History:
Tobacco Use: Tobacco Use/Smoking Are you a nonsmoker. Tobacco use other than smoking Are you an other
tobacco user? No.
Drugs/Alcohol: Drugs Have you used drugs other than those for medical reasons in the past 12 months?
No. Alcohol Screen Did you have a drink containing alcohol in the past year? Yes, How often did you have a drink
containing alcohol in the past year? 2 to 3 times a week (3 points), How many drinks did you have on a typical
day when you were drinking in the past year? 3 or 4 drinks (1 point), How often did you have 6 or more drinks on
one occasion in the past year? Never (0 point), Points 4, Interpretation Positive.
Medications: Not-Taking/PRN Dulcolax 5 MG Tablet Delayed Release take 4 tablets followed by 2 glasses of water
a day before procedure at 6 pm Orally Once a day, Medication List reviewed and reconciled with the patient
Allergies: N.K.D.A.
Objective:
Vitals: Temp 97.0 F, HR 98 /min, BP 195/116 mm Hg, 159/109 mm Hg, Ht 5 ft 9 in, Wt 224 lbs, BMI 33.08
Index.
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
Assessment:
Assessment:
1. Diverticulosis - K57.90
2. Hyperplastic colon polyp - K63.5 (Primary)
3. Internal hemorrhoids - K64.8
4. Fatty liver - K76.0
Plan:
1. Hyperplastic colon polyp
Notes: repeat colonoscopy in 1 year for surveillance due to multiple polyps and poor prep.
2. Fatty liver
Notes: advised pt weight reduction, reduction in alcohol/carbs/processed foods/sugar, increase in exercise
repeat fibroscan 1 year from previous.
Immunizations:
Immunization record has been reviewed and updated.
Preventive Medicine:
Counseling: Care goal follow-up plan: BMI management provided Yes, Above Normal BMI Follow-up Dietary
management education, guidance, and counseling.
Follow Up: prn
"""
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "hf_jBWRqbgAgvJlZyaZoTTTQTvnyiKIYmrriME"
model = "meta-llama/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model, token='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')

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
    max_length=3000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id
)

llm = HuggingFacePipeline(pipeline = pipeline, model_kwargs = {'temperature':0})

template = """
              Please provide me different sections of the medical notes and the type of the document
              ```{text}```
              SUMMARY:
           """
prompt = PromptTemplate(template=template, input_variables=["text"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

print(llm_chain.run(text))
