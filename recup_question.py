import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings


embedding_function = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.Client(Settings(persist_directory='./chroma_db',is_persistent=True))
collection = client.get_collection(name='actu_france_24', embedding_function=embedding_function)


def poser_question(question, n_results=5):
    resultats = collection.query(query_texts=[question],n_results=n_results)

    documents = resultats["documents"][0]
    metadatas = resultats["metadatas"][0]

    contexte = ""

    for doc, meta in zip(documents, metadatas):
        contexte += f"titre: {meta.get('titre','pas de titre')}\n"
        contexte += f"texte: {doc}\n"
        contexte += f"lien: {meta.get('lien','pas de titre')}\n"
        contexte += "---" * 40 + "\n"

    print(resultats)
    return contexte
