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
from verification_utils import verification_json, dump_verification_json


class DeniedModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Denied Reason", timeout=300, custom_id="denied_modal")


class VerificationView(discord.ui.View):
    def __init__(
        self,
    ):
        super().__init__(timeout=None)

    @discord.ui.button(label="Gender Verified", custom_id="gender_button")
    async def gender_verified_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        print("clicked")

    @discord.ui.button(label="18+ Verified", custom_id="age_button")
    async def age_verified_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        print("age button clicked")

    @discord.ui.button(label="Denied", custom_id="denied_button")
    async def denied_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        print("denied clicked")

    @discord.ui.button(label="Mute user", custom_id="mute_button")
    async def mute_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        print("mute")


class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command()
    async def verify(
        self,
        interaction: discord.Interaction,
        pose: discord.Attachment,
        id: discord.Attachment,
    ):
        chan = interaction.guild.get_channel(verification_json["verification_channel"])
        pose = await pose.to_file()
        id = await id.to_file()
        embed = (
            discord.Embed(
                title="New Verification Request", timestamp=interaction.created_at
            )
            .add_field(name="User", value=f"{interaction.user.mention}")
            .set_author(
                name=f"{interaction.user.name}", icon_url=interaction.user.avatar.url
            )
        )
        embed.set_image(url=id.url).set_thumbnail(url=pose.url)
        await chan.send(embed=embed, view=VerificationView())


async def setup(bot):
    await bot.add_cog(Verification(bot))
