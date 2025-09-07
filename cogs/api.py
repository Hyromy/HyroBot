from discord import app_commands, Interaction

from discord.ext.commands import Cog

from utils.bot import Hyro

class Api(Cog):
    def __init__(self, hyro: Hyro):
        self.hyro = hyro

    @app_commands.command()
    async def api_guild(self, interaction: Interaction):
        await interaction.response.defer(ephemeral = True)
        
        request =  self.hyro.api_url + "guild"
        resp = await self.hyro.web_client.get(request)
        data = await resp.json()

        await interaction.followup.send(f"{request} -> {data}")

async def setup(Hyro: Hyro):
    await Hyro.add_cog(Api(Hyro))
