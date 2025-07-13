from sqlalchemy.orm import Session
from . import models
from .db import get_db

def get_pokemons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pokemon).offset(skip).limit(limit).all()

def seach_pokemon_context(question: str, db: Session = next(get_db())) -> str:
    terms = re.findall(r'\b\w+\b', question.lower())
    pokemons = db.query(models.Pokemon).all()
    matched_info = []
    for pokemon in pokemons:
        name = pokemon.name.lower()
        type = pokemon.type.lower()
        generation = pokemon.generation.lower()
        pokemon_data = f"Nome: {name}, Tipo: {type}, Geração: {generation}"
        if any(term in name or term in type for term in terms) or any(term in pokemon_data.lower() for term in terms):
            matched_info.append(pokemon_data)
        elif not matched_info:
            return "Nenhum dado encontrado com base na pergunta."    
    return "\n".join(matched_info[:10])