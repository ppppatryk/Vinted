import os
import time
import discord
from discord.ext import commands
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

# Ustawienia ze zmiennych środowiskowych
TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])

# Ścieżki do przeglądarki i drivera
CHROMEDRIVER_PATH = "./chromedriver"
CHROME_BINARY_PATH = "./chrome-linux64/chrome"

# Link do monitorowania
VINTED_URL = "https://www.vinted.pl/catalog?catalog[]=3661&brand_ids[]=54661&search_id=20504041050&order=newest_first&time=1751358879&catalog_from=0&page=1&price_from=100&currency=PLN&sim_lock_ids[]=1313"

# Inicjalizacja bota Discord
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Pamięć ogłoszeń (FIFO 140 pozycji)
seen_ads = []

@bot.event
async def on_ready():
    print(f"✅ Zalogowano jako {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("✅ Bot działa!")
    await collect_initial_ads(channel)

async def collect_initial_ads(channel):
    global seen_ads
    soup = get_vinted_html()
    items = soup.find_all("div", class_="feed-grid__item")

    for item in items:
        ad_url = extract_ad_url(item)
        if ad_url:
            seen_ads.append(ad_url)
            if len(seen_ads) > 140:
                seen_ads = seen_ads[-140:]

    await channel.send("✅ Skończyłem zapisywać pierwsze ogłoszenia.")
    await monitor_ads(channel)

async def monitor_ads(channel):
    global seen_ads
    while True:
        try:
            soup = get_vinted_html()
            items = soup.find_all("div", class_="feed-grid__item")

            for item in items:
                ad_url = extract_ad_url(item)
                if not ad_url or ad_url in seen_ads:
                    continue

                title = extract_title(item)
                price = extract_price(item)
                if title and price:
                    await channel.send(f"🛍️ **{title}**\n💸 {price}\n🔗 {ad_url}")

                seen_ads.append(ad_url)
                if len(seen_ads) > 140:
                    seen_ads = seen_ads[-140:]

            time.sleep(1)
        except Exception as e:
            print(f"❌ Błąd monitorowania: {e}")
            await channel.send("⚠️ Wystąpił błąd podczas monitorowania, próbuję ponownie za 5s...")
            time.sleep(5)

def get_vinted_html():
    import os
    os.chmod('./chrome-linux64/chrome', 0o755)

    options = uc.ChromeOptions()
    options.binary_location = CHROME_BINARY_PATH
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = uc.Chrome(driver_executable_path=CHROMEDRIVER_PATH, options=options)
    browser.get(VINTED_URL)
    time.sleep(3)

    soup = BeautifulSoup(browser.page_source, "html.parser")
    browser.quit()
    return soup

def extract_ad_url(item):
    link_tag = item.find("a", href=True)
    if link_tag:
        return "https://www.vinted.pl" + link_tag["href"]
    return None

def extract_title(item):
    tag = item.find("p", {"data-testid": lambda x: x and "--description-title" in x})
    return tag.text.strip() if tag else None

def extract_price(item):
    tag = item.find("span", class_="web_ui__Text__subtitle")
    return tag.text.strip().replace("\xa0", " ") if tag else None

# Uruchomienie bota
bot.run(TOKEN)
