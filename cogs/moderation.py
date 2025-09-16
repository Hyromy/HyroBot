import discord

from asyncio import sleep
from discord import app_commands, Interaction, Member
from discord.ext.commands import Cog
from typing import Optional

from utils.bot import Hyro

class Moderation(Cog):
    def __init__(self, Hyro: Hyro):
        self.hyro = Hyro

        self.show = True
        self.name = "Moderación"
        self.description = "Comandos de moderación"
        self.icon = "🛡️"

    async def __interaction_response_check(self, interaction: Interaction, msg: str):
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral = True)
        
        else:
            await interaction.response.send_message(msg, ephemeral = True)

    async def _generic_missing_permissions_err(self, interaction: Interaction, missing_permissions: list[str]):
        await interaction.response.send_message(
            f"⛔ Necesitas permisos de {', '.join(f'`{i}`' for i in missing_permissions)} para usar este comando.",
            ephemeral = True
        )

    async def _generic_command_invoke_err(self, interaction: Interaction, msg: str):
        await self.__interaction_response_check(interaction, msg)

    async def _generic_unexpected_err(self, interaction: Interaction, err: Exception):
        print(f"Unexpected error in {interaction.command.name} command -> <{err.__class__.__name__}>: {err}")
        msg = f"❌ | Ocurrió un error inesperado"
        await self.__interaction_response_check(interaction, msg)

    @app_commands.command(description = "Elimina mensajes en el canal actual.")
    @app_commands.checks.has_permissions(manage_messages = True)
    @app_commands.describe(amount = "Número de mensajes a eliminar (1-100)")
    @app_commands.rename(amount = "cantidad")
    async def purge(self, interaction: Interaction,
        amount: Optional[app_commands.Range[int, 1, 100]] = 50
    ):
        await interaction.response.defer(ephemeral = True)
        deleted = await interaction.channel.purge(limit = amount)
        msg = await interaction.followup.send(f"🧹 | Eliminados {len(deleted)} mensajes.")

        await sleep(3)
        await msg.delete()

    @purge.error
    async def purge_error(self, interaction: Interaction, err: Exception):
        if isinstance(err, app_commands.MissingPermissions):
            await self._generic_missing_permissions_err(interaction, err.missing_permissions)

        else:
            await self._generic_unexpected_err(interaction, err)

    @app_commands.command(description = "Expulsa a un miembro del servidor.")
    @app_commands.checks.has_permissions(kick_members = True)
    @app_commands.describe(member = "Miembro a expulsar")
    @app_commands.rename(member = "miembro")
    async def kick(self, interaction: Interaction,
        member: Member
    ):
        await interaction.response.defer(ephemeral = True)

        if member == interaction.user:
            return await interaction.followup.send("❌ | No puedes expulsarte a ti mismo.", ephemeral = True)

        await member.kick()
        await interaction.followup.send(f"👢 | {member.mention} ha sido expulsado del servidor.")

    @kick.error
    async def kick_error(self, interaction: Interaction, err: Exception):
        if isinstance(err, app_commands.MissingPermissions):
            await self._generic_missing_permissions_err(interaction, err.missing_permissions)

        elif isinstance(err, app_commands.CommandInvokeError):
            await self._generic_command_invoke_err(interaction,
                "❌ | No puedo expulsar a ese usuario porque su rol es igual o superior al del bot."
            )

        else:
            await self._generic_unexpected_err(interaction, err)

    @app_commands.command(description = "Banea a un miembro del servidor.")
    @app_commands.checks.has_permissions(ban_members = True)
    @app_commands.describe(member = "Miembro a banear")
    @app_commands.rename(member = "miembro")
    async def ban(self, interaction: Interaction,
        member: Member
    ):
        await interaction.response.defer(ephemeral = True)

        if member == interaction.user:
            return await interaction.followup.send("❌ | No puedes banearte a ti mismo.", ephemeral = True)

        await member.ban()
        await interaction.followup.send(f"🔨 | {member.mention} ha sido baneado del servidor.")

    @ban.error
    async def ban_error(self, interaction: Interaction, err: Exception):
        if isinstance(err, app_commands.MissingPermissions):
            await self._generic_missing_permissions_err(interaction, err.missing_permissions)

        elif isinstance(err, app_commands.CommandInvokeError):
            await self._generic_command_invoke_err(interaction,
                "❌ | No puedo banear a ese usuario porque su rol es igual o superior al del bot."
            )

        else:
            await self._generic_unexpected_err(interaction, err)

async def setup(hyro: Hyro):
    await hyro.add_cog(Moderation(hyro))
