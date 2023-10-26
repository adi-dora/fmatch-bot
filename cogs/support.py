import json
import random
import traceback
from typing import Optional
from unicodedata import name
import discord
import datetime
from discord.ext import commands, tasks
from discord.interactions import Interaction
from dateutil import parser
import typing
import os
import io
import asyncio


from discord import Permissions, app_commands
from datetime import datetime as dt

from discord.app_commands import Choice
from discord.app_commands import AppCommandError


class CloseTicketView(discord.ui.View):
    def __init__(self, user: discord.Member | discord.User):
        super().__init__(timeout=None)
        self.member = user

    @discord.ui.button(
        style=discord.ButtonStyle.gray,
        label="Close Ticket",
        custom_id="close_ticket",
        emoji="❌",
    )
    async def close_ticket(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        try:
            with open("support.json", "r") as f:
                support = json.load(f)
            log_channel = interaction.guild.get_channel(support["log_channel"])
            for user in support["tickets"]:
                if support["tickets"][user] == interaction.channel.id:
                    del support["tickets"][user]
                    del support['last_message'][user]
                    break
            with open(f"log_{self.member.name}.txt", "a") as f:
                async for msg in interaction.channel.history(limit=None):
                    time = msg.created_at

                    second_time = time - datetime.timedelta(hours = 4)

                    second_time = second_time.strftime("%I:%M %p")

                    format_time = time.strftime("%A, %d %B %Y %I:%M %p")
                    f.write(
                        f'[{format_time}] - {msg.author.name}: "{msg.content}"\n'
                    )

            await log_channel.send(
                f"New ticket closed by {interaction.user.mention}",
                file=discord.File(f"./log_{self.member.name}.txt"),
            )

            await interaction.response.send_message('Ticket closing...')

            await asyncio.sleep(5)


            await interaction.channel.delete(reason="Ticket closed by user")

            os.remove(f"./log_{self.member.name}.txt")

            with open("support.json", "w") as f:
                json.dump(support, f, indent=1)
        except:
            traceback.print_exc()


class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    with open("support.json", "r") as f:
        support = json.load(f)

    @discord.ui.select(
        placeholder="What can we help you with?",
        min_values=1,
        max_values=1,
        options=[discord.SelectOption(label=option) for option in support["issues"]],
        custom_id="ticket_dropdown",
    )
    async def issue_dropdown(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        with open("support.json", "r") as f:
            support = json.load(f)
        try:
            if str(interaction.user.id) in support["tickets"]:
                return await interaction.response.send_message(
                    "You already have a ticket open!", ephemeral=True
                )
            category_to_create = None
            if select.values[0] == "Appeal":
                category_to_create = interaction.guild.get_channel(
                    support["appeal_category"]
                )
            else:
                category_to_create = interaction.guild.get_channel(support["category"])

            overwrites = category_to_create.overwrites
            overwrites[interaction.user] = discord.PermissionOverwrite(read_messages=True)

            ticket = await interaction.guild.create_text_channel(
                f"{interaction.user.name}",
                reason=f"New ticket opened for {select.values[0]}",
                category=category_to_create,
                overwrites=overwrites,
                topic=f"{interaction.user.display_name} created ticket for reason: {select.values[0]}",
            )

            support_role = interaction.guild.get_role(support["support_role"])
            embed = discord.Embed(
                title="New Ticket Created",
                description=f"Created by {interaction.user.mention} for reason: {select.values[0]}",
                timestamp=interaction.created_at,
            )
            embed.set_footer(
                text=f'This thread will be closed in {support["delay_to_close"]/3600} hours if inactive'
            ).set_thumbnail(url=interaction.user.avatar.url)

            m = await ticket.send(
                f"{support_role.mention} {interaction.user.mention}",
                embed=embed,
                view=CloseTicketView(interaction.user),
            )
            await m.pin()
            support["tickets"][interaction.user.id] = ticket.id
            support["last_message"][interaction.user.id] = str(datetime.datetime.now())
            with open("support.json", "w") as f:
                json.dump(support, f, indent=1)

            await interaction.response.send_message(
                f"A new ticket has been created in {ticket.mention} for your issue.",
                ephemeral=True,
            )
        
        except:
            traceback.print_exc()


class Support(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @tasks.loop(minutes=1)
    async def check_inactivity(self):
        with open("support.json", "r") as f:
            support = json.load(f)
        
        try:
            temp = support['last_message'].copy()

            for ticket in temp:
                if (
                    datetime.datetime.now() - parser.parse(support["last_message"][ticket])
                ).total_seconds() > support["delay_to_close"]:
                    del support["last_message"][ticket]
                    chan = self.bot.get_channel(support["tickets"][ticket])
                    del support["tickets"][ticket]
                    member = self.bot.get_user(int(ticket))
                    log_channel = self.bot.get_channel(support["log_channel"])
                    with open(f"log_{member.name}.txt", "a") as f:
                        async for msg in chan.history(limit=None, oldest_first=False):
                            time = msg.created_at

                            second_time = time - datetime.timedelta(hours = 4)

                            second_time = second_time.strftime("%I:%M %p")

                            format_time = time.strftime("%A, %d %B %Y %I:%M %p")
                            
                            f.write(
                                f'[{format_time}] - {msg.author.name}: "{msg.content}"\n'
                            )

                    await log_channel.send("Ticket closed for inactivity", file=discord.File(f"log_{member.name}.txt"))

                    os.remove(f"./log_{member.name}.txt")
                    with open("support.json", "w") as f:
                        json.dump(support, f, indent = 1)

                    await chan.delete(reason=f"Deleted for inactivity")
        except:
            traceback.print_exc()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        with open("support.json", "r") as f:
            support = json.load(f)

        for ticket in support["tickets"]:
            if support["tickets"][ticket] == message.channel.id and str(ticket) == str(
                message.author.id
            ):
                support["last_message"][ticket] = str(datetime.datetime.now())

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        with open("support.json", "r") as f:
            support = json.load(f)
        
        temp = support['tickets'].copy()

        if member.id in temp.keys():
            chan = member.guild.get_channel(support["tickets"][member.id])
            del support['tickets'][member.id]
            await chan.delete(reason=f"Ticket user {member.name} left server")
            log_channel = member.guild.get_channel(support["log_channel"])
            with open(f"log_{member.name}.txt", "a") as f:
                async for msg in chan.history(limit=None):
                    time = msg.created_at

                    second_time = time - datetime.timedelta(hours = 4)

                    second_time = second_time.strftime("%I:%M %p")

                    format_time = time.strftime("%A, %d %B %Y %I:%M %p")
                    f.write(
                        f'[{format_time}] - {msg.author.name}: "{msg.content}"\n'
                    )

                await log_channel.send(f"Ticket closed - member {member.mention} left server", file=discord.File(f'log_{member.name}.txt'))

            os.remove(f"./log_{member.name}.txt")

    @commands.Cog.listener()
    async def on_ready(self):
        print("ready")
        with open("support.json", "r") as f:
            support = json.load(f)

        if support["message"] is None:
            channel = self.bot.get_channel(support["channel"])
            try:
                m = await channel.send("br", view=DropdownView())
            except Exception as e:
                traceback.print_exc()

            support["message"] = m.id
        else:
            self.bot.add_view(DropdownView(), message_id=support["message"])
            for ticket in support["tickets"]:
                self.bot.add_view(
                    CloseTicketView(self.bot.get_user(ticket)),
                    message_id=support["tickets"][ticket],
                )

        with open("support.json", "w") as f:
            json.dump(support, f, indent=1)
        
        self.check_inactivity.start()
        



async def setup(bot):
    """Load the Giveaway cog."""
    await bot.add_cog(Support(bot))
