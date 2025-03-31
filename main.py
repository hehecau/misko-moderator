import discord
import os
from dotenv import load_dotenv
import datetime
import random
from discord.ext import commands

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True  # Umožňuje prístup k obsahu správ
bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print("Discord bot started")
    try:
        # Načítanie cogu správne
        await bot.load_extension('cogs.commands')
        print("Cog loaded successfully!")
    except Exception as e:
        print(f"Error loading cog: {e}")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.id == 830513996443680818:
        banned_words = ["badword1", "badword2"]  # Pridaj svoje zakázané slová sem
        for word in banned_words:
            if word in message.content.lower():
                member = message.guild.get_member(message.author.id)
                timeout_duration = datetime.timedelta(minutes=random.randint(1, 20))  # nastaviteľný čas
                await member.timeout(timeout_duration, reason=f"Timeout na {timeout_duration} minút")
                await message.channel.send(f"Misko dostal timeout na {timeout_duration} minut pretože použil zlé slovo!!!")

bot.run(os.getenv("TOKEN"))
