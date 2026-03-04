import streamlit as st
import requests

st.title('chatbot qui répond aux questions politiques')

question = st.text_input('posez votre question')

if st.button('envoyer message') and question:
    response = requests.post('http://127.0.0.1:8000/chatbot', json={'question': question})
    data = response.json()



    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader('réponse du LLM sans contexte')
        st.write(data['reponse_sans_contexte'])

    with col2:
        st.subheader('réponse du LLM avec contexte')
        st.write(data['reponse_avec_contexte'])

    with col3:
        st.subheader("contexte récupéré")
        st.markdown(f'<p style="font-size:14px; line-height:1.4">{data.get("contexte", "")}</p>', unsafe_allow_html=True)
    # contexte = poser_question(question)
    # prompt = f'Voici des articles pertinents :\n{contexte}\n\nQuestion : {question}\nRéponds de manière claire, développée le plus possible en bloc de texte sans listes numérotées/puces et sans rediriger vers les liens :'
    # prompt2 = 'Qui est rachida dati ?'

    # response1 = ollama.chat(
    #     model='mistral',
    #     messages=[
    #         {'role': 'system', 'content': 'Tu es un assistant qui répond uniquement à partir du contexte fourni.'},
    #         {'role': 'user', 'content': prompt}])
    #
    # response2 = ollama.chat(
    #     model='mistral',
    #     messages=[
    #         {'role': 'system', 'content': 'Tu es un assistant qui répond uniquement à l\'aide de tes connaissances.'},
    #         {'role': 'user', 'content': prompt2}])



