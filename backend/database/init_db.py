import requests
from database.db import SessionLocal, engine
from database.models import Base, Pokemon

Base.metadata.create_all(bind=engine)

def fetch_pokemon_data():
    session = SessionLocal()
    for i in range(1, 152):  # Exemplo com 151 primeiros
        poke = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}").json()
        species = requests.get(poke["species"]["url"]).json()
        generation = requests.get(species["generation"]["url"]).json()

        new_poke = Pokemon(
            id=poke["id"],
            name=poke["name"].capitalize(),
            types=[t["type"]["name"] for t in poke["types"]],
            stats=[s["base_stat"] for s in poke["stats"]],
            generation=generation["name"].replace("generation-", "G").upper(),
            descriptions=[entry["flavor_text"] for entry in species["flavor_text_entries"] if entry["language"]["name"] == "en"][:3]
        )
        session.merge(new_poke)
    session.commit()
    session.close()

if __name__ == "__main__":
    fetch_pokemon_data()

# Como rodar:
# Se não tiver instalados os requisitos necessários: 
# pip install fastapi sqlalchemy requests
# Rode o arquivo: 
# python app/init_db.py