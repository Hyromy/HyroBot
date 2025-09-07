import discord

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
    