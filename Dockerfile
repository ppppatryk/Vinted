# Ustawienia katalogu roboczego
WORKDIR /app

# Skopiuj pliki do obrazu
COPY . .

# Instalacja zależności Pythona
RUN pip install --no-cache-dir -r requirements.txt

# Pobierz Chromium i nadaj uprawnienia
RUN python download_chrome.py && chmod +x chrome-linux/chrome

# Start
CMD ["python", "bot.py"]
