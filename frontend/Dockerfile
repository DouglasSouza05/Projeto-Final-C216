# Usando uma imagem base do Python
FROM python:3.10-slim

# Instalando dependências
RUN pip install flask requests

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando o código para o container
COPY . /app

# Exportando a porta 3000
EXPOSE 3000

# Comando para rodar a aplicação
CMD ["python", "app.py"]