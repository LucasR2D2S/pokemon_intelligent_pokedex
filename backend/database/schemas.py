from pydantic import BaseModel
from typing import List

class PokemonBase(BaseModel):
    name: str
    types: List[str]
    stats: List[int]
    generation: str
    physical_characteristics: str
    behavior: str
    habitat: str
    general_description: str
    full_description: str

class Pokemon(PokemonBase):
    id: int
    class Config:
        orm_mode = True