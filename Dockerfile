# Usar uma imagem base do Python
FROM python:3.9-slim

# Atualizar os pacotes e instalar dependências
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    default-jdk \
    gnupg \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Adicionar o repositório do Google Chrome e instalar a versão mais recente
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable

# Instalar o ChromeDriver mais recente (compatível com a versão do Chrome instalada)
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver_linux64.zip

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . .

# Instalar as dependências Python do projeto
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Definir o comando padrão para rodar o script
CMD ["python", "questao2/questao2.py", "511082"]
