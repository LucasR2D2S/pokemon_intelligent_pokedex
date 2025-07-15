from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.schema import Document
from database.db import SessionLocal
from database.models import Pokemon

embedding = OllamaEmbeddings(model="nomic-embed-text", base_url="http://localhost:11436")
index = None

def build_index():
    global index
    db = SessionLocal()
    pokemons = db.query(Pokemon).all()
    docs = [
        Document(page_content=f"{p.name}: {p.types}, Geração {p.generation}. {p.descriptions}", metadata={"id": p.id})
        for p in pokemons
    ]
    index = FAISS.from_documents(docs, embedding)


def retrieve_context(question: str, k: int = 3) -> str:
    global index
    if not index:
        build_index()
    docs = index.similarity_search(question, k=k)
    return "\n".join([d.page_content for d in docs])
