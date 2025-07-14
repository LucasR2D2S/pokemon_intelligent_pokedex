from sqlalchemy.orm import Session
from . import models
from .db import get_db

def get_pokemons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pokemon).offset(skip).limit(limit).all()

def get_pokemon_by_generation(db: Session, pokemon_generation: str):
    return db.query(models.Pokemon).filter(models.Pokemon.generation == pokemon_generation).first()
