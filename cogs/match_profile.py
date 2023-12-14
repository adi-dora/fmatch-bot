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
import os

from typing_extensions import Annotated


from discord import Permissions, app_commands
from datetime import datetime as dt

from discord.app_commands import Choice
from discord.app_commands import AppCommandError
from utils.profile_utils import *


class ProfileView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="Create Profile", style=discord.ButtonStyle.green, custom_id="create_profile_btn"
    )
    async def create_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        try:
            await interaction.response.send_modal(ProfileModal(interaction.user))
        except:
            traceback.print_exc()

    @discord.ui.button(label="Bump Profile", custom_id="bump_profile_btn")
    async def bump_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        if interaction.user.id not in profile_json["profiles"]:
            return await interaction.response.send_message(
                "You do not have a profile!", ephemeral=True
            )
        # TODO: Check gender and send profile to specified channel; also check cooldown

    @discord.ui.button(label="Edit Profile", custom_id="edit_profile_btn")
    async def edit_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        await interaction.response.send_modal(ProfileModal(interaction.user))

    @discord.ui.button(label="Preview Profile", custom_id="preview_profile_btn")
    async def preview_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        if interaction.user.id not in profile_json["profiles"]:
            return await interaction.response.send_message(
                "You do not have a profile!", ephemeral=True
            )
        # TODO: Send embed of profile to channel

    @discord.ui.button(label="Upload Selfie", custom_id="selfie_btn")
    async def upload_selfie_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        if interaction.user.id not in profile_json["profiles"]:
            return await interaction.response.send_message(
                "You do not have a profile!", ephemeral=True
            )
        await interaction.response.send_message(
            "Check your DMs to upload your selfie!", ephemeral=True
        )
        await interaction.user.send(
            embed=discord.Embed(
                title="Upload Selfie Here",
                description="Please send an image of yourself to save to your profile",
                color=discord.Color.pink(),
                timestamp=interaction.created_at,
            )
        )


        def check(msg: discord.Message):
            return msg.channel == discord.DMChannel and len(msg.attachments) == 1 and msg.author == interaction.user
        
        msg = await self.bot.wait_for('message', timeout=300, check=check)
        print(msg.channel, msg.author.name)



        
        # TODO: Somehow handle the file upload


class ProfileModal(discord.ui.Modal, title="Create Profile"):
    def __init__(self, user: discord.Member | discord.User):
        super().__init__(timeout=600)
        

        self.fields = [
            discord.ui.TextInput(
                label="What is your name?",
                style=discord.TextStyle.short,
                required=True,
                default=profile_json["profiles"][user.id]["name"]
                if user.id in profile_json["profiles"]
                else None,
            ),
            discord.ui.TextInput(
                label="Where are you from?",
                style=discord.TextStyle.short,
                required=True,
                default=profile_json["profiles"][user.id]["location"]
                if user.id in profile_json["profiles"]
                else None,
            ),
            discord.ui.TextInput(
                label="Briefly describe your dating status!",
                style=discord.TextStyle.short,
                required=True,
                default=profile_json["profiles"][user.id]["status"]
                if user.id in profile_json["profiles"]
                else None,
            ),
            discord.ui.TextInput(
                label="How tall are you?",
                style=discord.TextStyle.short,
                required=True,
                default=profile_json["profiles"][user.id]["height"]
                if user.id in profile_json["profiles"]
                else None,
            ),
            discord.ui.TextInput(
                label="What are you looking for?",
                default=profile_json["profiles"][user.id]["seeking"]
                if user.id in profile_json["profiles"]
                else None,
                style=discord.TextStyle.short,
                required=True,
            ),
            # discord.ui.TextInput(
            #     label="What are your hobbies?",
            #     style=discord.TextStyle.short,
            #     required=True,
            #     default=profile_json["profiles"][user.id]["hobbies"]
            #     if user.id in profile_json["profiles"]
            #     else None,
            # ),
            # discord.ui.TextInput(
            #     label="Please write a bio, under 200 characters",
            #     required=True,
            #     default=profile_json["profiles"][user.id]["bio"]
            #     if user.id in profile_json["profiles"]
            #     else None,
            #     style=discord.TextStyle.short,
            #     max_length=200,
            # ),
        ]
        count = 0
        for item in self.fields:
            print(count)
            count += 1
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
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(ProfileView(self.bot), message_id=profile_json['profile_menu_id'])


    match = app_commands.Group(
        name="match", description="Handle and manage the match functionality"
    )

    @match.command()
    @commands.has_permissions(administrator=True)
    async def create(self, interaction: discord.Interaction):
        
        chan = interaction.guild.get_channel(profile_json["send_profile_channel"])
        m = await chan.send("Create your profile here!", view=ProfileView(self.bot))
        profile_json['profile_menu_id'] = m.id
        dump_profile_json(profile_json)


async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot))
