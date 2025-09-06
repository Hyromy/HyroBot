from discord.ext import commands

from utils.bot import Hyro

class Events(commands.Cog):
    def __init__(self, hyro: Hyro):
        self.hyro = hyro

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.hyro.user.name}")

async def setup(Hyro: commands.Bot):
    await Hyro.add_cog(Events(Hyro))
    