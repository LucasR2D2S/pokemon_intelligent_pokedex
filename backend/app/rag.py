from sqlalchemy.orm import Session
from .llm import ask_llm
from .crud import search_pokemon_context
from . import crud

def rag_pokemon_context(question:str) -> str:
    # Consulta base de dados para obter informações sobre os Pokémon e levar contexto ao LLM
    context = search_pokemon_context(question)

    prompt = f"""
    Você é um assistente especialista em Pokemon, e vai agir como uma Pokedex, Voce ira receber perguntas sobre todos os pokemons existentes e perguntas como <Qual o nome daquele pokemon com o rabo pegando fogo?> \
    e sua resposta seria por exemplo <Você deve estar pensando no Charmander! Ele é um dos Pokémon iniciais do tipo Fogo e é famoso pela chama em sua cauda, que mostra a força de sua vida. \
    Voce precisa basear sua resposta no seguinte contexto, e nao deve criar informacoes, bases no dados reais a seguir:\n\n{context}\n\n
    Pergunta: {question}\n\n
    Resposta:"""
    return ask_llm(prompt)
      

# CAVALO
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