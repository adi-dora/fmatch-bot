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

class ConfessionModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='New Confession', timeout=600, custom_id='confession_modal')

        self.confession = discord.ui.TextInput(label='New Confession', style=discord.TextStyle.long, custom_id='confession_text', required=True)
        self.add_item(self.confession)
    
    async def on_submit(self, interaction: Interaction) -> None:
        reply_chan = interaction.guild.get_channel(submission_json['confession_reply_channel'])
        
class SuggestionModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="New Suggestion", timeout=300, custom_id="suggestion_modal"
        )

        self.text = discord.ui.TextInput(
            label="Suggestion",
            style=discord.TextStyle.short,
            custom_id="suggestion_text",
            placeholder="Make sure to be as specific as possible!",
            required=True,
        )
        self.explanation = discord.ui.TextInput(
            label="Explanation",
            style=discord.TextStyle.long,
            custom_id="explanation_text",
            placeholder="How would this benefit the server?",
            required=True,
        )

        self.add_item(self.text)
        self.add_item(self.explanation)

    async def on_submit(self, interaction: Interaction) -> None:
        #Send suggestions to send_suggestion_channel field in JSON
        suggest_chan = interaction.guild.get_channel(
            submission_json["send_suggestion_channel"]
        )
        m = await suggest_chan.send(
            embed=discord.Embed(title="New Suggestion", color=discord.Color.green())
            .add_field(name="Suggested By", value=interaction.user.mention)
            .add_field(name="Suggestion", value=self.text.value, inline=False)
            .add_field(name="Explanation", value=self.explanation.value, inline=False)
            .set_thumbnail(url=interaction.user.avatar.url)
        )

        await m.add_reaction("✅")
        await m.add_reaction("❌")
        await interaction.response.send_message('Your suggestion has been sent to be voted on!', ephemeral=True)


class SuggestionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="New Suggestion", custom_id="suggest_button")
    async def suggest_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        await interaction.response.send_modal(SuggestionModal())


class Submission(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.add_view(
            SuggestionView(), message_id=submission_json["suggestion_id"]
        )

    @app_commands.command()
    @commands.has_permissions(administrator=True)
    async def suggestion(self, interaction: discord.Interaction):
        try:
    
            suggest_chan = interaction.guild.get_channel(
                submission_json["suggestion_channel"]
            )
            m = await suggest_chan.send(submission_json["suggestion_message"], view = SuggestionView())
            submission_json['suggestion_id'] = m.id
            dump_submission_json(submission_json)
            await interaction.response.send_message('Suggestion message sent')
        except:
            traceback.print_exc()

    
    @app_commands.command()
    @commands.has_permissions(administrator=True)
    async def confession(self, interaction: discord.Interaction):
        confession_chan = interaction.guild.get_channel(submission_json['confession_channel'])
        m = await confession_chan.send(submission_json["confession_message"], view = SuggestionView())
        submission_json['confession_id'] = m.id
        dump_submission_json(submission_json)

async def setup(bot:commands.Bot):
    await bot.add_cog(Submission(bot))