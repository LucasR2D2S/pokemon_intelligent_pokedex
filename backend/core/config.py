import os
from pydantic import BaseSettings, Field, validator
from typing import Optional

class Settings(BaseSettings):
    # Configurações com validações e variáveis de ambiente.
    
    database_url: str = Field(
        default="sqlite:///./pokedex.db",
        description="URL de conexão com o banco de dados"
    )

    ollama_host: str = Field(
        default="http://localhost:11436",
        description="Host do serviço Ollama"
    )

    ollama_model: str = Field(
        default="gemma3:4b",
        description="Modelo do Ollama a ser utilizado"
    )

    embedding_model: str = Field(
        default="nomic-embed-text",
        description="Modelo de embedding a ser utilizado"
    )

    api_title: str = Field(
        default="Pokemon Intelligent Pokedex API",
        description="Título da API"
    )

    api_description: str = Field(
        default="API para interagir com a Pokedex Inteligente, com RAG e LLM",
        description="Descrição da API"
    )

    api_version: str = Field(
        default="1.0.0",
        description="Versão da API"
    )

    # CORS settings
    allowed_origins: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:5173"],
        description="Lista de origens permitidas para CORS"
    )

    # Logging settings
    log_level: str = Field(
        default="INFO",
        description="Nível de log"
    )

    # Performance settings
    llm_timeout: int = Field(
        default=60,
        description="Timeout para chamadas ao LLM em segundos"
    )

    max_question_length: int = Field(
        default=500,
        description="Comprimento máximo permitido para perguntas"
    )

    vector_store_k: str = Field(
        default=3,
        description="Número de documentos similares a serem recuperados"
    )

    environment: str = Field(
        default="development",
        description="Ambiente de execução (development, production, etc.)"
    )

    @validator("ollama_host")
    def validate_ollama_host(cls, v):
        # Validando URL do Ollama
        if not v.startswith(('http://', 'https://')):
            raise ValueError("Ollama host must start with http:// or https://") 
        return v.rstrip('/')
    
    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v.upper()
    
    @validator('environment')
    def validate_environment(cls, v):
        valid_envs = ['development', 'production', 'testing']
        if v not in valid_envs:
            raise ValueError(f"environment must be one of {valid_envs}")
        return v.lower()
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        env_prefix = "POKEDEX_"

settings = Settings()