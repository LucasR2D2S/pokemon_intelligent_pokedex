from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.schema import Document
from database.db import SessionLocal
from database.models import Pokemon
from core.config import settings  # Using our new config system
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class FAISSManager:
    def __init__(self):
        self.index: Optional[FAISS] = None
        self.embedding = OllamaEmbeddings(
            model=settings.embedding_model, 
            base_url=settings.ollama_host
        )

    def build_index(self) -> None:
        db = SessionLocal()
        try:
            logger.info("Iniciando a construção do índice FAISS.")

            pokemons = db.query(Pokemon).all()
            if not pokemons:
                logger.warning("Nenhum Pokémon encontrado no banco de dados para construir o índice."),
                raise ValueError("Nenhum Pokémon encontrado no banco de dados.")
            
            docs = []

            for pokemon in pokemons:
                doc_text = self._format_pokemon_document(pokemon)
                docs.append(Document(
                    page_content=doc_text, 
                    metadata={
                        "id": pokemon.id,
                        "name": pokemon.name,
                        "types": pokemon.types,
                        "generation": pokemon.generation,
                        "stats": pokemon.stats,
                        "full_description": pokemon.full_description
                    }
                ))

            self.index = FAISS.from_documents(docs, self.embedding)
            logger.info(f"Índice FAISS construído com sucesso, com {len(docs)} documentos.")

        except Exception as e:
            logger.error(f"Erro ao construir o índice FAISS: {str(e)}")
            raise
        finally:
            db.close()

    def _format_pokemon_document(self, pokemon: Pokemon) -> str:
        # Formata as informações do Pokémon em um texto coerente para o documento.
        full_description = getattr(pokemon, 'full_description', None)
        if not full_description:
            parts = []

            if hasattr(pokemon, 'general_description') and pokemon.general_description:
                parts.append(pokemon.general_description)
            if hasattr(pokemon, 'physical_characteristics') and pokemon.physical_characteristics:
                parts.append(f"Physical: {pokemon.physical_characteristics}")
            if hasattr(pokemon, 'behavior') and pokemon.behavior:
                parts.append(f"Behavior: {pokemon.behavior}")
            if hasattr(pokemon, 'habitat') and pokemon.habitat:
                parts.append(f"Habitat: {pokemon.habitat}")

            full_description = "\n".join(parts)
        
        return (
            f"Name: {pokemon.name}\n"
            f"Types: {', '.join(pokemon.types) if pokemon.types else 'Unknown'}\n"
            f"Generation: {pokemon.generation}\n"
            f"Stats: {', '.join(map(str, pokemon.stats)) if pokemon.stats else 'Unknown'}\n"
            f"Description:\n{full_description}"
        )
    
    def retrieve_context(self, question: str, k: int = None) -> str:
        # Question: Questão do usuário
        # k: Numero de documentos sendo buscados
        # Return: Contextos similares contatenados

        if k is None:
            k = settings.vector_store_k

        try:
            if not self.index:
                logger.info("Index not found, building new index")
                self.build_index()

            docs = self.index.similarity_search(question, k=k)

            if not docs:
                logger.warning("Sem documentos similares sobre a pergunta")
                return ("Sem informações relevantes encontradas")
            
            context = "\n---\n".join([doc.page_content for doc in docs])

            logger.info(f"Retornado {len(docs)} documentos para contexto")
            return context
        
        except Exception as e:
            logger.error(f"Erro retornando contexto {str(e)}")
            return "Erro retornando informações de Pokemon."
        
    def rebuild_index(self) -> None:
        # Forçar o rebuild do index.
        logger.info("Forçando o rebuild do index")
        self.index = None
        self.build_index()

    def get_index_info(self) -> dict:
        # Buscando informações sobre o index atual
        if not self.index:
            return{"status": "not_built", "document_count": 0}
        
        return {
            "status": "ready",
            "document_count": self.index.index.ntotal,
            "embedding_model": settings.embedding_model
        }
    

faiss_manager = FAISSManager()

def retrieve_context(question: str, k: int = None) -> str:
    # Retornando contexto usando o FAISS manager.
    return faiss_manager.retrieve_context(question,k)

def build_index() -> None:
    # Construindo index utilizando o FAISS manager.
    faiss_manager.build_index()