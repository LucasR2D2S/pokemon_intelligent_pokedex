from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.crud import get_pokemons
import os
import pickle

# Inicializa embedding
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Caminho onde o índice será salvo
FAISS_INDEX_PATH = "faiss_index/index.pkl"

# Gera documentos do banco de dados
def generate_documents(db: Session):
    pokemons = get_pokemons(db)
    documents = []

    for pokemon in pokemons:
        content = f"""
        Nome: {pokemon.name}
        Tipos: {', '.join(pokemon.types)}
        Geração: {pokemon.generation}
        Status:
          HP={pokemon.stats['hp']}, Ataque={pokemon.stats['attack']}, Defesa={pokemon.stats['defense']}, Velocidade={pokemon.stats['speed']}
        Descrição: {pokemon.descriptions}
        """
        documents.append(Document(page_content=content.strip(), metadata={"name": poke.name}))
    return documents

# Cria e salva o índice
def create_faiss_index():
    db = SessionLocal()
    documents = generate_documents(db)
    vectorstore = FAISS.from_documents(documents, embedding_model)
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    with open(FAISS_INDEX_PATH, "wb") as f:
        pickle.dump(vectorstore, f)
    print("Índice FAISS criado e salvo com sucesso.")
