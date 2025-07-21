from sqlalchemy import Column, Integer, String, JSON
from database.db import Base

class Pokemon(Base):
    __tablename__ = "pokemons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    types = Column(JSON)  # lista de tipos
    stats = Column(JSON)  # lista de stats
    generation = Column(String)
    physical_characteristics = Column(Text)
    behavior = Column(Text)
    habitat = Column(Text)
    general_description = Column(Text)
    full_description = Column(Text)  # concatenada para FAISS