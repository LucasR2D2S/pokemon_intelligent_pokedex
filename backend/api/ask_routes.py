from fastapi import APIRouter, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from services.ask_service import ask_assistant
from pydantic import BaseModel

router = APIRouter()

class AskInput(BaseModel):
    question: str


@router.post("/ask")
async def ask(request: Request):
    try:
        data = await request.json()
        question = data.get("question")
        if not question:
            raise HTTPException(status_code=400, detail="Pergunta ausente")

        # Executa função síncrona em threadpool para evitar travamento
        resposta = await run_in_threadpool(ask_assistant, question)
        return {"answer": resposta}

    except Exception as e:
        import traceback
        print("\n[ERRO INTERNO]")
        traceback.print_exc()
        print("[FIM DO ERRO]\n")
        raise HTTPException(status_code=500, detail="Erro interno ao processar pergunta")


"""
@router.post("/ask")
async def ask(request: Request):
    data = await request.json()
    question = data.get("question")
    if not question:
        raise HTTPException(status_code=400, detail="Pergunta ausente")
    return {"answer": ask_assistant(question)}


teste de rota simples para verificar se o servidor está funcionando
@router.post("/ask")
async def simple_ask(input: AskInput):
    return {"answer": f"Sua pergunta foi: {input.question}"}
"""