from recup_question import poser_question
import ollama
import os


question = "quels états sont en guerre ?"

contexte = poser_question(question, n_results=5)
print(contexte)
print("\n" + "="*50 + "\n")

prompt = f"Voici des articles pertinents :\n{contexte}\n\nQuestion : {question}\nRéponds de manière claire, développée le plus possible en bloc de texte sans listes numérotées/puces et sans rediriger vers les liens :"

response = ollama.chat(
    model="mistral",
    messages=[{"role": "system",
    "content": "Tu es un assistant qui répond uniquement à partir du contexte fourni."},
    {"role": "user", "content": prompt}])


print(response['message']['content'])