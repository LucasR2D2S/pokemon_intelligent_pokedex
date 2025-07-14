import requests
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal, engine
import time

# Para criar o banco de dados da aplicação
models.Base.metadata.create_all(bind=engine)

def fetch_pokemon_data(poke_id: int) -> schemas.PokemonCreate:
    print(f"Buscando dados para o Pokémon ID {poke_id}")
    base_url = "https://pokeapi.co/api/v2"

    # Utilizando as informações da pokeapi
    pokemon_url = f"{base_url}/pokemon/{poke_id}"
    species_url = f"{base_url}/pokemon-species/{poke_id}"

    pokemon_resp = requests.get(pokemon_url).json()
    species_resp = requests.get(species_url).json()

    name = pokemon_resp["name"]
    types = [t["type"]["name"] for t in pokemon_resp["types"]]
    stats = [{s["stat"]["name"]: s["base_stat"]} for s in pokemon_resp["stats"]]

    generation = species_resp["generation"]["name"]

    # Descrição em português ou em inglês se não tiver disponível
    flavor_text_entries = species_resp["flavor_text_entries"]
    descriptions = next(
        (entry["flavor_text"] for entry in flavor_text_entries if entry["language"]["name"] == "en"),
        flavor_text_entries[0]["flavor_text"] if flavor_text_entries else "No description available"
    ).replace("\n", " ").replace("\f", " ")

    return schemas.PokemonCreate(
        id=poke_id,
        name=name,
        types=types,
        stats=stats,
        generation=generation,
        descriptions=descriptions,
    )

def populate_pokemon(limit: int = 151):  # pode mudar pra 898 depois
    db: Session = SessionLocal()
    for poke_id in range(1, limit + 1):
        try:
            pokemon = fetch_pokemon_data(poke_id)
            db_pokemon = models.Pokemon(**pokemon.dict())
            db.merge(db_pokemon)
            db.commit()
            print(f"Pokémon {pokemon.name} inserido.")
            time.sleep(0.5)  # Evita rate limit
        except Exception as e:
            print(f"Erro ao processar o Pokémon ID {poke_id}: {e}")
    db.close()

if __name__ == "__main__":
    populate_pokemon(limit=151)

# Como rodar:
# Se não tiver instalados os requisitos necessários: 
# pip install fastapi sqlalchemy requests
# Rode o arquivo: 
# python app/init_db.py