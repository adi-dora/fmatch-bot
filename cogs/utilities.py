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

    @app_commands.command(
        name="avatar", description="Get the avatar of a user in the server!"
    )
    async def avatar(
        self, interaction: discord.Interaction, user: discord.Member | None
    ):
        if user is None:
            user = interaction.user
        await interaction.response.send_message(
            embed=discord.Embed(
                color=discord.Color.pink(),
                timestamp=interaction.created_at,
                description=user.mention,
            )
            .set_image(
                url=user.guild_avatar.url
                if user.guild_avatar is not None
                else user.display_avatar.url
            )
            .set_footer(text=f"ID: {user.id}")
            .set_author(name=user.name, icon_url=user.avatar.url)
        )

    @app_commands.command(
        description="Get statistics about the current members of the server!"
    )
    async def membercount(self, interaction: discord.Interaction):
        try:
            online = 0
            idle = 0
            dnd = 0
            offline = 0
            bots = 0
            total_count = 0
            await interaction.response.defer()
            async for member in interaction.guild.fetch_members():
                member = interaction.guild.get_member(member.id)
                
                if member.bot:
                    bots += 1

                elif member.status == discord.Status.online:
                    online += 1
                elif member.status == discord.Status.idle:
                    idle += 1
                elif member.status == discord.Status.dnd:
                    dnd += 1
                else:
                    offline += 1
                total_count += 1

            await interaction.followup.send(
                embed=discord.Embed(
                    description=f":green_circle: : {online} \n :yellow_circle: : {idle} \n :red_circle: : {dnd}",
                    color=discord.Color.pink(),
                    timestamp=interaction.created_at,
                )
                .add_field(name="Total Member Count", value=total_count)
                .add_field(
                    name="Members (without bots)",
                    value=total_count - bots,
                    inline=False,
                )
                .add_field(name="Bots", value=bots)
                .add_field(name="Online", value=online + idle + dnd, inline=True)
                .add_field(name="Offline", value=offline)
                .set_thumbnail(url=interaction.guild.icon.url)
                .set_footer(text=f"Server ID: {interaction.guild.id}")
            )
        except:
            traceback.print_exc()


async def setup(bot):
    await bot.add_cog(Utilities(bot))
