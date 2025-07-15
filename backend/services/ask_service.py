from utils.faiss import retrieve_context
from core.llm import ask_llm

def ask_assistant(question: str):
    context = retrieve_context(question)
    prompt = f"Use as informações abaixo para responder a pergunta:\n\n{context}\n\nPergunta: {question}"
    return ask_llm(prompt)