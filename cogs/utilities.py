import json
import traceback

import discord
from discord import app_commands
from discord.ext import commands
from discord.interactions import Interaction
from discord.app_commands import Choice
from utils.verification_utils import verification_json, dump_verification_json

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @app_commands.command(description='Get information about a user!')
    @app_commands.describe(user="Provide a user or see your own stats")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member | None):
        print("user")

async def setup(bot):
    await bot.add_cog(Utilities(bot))