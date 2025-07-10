#!/bin/bash

echo "📥 Pobieram Chromium..."
wget https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chrome-linux64.zip
unzip chrome-linux64.zip
chmod +x chrome-linux64/chrome


echo "✅ Gotowe. Uruchamiam bota..."
python bot.py
