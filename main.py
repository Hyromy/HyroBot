from asyncio import run
from aiohttp import ClientSession
from discord import Intents
from dotenv import load_dotenv
from os import getenv

from utils.bot import Hyro
from utils.functions import get_cogs_name
from utils.logger import set_logger

async def main():
    debug = getenv("DEBUG", True) != "False"
    
    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    KWARGS = {
        "api_url": getenv("API_URL"),
        "command_prefix": ",",
        "debug": debug,
        "initial_extensions": get_cogs_name(),
        "intents": intents,
        "web_client": ClientSession(),
        "testing_guild_id": int(getenv("HOME_GUILD"))
    }

    async with Hyro(**KWARGS) as hyro:
        await hyro.start(
            getenv(("DEBUG_" if debug else "") + "DISCORD_BOT_TOKEN")
        )

if __name__ == '__main__':
    load_dotenv()
    set_logger()

    try: 
        run(main())
    
    except KeyboardInterrupt:
        print("Kill Switch Activated")

    except Exception as e:
        print(f"asyncio.run fail -> <{e.__class__.__name__}>: {e}")
