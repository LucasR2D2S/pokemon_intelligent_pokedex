import requests
import csv

base_url = "https://pokeapi.co/api/v2/pokemon"
response = requests.get(f"{base_url}?limit=1026") # Ajuste o limite conforme necessário
pokemon_list = response.json()['results']

pokemon_data = []
for pokemon_entry in pokemon_list:
    detail_response = requests.get(pokemon_entry['url'])
    details = detail_response.json()

    name = details['name']

    # Tipos
    types = [t['type']['name'] for t in details['types']]
    type_str = ", ".join(types) # Para unir múltiplos tipos em uma string

    # Stats
    hp = next((s['base_stat'] for s in details['stats'] if s['stat']['name'] == 'hp'), None)
    attack = next((s['base_stat'] for s in details['stats'] if s['stat']['name'] == 'attack'), None)
    defense = next((s['base_stat'] for s in details['stats'] if s['stat']['name'] == 'defense'), None)
    speed = next((s['base_stat'] for s in details['stats'] if s['stat']['name'] == 'speed'), None)

    # Image URL
    # Preferir official-artwork se disponível, senão front_default
    #image_url = details['sprites']['other'].get('official-artwork', {}).get('front_default')
    #if not image_url:
        #image_url = details['sprites'].get('front_default')
    # Ou a URL padronizada com ID:
    pokemon_id = details['id']
    image_url = f"https://assets.pokemon.com/assets/cms2/img/pokedex/detail/{str(pokemon_id).zfill(3)}.png"

    pokemon_data.append({
        'name': name,
        'type': type_str,
        'hp': hp,
        'attack': attack,
        'defense': defense,
        'speed': speed,
        'image_url': image_url
    })

    csv_file = "pokemons.csv"
    csv_columns = ['name', 'type', 'hp', 'attack', 'defense', 'speed', 'image_url']

    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in pokemon_data:
            writer.writerow(data)

print(f"CSV '{csv_file}' criado com sucesso!")