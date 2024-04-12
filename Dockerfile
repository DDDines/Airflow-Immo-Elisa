# Use a imagem oficial do Airflow com Python 3.9 como base
FROM apache/airflow:2.2.3-python3.9

# Define o diretório de trabalho no container
WORKDIR /usr/src/app

# Atualiza o pip
RUN pip install --upgrade pip

# Copia o arquivo requirements.txt para o diretório atual no container
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt