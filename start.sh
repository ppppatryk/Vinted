#!/bin/bash
echo "📥 Pobieram Chromium..."

wget -q https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1155276/chrome-linux.zip -O chrome-linux.zip
unzip -qq chrome-linux.zip

echo "✅ Nadaję prawa do uruchamiania..."
chmod +x chrome-linux/chrome

echo "✅ Gotowe. Uruchamiam bota..."
python bot.py
