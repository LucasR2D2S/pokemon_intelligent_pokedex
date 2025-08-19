from fastapi import APIRouter, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from services.ask_service import ask_assistant
from pydantic import BaseModel, Field, validator
import logging
from typing import Optional
import time

logger = logging.getLogger(__name__)

router = APIRouter()

class AskInput(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=500,
        description="A pergunta que o usuário deseja fazer à Pokédex.",
        example="Qual é o tipo do Pikachu?"
    )

    # Validações adicionais para a pergunta
    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError("A pergunta não pode estar vazia.")

        dangerous_chars = ['<', '>', '{', '}', '[', ']', '(', ')', ';', ':', '"', "'", '\\', '/', '|']
        if any(char in v for char in dangerous_chars):
            raise ValueError("A pergunta contém caracteres potencialmente perigosos.")  
        
        return v.strip()

class AskResponse(BaseModel):
    answer: str 
    status: str = "success"
    processing_time: Optional[float] = None

class QuestionProcessingError(Exception):
    #Utilizado quando para lidar com erros nas perguntas
    pass

class LLMServiceError(Exception):
    #Utilizado para lidar com erros no processo de LLM
    pass

@router.post("/ask", responde_model=AskResponse)
async def ask(ask_input: AskInput):
    
    start_time=time.time()

    try:
        logger.info(
            f"Recebendo pergunta do usuário",
            extra={
                "question_length": len(ask_input.question),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "user_ip": "unknown"  # Pode ser extraído de request.client.host se necessário
            }
        )

        data = await ask_input.json()
        question = data.get("question")
        
        # Executa função síncrona em threadpool para evitar travamento
        resposta = await run_in_threadpool(ask_assistant, question)
        
        if not resposta or resposta.stip() == "":
            raise QuestionProcessingError("Resposta do assistente vazia")
        
        processing_time = time.time() - start_time

        logger.info(
            "Resposta processada com sucesso",
            extra={
                "processing_time": processing_time,
                "answer_length": len(resposta)
            }
        )

        return AskResponse(
            answer=resposta,
            status="success",
            processing_time=processing_time
        )

    except QuestionProcessingError as e:
        logger.warning(f"Processo da pergunta falhou: {str(e)}")
        raise HTTPException(
            status_code=422,
            detail="Não foi possível processar a pergunta reenvie de uma outra maneira."
        )
    
    except LLMServiceError as e:
        logger.error(f"Erro no modelo: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Modelo temporariamente indisponivel, por favor tente novamente mais tarde"
        )

    except Exception as e:
        logger.error(
            "Erro no processamento da pergunta",
            exc_info=True,
            extra={"question_length": len(ask_input.question)}
        )
        
        raise HTTPException(
            status_code=500,
            detail="Um erro inesperado occoreu. O suporte foi notificado"
        )

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