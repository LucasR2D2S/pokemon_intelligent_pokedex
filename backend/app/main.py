from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .db import engine, get_db
from app.rag.query import query_pokemon_index

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "API da Pokédex Inteligente rodando!"}

@app.get("/pokemon/", response_model=list[schemas.Pokemon])
def read_pokemons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pokemons(db, skip=skip, limit=limit)

@app.get("/pokemon/{pokemon_id}", response_model=schemas.Pokemon)
def read_pokemon(pokemon_id: int, db: Session = Depends(get_db)):
    db_pokemon = crud.get_pokemon(db, pokemon_id=pokemon_id)
    if db_pokemon is None:
        raise HTTPException(status_code=404, detail="Pokémon não encontrado")
    return db_pokemon

@app.post("/generate-team/", response_model=list[schemas.Pokemon])
def read_pokemons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pokemons(db, skip=skip, limit=limit)

@app.post("/ask")
def ask_question(payload: dict):
    question = payload.get("question", "")

    # Busca contexto relevante com FAISS
    context_docs = query_pokemon_index(question)
    context_text = "\n\n".join([doc.page_content for doc in context_docs])

    # Monta o prompt com contexto real
    full_prompt = f"""Você é um especialista em Pokemon, deve responder perguntas como uma Pokédex.

    Utilize o seguinte contexto de base pra responder à pergunta:
    {context_text}

    Para gerar a pergunta, não imagine ou crie informações, apenas use o contexto fornecido.

    Pergunta: {question}
    Resposta:"""
    # Chama o LLM com o prompt completo
    try:
        response = payload.post(
            "http://localhost:11436/api/generate",
            json={"model": "gemma3:4b", "prompt": full_prompt}
        )
        response.raise_for_status()
        content = response.json()["response"]
        return {"answer": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao se comunicar com o LLM: {e}")