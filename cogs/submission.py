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





class ReplyModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="Reply to this Confession", timeout=500, custom_id="reply_modal"
        )

        self.reply = discord.ui.TextInput(
            label="Reply",
            style=discord.TextStyle.long,
            custom_id="reply_text",
        )
        self.add_item(self.reply)

    async def on_submit(self, interaction: Interaction) -> None:
        await interaction.response.send_message('Your reply to this confession has been posted!', ephemeral=True)


class ReplyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Reply to this confession",
        custom_id="reply_button",
        style=discord.ButtonStyle.primary,
    )
    async def reply_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        reply_chan = interaction.guild.get_channel(submission_json['confession_reply_channel'])
        modal = ReplyModal()
        await interaction.response.send_modal(modal)
        await modal.wait()
        await reply_chan.send(f'{interaction.message.jump_url}',
            embed=discord.Embed(
                title="New Reply",
                description=modal.reply.value,
                color=discord.Color.purple(),
                timestamp=interaction.created_at,
            )
        )


class ConfessionModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(
            title="New Confession", timeout=600, custom_id="confession_modal"
        )

        self.confession = discord.ui.TextInput(
            label="New Confession",
            style=discord.TextStyle.long,
            custom_id="confession_text",
            required=True,
        )
        self.add_item(self.confession)

    async def on_submit(self, interaction: Interaction) -> None:
        reply_chan = interaction.guild.get_channel(
            submission_json["confession_send_channel"]
        )
        await reply_chan.send(
            embed=discord.Embed(
                title="New Confession",
                color=discord.Color.pink(),
                timestamp=interaction.created_at,
                description=self.confession.value,
            ),
            view=ReplyView(),
        )
        await interaction.response.send_message(
            f"Your confession has been successfully sent to {reply_chan.mention}",
            ephemeral=True,
        )


class ConfessionView(discord.ui.View):
    def __init__(
        self,
    ):
        super().__init__(timeout=None)

    @discord.ui.button(label="Confess", custom_id="confess_button")
    async def confess_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        await interaction.response.send_modal(ConfessionModal())


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
        # Send suggestions to send_suggestion_channel field in JSON
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
        await interaction.response.send_message(
            "Your suggestion has been sent to be voted on!", ephemeral=True
        )


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
        self.bot.add_view(SuggestionView(), message_id=submission_json["suggestion_id"])
        self.bot.add_view(ConfessionView(), message_id=submission_json["confession_id"])

    @app_commands.command()
    @commands.has_permissions(administrator=True)
    async def suggestion(self, interaction: discord.Interaction):
        suggest_chan = interaction.guild.get_channel(
            submission_json["suggestion_channel"]
        )
        m = await suggest_chan.send(
            submission_json["suggestion_message"], view=SuggestionView()
        )
        submission_json["suggestion_id"] = m.id
        dump_submission_json(submission_json)
        await interaction.response.send_message("Suggestion message sent")

    @app_commands.command()
    @commands.has_permissions(administrator=True)
    async def confession(self, interaction: discord.Interaction):
        confession_chan = interaction.guild.get_channel(
            submission_json["confession_channel"]
        )
        m = await confession_chan.send(
            submission_json["confession_message"], view=ConfessionView()
        )
        submission_json["confession_id"] = m.id
        dump_submission_json(submission_json)


async def setup(bot: commands.Bot):
    await bot.add_cog(Submission(bot))
