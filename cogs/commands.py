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



async def setup(bot):
    await bot.add_cog(CommandCog(bot))