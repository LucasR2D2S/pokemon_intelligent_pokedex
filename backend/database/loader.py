import requests
from database.db import SessionLocal, engine
from database.models import Base, Pokemon
from backend.utils.bulbapedia import scrape_biology_section


def fetch_pokemon_data(start: int = 1, end: int = 151):
    session = SessionLocal()
    for i in range(1, 152):  # Exemplo com 151 primeiros
        poke = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}").json()
        species = requests.get(poke["species"]["url"]).json()
        generation = requests.get(species["generation"]["url"]).json()
        wiki_pokemon = scrape_biology_section(poke["name"])

        flavor_texts = [
            entry["flavor_text"].replace("\n", " ").replace("\f", " ").strip()
            for entry in species["flavor_text_entries"]
            if entry["language"]["name"] == "en"
        ][:3]

        full_description = "\n\n".join(flavor_texts)

        if wiki_pokemon:
            full_description += "\n\n[Biology - Bulbapedia]\n" + wiki_pokemon

        new_poke = Pokemon(
            id=poke["id"],
            name=poke["name"].capitalize(),
            types=[t["type"]["name"] for t in poke["types"]],
            stats=[s["base_stat"] for s in poke["stats"]],
            generation=generation["name"].replace("generation-", "G").upper(),
            descriptions= full_description
        )
        session.merge(new_poke)
    session.commit()
    session.close()