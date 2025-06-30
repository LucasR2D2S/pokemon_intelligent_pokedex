from pydantic import BaseModel

class Pokemon(BaseModel):
    id: int
    name: str
    type: str
    hp: int
    attack: int
    defense: int
    speed: int
    image_url: str

    class Config:
        orm_mode = True
