from discord import (
    ButtonStyle,
    SelectOption,
    Interaction,
)
from discord.ui import (
    Button,
    Select,
    View,
)
from discord.ext.commands import Cog

from utils.bot import Hyro

class GeneralHelpView(View):
    def __init__(self, hyro: Hyro):
        super().__init__(timeout = 60)

        self.add_item(self.CogSelect(hyro))
        self.add_item(CloseBtn())
        
    class CogSelect(Select):
        def __init__(self, hyro: Hyro):
            self.hyro = hyro

            super().__init__(
                placeholder = "Elige una categoría de comandos",
                min_values = 1,
                max_values = 1,
                options = [
                    SelectOption(
                        label = cog.name,
                        value = cog.__class__.__name__,
                        description = cog.description or None,
                        emoji = cog.icon or None
                    ) for cog in hyro.cogs.values()
                    if getattr(cog, "show", False) and hasattr(cog, "name")
                ]
            )

        async def callback(self, interaction: Interaction):
            command_cog = self.hyro.get_cog("Commands")
            await interaction.response.edit_message(
                view = CommandHelpView(self.hyro, command_cog),
                embed = command_cog._cog_help_embed(
                    self.hyro.get_cog(self.values[0])
                ),
            )

class CommandHelpView(View):
    def __init__(self, hyro: Hyro, command_cog: Cog):
        super().__init__(timeout = 60)

        self.command_cog = command_cog

        self.add_item(self.BackBtn(hyro, command_cog))
        self.add_item(CloseBtn())

    async def on_timeout(self):
        self.stop()
        for item in self.children:
            item.disabled = True

    class BackBtn(Button):
        def __init__(self, hyro: Hyro, command_cog: Cog):
            super().__init__(
                label = "Volver",
                style = ButtonStyle.gray
            )
            self.hyro = hyro
            self.command_cog = command_cog

        async def callback(self, interaction: Interaction):
            await interaction.response.edit_message(
                embed = self.command_cog._general_help_embed(),
                view = GeneralHelpView(self.hyro)
            )

class CloseBtn(Button):
    def __init__(self):
        super().__init__(
            label = "Cerrar",
            style = ButtonStyle.red
        )

    async def callback(self, interaction: Interaction):
        self.view.stop()
        await interaction.message.delete()
