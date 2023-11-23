import json
import random
import traceback
from typing import Optional
from unicodedata import name
import discord
from discord.ext import commands


from discord import app_commands


class Custom(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def example(self, ctx: commands.Context):
        chan_to_send = ctx.guild.get_channel(1135052505139658782)
        await chan_to_send.send(
            "This message will be sent to the channel specified above"
        )
        await ctx.send("Msg sent to channel")

    @app_commands.command()
    @commands.has_permissions(administrator=True)
    async def example2(self, interation: discord.Interaction):
        chan_to_send = interation.guild.get_channel(1135052505139658782)
        await chan_to_send.send(
            embed=discord.Embed(
                color=discord.Color.green(),
                title="Example Message",
                description="This message will be sent to the channel specified above",
                timestamp=interation.created_at,
            )
        )
        await interation.response.send_message("Msg sent to channel", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Custom())
