import zipfile
import requests
import os

# Link do Chromium snapshot (działa z undetected-chromedriver)
CHROME_URL = "https://storage.googleapis.com/chromium-browser-snapshots/Linux_x64/1181205/chrome-linux.zip"

def download_and_extract(url, extract_to="."):
    filename = "chrome-linux.zip"
    print("📥 Pobieram Chromium...")
    r = requests.get(url, stream=True)
    with open(filename, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print("✅ Rozpakowuję...")
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove(filename)
    print("✅ Gotowe.")

download_and_extract(CHROME_URL)
