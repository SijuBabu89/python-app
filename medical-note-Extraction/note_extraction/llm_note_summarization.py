from openai import OpenAI
import os
from datetime import datetime
import json


def llm_note_extraction(note, question):
    # Pretend you as a expert in content extraction, Please extract HPI, Objective and Assessment from below medical note and give the output in json format
    note = question + ' ' + 'and give the output in json format' + '''' :
    
    ''' + note
    os.environ['OPENAI_API_KEY'] = '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'
    client = OpenAI()
    t1 = datetime.now()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": note
            }
        ],
        temperature=0,
        max_tokens=2197,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    content = response.choices[0].message.content
    # Load the text data as a Python dictionary
    json_string = content.replace(r'\n', '\n')
    print(json_string)
    json_string = ''.join(char for char in json_string if ord(char) < 128)
    data_dict = json.loads(json_string, strict=False)

    # Convert the dictionary to a JSON-formatted string with indentation for better readability
    #json_output = json.dumps(data_dict, indent=2)
    return data_dict
