#!/bin/bash

# Pobieranie Chromium, jeśli nie istnieje
if [ ! -f "./chrome-linux/chrome" ]; then
  python3 download_chrome.py
fi

# Uruchamianie bota
python3 bot.py
