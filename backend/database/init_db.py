from database.loader import fetch_pokemon_data

if __name__ == "__main__":
    fetch_pokemon_data(1, 151)

# Como rodar:
# Se não tiver instalados os requisitos necessários: 
# pip install fastapi sqlalchemy requests
# Rode o arquivo: 
# python app/init_db.py