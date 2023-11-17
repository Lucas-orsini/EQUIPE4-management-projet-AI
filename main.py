import requests
import xml.etree.ElementTree as ET
from airtable import Airtable
from openai import OpenAI

client = OpenAI()


import time

# Configuration de la clé API pour Airtable
AIRTABLE_API_KEY = 'keyjFQshpzDh9GFPx'
AIRTABLE_BASE_ID = 'appCgHMUSeUSwpwe9'
AIRTABLE_TABLE_NAME = 'tblX5SimehVYPItFr'

# Configuration de la clé API pour OpenAI (ChatGPT)
OPENAI_API_KEY = ''
client = OpenAI(api_key=OPENAI_API_KEY)

# Configuration de l'ID d'application pour Wolfram Alpha
WOLFRAM_APP_ID = '462T9V-4YK943YP43'

# Initialisation des clients Airtable et OpenAI
airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, api_key=AIRTABLE_API_KEY)


def check_new_records():
    print("Vérification des nouveaux enregistrements...")
    records = airtable.get_all(sort='-createdTime')
    for record in records:
        print(f"Traitement de l'enregistrement : {record['id']}")
        process_record(record)
        print(f"Enregistrement {record['id']} traité.")
    print("Fin de la vérification.")

def process_record(record):
    data = {
        'Lipides': record['fields'].get('Lipides'),
        'Proteins': record['fields'].get('Proteins'),
        'Glucides': record['fields'].get('Glucides')
    }
    prompt = create_chatgpt_prompt(data)
    chatgpt_response = get_completion(prompt)

    # Traitement de la réponse de ChatGPT
    lines = chatgpt_response.split('\n')
    current_nutrient = None
    for line in lines:
        if line.strip().endswith(':'):
            current_nutrient = line.strip()[:-1]  # Enlever le caractère ':'
        elif current_nutrient and '-' in line:
            try:
                item, amount = line.split('-')
                amount = amount.strip()
                if amount:
                    wolfram_result = send_to_wolfram_alpha(f"{item.strip()} contains {amount}")
                    print(f"Résultat de Wolfram Alpha pour '{line}': {wolfram_result}")
            except ValueError as e:
                print(f"Ligne non traitable : {line}")
        else:
            print(f"Ligne non traitable : {line}")




def create_chatgpt_prompt(data):
    prompts = []
    for nutrient, amount in data.items():
        if amount:
            prompts.append(f"Could you give me a list of common foods that contain about {amount} grams of {nutrient} per serving? "
                           f"I am looking for foods that are readily available and commonly consumed, ideally with a precise measurement for each food "
                           f"(for example, '100 grams of chicken containing X grams of {nutrient}'). This list will be used for detailed nutritional calculations.")
    return " ".join(prompts)



def get_completion(prompt):
    print("Envoi du prompt à ChatGPT...")
    response = client.completions.create(
        model="text-davinci-003",  # Modèle utilisé
        prompt=prompt,             # Invite envoyée
        max_tokens=150             # Nombre de tokens
    )
    print("Réponse reçue de ChatGPT.")
    return response.choices[0].text.strip()



def send_to_wolfram_alpha(plan_alimentaire):
    print(f"Envoi de la demande à Wolfram Alpha : {plan_alimentaire}")
    base_url = "http://api.wolframalpha.com/v2/query?"
    query = f"nutritional information of {plan_alimentaire}"
    params = {
        "input": query,
        "appid": WOLFRAM_APP_ID,
        "format": "plaintext"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    root = ET.fromstring(response.content)
    result = {}
    for pod in root.findall(".//pod"):
        title = pod.get('title')
        values = [plaintext.text for plaintext in pod.findall(".//plaintext") if plaintext.text]
        if values:
            result[title] = values
    return result
    
while True:
    check_new_records()
    print("Attente avant la prochaine vérification...")
    time.sleep(60)  # Pause avant la prochaine itération
