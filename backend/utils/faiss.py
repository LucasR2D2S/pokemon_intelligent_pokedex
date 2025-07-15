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
    docs = []

    # Formatando documento para melhor a resposta
    for p in pokemons:
        doc_text = (
            f"Nome: {p.name}\n"
            f"Tipos: {', '.join(p.types)}\n"
            f"Geração: {p.generation}\n"
            f"Estatísticas: {', '.join(str(s) for s in p.stats)}\n\n"
            f"Descrição Completa:\n{p.descriptions}"
        )
        docs.append(Document(page_content=doc_text, metadata={"id": p.id}))
    index = FAISS.from_documents(docs, embedding)


def retrieve_context(question: str, k: int = 3) -> str:
    global index
    if not index:
        build_index()
    docs = index.similarity_search(question, k=k)
    return "\n".join([d.page_content for d in docs])
