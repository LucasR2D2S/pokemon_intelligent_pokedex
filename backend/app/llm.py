import requests
from fastapi import HTTPException

def ask_llm(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11436/api/generate",
            json={"model": "gemma3:4b",
                  "prompt": prompt,
                  "stream": False
                  },
        )
        data = response.json()
        return data.get("response", "").strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao se comunicar com o LLM: {str(e)}")