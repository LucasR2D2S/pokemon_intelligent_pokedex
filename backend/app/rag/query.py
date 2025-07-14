from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
import os

def query_pokemon_index(query: str, k: int = 5):
    embeddings = OllamaEmbeddings(model="gemma3:4b", base_url="http://localhost:11436")
    db = FAISS.load_local("app/rag/vectorstore/pokemon_faiss_index", embeddings)
    results = db.similarity_search(query, k=k)
    return results