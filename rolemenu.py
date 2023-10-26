import json
import random
import traceback
from typing import Optional
from unicodedata import name
import discord
import datetime
from discord.ext import commands, tasks
from discord.interactions import Interaction
import uuid
from dateutil import parser
import typing

from typing_extensions import Annotated


from discord import Permissions, app_commands
from datetime import datetime as dt

from discord.app_commands import Choice
from discord.app_commands import AppCommandError


class RoleView(discord.ui.View):
    def __init__(self, max_values: int):
        super().__init__(timeout=None)
        self.max_values = max_values

    
    

class RoleMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
    

    menu = app_commands.Group(name='menu', description='Create and manage role menus')

    @menu.command(description='Create a new role menu')
    @commands.has_permissions(manage_roles=True)
    async def create(self, interaction: Interaction, name: str, message: str, channel: discord.TextChannel):
        with open('rolemenu.json', 'r') as f:
            menu = json.load(f)
        
        menu['menus'].append({"name": name, "message": message, "channel": channel.id})

        with open("rolemenu.json", "w") as f:
            json.dump(menu, f)

        await interaction.response.send_message(f'The ``{name.title()}`` menu has been created! Use the command ``menu add`` to add roles to the menu.')
    
    with open('rolemenu.json', 'r') as f:
        menu = json.load(f)
    @menu.command()
    @app_commands.choices([Choice(name = m['name'], value= str(m['name']).lower()) for m in menu['menus']])
    async def add(self, interaction: discord.Interaction, name: str, role: discord.Role):
        with open("rolemenu.json", "r") as f:
            menu = json.load(f)
        
        

async def setup(bot: commands.Bot):
    await bot.add_cog(RoleMenu(bot))