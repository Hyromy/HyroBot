from datetime import datetime

from discord import (
    Color,
    Embed,
    Interaction,
    TextStyle,
)
from discord.ui import (
    Modal,
    TextInput,
)
from os import getenv

class Feedback(Modal):
    title = "Envía tus comentarios"
    feedback_title = TextInput(
        label = "Título",
        placeholder = "Introduce el título de tu comentario",
    )
    content = TextInput(
        label = "Contenido",
        style = TextStyle.long,
        placeholder = "Introduce el contenido de tu comentario aquí...",
        required = False,
        max_length = 512
    )

    async def __send(self, interaction: Interaction, feedback: dict):
        embed = Embed(
            title = feedback["title"],
            description = feedback["content"],
            color = Color.blurple()
        )
        embed.set_author(
            name = f"Enviado por {interaction.user.name} ({interaction.user.id})",
            icon_url = str(interaction.user.display_avatar.url)
        )
        embed.set_footer(text = datetime.now("America/Mexico_City").strftime("%Y/%m/%d - %H:%M:%S"))

        channel = interaction.client.get_channel(int(getenv("DEBUG_CHANNEL_ID")))
        await channel.send(embed = embed)

    async def on_submit(self, interaction: Interaction):
        await self.__send(interaction, {
            "title": self.feedback_title.value,
            "content": self.content.value
        })

        await interaction.response.send_message(
            "Gracias por tu comentario!",
            ephemeral = True
        )

    async def on_error(self, interaction: Interaction, e: Exception):
        print(f"<{e.__class__.__name__}>: {e}")
        
        await interaction.response.send_message(
            "Ocurrió un error al enviar tu comentario.",
            ephemeral = True
        )
