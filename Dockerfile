# Ustaw bazowy obraz z Pythonem
FROM python:3.11

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki projektu
COPY . .
RUN chmod +x start.sh

# Instaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Uruchom bota
CMD ["./start.sh"]

