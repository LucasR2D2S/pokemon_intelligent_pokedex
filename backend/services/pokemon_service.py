from sqlalchemy.orm import Session
from database import models

def get_pokemon_by_name(db: Session, name: str):
    return db.query(models.Pokemon).filter(models.Pokemon.name.ilike(name)).first()

def get_pokemon_by_names(db: Session, names: list[str]):
    return db.query(models.Pokemon).filter(models.Pokemon.name.in_(names)).all()

def get_pokemons_by_type(db: Session, type: str):
    return db.query(models.Pokemon).filter(models.Pokemon.types.contains([type])).all()

def get_all_pokemons(db: Session):
    return db.query(models.Pokemon).all()