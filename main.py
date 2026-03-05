#main.py
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from recup_question import poser_question
import ollama
from openai import OpenAI

load_dotenv()

app = FastAPI()

gpt = OpenAI(api_key = os.getenv('API_KEY_AZURE'),base_url= os.getenv('URL_AZURE'))
ollama_client = ollama.Client(host='http://ollama:11434')

class Question(BaseModel):
    question: str
    llm: str

@app.post('/chatbot')
def chatbot(request: Question):
    question = request.question
    llm = request.llm
    contexte = poser_question(question, n_results=5)

#sans contexte
    prompt_sans_contexte = question
    prompt_avec_contexte = f'''Voici des articles pertinents :\n{contexte}\n\nQuestion : {question}\nRéponds en langue française de manière claire, 
        développée le plus possible en bloc de texte sans listes numérotées/puces et sans rediriger vers les liens. N'invente pas une réponse
         si elle n'est pas dans le contexte qu'on te donne:'''

    if llm == 'ollama':
        reponse_sans_contexte = ollama_client.chat(
            model='mistral',
            messages=[
                {'role': 'system',
                 'content': 'Tu es un assistant qui répond uniquement à l\'aide de tes connaissances.'},
                {'role': 'user', 'content': prompt_sans_contexte}, ])
        reponse_sans_contexte = reponse_sans_contexte['message']['content']

        reponse_avec_contexte = ollama_client.chat(
            model='mistral',
            messages=[
                {'role': 'system', 'content': 'Tu es un assistant qui répond uniquement à partir du contexte fourni.'},
                {'role': 'user', 'content': prompt_avec_contexte}])
        reponse_avec_contexte = reponse_avec_contexte['message']['content']

    elif llm == 'gpt5':
        reponse_sans_contexte = gpt.chat.completions.create(
            model="gpt-5.1-chat",
            messages=[
                {"role": "system", "content": "Tu dois répondre uniquement en français."},
                {"role": "user", "content": prompt_sans_contexte}
            ])
        reponse_sans_contexte = reponse_sans_contexte.choices[0].message.content

        reponse_avec_contexte = gpt.chat.completions.create(
            model="gpt-5.1-chat",
            messages=[
                {"role": "system", "content": "Tu dois répondre uniquement avec le contexte qui t'est donné, en français."},
                {"role": "user", "content": prompt_avec_contexte}
            ])
        reponse_avec_contexte = reponse_avec_contexte.choices[0].message.content


    return {
        'reponse_sans_contexte': reponse_sans_contexte,
        'reponse_avec_contexte': reponse_avec_contexte,
        'contexte': contexte}

    # reponse_sans_contexte = ollama.chat(
    #     model='mistral',
    #     messages=[
    #         {'role': 'system', 'content': 'Tu es un assistant qui répond uniquement à l\'aide de tes connaissances.'},
    #         {'role': 'user', 'content': prompt_sans_contexte},])
    #
    # reponse_avec_contexte = ollama.chat(
    #     model='mistral',
    #     messages=[{'role': 'system', 'content': 'Tu es un assistant qui répond uniquement à partir du contexte fourni.'},
    #               {'role': 'user', 'content': prompt_avec_contexte}])