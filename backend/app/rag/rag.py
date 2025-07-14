from langchain.vectorstores import FAISS
from langchain.embeddings import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
import os

# Caminho do índice
INDEX_PATH = "data/faiss_index"

# Função principal para responder perguntas
def answer_question_with_faiss(question: str) -> str:
    # 1. Conecta ao índice FAISS
    if not os.path.exists(INDEX_PATH):
        raise ValueError("Índice FAISS não encontrado. Gere-o primeiro.")

    vectorstore = FAISS.load_local(INDEX_PATH, embeddings=OllamaEmbeddings(model="gemma3:4b"), allow_dangerous_deserialization=True)

    # 2. Conecta ao modelo LLM
    llm = Ollama(model="gemma3:4b", base_url="http://localhost:11436")

    # 3. Define o prompt com contexto
    prompt = PromptTemplate.from_template("""Você é um especialista em Pokemon, deve responder perguntas como uma Pokédex.

    Utilize o seguinte contexto de base pra responder à pergunta:
    {context}

    Para gerar a pergunta, não imagine ou crie informações, apenas use o contexto fornecido.

    Pergunta: {question}
    Resposta:""")

    # 4. Monta a cadeia de QA com RAG
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=False
    )

    # 5. Executa a cadeia
    result = qa_chain.run(question)
    return result
