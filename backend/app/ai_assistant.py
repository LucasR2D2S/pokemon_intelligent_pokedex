import requests
from fastapi import HTTPException

def ask_llm(question: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11435/api/generate",
            json={"model": "gemma3:4b",
                  "prompt": f"Você é uma Pokedex, Voce ira receber perguntas sobre todos os pokemons existentes e perguntas como <Qual o nome daquele pokemon com o rabo pegando fogo?> \
                    e sua resposta seria por exemplo <Você deve estar pensando no Charmander! Ele é um dos Pokémon iniciais do tipo Fogo e é famoso pela chama em sua cauda, que mostra a força de sua vida. \
                    Se a chama está fraca, significa que ele não está muito bem.>. Responda a seguinte pergunta:\n\n{question}\n\nResposta:",
                  "stream": False
                  },
            timeout=10  # Timeout after 10 seconds
        )
        data = response.json()
        return data.get("response", "").strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao se comunicar com o LLM: {str(e)}")