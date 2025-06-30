from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db
import json

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
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