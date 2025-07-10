FROM python:3.11-slim

# Instalacja zależności systemowych
RUN apt-get update && \
    apt-get install -y wget unzip chromium && \
    rm -rf /var/lib/apt/lists/*

# Ustawienia katalogu roboczego
WORKDIR /app

# Kopiuj wszystkie pliki do obrazu
COPY . .

# Instalacja zależności Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Pobranie Chromium przed uruchomieniem
RUN python download_chrome.py

# Komenda startowa
CMD ["python", "bot.py"]
