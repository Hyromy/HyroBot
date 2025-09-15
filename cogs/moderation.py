import discord

from asyncio import sleep
from datetime import timedelta
from discord import (
    app_commands,
    Interaction,
    Member,
)
from discord.utils import format_dt, utcnow
from discord.ext.commands import Cog
from typing import Optional

from utils.bot import Hyro

class Moderation(Cog):
    def __init__(self, Hyro: Hyro):
        self.hyro = Hyro

    async def exception_handler(self, interaction: Interaction, err: Exception, *,
        invoke_err_msg: str = None
    ):
        """
        Handle exceptions for commands.
        """

        print(f"Error in {interaction.command.name} command -> <{err.__class__.__name__}>: {err}")

        if isinstance(err, app_commands.MissingPermissions):
            return await self._generic_missing_permissions_err(interaction, err.missing_permissions)

        if isinstance(err, app_commands.CommandInvokeError) and invoke_err_msg is not None:
            return await self._generic_command_invoke_err(interaction, invoke_err_msg)

        await self._generic_unexpected_err(interaction, err)

    async def _generic_missing_permissions_err(self, interaction: Interaction, missing_permissions: list[str]):
        """
        Handle missing permissions error for commands.
        """

        await interaction.response.send_message(
            f"⛔ Necesitas permisos de {', '.join(f'`{i}`' for i in missing_permissions)} para usar este comando.",
            ephemeral = True
        )

    async def _generic_command_invoke_err(self, interaction: Interaction, msg: str):
        """
        Handle command invoke error for commands.
        """

        await self.__interaction_response_check(interaction, msg)

    async def _generic_unexpected_err(self, interaction: Interaction, err: Exception):
        """
        Handle unexpected errors for commands.
        """

        print(f"Unexpected error in {interaction.command.name} command -> <{err.__class__.__name__}>: {err}")
        await self.__interaction_response_check(interaction, "❌ | Ocurrió un error inesperado")

    async def __interaction_response_check(self, interaction: Interaction, msg: str):
        """
        Check if the interaction response is done, if it is, use followup to send the message.
        """

        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral = True)
        
        else:
            await interaction.response.send_message(msg, ephemeral = True)

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
        await self.exception_handler(interaction, err)

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
        await self.exception_handler(interaction, err,
            invoke_err_msg = "❌ | No puedo expulsar a ese usuario porque su rol es igual o superior al del bot."
        )

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
        await self.exception_handler(interaction, err,
            invoke_err_msg = "❌ | No puedo banear a ese usuario porque su rol es igual o superior al del bot."
        )

    @app_commands.command(description = "Desbanea a un miembro del servidor.")
    @app_commands.checks.has_permissions(ban_members = True)
    @app_commands.describe(member = "Miembro a desbanear")
    @app_commands.rename(member = "miembro")
    async def unban(self, interaction: Interaction,
        member: str
    ):
        await interaction.response.defer(ephemeral = True)
        ban = next(
            (ban for ban in [
                ban async for ban in interaction.guild.bans()
            ] if str(ban.user.id) == member),
            None
        )
        if not ban:
            return await interaction.followup.send("❌ | No hay usuarios baneados.", ephemeral = True)
        
        await interaction.guild.unban(ban.user)
        await interaction.followup.send(f"✅ | {ban.user.mention} ha sido desbaneado del servidor.", ephemeral = True)

    @unban.autocomplete('member')
    async def unban_autocomplete_user(self, interaction: Interaction, current: str):
        return [
            app_commands.Choice(name = f"{ban.user.display_name} | {ban.user.name}", value = str(ban.user.id)) for ban in [
                ban async for ban in interaction.guild.bans()
                if any(current.lower() in src.lower() for src in (ban.user.name, ban.user.display_name))
            ][:25]
        ]

    @unban.error
    async def unban_error(self, interaction: Interaction, err: Exception):
        await self.exception_handler(interaction, err,
            invoke_err_msg = "❌ | No puedo desbanear a ese usuario porque su rol es igual o superior al del bot."
        )

    @app_commands.command(description = "Coloca un timeout a un miembro del servidor.")
    @app_commands.checks.has_permissions(moderate_members = True)
    @app_commands.describe(
        member = "Miembro a colocar timeout",
        duration = "Duración del timeout",
    )
    @app_commands.rename(
        member = "miembro",
        duration = "duración",
    )
    async def timeout(self, interaction: Interaction,
        member: Member,
        duration: int,
    ):
        await interaction.response.defer(ephemeral = True)

        if member == interaction.user:
            return await interaction.followup.send("❌ | No puedes colocarte un timeout a ti mismo.", ephemeral = True)

        until = utcnow() + timedelta(seconds = duration)
        await member.timeout(until)
        await interaction.followup.send(
            f"⏱️ | {member.mention} ha sido puesto en timeout hasta {format_dt(until, "T")}",
            ephemeral = False
        )

    @timeout.autocomplete('duration')
    async def timeout_autocomplete_duration(self, interaction: Interaction, current: str):
        return [
            opt for opt in [
                app_commands.Choice(name = "1 minuto", value = 60),
                app_commands.Choice(name = "5 minutos", value = 300),
                app_commands.Choice(name = "10 minutos", value = 600),
                app_commands.Choice(name = "30 minutos", value = 1800),
                app_commands.Choice(name = "1 hora", value = 3600),
                app_commands.Choice(name = "6 horas", value = 21600),
                app_commands.Choice(name = "12 horas", value = 43200),
                app_commands.Choice(name = "1 día", value = 86400),
            ] if current.lower() in opt.name.lower()
        ]

    @timeout.error
    async def timeout_error(self, interaction: Interaction, err: Exception):
        await self.exception_handler(interaction, err,
            invoke_err_msg = "❌ | No puedo colocar un timeout a ese usuario porque su rol es igual o superior al del bot."
        )

    @app_commands.command(description = "Remueve el timeout a un miembro del servidor.")
    @app_commands.checks.has_permissions(moderate_members = True)
    @app_commands.describe(member = "Miembro al que se le removerá el timeout")
    @app_commands.rename(member = "miembro")
    async def unset_timeout(self, interaction: Interaction,
        member: str
    ):
        await interaction.response.defer(ephemeral = True)

        try:
            m = interaction.guild.get_member(int(member))
        except ValueError:
            return await interaction.followup.send("❌ | No hay miembros con un timeout activo.", ephemeral = True)

        await m.timeout(None)
        await interaction.followup.send(f"✅ | Timeout removido para {m.mention}.", ephemeral = True)

    @unset_timeout.autocomplete('member')
    async def unset_timeout_autocomplete_member(self, interaction: Interaction, current: str):
        return [
            app_commands.Choice(name = f"{m.display_name} | {m.name}", value = str(m.id)) for m in [
                m for m in interaction.guild.members
                if (
                    m.timed_out_until is not None and m.timed_out_until > utcnow()
                    and any(current.lower() in src.lower() for src in (m.display_name, m.name))
                )
            ][:25]
        ]

    @unset_timeout.error
    async def unset_timeout_error(self, interaction: Interaction, err: Exception):
        await self.exception_handler(interaction, err,
            invoke_err_msg = "❌ | No puedo remover el timeout a ese usuario porque su rol es igual o superior al del bot."
        )

async def setup(hyro: Hyro):
    await hyro.add_cog(Moderation(hyro))
