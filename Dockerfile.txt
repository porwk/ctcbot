# Use uma imagem base Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie o código da aplicação e o requirements.txt
COPY . /app

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Comando para iniciar a aplicação
CMD ["python", "bot_telegram.py"]

