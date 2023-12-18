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
import asyncio
import typing
import os

from typing_extensions import Annotated


from discord import Permissions, app_commands
from datetime import datetime as dt

from discord.app_commands import Choice
from discord.app_commands import AppCommandError
from utils.profile_utils import *


class EditProfileView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        # TODO: Add the two buttons for general or dating and send

    @discord.ui.button(label="General Profile")
    async def edit_general_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        general_modal = GeneralProfileModal(
            interaction.user, profile_json["profiles"][str(interaction.user.id)]
        )
        await interaction.response.send_modal(general_modal)
        await general_modal.wait()
        profile_json["profiles"][str(interaction.user.id)] = general_modal.profile
        dump_profile_json(profile_json)
        await interaction.followup.send(
            "Your General Profile has been updated successfully!", ephemeral=True
        )

    @discord.ui.button(label="Dating Profile")
    async def edit_dating_profile(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        dating_modal = DatingProfileModal(
            interaction.user, profile_json["profiles"][str(interaction.user.id)]
        )
        await interaction.response.send_modal(dating_modal)
        await dating_modal.wait()
        await interaction.followup.send(
            "Your Dating Profile has been updated successfully!", ephemeral=True
        )


class GeneralProfileModal(discord.ui.Modal, title="General Profile"):
    def __init__(self, user: discord.Member | discord.User, profile: dict | None):
        super().__init__(timeout=600)
        self.profile = profile if profile is not None else {}

        self.fields = [
            discord.ui.TextInput(
                label="What is your name?",
                style=discord.TextStyle.short,
                required=True,
                default=profile_json["profiles"][str(user.id)]["name"]
                if str(user.id) in profile_json["profiles"]
                else None,
            ),
            discord.ui.TextInput(
                label="Where are you from?",
                style=discord.TextStyle.short,
                required=True,
                default=profile_json["profiles"][str(user.id)]["location"]
                if str(user.id) in profile_json["profiles"]
                else None,
            ),
            discord.ui.TextInput(
                label="How tall are you?",
                style=discord.TextStyle.short,
                required=True,
                default=profile_json["profiles"][str(user.id)]["height"]
                if str(user.id) in profile_json["profiles"]
                else None,
            ),
        ]
        for item in self.fields:
            self.add_item(item)

    async def on_submit(self, interaction: Interaction):
        self.profile["name"] = self.fields[0].value
        self.profile["location"] = self.fields[1].value
        self.profile["height"] = self.fields[2].value
        await interaction.response.defer()


class DatingProfileModal(discord.ui.Modal, title="Dating Profile"):
    def __init__(
        self,
        user: discord.Member | discord.User,
        profile: dict,
        parent_interaction: discord.Interaction = None,
    ):
        super().__init__(custom_id="dating_profile_view", timeout=600)
        self.profile = profile
        self.interaction = parent_interaction
        self.fields = [
            discord.ui.TextInput(
                label="What are you looking for?",
                default=profile_json["profiles"][str(user.id)]["seeking"]
                if str(user.id) in profile_json["profiles"]
                else None,
                style=discord.TextStyle.short,
                required=True,
            ),
            discord.ui.TextInput(
                label="Briefly describe your dating status!",
                style=discord.TextStyle.long,
                required=True,
                default=profile_json["profiles"][str(user.id)]["status"]
                if str(user.id) in profile_json["profiles"]
                else None,
            ),
            discord.ui.TextInput(
                label="What are your hobbies?",
                style=discord.TextStyle.long,
                required=True,
                default=profile_json["profiles"][str(user.id)]["hobbies"]
                if str(user.id) in profile_json["profiles"]
                else None,
            ),
            discord.ui.TextInput(
                label="Please write a bio, under 200 characters",
                required=True,
                default=profile_json["profiles"][str(user.id)]["bio"]
                if str(user.id) in profile_json["profiles"]
                else None,
                style=discord.TextStyle.long,
                max_length=200,
            ),
        ]
        for item in self.fields:
            self.add_item(item)

    async def on_submit(self, interaction: discord.Interaction):
        self.profile["seeking"] = self.fields[0].value
        self.profile["status"] = self.fields[1].value
        self.profile["hobbies"] = self.fields[2].value
        self.profile["bio"] = self.fields[3].value
        await interaction.response.defer()

        profile_json["profiles"][str(interaction.user.id)] = self.profile
        dump_profile_json(profile_json)
        if self.interaction:
            await self.interaction.edit_original_response(
                content="Your profile has been set up sucessfully!",
                view=discord.ui.View(),
            )

            profile_embed, gender = create_profile_embed(interaction.user)
            profile_embed.timestamp = interaction.created_at

            gender = gender.replace(" ", "_")
            gender = gender.lower()
            chan = interaction.guild.get_channel(profile_json[gender + "_channel"])
            file = discord.utils.MISSING
            if "selfie" in profile_json["profiles"][str(interaction.user.id)]:
                file = get_selfie(interaction.user)

            await chan.send(interaction.user.mention, embed=profile_embed, file=file)


class DatingProfileView(discord.ui.View):
    def __init__(self, profile: dict, parent_interaction: discord.Interaction):
        super().__init__(timeout=300)
        self.profile = profile
        self.interaction = parent_interaction

    @discord.ui.button(label="Dating Profile", custom_id="dating_profile_btn")
    async def dating_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        dating_modal = DatingProfileModal(
            interaction.user, self.profile, self.interaction
        )
        await interaction.response.send_modal(dating_modal)


class GeneralProfileView(discord.ui.View):
    def __init__(self, parent_interaction: discord.Interaction):
        super().__init__(timeout=300)
        self.interaction = parent_interaction

    @discord.ui.button(label="General Profile", custom_id="general_profile_btn")
    async def general_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        general_modal = GeneralProfileModal(interaction.user)
        await interaction.response.send_modal(general_modal)
        await general_modal.wait()
        await interaction.edit_original_response(
            content="Part 2: The Dating Profile",
            view=DatingProfileView(general_modal.profile, interaction),
        )


class ProfileView(discord.ui.View):
    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(
        label="Create Profile",
        style=discord.ButtonStyle.green,
        custom_id="create_profile_btn",
    )
    async def create_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        if str(interaction.user.id) in profile_json["profiles"]:
            return await interaction.response.send_message(
                "You aleady have a profile!", ephemeral=True
            )
        await interaction.response.send_message(
            "Welcome! To create your profile, there are two parts you must complete. ```Part 1``` **General Questions**",
            ephemeral=True,
            view=GeneralProfileView(interaction),
        )

    @discord.ui.button(label="Bump Profile", custom_id="bump_profile_btn")
    async def bump_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        if str(interaction.user.id) not in profile_json["profiles"]:
            return await interaction.response.send_message(
                "You do not have a profile!", ephemeral=True
            )
        # TODO: Check gender and send profile to specified channel; also check cooldown

    @discord.ui.button(label="Edit Profile", custom_id="edit_profile_btn")
    async def edit_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        if str(interaction.user.id) not in profile_json["profiles"]:
            return await interaction.response.send_message("You do not have a profile!")
        await interaction.response.send_message(
            "Choose a part of your profile to edit",
            ephemeral=True,
            view=EditProfileView(),
        )

    @discord.ui.button(label="Preview Profile", custom_id="preview_profile_btn")
    async def preview_profile_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        if str(interaction.user.id) not in profile_json["profiles"]:
            return await interaction.response.send_message(
                "You do not have a profile!", ephemeral=True
            )
        try:
            await interaction.response.send_message(
                embed=create_profile_embed(interaction.user)[0],
                ephemeral=True,
                file=get_selfie(interaction.user)
                if "selfie" in profile_json["profiles"][str(interaction.user.id)]
                else discord.utils.MISSING,
            )
        except:
            traceback.print_exc()

    @discord.ui.button(label="Upload Selfie", custom_id="selfie_btn")
    async def upload_selfie_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        if str(interaction.user.id) not in profile_json["profiles"]:
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
            return (
                type(msg.channel) == discord.channel.DMChannel
                and len(msg.attachments) == 1
                and msg.author == interaction.user
            )

        try:
            msg = await self.bot.wait_for("message", timeout=300, check=check)
        except asyncio.TimeoutError:
            await interaction.user.send(
                "The request timed out! Please try again by clicking the button in the server!"
            )
        else:
            selfie = msg.attachments[0]
            await selfie.save(f"res/{interaction.user.id}.png")
            profile_json["profiles"][str(interaction.user.id)][
                "selfie"
            ] = f"./res/{interaction.user.id}.png"
            dump_profile_json(profile_json)
        await interaction.user.send(
            "Your selfie has been added to your profile successfully!"
        )


class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(
            ProfileView(self.bot), message_id=profile_json["profile_menu_id"]
        )

    match = app_commands.Group(
        name="match", description="Handle and manage the match functionality"
    )

    @match.command()
    @commands.has_permissions(administrator=True)
    async def create(self, interaction: discord.Interaction):
        chan = interaction.guild.get_channel(profile_json["send_profile_channel"])
        m = await chan.send("Create your profile here!", view=ProfileView(self.bot))
        profile_json["profile_menu_id"] = m.id
        dump_profile_json(profile_json)


async def setup(bot: commands.Bot):
    await bot.add_cog(Profile(bot))
