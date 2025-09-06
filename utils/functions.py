from pathlib import Path
from re import match

from discord import Interaction

from os import getenv

def get_cogs_name(cogs_folder:str = "cogs") -> list[str]:
    """Get a list of all cog names in the specified folder in the root directory."""

    base = Path.cwd() / cogs_folder
    if not base.is_dir():
        raise FileNotFoundError("Cogs directory not found")

    cogs_name = []
    for file in base.rglob("*.py"):
        if match(r"__.*__", file.stem):
            continue

        rel_path = file.relative_to(base.parent).with_suffix("")
        cogs_name.append(".".join(rel_path.parts))

    return cogs_name

def is_owner_action(interaction: Interaction) -> bool:
    """Check if the interaction user is the bot owner."""

    return interaction.user.id == int(getenv("OWNER_ID"))