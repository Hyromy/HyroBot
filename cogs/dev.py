from discord import app_commands, Interaction
from discord.ext.commands import Cog
from os import getenv

from utils.bot import Hyro
from utils.modals import Feedback

class Dev(Cog):
    def __init__(self, hyro: Hyro):
        self.hyro = hyro

    @app_commands.command(description = "Envía un comentario al creador del bot.")
    async def feedback(self, interaction: Interaction):
        if getenv("DEBUG_CHANNEL_ID") is None:
            await interaction.response.send_message(
                "Actualmente no se tiene un canal de comentarios configurado para este bot. No se pueden enviar comentarios.",
                delete_after = 10,
            )
            return

        await interaction.response.send_modal(Feedback())

async def setup(Hyro: Hyro):
    await Hyro.add_cog(Dev(Hyro))
