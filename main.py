from asyncio import run, gather
from os import getenv

from discord import Intents
from discord.ext.commands import Bot
from dotenv import load_dotenv

from utils import on_load

intents = Intents.default()
intents.message_content = True

Hyromy = Bot(
    command_prefix = ".",
    intents = intents
)

@Hyromy.event
async def on_ready():
    tasks = {
        "cogs": on_load.load_cogs(Hyromy),
        "header": on_load.header(Hyromy)
    }
    response = await gather(*tasks.values())
    results = dict(zip(tasks.keys(), response))

    print(results["header"])
    print()

load_dotenv(".env")

async def main():
    async with Hyromy:
        await Hyromy.start(getenv("DISCORD_BOT_TOKEN"))

if __name__ == "__main__":
    print("Iniciando...")
    run(main())
