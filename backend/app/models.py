from sqlalchemy import Column, Integer, String, JSON
from .db import Base

# Criando modelo do objeto Pokemon
class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    types = Column(JSON)
    stats = Column(JSON)
    generation = Column(String)
    descriptions = Column(String)