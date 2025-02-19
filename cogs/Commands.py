import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, Hyromy:commands.Bot):
        self.Hyromy = Hyromy

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.Hyromy.latency * 1000)}ms")

async def setup(Hyromy:commands.Bot):
    await Hyromy.add_cog(Commands(Hyromy))