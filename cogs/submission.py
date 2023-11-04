import json
import traceback
import datetime
import asyncio
import typing

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.interactions import Interaction
from discord.app_commands import Choice
from discord.app_commands import AppCommandError
from utils.submission_utils import *


class SuggestionModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='New Suggestion', timeout=300, custom_id='suggestion_modal')

class SuggestionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='New Suggestion', custom_id='suggest_button')
    async def suggest_button(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(SuggestionModal())
        

class Submission(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def suggestion(self, interaction: discord.Interaction):
        suggest_chan = interaction.guild.get_channel(submission_json['suggestion_channel'])
        await suggest_chan.send(submission_json['suggestion_message'])


    

