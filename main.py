import feedparser
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import hashlib

embedding_function = embedding_functions.DefaultEmbeddingFunction()
client = chromadb.Client(
    Settings(
        persist_directory='./chroma_db',
        is_persistent=True
    )
)

collection = client.get_or_create_collection(name='actu_france_24', embedding_function=embedding_function)

def chunk_article(texte, chunk_size=800, overlap=150):
    chunk = []
    debut = 0
    while debut < len(texte):
        fin = debut + chunk_size
        chunk.append(texte[debut:fin])
        debut += chunk_size - overlap
    return chunk

urls = {
    'Europe': 'https://www.france24.com/fr/europe/rss',
    'Monde': 'https://www.france24.com/fr/monde/rss',
    'Afrique': 'https://www.france24.com/fr/afrique/rss',
    'Moyen-Orient': 'https://www.france24.com/fr/moyen-orient/rss',
    'France': 'https://www.france24.com/fr/france/rss',
    'Asie-Pacifique': 'https://www.france24.com/fr/asie-pacifique/rss',
    'Amériques': 'https://www.france24.com/fr/amériques/rss'}

textes = []
metadatas = []

for endroit, url in urls.items():
    feed = feedparser.parse(url)

    for article in feed.entries:
        titre = article['title']
        texte = titre + ' ' + article.get('summary', '')
        titre_id = hashlib.md5(titre.encode()).hexdigest()
        chunk = chunk_article(texte)

        for i, chunk in enumerate(chunk):
            chunk_id = hashlib.md5(chunk.encode()).hexdigest()

            collection.add(
            ids = [chunk_id],
            metadatas = [{'endroit': endroit,
                'titre': article.get('title'),
                'chunk': i,
                'résumé': article.get('summary', 'pas de résumé'),
                'lien': article.get('link', 'pas de lien')}],
            documents = [chunk])

#VOIR CE QU'IL YA DANS MA CHROMADB MAGNIFIQUE
resultats = collection.get(include=['documents', 'metadatas'])

documents = resultats['documents']
metadatas = resultats['metadatas']

for doc, meta in zip(documents, metadatas):
    print(f"Chunk : {doc}")
    print(f"Métadonnées : {meta}")
    print("---"*40)