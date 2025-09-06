from discord import app_commands, Interaction, Member
from discord.ext.commands import Cog
from discord.utils import format_dt
from typing import Optional

from utils.bot import Hyro

class Commands(Cog):
    def __init__(self, hyro: Hyro):
        self.hyro = hyro

    @app_commands.command(description = "Envía un pong para comprobar la latencia.")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f"Pong! {round(self.hyro.latency * 1000)}ms")

    @app_commands.command(description = "Calcula la suma de dos números")
    @app_commands.rename(
        x = "número_1",
        y = "número_2"
    )
    @app_commands.describe(
        x = "Primer número a sumar",
        y = "Segundo número a sumar"
    )
    async def sum(self, interaction: Interaction,
        x: int,
        y: int
    ):
        await interaction.response.send_message(f"{x} + {y} = {x + y}")

    @app_commands.command(description = "Muestra la fecha de registro en Discord de un miembro del servidor")
    @app_commands.rename(member = "miembro")
    async def joined(self, interaction: Interaction,
        member: Optional[Member] = None
    ):
        member = member or interaction.user
        assert isinstance(member, Member)
        if member.joined_at:
            await interaction.response.send_message(f"{member.display_name} se unió a discord el: {format_dt(member.joined_at)}")

        else:
            await interaction.response.send_message("No se puede obtener la información")

async def setup(Hyro: Hyro):
    await Hyro.add_cog(Commands(Hyro))
    