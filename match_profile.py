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


class ProfileModal(discord.ui.Modal, title="Create Profile"):
    def __init__(self, user: discord.User):
        super().__init__(timeout=600)

        with open("profile.json", "r") as f:
            profile = json.load(f)

        self.name = discord.TextInput(
            label="What is your name?",
            style=discord.TextStyle.long,
            value=profile["profiles"][user.id]["name"]
            if user.id in profile["profiles"]
            else None,
        )
        self.location = discord.TextInput(
            label="Where are you from?",
            style=discord.TextStyle.long,
            value=profile["profiles"][user.id]["location"]
            if user.id in profile["profiles"]
            else None,
        )
        self.status = discord.TextInput(
            label="Briefly describe your dating status!",
            style=discord.TextStyle.long,
            value=profile["profiles"][user.id]["status"]
            if user.id in profile["profiles"]
            else None,
        )
        self.height = discord.TextInput(
            label="How tall are you?",
            style=discord.TextStyle.short,
            value=profile["profiles"][user.id]["height"]
            if user.id in profile["profiles"]
            else None,
        )
        self.seeking = discord.TextInput(
            label="What are you looking for? Type None if you don't want to share!",
            value=profile["profiles"][user.id]["seeking"]
            if user.id in profile["profiles"]
            else None,
            style=discord.TextStyle.long,
        )
        self.hobbies = discord.TextInput(
            label="What are your hobbies?",
            style=discord.TextStyle.long,
            value=profile["profiles"][user.id]["hobbies"]
            if user.id in profile["profiles"]
            else None,
        )
        self.bio = discord.TextInput(
            label="Please write a bio, under 200 characters",
            value=profile["profiles"][user.id]["bio"]
            if user.id in profile["profiles"]
            else None,
            style=discord.TextStyle.long,
        )

    async def on_submit(self, interaction: Interaction):
        with open("profile.json", "r") as f:
            profile = json.load(f)

        profile["profiles"][interaction.user.id] = {
            "name": self.name,
            "location": self.location,
            "status": self.status,
            "height": self.height,
            "seeking": self.seeking,
            "hobbies": self.hobbies,
            "bio": self.bio,
        }

        with open("profile.json", "r") as f:
            json.dump(profile, f)

        await interaction.response.send_message(
            "Your profile has been created successfully!", ephemeral=True
        )

        is_male = True  # TODO: Check gender role of user and send profile to corresponding profile channel

        profile_embed = discord.Embed(
            title=interaction.user.global_name,
            description=f"User: {interaction.user.mention}",
            color=discord.Color.pink(),
            timestamp=interaction.created_at,
        ).set_thumbnail(url = interaction.user.display_avatar.url)

        #TODO: Finish creating profile embed and send to channel


    async def on_timeout(self):
        return await super().on_timeout()


class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # TODO: Create modal for user to choose their profile

    profile = app_commands.Group(
        name="profile", description="Create and manage the profile functionality"
    )

    channel = app_commands.Group(
        name="channel",
        description="Manage the channels for the male and female profiles",
        parent=profile,
    )
        



    @channel.command()
    @commands.has_permissions(manage_channels=True)
    async def male(
        self, interaction: discord.Interaction, channel: discord.TextChannel | None
    ):
        with open("profile.json", "r") as f:
            profile = json.load(f)

        if channel is None:
            if profile["male"] is None:
                return await interaction.response.send_message(
                    "No channel has been set for the male profiles"
                )

            return await interaction.response.send_message(
                "The current male profile channel has been set to: "
                + interaction.guild.get_channel(profile["male"])
            )

        profile["male"] = channel.id

        return await interaction.response.send_message(
            "The male profile channel has been set to: " + channel.mention
        )

    @channel.command()
    @commands.has_permissions(manage_channels=True)
    async def female(
        self, interaction: discord.Interaction, channel: discord.TextChannel | None
    ):
        with open("profile.json", "r") as f:
            profile = json.load(f)

        if channel is None:
            if profile["female"] is None:
                return await interaction.response.send_message(
                    "No channel has been set for the female profiles"
                )

            return await interaction.response.send_message(
                "The current female profile channel has been set to: "
                + interaction.guild.get_channel(profile["female"])
            )

        profile["female"] = channel.id

        return await interaction.response.send_message(
            "The female profile channel has been set to: " + channel.mention
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot))
