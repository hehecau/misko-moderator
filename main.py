import discord
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random
from discord.ext import commands, tasks
import json
import requests
from bs4 import BeautifulSoup

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)
gif_file = "frequent_gifs.json"

def is_url(string):
    return string.startswith("http://") or string.startswith("https://")

@tasks.loop(hours=24)
async def daily_message():
    channel = bot.get_channel(1339264344680300605) # general
    today = datetime.now()
    end_of_year = datetime(today.year, 12, 31)
    end_of_school_year = datetime(today.year, 6, 30)
    end_of_school_year_days = (end_of_school_year - today).days # pocet dni do konca skolskeho roka
    end_of_year_days = (end_of_year - today).days #pocet dni do konca roka
    website_data = requests.get(r"https://kalendar.aktuality.sk/")
    soup_data = BeautifulSoup(website_data.text, 'html.parser')
    # najdenie dnesnych menin
    link = soup_data.find('a', class_='name-link first-name')
    title = link['title']

    embed = discord.Embed(title=f"Dnešný deň - {today.strftime("%d.%m.%Y")}", colour=0xffdd00)
    embed.set_author(name="Misko Bot")
    embed.add_field(name="Koniec roka", value=f"Do konca roka ostáva: **{end_of_year_days} dní**", inline=False)
    embed.add_field(name="Koniec školského roka", value=f"Do konca školského roka ostáva: **{end_of_school_year_days} dní**", inline=False)
    embed.add_field(name="Meniny", value=f"Dnes má meniny: **{title}**", inline=False)
    await channel.send(embed=embed)


@bot.event
async def on_ready():
    print("Discord bot started")
    try:
        await bot.load_extension('cogs.commands')
        print("Cog loaded successfully!")
    except Exception as e:
        print(f"Error loading cog: {e}")
    next_midnight = datetime.combine(datetime.now().date() + timedelta(days=1), datetime.min.time())
    seconds_until_midnight = (next_midnight - datetime.now()).seconds
    await discord.utils.sleep_until(next_midnight)
    daily_message.start()

def load_gif_urls():
    try:
        with open(gif_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_gif_urls(urls):
    with open(gif_file, 'w') as f:
        json.dump(urls, f)

gif_urls = load_gif_urls()
banned_words = ["niga", "nigga", "niger", "nigger", "bože", "sigma"]
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    # Zapamatanie GIFov
    if "gif" in message.content.lower() and is_url(message.content):
        if message.content not in gif_urls and message.author != bot.user:
            gif_urls.append(message.content)
            save_gif_urls(gif_urls)

    # Odoslanie nahodneho gifu zo suboru
    if bot.user.mentioned_in(message) or random.random() < 0.1: # 20%
        if gif_urls:
            random_gif = random.choice(gif_urls)
            await message.channel.send(random_gif)


    # Miskov filter na spravy
    if message.author.id == 830513996443680818:
        for word in banned_words:
            if word in message.content.lower():
                member = message.guild.get_member(message.author.id)
                timeout_duration = timedelta(minutes=random.randint(1, 20))  # nastaviteľný čas
                await member.timeout(timeout_duration, reason=f"Timeout na {timeout_duration} minút")
                await message.channel.send(f"Misko dostal timeout na {timeout_duration} minut pretože použil zlé slovo!!!")

bot.run(os.getenv("TOKEN"))
