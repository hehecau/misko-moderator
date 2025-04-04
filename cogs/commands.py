import random
import time
from datetime import timedelta
import discord
from discord.ext import commands

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Spamuser
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

    # help
    @commands.command(name="helpme")
    async def sendHelpMessage(self, ctx):
        embed = discord.Embed(title="Misko bot v1.0", url="https://github.com/hehecau/misko-moderator", description="Open source discord.py based discord bot na moderáciu miska.", colour=0xffdd00)
        embed.set_author(name="Misko bot")
        embed.add_field(name="Príkazy", value="**?spamuser <Počet> <Uživateľ>** - Podľa počtu začne spamovať tag na uživateľa (misko nepodporuje nad 100 braincells)\n**?helpme** - Zobrazí toto menu.\n**?timeout <@User> <Dĺžka>** - timeoutne používateľa", inline=False)
        embed.set_thumbnail(url="https://i.imgur.com/fm6q0oN.png")
        embed.set_footer(text="misko moderator - vyrobene v socialistickej demokratickej republike", icon_url="https://i.imgur.com/fm6q0oN.png")
        await ctx.send(embed=embed)

    #timeout
    @commands.command(name="timeout")
    @commands.has_permissions(administrator=True)
    async def timeout(self, ctx, user: discord.Member, length: int):
        if length < 43200: # mesiac
            duration = timedelta(seconds=length * 60)
            await user.timeout(duration)
            await ctx.send(f"Používateľ {user.name} bol timeoutnutý na {length} minút.")
        else:
            await ctx.send('Maximálny časový limit je 43200 sekúnd (1 mesiac).')

    @timeout.error
    async def timeout_errorHandle(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Použitie: `?timeout <@User> <Dĺžka (minúty)>`")

    @commands.command(name="clean")
    @commands.has_permissions(manage_messages=True)
    async def cleanMessages(self, ctx, count: int):
        if count < 100:
            await ctx.channel.purge(limit=count)
            await ctx.send(f"Zmazaných {count} správ.", delete_after=5)
        else:
            await ctx.send(f"Nemožno zmazať viac ako 100 správ.", delete_after=5)

    @cleanMessages.error
    async def cleanMessageError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Použitie: `?clean <Počet správ>")

    @commands.command(name="coinflip")
    async def makeACoinFlip(self, ctx, side: int, opponent: discord.Member):
        vysledok = random.randint(1, 2)
        side_string = "hlava" if side == 1 else "znak"
        vysledok_str = "hlava" if vysledok == 1 else "znak"
        embed = discord.Embed(title="Coin Flip", description=f"Coinflip medzi - {ctx.author.display_name} a {opponent.display_name}\n{ctx.author.display_name} si vybral: **{side_string}**\n{opponent.display_name} si vybral: **{vysledok_str}**", colour=0xfffb00)
        embed.set_author(name="Coin Flip - Misko bot")

        if side == vysledok:
            embed.add_field(name="Výsledok hodu mincou", value=f"Výsledok hodu je: **{vysledok_str}** - vyhráva {ctx.author.display_name}!", inline=False)
        else:
            embed.add_field(name="Výsledok hodu mincou", value=f"Výsledok hodu je: **{vysledok_str}** - vyhráva {opponent.display_name}!", inline=False)

        if vysledok == 1:
            embed.set_image(url="https://i.imgur.com/dc76ePW.png")
        else:
            embed.set_image(url="https://i.imgur.com/QP5O8dV.png")
        embed.set_footer(text="Coinflip - Misko bot")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(CommandCog(bot))