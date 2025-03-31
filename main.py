import discord
import os
from dotenv import load_dotenv
import datetime
import random

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents, command_prefix="?")

@client.event
async def on_ready():
    print("Discord bot started")

banned_words = ["nigga", "nigerska", "niga", "niger"]
@client.event
async def on_message(message):
    if message.author.id == 830513996443680818:
        for word in banned_words:
            if str(message.content).lower() == word:
                member = message.guild.get_member(message.author.id)
                timeout_duration = datetime.timedelta(minutes=random.randint(1, 20))  # nastavitelny cas
                await member.timeout(timeout_duration, reason=f"Timeout na {timeout_duration} minút")
                await message.channel.send(f"fMisko dostal timeout na {timeout_duration} minut pretoze pouzil zle slovicko!!!")


client.run(os.getenv('TOKEN'))