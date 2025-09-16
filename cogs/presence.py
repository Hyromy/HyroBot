import discord

from asyncio import sleep
from discord.ext.commands import Cog

from utils.bot import Hyro

class Presence(Cog):
    def __init__(self, Hyro: Hyro):
        self.hyro = Hyro

    async def count_status(self):
        await self.hyro.wait_until_ready()
        i = 0

        while not self.hyro.is_closed():
            await self.hyro.change_presence(
                activity = discord.Activity(
                    type = discord.ActivityType.playing,
                    name = f"Counting: {i}"
                )
            )
            i += 1
            await sleep(10)

async def setup(Hyro: Hyro):
    await Hyro.add_cog(Presence(Hyro))
