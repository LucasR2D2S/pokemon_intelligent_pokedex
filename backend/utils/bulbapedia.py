import requests
from bs4 import BeautifulSoup

def scrape_biology_section(pokemon_name: str) -> str:
    """
    Faz scraping da seção 'Biology' da Bulbapedia para um Pokémon.
    Retorna o texto da seção ou None se falhar.
    """
    base_url = "https://bulbapedia.bulbagarden.net/wiki/"
    formatted_name = pokemon_name.capitalize().replace(" ", "_") + "_(Pokémon)"
    url = base_url + formatted_name

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        content = soup.find('span', id='Biology')
        if not content:
            return None

        bio_paragraphs = []
        for tag in content.find_parent().find_next_siblings():
            if tag.name == 'h2':  # chegou na próxima seção
                break
            if tag.name == 'p':
                bio_paragraphs.append(tag.text.strip())
        return "\n\n".join(bio_paragraphs)
    except Exception as e:
        print(f"[ERRO] Falha ao buscar '{pokemon_name}': {e}")
        return None
"""
if __name__ == "__main__":
    print("Testando com Pikachu:")
    pikachu_bio = scrape_biology_section("pikachu")
    if pikachu_bio:
        print(pikachu_bio)
        print("\n--- Fim da biologia do Pikachu ---\n")
    else:
        print("\n--- Não foi possível obter a biologia do Pikachu ---\n")

    print("Testando com Charmander:")
    charmander_bio = scrape_biology_section("charmander")
    if charmander_bio:
        print(charmander_bio)
        print("\n--- Fim da biologia do Charmander ---\n")
    else:
        print("\n--- Não foi possível obter a biologia do Charmander ---\n")

    print("Testando com um Pokémon inexistente (ou com erro no nome):")
    nonexistent_bio = scrape_biology_section("NonExistentPokemon123")
    if nonexistent_bio:
        print("\n--- Fim da biologia do Pokémon inexistente ---\n")
    else:
        print("\n--- Não foi possível obter a biologia do Pokémon inexistente ---\n")
"""   