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
from utils.profile_utils import *


class ProfileView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label='Create Profile', style=discord.ButtonStyle.green, id="create_profile_btn")
    async def create_profile_btn(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(ProfileModal(interaction.user))
    
    @discord.ui.button(label='Bump Profile', id="bump_profile_btn")
    async def bump_profile_btn(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id not in profile_json['profiles']:
            return await interaction.response.send_message("You do not have a profile!", ephemeral=True)
        #TODO: Check gender and send profile to specified channel; also check cooldown
    
    @discord.ui.button(label='Edit Profile', id="edit_profile_btn")
    async def edit_profile_btn(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.send_modal(ProfileModal(interaction.user))
    
    @discord.ui.button(label="Preview Profile", id="preview_profile_btn")
    async def preview_profile_btn(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id not in profile_json['profiles']:
            return await interaction.response.send_message("You do not have a profile!", ephemeral=True)
        #TODO: Send embed of profile to channel
    
    @discord.ui.button(label = 'Upload Selfie', id='selfie_btn')
    async def upload_selfie_btn(self, interaction: discord.Interaction, button: discord.Button):
        if interaction.user.id not in profile_json['profiles']:
            return await interaction.response.send_message("You do not have a profile!", ephemeral=True)
        #TODO: Somehow handle the file upload
        
    

class ProfileModal(discord.ui.Modal, title="Create Profile"):
    def __init__(self, user: discord.Member | discord.User):
        super().__init__(timeout=600)

        self.fields = [
            discord.TextInput(
                label="What is your name?",
                style=discord.TextStyle.short,
                required=True,
                value=profile_json["profiles"][user.id]["name"]
                if user.id in profile_json["profiles"]
                else None,
            ),
            discord.TextInput(
                label="Where are you from?",
                style=discord.TextStyle.short,
                required=True,
                value=profile_json["profiles"][user.id]["location"]
                if user.id in profile_json["profiles"]
                else None,
            ),
            discord.TextInput(
                label="Briefly describe your dating status!",
                style=discord.TextStyle.long,
                required=True,
                value=profile_json["profiles"][user.id]["status"]
                if user.id in profile_json["profiles"]
                else None,
            ),
            discord.TextInput(
                label="How tall are you?",
                style=discord.TextStyle.short,
                required=True,
                value=profile_json["profiles"][user.id]["height"]
                if user.id in profile_json["profiles"]
                else None,
            ),
            discord.TextInput(
                label="What are you looking for? Type None if you don't want to share!",
                value=profile_json["profiles"][user.id]["seeking"]
                if user.id in profile_json["profiles"]
                else None,
                style=discord.TextStyle.long,
                required=True,
            ),
            discord.TextInput(
                label="What are your hobbies?",
                style=discord.TextStyle.long,
                required=True,
                value=profile_json["profiles"][user.id]["hobbies"]
                if user.id in profile_json["profiles"]
                else None,
            ),
            discord.TextInput(
                label="Please write a bio, under 200 characters",
                required=True,
                value=profile_json["profiles"][user.id]["bio"]
                if user.id in profile_json["profiles"]
                else None,
                style=discord.TextStyle.long,
                max_length=200,
            ),
        ]
        for item in self.fields:
            self.add_item(item)

    async def on_submit(self, interaction: Interaction):
        profile_json["profiles"][interaction.user.id] = {
            "name": self.fields[0],
            "location": self.fields[1],
            "status": self.fields[2],
            "height": self.fields[3],
            "seeking": self.fields[4],
            "hobbies": self.fields[5],
            "bio": self.fields[6],
        }

        dump_profile_json(profile_json)

        await interaction.response.send_message(
            "Your profile has been updated successfully!", ephemeral=True
        )

        is_male = True  # TODO: Check gender role of user and send profile to corresponding profile channel

        # profile_embed = create_profile_embed(interaction.user)
        # profile_embed.timestamp = interaction.created_at

        # TODO: Finish creating profile embed and send to channel


class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    match = app_commands.Group(name='match', description='Handle and manage the match functionality')

    @match.command()
    @commands.has_permissions(administrator=True)
    async def create(self, interaction: discord.Interaction):
         chan = interaction.guild.get_channel(profile_json['send_profile_channel'])
         await chan.send("Create your profile here!", view=ProfileView())


async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot))
