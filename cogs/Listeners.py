import discord
from discord.ext import commands

class Listeners(commands.Cog):
    def __init__(self, Hyromy:commands.Bot):
        self.Hyromy = Hyromy

    @commands.Cog.listener()
    async def on_message(self, msg:discord.Message):
        if msg.author.bot:
            return

        if self.Hyromy.user.mentioned_in(msg) and "prefix" in msg.content:
            await msg.channel.send("Mi prefijo es `.`")

async def setup(Hyromy:commands.Bot):
    await Hyromy.add_cog(Listeners(Hyromy))