import requests
import os
import time
import json
from backend.database.db import SessionLocal, Base, engine
from .models import Pokemon
from backend.utils.bulbapedia import scrape_biology_section
from backend.utils.description_parser import parse_biology_description

# Configuração de sessão HTTP
session_http = requests.Session()
session_http.headers.update({
    "User-Agent": "Pokedex-Inteligente/1.0 (https://github.com/LucasR2D2S/pokemon_intelligent_pokedex)"
})

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)


def get_cached_json(url, cache_name):
    """Busca dados da API com cache local simples."""
    cache_path = os.path.join(CACHE_DIR, cache_name)
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            return json.load(f)

    data = session_http.get(url).json()
    with open(cache_path, "w") as f:
        json.dump(data, f)
    return data

def fetch_pokemon_data(start: int, end: int):
    session = SessionLocal()
    try:
        for i in range(start, end):  # Os primeiros 151 Pokémon por exemplo
            poke = get_cached_json(f"https://pokeapi.co/api/v2/pokemon/{i}", f"pokemon_{i}.json")
            species = get_cached_json(poke["species"]["url"], f"species_{i}.json")
            generation = get_cached_json(species["generation"]["url"], f"generation_{i}.json")
            wiki_biology = scrape_biology_section(poke["name"])
            name = poke["name"].capitalize()

            # Dividir descrição da Bulbapedia
            physical, behavior, habitat = parse_biology_description(wiki_biology)

            # Descrição oficial da Pokédex
            pokedex_desc = " ".join(
                entry["flavor_text"].replace("\n", " ").replace("\f", " ")
                for entry in species["flavor_text_entries"]
                if entry["language"]["name"] == "en"
            )[:500]  # limitar tamanho

            full_description = (
                f"{pokedex_desc}\n\n"
                f"[Physical Characteristics] {physical}\n"
                f"[Behavior] {behavior}\n"
                f"[Habitat] {habitat}"
            )

            new_poke = Pokemon(
                id=poke["id"],
                name=poke["name"].capitalize(),
                types=[t["type"]["name"] for t in poke["types"]],
                stats=[s["base_stat"] for s in poke["stats"]],
                generation=generation["name"].replace("generation-", "G").upper(),
                physical_characteristics=physical,
                behavior=behavior,
                habitat=habitat,
                general_description=pokedex_desc,
                full_description=full_description,
            )
            session.merge(new_poke)
            # Respeitar limite da PokéAPI
            time.sleep(0.6)
            session.commit()
            print(f"Banco de dados populado com sucesso, com pokemon {name}!")
    finally:
        session.close()