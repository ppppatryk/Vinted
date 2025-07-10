#!/bin/bash
echo "📥 Pobieram Chromium..."
#nowy
https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chrome-linux64.zip
unzip -qq chrome-linux64.zip

echo "✅ Nadaję prawa do uruchamiania..."
chmod +x chrome-linux64/chrome

echo "✅ Gotowe. Uruchamiam bota..."
python bot.py
