import discord

from discord import (
    app_commands,
    Color,
    Embed,
    Interaction,
    Member,
)
from discord.ext.commands import Cog
from discord.utils import format_dt
from typing import Optional
from os import getenv
from random import choice

from utils.bot import Hyro
from utils.views import GeneralHelpView, CommandHelpView

class Commands(Cog):
    def __init__(self, hyro: Hyro):
        self.hyro = hyro

        self.show = True
        self.name = "Comandos generales"
        self.description = "Comandos generales del bot"
        self.icon = "🌐"

    def __set_embed_footer(self, embed: Embed):
        owner = self.hyro.get_user(int(getenv("OWNER_ID")))
        if owner:
            embed.add_field(name = "", value = "", inline = False)
            embed.set_footer(
                text = f"@{owner.name}{" - " + self.hyro.version or ''}",
                icon_url = owner.display_avatar.url
            )

    def _general_help_embed(self) -> Embed:
        cog = choice(list([
            cog for cog in self.hyro.cogs.values()
            if getattr(cog, "show", False) and hasattr(cog, "name")
        ]))
        cmd = choice(list(cog.get_app_commands()))

        try:
            from utils.vars import CMDS_ID
        except ImportError:
            CMDS_ID = dict()

        embed = Embed(
            color = Color.blurple(),
            title = f"Ayuda de {self.hyro.user.name}",
            description = "Ayuda general del bot, así como las categorías y comandos disponibles."
        )
        embed.add_field(
            name = "Comandos",
            value = f"Usa el menú desplegable o escribe </help:{CMDS_ID.get("commands", dict()).get("help", 0)}> `{cog.name} {cmd.name}` para más información",
            inline = False
        )
        embed.add_field(
            name = "Sugerencias o bugs",
            value = f"Envía tus comentarios con </feedback:{CMDS_ID.get("dev", dict()).get("feedback", 0)}>",
            inline = False
        )
        embed.add_field(
            name = "Lista de cambios",
            value = "Actualizaciones en [GitHub](https://github.com/Hyromy/HyroBot/releases)",
            inline = False
        )
        self.__set_embed_footer(embed)
            
        return embed
    
    def _cog_help_embed(self, cog: Cog) -> Embed:
        embed = Embed(
            color = Color.blurple(),
            title = f"Ayuda de {((cog.icon + " ") if cog.icon else "") + cog.name}",
            description = cog.description or "No hay descripción disponible."
        )
        embed.add_field(
            name = "Parámetros",
            value = f"`()` Opcional `<>` Obligatorio",
            inline = False
        )

        try:
            from utils.vars import CMDS_ID
        except ImportError:
            CMDS_ID = dict()

        embed.add_field(name = "", value = "", inline = False)
        for cmd in sorted(cog.get_app_commands(), key = lambda c: c.name):
            args = []
            for name, param in cmd.callback.__annotations__.items():
                if name == "interaction":
                    continue

                is_optional = "Optional" in str(param)
                arg_str = "`" + (f"({name})" if is_optional else f"<{name}>") + "`"
                args.append(arg_str)

            embed.add_field(
                name = f"</{cmd.name}:{CMDS_ID.get(cog.__class__.__name__.lower(), dict()).get(cmd.name, 0)}> {' '.join(args) if args else ''}",
                value = cmd.description or "No hay descripción disponible.",
                inline = False
            )
        self.__set_embed_footer(embed)

        return embed

    @app_commands.command(description = "Muestra el mensaje de ayuda del bot.")
    @app_commands.describe(category = "La categoría de la que quieres ver los comandos")
    @app_commands.rename(category = "categoría")
    async def help(self, interaction: Interaction,
        category: Optional[str] = None
    ):
        await interaction.response.defer()

        if not category:
            return await interaction.followup.send(
                embed = self._general_help_embed(),
                view = GeneralHelpView(self.hyro)
            )

        await interaction.followup.send(
            embed = self._cog_help_embed(
                self.hyro.get_cog(category)
            ),
            view = CommandHelpView(self.hyro, self.hyro.get_cog("Commands"))
        )

    @help.autocomplete(name = "category")
    async def help_autocomplete(self, interaction: Interaction, current: str):
        return [
            app_commands.Choice(
                name = f"{cog.icon} {cog.name}",
                value = cog.__class__.__name__
            ) for cog in self.hyro.cogs.values()
            if (
                getattr(cog, "show", False) and hasattr(cog, "name")
                and current.lower().strip() in cog.name.lower()
            )
        ][:25]

    @app_commands.command(description = "Envía un pong para comprobar la latencia.")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f"Pong! {round(self.hyro.latency * 1000)}ms")

    @app_commands.command(description = "Muestra información sobre un emoji personalizado")
    async def emoji(self, interaction: Interaction, emoji: str):
        custom_emoji = None
        for e in interaction.guild.emojis:
            if str(e) == emoji:
                custom_emoji = e
                break

        if custom_emoji is None:
            await interaction.response.send_message("No es un emoji personalizado válido.", ephemeral = True)
            return

        embed = discord.Embed(
            title = f"Información del emoji {custom_emoji.name}",
            color = discord.Color.blurple()
        )
        embed.set_thumbnail(url = str(custom_emoji.url))
        embed.add_field(name = "ID", value = custom_emoji.id, inline = True)
        embed.add_field(name = "Animado", value = "Sí" if custom_emoji.animated else "No", inline = True)
        embed.add_field(name = "Creado el", value = format_dt(custom_emoji.created_at), inline = True)

        await interaction.response.send_message(embed = embed)

    @app_commands.command(description = "Muestra información sobre el servidor")
    async def server_info(self, interaction: Interaction):
        guild = interaction.guild
        assert guild is not None

        embed = discord.Embed(
            title = f"Información de {guild.name}",
            color = discord.Color.blurple(),
            description = guild.description
        )
        if guild.banner: embed.set_image(url = str(guild.banner.url))
        
        embed.set_thumbnail(url = str(guild.icon.url) if guild.icon else "")
        embed.add_field(name = "✨ ID", value = guild.id, inline = True)
        embed.add_field(name = "👑 Dueño", value = f"<@{guild.owner_id}>", inline = True)
        embed.add_field(name = "👥 Miembros", value = guild.member_count, inline = True)
        embed.add_field(name = "📚 Categorías", value = len(guild.categories), inline = True)
        embed.add_field(name = "💬 Canales de texto", value = len(guild.text_channels), inline = True)
        embed.add_field(name = "🔊 Canales de voz", value = len(guild.voice_channels), inline = True)
        embed.add_field(name = "🎭 Roles", value = len(guild.roles), inline = True)
        embed.add_field(name = "😃 Emojis", value = len(guild.emojis), inline = True)
        embed.add_field(name = "👹 Stickers", value = len(guild.stickers), inline = True)
        if guild.system_channel:
            embed.add_field(name = "⚙ Canal del sistema", value = guild.system_channel.mention, inline = True)

        embed.set_footer(text = f"Fundado el {guild.created_at.strftime('%Y/%m/%d')}, {(interaction.created_at - guild.created_at).days} días atrás")

        await interaction.response.send_message(embed = embed)

    @app_commands.command(description = "Muestra información sobre un miembro del servidor")
    @app_commands.rename(member = "miembro")
    @app_commands.describe(member = "El miembro del que quieres ver la información")
    async def user_info(self, interaction: Interaction, 
        member: Optional[Member] = None
    ):
        member = member or interaction.user
        assert isinstance(member, Member)

        embed = discord.Embed(
            title = f"Información de {member}",
            color = member.color if str(member.color) != "#000000" else discord.Color.blurple()
        )
        embed.set_thumbnail(url = str(member.display_avatar.url))
        embed.add_field(name = "✨ ID", value = member.id, inline = True)
        embed.add_field(name = "📆 Unido el", value = f"{format_dt(member.joined_at)} {(interaction.created_at - member.joined_at).days} días atrás", inline = True)
        embed.add_field(name = "🎭 Roles", value = sum(1 for _ in member.roles if not _.is_default()), inline = False)

        embed.set_footer(text = f"Cuenta creada el {member.created_at.strftime('%Y/%m/%d')}, {(interaction.created_at - member.created_at).days} días atrás")

        await interaction.response.send_message(embed = embed)

async def setup(Hyro: Hyro):
    await Hyro.add_cog(Commands(Hyro))
