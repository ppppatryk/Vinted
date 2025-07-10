import discord
from discord.ext import commands
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import os

TOKEN = os.environ["DISCORD_TOKEN"]
CHANNEL_ID = int(os.environ["CHANNEL_ID"])
VINTED_URL = "https://www.vinted.pl/catalog?catalog[]=3661&brand_ids[]=54661&search_id=20504041050&order=newest_first&time=1751358879&catalog_from=0&page=1&price_from=100&currency=PLN&sim_lock_ids[]=1313"

CHROMEDRIVER_PATH = "./chromedriver"
CHROME_BINARY_PATH = "./chrome-linux/chrome"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

seen_ads = []

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("✅ Bot działa")
    await collect_initial_ads(channel)

async def collect_initial_ads(channel):
    global seen_ads
    options = uc.ChromeOptions()
    options.binary_location = CHROME_BINARY_PATH
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    browser = uc.Chrome(driver_executable_path=CHROMEDRIVER_PATH, options=options)
    
    browser.get(VINTED_URL)
    time.sleep(3)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    items = soup.find_all("div", class_="feed-grid__item")
    for item in items:
        link_tag = item.find("a", href=True)
        title_tag = item.find("p", {"data-testid": lambda x: x and "--description-title" in x})
        price_tag = item.find("span", class_="web_ui__Text__subtitle")
        if not link_tag or not title_tag or not price_tag:
            continue
        url = "https://www.vinted.pl" + link_tag["href"]
        seen_ads.append(url)
        if len(seen_ads) > 140:
            seen_ads = seen_ads[-140:]

    await channel.send("✅ Skończyłem zapisywać pierwsze ogłoszenia.")
    browser.quit()
    await check_new_ads(channel)

async def check_new_ads(channel):
    global seen_ads
    while True:
        try:
            options = uc.ChromeOptions()
            options.binary_location = CHROME_BINARY_PATH
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            browser = uc.Chrome(driver_executable_path=CHROMEDRIVER_PATH, options=options)

            browser.get(VINTED_URL)
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            items = soup.find_all("div", class_="feed-grid__item")
            for item in items:
                link_tag = item.find("a", href=True)
                title_tag = item.find("p", {"data-testid": lambda x: x and "--description-title" in x})
                price_tag = item.find("span", class_="web_ui__Text__subtitle")
                if not link_tag or not title_tag or not price_tag:
                    continue
                url = "https://www.vinted.pl" + link_tag["href"]
                title = title_tag.text.strip()
                price = price_tag.text.strip()

                if url not in seen_ads:
                    await channel.send(f"🛍️ **{title}**\n💸 {price}\n🔗 {url}")
                    seen_ads.append(url)
                    if len(seen_ads) > 140:
                        seen_ads = seen_ads[-140:]

            browser.quit()
            time.sleep(1)
        except Exception as e:
            print("Błąd:", e)
            await channel.send("❌ Wystąpił błąd podczas skanowania. Próbuję ponownie...")
            time.sleep(5)
