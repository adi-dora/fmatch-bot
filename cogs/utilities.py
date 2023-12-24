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

    @app_commands.command(description="Get information about a user!")
    @app_commands.describe(user="Provide a user or see your own stats")
    async def userinfo(
        self, interaction: discord.Interaction, user: discord.Member | None
    ):
        if user is None:
            user = interaction.user

        await interaction.response.send_message(
            embed=discord.Embed(
                description=user.mention,
                timestamp=interaction.created_at,
                color=discord.Color.pink(),
            )
            .add_field(name="Joined Server", value=user.joined_at.strftime("%m/%d/%Y"))
            .add_field(
                name="Joined Discord", value=user.created_at.strftime("%m/%d/%Y")
            )
            .add_field(
                name=f"Roles ({len(user.roles)})",
                value=" ".join(role.mention for role in user.roles),
                inline=False,
            )
            .set_author(name=user.name, icon_url=interaction.user.avatar.url)
            .set_footer(text=f"ID: {user.id}")
            .set_thumbnail(url=user.avatar.url)
        )


async def setup(bot):
    await bot.add_cog(Utilities(bot))
