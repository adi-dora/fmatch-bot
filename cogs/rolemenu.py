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


class RoleMenuOptions(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        with open("rolemenu.json", "r") as f:
            menu = json.load(f)

        self.add_item(
            discord.ui.Button(
                label="Start Here", url=menu["first_rolemenu_message_link"]
            )
        )

    @discord.ui.button(
        label="Check Roles",
        custom_id="check_roles_btn",
        style=discord.ButtonStyle.primary,
    )
    async def check_roles_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        with open("rolemenu.json", "r") as f:
            roles = json.load(f)
        embed = discord.Embed(
            description="Here are all the roles you have from each rolemenu!",
            color=discord.Color.pink(),
            timestamp=interaction.created_at,
        ).set_thumbnail(url=interaction.user.avatar.url)
        for menu in roles["menus"]:
            embed.add_field(
                name=menu["name"],
                value="\n".join(
                    interaction.guild.get_role(x["role"]).mention
                    for x in menu["roles"]
                    if interaction.guild.get_role(x["role"]) in interaction.user.roles
                ),
                inline=False,
            )

        await interaction.response.send_message(
            embed=embed, ephemeral=True, delete_after=30
        )


class RoleMenuSelect(discord.ui.Select):
    def __init__(self, role_menu: dict):
        self.menu = role_menu
        super().__init__(
            custom_id="role_select",
            min_values=0,
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
        try:
            menu_roles = [
                interaction.guild.get_role(val["role"]) for val in self.menu["roles"]
            ]
            roles_selected = [
                interaction.guild.get_role(int(val)) for val in self.values
            ]

            await interaction.user.remove_roles(
                *menu_roles, reason="User updated rolemenu roles"
            )
            await interaction.user.add_roles(
                *roles_selected, reason="User updated rolemenu roles"
            )

            await interaction.response.send_message(
                "You have been given the selected roles successfully!",
                ephemeral=True,
                delete_after=30,
            )
            await interaction.message.edit()
        except:
            traceback.print_exc()


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
    @commands.has_permissions(administrator=True)
    async def create(self, interaction: discord.Interaction, menu_id: int | None):
        try:
            with open("rolemenu.json", "r") as f:
                menu = json.load(f)
            menus = menu["menus"]
            if menu_id is not None:
                menus = menu["menus"][menu_id]

            for i in range(len(menus)):
                chan = interaction.guild.get_channel(menus[i]["channel"])
                msg = menus[i]["message"]
                file = (
                    discord.File(menus[i]["file_path"])
                    if menus[i]["file_path"] is not None
                    else discord.utils.MISSING
                )
                m = await chan.send(msg, file=file, view=RoleMenuView(menus[i]))

                menu["menus"][i]["message_id"] = m.id

            await interaction.response.send_message(
                "Your rolemenu(s) have been created successfully!"
            )
            with open("rolemenu.json", "w") as f:
                json.dump(menu, f, indent=1)
        except:
            traceback.print_exc()

    @menu.command()
    @commands.has_permissions(administrator=True)
    async def create_options(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=RoleMenuOptions())


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleMenu(bot))
