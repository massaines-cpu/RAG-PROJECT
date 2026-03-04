from fastapi import FastAPI
from pydantic import BaseModel
from recup_question import poser_question
import ollama

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post('/chatbot')
def chatbot(request: Question):
    question = request.question
    contexte = poser_question(question, n_results=5)

#sans contexte
    prompt_sans_contexte = question
    prompt_avec_contexte = f'''Voici des articles pertinents :\n{contexte}\n\nQuestion : {question}\nRéponds de manière claire, 
        développée le plus possible en bloc de texte sans listes numérotées/puces et sans rediriger vers les liens :'''
    reponse_sans_contexte = ollama.chat(
        model='mistral',
        messages=[
            {'role': 'system', 'content': 'Tu es un assistant qui répond uniquement à l\'aide de tes connaissances.'},
            {'role': 'user', 'content': prompt_sans_contexte},])

    reponse_avec_contexte = ollama.chat(
        model='mistral',
        messages=[{'role': 'system', 'content': 'Tu es un assistant qui répond uniquement à partir du contexte fourni.'},
                  {'role': 'user', 'content': prompt_avec_contexte}])

    return {
        'reponse_sans_contexte': reponse_sans_contexte['message']['content'],
        'reponse_avec_contexte': reponse_avec_contexte['message']['content'],
        'contexte': contexte}