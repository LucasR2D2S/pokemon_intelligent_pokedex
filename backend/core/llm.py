import requests
from core.config import OLLAMA_HOST, MODEL_NAME
import json

def ask_llm(prompt: str) -> str:
    try:
        full_text = ""
        with requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": MODEL_NAME, "prompt": prompt, "stream": True},
            stream=True,
            timeout=60  # segurança contra travamentos
        ) as response:
            for line in response.iter_lines():
                if line:
                    # remove prefixo "data: " se existir (Ollama envia assim às vezes)
                    line = line.decode("utf-8").strip()
                    if line.startswith("data: "):
                        line = line[len("data: "):]
                    try:
                        part = json.loads(line)
                        full_text += part.get("response", "")
                    except json.JSONDecodeError:
                        print(f"[ignorado] linha inválida: {line}")
        return full_text or "Sem resposta do modelo."
    except Exception as e:
        print(f"Erro no ask_llm: {e}")
        return f"Erro ao se comunicar com o modelo: {e}"
    
"""
def ask_llm(prompt: str) -> str:
    try:
        json = {}
        with requests.post(f"{OLLAMA_HOST}/api/generate", json={"model": MODEL_NAME, "prompt": prompt, "stream": True}) as response:
            full_text = ""
            for line in response.iter_lines():
                if line:
                    part = json.loads(line)
                    full_text += part.get("response", "")
        return full_text
    except Exception as e:
        return f"Erro ao se comunicar com o modelo: {e}"
"""