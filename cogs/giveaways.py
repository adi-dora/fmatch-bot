import json
import random
import traceback
import discord
import datetime
from discord.ext import commands
from discord.interactions import Interaction
import uuid
from dateutil import parser

from discord import app_commands
from datetime import datetime as dt

from discord.app_commands import Choice
from discord.app_commands import AppCommandError


class GiveawayView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Enter Giveaway!", emoji=discord.PartialEmoji(name="\N{HOURGLASS}")
    )
    async def enter(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        with open("giveaways.json", "r") as f:
            giveaways = json.load(f)

        for giveaway in giveaways["giveaways"]:
            if giveaway["message"] == interaction.message.id:
                if interaction.user.id in giveaway["participants"]:
                    return await interaction.followup.send(
                        "You have already entered the giveaway!\n", ephemeral=True
                    )

                required_role = interaction.guild.get_role(giveaway["required_role"])
                if (
                    required_role is not None
                    and required_role not in interaction.user.roles
                ):
                    return await interaction.followup.send(
                        f"You don't have the required role ``{required_role.name}`` for this giveaway!\n",
                        ephemeral=True,
                    )

                giveaway["participants"].append(interaction.user.id)
                embed = interaction.message.embeds[0]
                embed.remove_field(len(embed.fields) - 1)
                embed.add_field(name="Entries", value=len(giveaway["participants"]))
                await interaction.message.edit(embed=embed)

        with open("giveaways.json", "w") as f:
            json.dump(giveaways, f, indent=1)

        await interaction.followup.send(
            "You have been entered into the giveaway!\n", ephemeral=True
        )


class ConfirmationView(discord.ui.View):
    def __init__(
        self,
        *,
        prize: str,
        winners: int,
        time: dt,
        host: discord.Member,
        role: discord.Role,
        id: str,
        reqrole: discord.Role,
        channel: discord.TextChannel,
        bot: discord.Client,
    ):
        super().__init__(timeout=600)
        self.prize = prize
        self.winners = winners
        self.time = time
        self.reqrole = reqrole
        self.host = host
        self.role = role
        self.id = id
        self.channel = channel
        self.bot = bot

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, emoji="✔️")
    async def confirm(
        self,
        interaction: Interaction,
        button: discord.ui.Button,
    ):
        try:
            with open("giveaways.json", "r") as f:
                giveaways = json.load(f)

            giveaway_embed = discord.Embed(
                title="Prize: " + self.prize.title(),
                color=discord.Color.green(),
                timestamp=interaction.created_at,
            )
            giveaway_embed.add_field(
                name="Giveaway Ends",
                value=f"<t:{int(self.time.timestamp())}:R>",
                inline=False,
            ).set_thumbnail(url=interaction.guild.icon.url)
            giveaway_embed.add_field(
                name="Hosted By", value=self.host.mention, inline=True
            ).set_footer(text=f"ID: {self.id}")
            giveaway_embed.add_field(
                name="Required Role",
                value=self.reqrole.mention if self.reqrole else "@everyone",
                inline=True,
            )
            giveaway_embed.add_field(
                name="Number of Winners", value=self.winners, inline=False
            ).add_field(name="Entries", value=0, inline=True)

            m = await self.channel.send(
                (f"{self.role.mention} " if self.role else "") + "New Giveaway!",
                embed=giveaway_embed,
                view=GiveawayView(),
            )

            giveaways["giveaways"].insert(
                0,
                {
                    "id": self.id,
                    "prize": self.prize,
                    "num_winners": self.winners,
                    "time": str(self.time),
                    "host": self.host.id,
                    "participants": [],
                    "channel": self.channel.id,
                    "role": self.role.id if self.role else None,
                    "message": m.id,
                    "ongoing": True,
                    "winners": [],
                    "required_role": self.reqrole.id if self.reqrole else None,
                },
            )
            await interaction.response.send_message("The giveaway has been created!")
            await interaction.message.edit(view=None)
            with open("giveaways.json", "w") as f:
                json.dump(giveaways, f, indent=1)
            await discord.utils.sleep_until(self.time)
            self.bot.dispatch("giveaway_end", interaction, self.id)

        except:
            traceback.print_exc()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, emoji="✖️")
    async def decline(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message("The giveaway has been cancelled!")
        await interaction.message.edit(view=None)


class Giveaway(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        with open("giveaways.json") as f:
            giveaways = json.load(f)

        for giveaway in giveaways:
            if giveaway["ongoing"]:
                channel = self.bot.get_channel(giveaway["channel"])
                message = channel.get_partial_message(giveaway["message"])
                await discord.utils.sleep_until(parser.parse(giveaway["time"]))
                self.bot.dispatch("giveaway_end", message.interaction, giveaway["id"])

    giveaway = app_commands.Group(
        name="giveaway", description="Host and manage giveaways!"
    )

    @giveaway.command(
        name="start",
        description="Start a giveaway!",
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        channel="The channel to host the giveaway in",
        pingrole="The role to ping for the giveaway. Optional",
        amount="The amount of the selected unit of time. E.g. If amount is 7 and unit is Days, the giveaway will last for 7 days",
        unit="The time increment for the giveaway. Select how many of this unit of time with the amount parameter",
        requiredrole="The role required to enter the giveaway. If left blank, anyone can enter.",
        prize="The prize of the giveaway!",
        winners="The number of winners for the giveaway",
    )
    @app_commands.choices(
        unit=[
            app_commands.Choice(name="Seconds", value="seconds"),
            app_commands.Choice(name="Minutes", value="minutes"),
            app_commands.Choice(name="Hours", value="hours"),
            app_commands.Choice(name="Days", value="days"),
            app_commands.Choice(name="Weeks", value="weeks"),
            app_commands.Choice(name="Months", value="months"),
        ]
    )
    async def start_giveaway(
        self,
        interaction: Interaction,
        amount: int,
        unit: str,
        channel: discord.TextChannel,
        prize: str,
        winners: int,
        pingrole: discord.Role = None,
        requiredrole: discord.Role = None,
    ):
        giveaway_id = uuid.uuid4()
        if unit == "seconds":
            total_time = amount

        if unit == "minutes":
            total_time = amount * 60

        if unit == "hours":
            total_time = amount * 3600

        if unit == "days":
            total_time = amount * 86400

        if unit == "weeks":
            total_time = amount * 604800

        if unit == "months":
            total_time = amount * 2419200

        confirmation_embed = discord.Embed(
            title="Giveaway Settings",
            description="Are you sure these are the settings for the giveaway?",
            color=discord.Color.orange(),
            timestamp=interaction.created_at,
        )

        delta = datetime.datetime.now() + datetime.timedelta(seconds=total_time)

        confirmation_embed.set_author(
            name=f"Hosted by: {interaction.user.name}",
            icon_url=interaction.user.display_avatar.url,
        )
        confirmation_embed.add_field(name="Prize", value=prize.title()).add_field(
            name="Duration", value=f"{amount} {unit} (<t:{int(delta.timestamp())}>)"
        ).add_field(name="Channel", value=channel.mention).add_field(
            name="Pinged Role", value=f'{pingrole.mention if pingrole else "None"}'
        ).add_field(
            name="Winners", value=winners
        ).set_image(
            url=interaction.guild.icon.url
        ).set_footer(
            text=f"ID: {giveaway_id}"
        ).add_field(
            name="Required Role",
            value=f'{requiredrole.mention if requiredrole else "None"}',
        )

        await interaction.response.send_message(
            embed=confirmation_embed,
            view=ConfirmationView(
                prize=prize,
                winners=winners,
                time=delta,
                host=interaction.user,
                role=pingrole,
                id=str(giveaway_id),
                channel=channel,
                bot=self.bot,
                reqrole=requiredrole,
            ),
        )

    @giveaway.command()
    @app_commands.describe(
        id="The ID of the giveaway. Displayed in the footer of the giveaway embed.",
        user="The winner to reroll. If no one is provided, every winner will be rerolled.",
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def reroll(
        self,
        interaction: Interaction,
        id: str,
        user: discord.Member | discord.User | None,
    ):
        with open("giveaways.json", "r") as f:
            giveaways = json.load(f)

        for giveaway in giveaways["giveaways"]:
            if giveaway["id"] == id:
                channel = interaction.guild.get_channel(giveaway["channel"])
                msg = channel.get_partial_message(giveaway["message"])
                if giveaway["ongoing"]:
                    return await interaction.response.send_message(
                        "This giveaway is still ongoing!"
                    )
                if len(giveaway["participants"]) == 0:
                    return await interaction.response.send_message(
                        "There were no other entries for the giveaway!"
                    )

                if user is None:
                    count = giveaway["num_winners"]
                    while count and giveaway["participants"]:
                        new_win = random.choice(giveaway["participants"])
                        giveaway["participants"].remove(new_win)
                        giveaway["winners"].append(new_win)
                        count -= 1

                    removable = temp = giveaway["num_winners"] - count
                    while removable:
                        giveaway["participants"].append(giveaway["winners"].pop(0))
                        removable -= 1

                    await interaction.response.send_message(
                        f'Rerolled {temp}/{giveaway["num_winners"]} winners'
                    )
                    winners = []
                    for winner in giveaway["winners"]:
                        winners.append(
                            interaction.guild.get_member(winner)
                            if interaction.guild.get_member(winner) is not None
                            else self.bot.get_user(winner)
                        )

                    await msg.reply(
                        f'{", ".join(winner.mention for winner in winners)} won the giveaway!'
                    )
                    await msg.edit(
                        content=f'Giveaway ended! Winners: {", ".join(winner.mention for winner in winners)}'
                    )
                    with open("giveaways.json", "w") as f:
                        json.dump(giveaways, f, indent=1)
                    return

                if user.id not in giveaway["winners"]:
                    return await interaction.response.send_message(
                        "This user never won the giveaway!"
                    )

                giveaway["winners"].remove(user.id)

                giveaway["participants"].remove(winner)
                giveaway["participants"].append(user.id)
                giveaway["winners"].append(winner)

                winner = (
                    interaction.guild.get_member(winner)
                    if interaction.guild.get_member(winner) is not None
                    else self.bot.get_user(winner)
                )

                await msg.reply(f"{winner.mention} won the giveaway!")

                with open("giveaways.json", "w") as f:
                    json.dump(giveaways, f, indent=1)
                return

        await interaction.response.send_message("The ID provided was invalid!")

    def fetch_giveaways(self):
        with open("giveaways.json", "r") as f:
            giveaways = json.load(f)

        return giveaways["giveaways"]

    @giveaway.command()
    @app_commands.describe(
        giveaways="The giveaway to fetch the information for. A list of all giveaways is displayed, most recent first."
    )
    async def details(self, interaction: discord.Interaction, giveaways: str):
        with open("giveaways.json", "r") as f:
            _giveaways = json.load(f)

        for giveaway in _giveaways["giveaways"]:
            if giveaway["id"] == giveaways:
                host = interaction.guild.get_member(giveaway["host"])
                role = (
                    interaction.guild.get_role(giveaway["role"])
                    if giveaway["role"]
                    else None
                )
                reqrole = (
                    interaction.guild.get_role(giveaway["required_role"])
                    if giveaway["required_role"]
                    else None
                )
                channel = interaction.guild.get_channel(giveaway["channel"])
                message = channel.get_partial_message(giveaway["message"])
                time_remaining = parser.parse(giveaway["time"]).timestamp()
                details = discord.Embed(
                    title="Giveaway Details",
                    color=discord.Color.purple(),
                    timestamp=interaction.created_at,
                )

                details.set_author(
                    name=f"Hosted by: {host.display_name}",
                    icon_url=interaction.user.display_avatar.url,
                )
                details.add_field(
                    name="Prize", value=giveaway["prize"].title()
                ).add_field(
                    name="Ends",
                    value=f"<t:{int(time_remaining)}> (<t:{int(time_remaining)}:R>)",
                ).add_field(
                    name="Channel", value=channel.mention
                ).add_field(
                    name="Message", value=message.jump_url
                ).add_field(
                    name="Pinged Role", value=f'{role.mention if role else "None"}'
                ).add_field(
                    name="Number of Winners", value=giveaway["num_winners"]
                ).set_image(
                    url=interaction.guild.icon.url
                ).set_footer(
                    text=f'ID: {giveaway["id"]}'
                ).add_field(
                    name="Required Role",
                    value=f'{reqrole.mention if reqrole else "None"}',
                )

                return await interaction.response.send_message(embed=details)

        return await interaction.response.send_message("The ID provided was invalid!")

    @details.autocomplete("giveaways")
    async def autocomplete_callback(
        self, interaction: discord.Interaction, current: str
    ):
        return [
            Choice(name=_giveaway["prize"].title(), value=_giveaway["id"])
            for _giveaway in self.fetch_giveaways()
            if current.lower() in _giveaway["prize"].lower()
        ]

    @commands.Cog.listener()
    async def on_giveaway_end(self, interaction: discord.Interaction, id: str):
        with open("giveaways.json", "r") as f:
            giveaways = json.load(f)
        try:
            for giveaway in giveaways["giveaways"]:
                if giveaway["id"] == id:
                    counter = giveaway["num_winners"]
                    channel = interaction.guild.get_channel(giveaway["channel"])
                    message = channel.get_partial_message(giveaway["message"])
                    giveaway["ongoing"] = False
                    winners = []
                    if len(giveaway["participants"]) == 0:
                        return await message.reply(
                            "There were no participants in this giveaway!"
                        )
                    while counter and giveaway["participants"]:
                        winner = random.choice(giveaway["participants"])

                        giveaway["participants"].remove(winner)
                        winner = interaction.guild.get_member(winner)
                        if winner is not None:
                            winners.append(winner)
                            giveaway["winners"].append(winner.id)
                            counter -= 1

                    await message.reply(
                        f'{", ".join(winner.mention for winner in winners)} won the giveaway! Make sure to claim soon or the giveaway wll be rerolled!'
                    )
                    await message.edit(
                        content=f'Giveaway Ended! Winner: {", ".join(winner.mention for winner in winners) if len(winners) != 0 else "None"}!',
                        view=None,
                    )

                    with open("giveaways.json", "w") as f:
                        json.dump(giveaways, f, indent=1)
                    break
        except:
            traceback.print_exc()

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: AppCommandError
    ):
        traceback.print_exc()


async def setup(bot):
    """Load the Giveaway cog."""
    await bot.add_cog(Giveaway(bot))
