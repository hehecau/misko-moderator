import time

import discord
from discord.ext import commands

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spamuser(self, ctx, times: int, user: discord.User):
        if times < 100:
            for _ in range(times):
                await ctx.send(f"{user.mention}")
                time.sleep(0.9)
        else:
            await ctx.send("Misko nema mozgovu kapacitu na take velke cisla")

    @spamuser.error
    async def spamuser_errorHandle(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Použitie: `?spamuser <Počet opakovaní> <@User>`")

    @commands.command(name="helpme")
    async def sendHelpMessage(self, ctx):
        embed = discord.Embed(title="Misko bot v1.0", url="https://github.com/hehecau/misko-moderator", description="Open source discord.py based discord bot na moderáciu miska.", colour=0xffdd00)
        embed.set_author(name="Misko bot")
        embed.add_field(name="Príkazy", value="**?spamuser <Počet> <Uživateľ>** - Podľa počtu začne spamovať tag na uživateľa (misko nepodporuje nad 100 braincells)\n**?helpme** - Zobrazí toto menu.", inline=False)
        embed.set_thumbnail(url="https://i.imgur.com/fm6q0oN.png")
        embed.set_footer(text="misko moderator - vyrobene v socialistickej demokratickej republike", icon_url="https://i.imgur.com/fm6q0oN.png")
        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(CommandCog(bot))