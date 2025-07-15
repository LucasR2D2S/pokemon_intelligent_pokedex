from pydantic import BaseModel
from typing import List

class PokemonBase(BaseModel):
    name: str
    types: List[str]
    stats: List[int]
    generation: str
    descriptions: List[str]

class Pokemon(PokemonBase):
    id: int
    class Config:
        orm_mode = True