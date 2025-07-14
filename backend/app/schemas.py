from pydantic import BaseModel
from typing import List, Dict

# Criando schema do objeto Pokemon
class PokemonCreate(BaseModel):
    id: int
    name: str
    types: List[str]
    stats: List[Dict[str, int]]
    generation: str
    descriptions: str

class Pokemon(PokemonCreate):
    class Config:
        orm_mode = True