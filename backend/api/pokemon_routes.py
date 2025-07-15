from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from services.pokemon_service import (
    get_pokemon_by_name, get_pokemons_by_type,
    get_pokemon_by_names, get_all_pokemons
)

router = APIRouter()

@router.get("/pokemon/by-name")
def read_pokemon(name: str, db: Session = Depends(get_db)):
    return get_pokemon_by_name(db, name)

@router.get("/pokemon/by-names")
def read_pokemons(names: list[str], db: Session = Depends(get_db)):
    return {"team": get_pokemon_by_names(db, names)}

@router.get("/pokemon/by-type")
def read_by_type(type: str, db: Session = Depends(get_db)):
    return get_pokemons_by_type(db, type)

@router.get("/pokemon/all")
def read_all(db: Session = Depends(get_db)):
    return get_all_pokemons(db)