FROM python:3.11-slim

# Variável para não gerar arquivos pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y build-essential

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY . /app

# Instala dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe a porta da API
EXPOSE 8000

# Comando padrão para rodar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
