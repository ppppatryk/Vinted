#!/bin/bash
echo "📥 Pobieram Chromium..."
#nowy
wget https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chrome-linux.zip
unzip -qq chrome-linux.zip

echo "✅ Nadaję prawa do uruchamiania..."
chmod +x chrome-linux/chrome

echo "✅ Gotowe. Uruchamiam bota..."
python bot.py
