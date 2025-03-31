import discord
from discord.ext import commands

class CommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spam(self, ctx, times: int, user: discord.User):
        """
        Spamuje tag užívateľa určitý počet krát.
        :param times: počet opakovaní tagu
        :param user: užívateľ, ktorý bude tagovaný
        """
        for _ in range(times):
            await ctx.send(f"{user.mention}")

    @commands.command()
    async def hello(self, ctx):
        """
        Jednoduchý príkaz na pozdrav.
        """
        await ctx.send("Ahoj! 👋")

    @commands.command()
    async def echo(self, ctx, *, message: str):
        """
        Opakuje správu od používateľa.
        """
        await ctx.send(message)

# Pridanie cogu do bota (s await)
async def setup(bot):
    await bot.add_cog(CommandCog(bot))