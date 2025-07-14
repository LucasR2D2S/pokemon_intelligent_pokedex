import os
import json
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.schema import Document
from ..db import SessionLocal
from sqlalchemy.orm import Session
from ..llm import ask_llm
from ..crud import search_pokemon_context
from .. import crud

def load_pokemon_documents():
    db = SessionLocal()
    pokemons = crud.get_all_pokemons(db)
    docs = []

    for pokemon in pokemons:
        content = (
            f"Nome: {pokemon.name}\n"
            f"Tipo: {pokemon.type}\n"
            f"HP: {pokemon.hp}, Ataque: {pokemon.attack}, Defesa: {pokemon.defense}, Velocidade: {pokemon.speed}\n"
            f"Geração: {pokemon.generation}\n"
            f"Descrição: {pokemon.description or ''}"
        )
        docs.append(Document(page_content=content, metadata={"name": pokemon.name, "description": pokemon.description}))
    
    return docs

def build_index():
    docs = load_pokemon_documents()
    embeddings = OllamaEmbeddings(model="gemma3:4b", base_url="http://localhost:11436")
    db = FAISS.from_documents(docs, embedding=embeddings)
    db.save_local("app/rag/vectorstore/faiss_index")

if __name__ == "__main__":
    build_index()
      

# Horse
# _,,)\.~,,._
# (( `  ``)\))),,_
#  |      \ ''((\)))),,_
#  | ●    |   ''((\())) "-._______________-__.-"    `-.-,_______
#  |     .'\    ''))))'                                          -,___
#  |     |   `.     ''                                             ((((
#  \, _)     \/                                                       |))))
#   `'        |                                                         (((((
#             \                       |                                 ))))))
#              `|    |                ,\                               ((((((
#               |   / `-.__________________.<  \   |  _______         )))))
#               |   |  /                                     `. \  \  ((((
#               |  / \ |                                       `.\  | (((
#               \  | | |                                         | |  |  ))
#                | | | |                                         | |  |((
# 	             | | | |                                         | |  |
# 	             | | | |                                         | |  |
# 	             | | | |                                         | |  |
# 	             | | | |                                         | |  |
# 	          /____|___|                                      /__/____|