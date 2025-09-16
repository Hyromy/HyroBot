from aiohttp import ClientSession
from discord import Object
from discord.ext.commands import Bot
from typing import List, Optional
from os import getenv

class Hyro(Bot):
    def __init__(
        self,
        *args,
        api_url: str,
        debug: bool = True,
        initial_extensions: List[str],
        web_client: ClientSession,
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        
        self.api_url = api_url
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions

        self.debug = debug
        self.version = None

    async def setup_hook(self):
        print(f"Setting up {self.user}...")

        self.remove_command("help")

        await self.__load_extensions()
        await self.__set_version()
        await self.__set_testing_guild()
        await self.__set_app_commands()
        await self.__set_views()
        await self.__set_dynamic()

    async def close(self):
        await super().close()
        
        await self.web_client.close()

    async def __load_extensions(self):
        for extension in self.initial_extensions:
            error = None
            try:
                await self.load_extension(extension)

            except Exception as e:
                error = e

            tag = "OK" if not error else "FAIL"
            reason = "loaded" if not error else f"failed to load: -> {error}"
            print(f"[{tag}]\t{self.user.name}.{extension.split('.', 1)[-1]} {reason}")

        loaded = len(self.extensions)
        extensions = len(self.initial_extensions)

        print(f"\nLoaded {loaded} / {extensions} extensions")

    async def __set_version(self):
        self.version = (
            await (
                await self.web_client.get(getenv("REPO_URL"))
            ).json()
        )[0]["name"]

    async def __set_testing_guild(self):
        if self.testing_guild_id:
            guild = Object(self.testing_guild_id)
            self.tree.copy_global_to(guild = guild)
            await self.tree.sync(guild = guild)

    async def __set_app_commands(self):
        await self.tree.sync()

    async def __set_views(self):
        pass

    async def __set_dynamic(self):
        pass
