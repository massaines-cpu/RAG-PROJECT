import streamlit as st
import requests

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="La Gazette du Monde", page_icon="🗞️", layout="wide")


# --- 2. STYLE CSS (THÈME JOURNAL RÉTRO) ---
st.markdown(
    """
<style>
    .stApp {
        background-color: #f4ecd8;
        color: #2b2b2b;
        font-family: 'Times New Roman', Times, serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .newspaper-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        border-bottom: 4px double #2b2b2b;
        border-top: 4px double #2b2b2b;
        padding: 15px 0;
        margin-bottom: 5px;
        font-family: 'Georgia', serif;
    }
    .newspaper-subtitle {
        text-align: center;
        font-style: italic;
        font-size: 1.2rem;
        border-bottom: 1px solid #2b2b2b;
        margin-bottom: 30px;
        padding-bottom: 10px;
    }
    .column-title {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 15px;
        text-transform: uppercase;
    }
    .article-body {
        text-align: justify;
        font-size: 1rem;
        line-height: 1.6;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --- 3. EN-TÊTE DU JOURNAL ---
st.markdown(
    '<div class="newspaper-title">LA GAZETTE DU MONDE</div>', unsafe_allow_html=True
)
st.markdown(
    "<div class='newspaper-subtitle'>L'Édition Spéciale du Télégraphe Automatisé - Édition du Soir</div>",
    unsafe_allow_html=True,
)

# --- 4. LOGIQUE DE CHAT ---
# 1. On affiche la question en forçant la couleur noire via HTML
st.markdown("<p style='color: black;'>Que désirez-vous savoir aujourd'hui, cher lecteur ?</p>", unsafe_allow_html=True)

# 2. On crée le champ de texte juste en dessous, en masquant son label (qui est obligatoire mais qu'on peut cacher)
question = st.text_input("label_cache", label_visibility="collapsed")

# 1. Le texte en noir via HTML
st.markdown("<p style='color: black;'>Choisir le type de LLM</p>", unsafe_allow_html=True)

# 2. Le menu déroulant avec le label masqué
llm = st.selectbox(
    "label_cache_llm",
    ["ollama", "gpt4"],
    label_visibility="collapsed"
)
if st.button(":green[Envoyer Message]") and question:
    with st.spinner("Transmission au télégraphiste..."):
        try:
            response = requests.post(
                "http://api:8000/chatbot", json={"question": question, "llm": llm}
            )
            response.raise_for_status()
            data = response.json()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(
                    '<div class="column-title">Réponse sans contexte</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="article-body">{data["reponse_sans_contexte"]}</div>',
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    '<div class="column-title">Réponse avec contexte</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f'<div class="article-body">{data["reponse_avec_contexte"]}</div>',
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    '<div class="column-title">Contexte récupéré</div>',
                    unsafe_allow_html=True,
                )
                # The context can be long, so we make it scrollable
                st.markdown(
                    f'<div class="article-body" style="height: 400px; overflow-y: scroll; padding: 10px;">{data["contexte"]}</div>',
                    unsafe_allow_html=True,
                )

        except requests.exceptions.RequestException as e:
            st.error(f"Erreur de liaison avec le télégraphiste : {e}")
        except Exception as e:
            st.error(f"Une erreur inattendue est survenue : {e}")

else:
    st.info("Veuillez saisir un sujet pour imprimer votre édition spéciale.")
