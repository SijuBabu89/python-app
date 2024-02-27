from transformers import BertModel, BertTokenizer, BertForTokenClassification, AutoTokenizer, AutoModel
import torch
import torch.nn as nn
import tensorflow as tf

local_model_path = "C:/workspace/myspace/clinical_bert-fine_tuned"

# Load the model and tokenizer
#model = AutoModel.from_pretrained(local_model_path)
#tokenizer = AutoTokenizer.from_pretrained(local_model_path)

tokenizer = BertTokenizer.from_pretrained(local_model_path)
model = BertForTokenClassification.from_pretrained(local_model_path)
print(tokenizer)

text = """
     59 y/o male patient with h/o dyspepsia, esophageal ulcer, and overweight is here for a follow up after a
colonoscopy/EGD. Colonoscopy show examined portion of the ileum was normal, a single colonic ulcer in the
cecum, erythematous mucosa in the rectum, and internal hemorrhoids. Advise patient to repeat colonoscop y
based on pathology for surveillance. EGD show LA grade C esophagitis, esophageal ulcers, gastroparesis,
gastritis, and a normal duodenum. Path report show no significant histopathology on esophagus or stomach.
Patient advised to repeat EGD in 3 months to check for healing and for surveillance. Results discussed with
patient. Significance of findings and importance of surveillance explained to patient. Anti reflux measures
including increase physical activity explained to patient. All patient questions were answered. Patient understand
and agrees to plan.  
Medical History:   Diabetic, Htn.9/13/23, 11:33 AM Print Preview
2/3Hospitalization/Major Diagnostic Procedure:  Denies Past Hospitalization.
Family History:  Mother: deceased, stomach cancer, diagnosed with Cancer.  Maternal uncle: alive, prostate  
cancer, diagnosed with Cancer. 
Social History: 
   Tobacco Use:  Tobacco Use/Smoking  Are you a  nonsmoke r. Tobacco use other than smoking  Are you an other  
tobacco user?  No. 
Medications: Taking Losartan Potassium-HCTZ 100-12.5 MG Tablet Orally , Taking metFORMIN HCl 1000 MG  
Tablet 1 tablet with a meal Orally Once a day , Taking Metoprolol Succinate 50 MG Tablet Extended Release as  
directed Orally , Taking Metoclopramide HCl 10 MG Tablet 1 tablet Orally Bedtime , Taking Omeprazole 40 MG  
Capsule Delayed Release TAKE 1 CAPSULE BY MOUTH EVERY DAY 30 MINUTES BEFORE BREAKFAST , Not-
Taking/PRN Lansoprazole 30 MG Capsule Delayed Release 1 capsule Orally Twice a Day one hour before breakfast  
and one hour before dinner , Not- Taking/PRN Dexlansoprazole 60 MG Capsule Delayed Release 1 capsule Orally 
Once a day one hour before breakfast , Not- Taking/PRN Metoclopramide HCl 10 MG Tablet 1 tablet Orally Twice a 
day one hour before dinner and at bedtime , Not- Taking/PRN Procardia XL 60 MG Tablet Extended Release Orally 
, Not- Taking/PRN Glucotrol XL 5 MG Tablet Extended Release 1 tablet with food Orally Once a day , Not-
Taking/PRN Milk of Magnesia 400 MG/5ML Suspension 45 ml Orally at bedtime , Not- Taking/PRN Lansoprazole 30  
MG Capsule Delayed Release 1 capsule Orally bid one hour before breakfast and dinner , Medication List  
reviewed and reconciled with the patient
"""
inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True,  max_length=512)
#print(inputs)

# with torch.no_grad():
#     outputs = model(**inputs)


with torch.no_grad():
    outputs = model(**inputs)

    # Extract the predicted labels (disease entities)
predicted_labels = outputs.logits.argmax(dim=2).tolist()[0]

print(predicted_labels)

# print(outputs)
#
#
# # Get the last_hidden_state tensor
# last_hidden_state = outputs.last_hidden_state
#
# # Step 2: Convert the tensor to a NumPy array
# tensor_as_numpy = last_hidden_state.detach().cpu().numpy()
#
# # Step 3: Convert numerical values to text
# text_values = [str(value) for value in tensor_as_numpy]
#
# print(text_values)
# # Convert the last_hidden_state tensor to a numpy array
# last_hidden_state_numpy = last_hidden_state[0, -1, :].cpu().detach().numpy()
# print(last_hidden_state_numpy)
#
# # Decode the numpy array into a list of tokens
# tokens = tokenizer.decode(last_hidden_state_numpy)
#
# # Concatenate the tokens into a string
# text = " ".join(tokens)
#
# # Print the text
# print(text)
# hidden_states = outputs.last_hidden_state
#
# # Your tensor (example)
# output_tensor = torch.tensor(hidden_states)
#
# # Convert the tensor to a list of lists
# output_list = output_tensor.tolist()
#
# # Convert the list of lists to a formatted string
# output_text = "\n".join(["\t".join(map(str, row)) for row in output_list])
#
# # Print the resulting text
# print(output_text)
#
#     # Convert the hidden states to token IDs
#     # Note: The hidden_states tensor may have a batch dimension, so you need to specify the index (e.g., [0]) to get tokens for a specific input
# input_tokens = tokenizer.convert_ids_to_tokens(hidden_states[0].flatten().tolist())
# print(input_tokens)

# print(outputs)
#
# # Get the last_hidden_state tensor
# last_hidden_state = outputs.last_hidden_state
#
# # Convert the last_hidden_state tensor to a numpy array
#
# # Get the last_hidden_state tensor
# last_hidden_state = outputs.last_hidden_state
#
# # Convert the last_hidden_state tensor to a numpy array
# last_hidden_state_numpy = last_hidden_state.cpu().detach().numpy()
#
# # Convert the NumPy array to a PyTorch tensor
# last_hidden_state_torch = torch.from_numpy(last_hidden_state_numpy[0])
#
# token_ids = torch.argmax(last_hidden_state_torch[0], dim=-1).tolist()
# print(last_hidden_state_numpy)
# print(token_ids)
# # Decode the list of token IDs into a string
# text = tokenizer.decode(token_ids)
#
# # Print the text
# print(text)
#
# # Decode the numpy array into a list of tokens
# # tokens = tokenizer.decode(last_hidden_state_numpy[0])
# #
# # # Concatenate the tokens into a string
# # text = " ".join(tokens)
# #
# # # Print the
# # text
# # print(text)

disease_entities = []
current_entity = None

# Retrieve the tokenized input text from the 'input_ids' key in the inputs dictionary
input_ids = inputs['input_ids'][0]

for i, label in enumerate(predicted_labels):
    if label == 1:
        if current_entity is None:
            current_entity = [i]
        else:
            current_entity.append(i)
    elif label == 0 and current_entity is not None:
        disease_entities.append(current_entity)
        current_entity = None

# Extract the disease entities from the tokenized input text
disease_text_entities = []
for entity in disease_entities:
    start, end = entity[0], entity[-1]
    disease_tokens = input_ids[start:end + 1]

    # Convert token IDs back to text using the tokenizer
    disease_text = tokenizer.decode(disease_tokens)
    disease_text_entities.append(disease_text)

print(disease_text_entities)



