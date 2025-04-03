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


async def setup(bot):
    await bot.add_cog(CommandCog(bot))