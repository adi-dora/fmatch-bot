import json
import random
import traceback
import discord
from discord.ext import commands
import uuid
from dateutil import parser

from typing_extensions import Annotated


from discord import Permissions, app_commands
from datetime import datetime as dt

from discord.app_commands import Choice
from discord.app_commands import AppCommandError


class RoleMenuSelect(discord.ui.Select):
    def __init__(self, role_menu: dict):
        self.menu = role_menu
        super().__init__(
            custom_id="role_select",
            max_values=self.menu["max_roles_selectable"],
            placeholder=self.menu["placeholder"],
            options=[
                discord.SelectOption(
                    label=role["label"], value=role["role"], emoji=role["emoji"]
                )
                for role in self.menu["roles"]
            ],
        )

    async def callback(self, interaction: discord.Interaction):
        menu_roles = [
            interaction.guild.get_role(val["role"]) for val in self.menu["roles"]
        ]
        roles_selected = [interaction.guild.get_role(val) for val in self.values]

        await interaction.user.remove_roles(*menu_roles)
        await interaction.user.add_roles(*roles_selected)

        await interaction.response.send_message(
            "You have been given the selected roles successfully!", ephemeral=True
        )


class RoleMenuView(discord.ui.View):
    def __init__(self, menu: dict):
        super().__init__(timeout=None)
        self.menu = menu
        self.add_item(RoleMenuSelect(self.menu))


class RoleMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        with open("rolemenu.json", "r") as f:
            menu = json.load(f)

        for role_menu in menu["menus"]:
            self.bot.add_view(
                RoleMenuView(role_menu), message_id=role_menu["message_id"]
            )

    menu = app_commands.Group(
        name="rolemenu", description="Create and manage role menus"
    )

    @menu.command()
    async def create(self, interaction: discord.Interaction, menu_id: int | None):
        with open("rolemenu.json", "r") as f:
            menu = json.load(f)
        menus = menu["menus"]
        if menu_id is not None:
            menus = menu["menus"][menu_id]

        for menu in menus:
            chan = interaction.guild.get_channel(menu["channel"])
            msg = menu["message"]
            file = (
                menu["file_path"]
                if menu["file_path"] is not None
                else discord.utils.MISSING
            )
            await chan.send(msg, file=file, view=RoleMenuView(menu))


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleMenu(bot))
