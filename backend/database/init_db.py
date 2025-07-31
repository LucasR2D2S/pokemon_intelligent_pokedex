from .loader import fetch_pokemon_data

if __name__ == "__main__":
    try:
        fetch_pokemon_data(1, 151)  # Carrega os primeiros 151 Pokémon
        print("Pokémon data has been successfully loaded into the database.")
    except Exception as e:
        print(f"Error loading Pokémon data: {e}")

# Como rodar:
# Se não tiver instalados os requisitos necessários: 
# pip install fastapi sqlalchemy requests
# Rode o arquivo: 
# python app/init_db.py