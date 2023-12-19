import json
import discord
from discord.ext import commands


from discord import app_commands
from utils.match_utils import *
from utils.profile_utils import *
from utils.verification_utils import *


class MatchView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # TODO: Add functionality to the Enter and Leave Queue buttons to keep track of who's in queue and whether they are eligble to enter. Then send profile to matches

    @discord.ui.button(label="Enter Queue", custom_id="enter_queue", emoji="\U00002764")
    async def enter_queue_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if str(interaction.user.id) not in profile_json["profiles"]:
            return await interaction.response.send_message(
                "You do not have a profile! Please create one before you can enter the queue!",
                ephemeral=True,
            )
        if (
            interaction.guild.get_role(verification_json["male_role"])
            in interaction.user.roles
            or interaction.guild.get_role(verification_json["trans_m_role"])
            in interaction.user.roles
        ):
            if (
                interaction.guild.get_role(match_json["male_pref_role"])
                in interaction.user.roles
            ):
                match_json["m_pref_m_queue"].append(str(interaction.user.id))
            else:
                match_json["m_pref_f_queue"].append(str(interaction.user.id))
        else:
            if (
                interaction.guild.get_role(match_json["male_pref_role"])
                in interaction.user.roles
            ):
                match_json["f_pref_m_queue"].append(str(interaction.user.id))
            else:
                match_json["f_pref_f_queue"].append(str(interaction.user.id))

        dump_match_json(match_json)
        await interaction.user.add_roles(
            interaction.guild.get_role(match_json["matchmaking_role"]),
            reason="User entered matchmaking queue",
        )

    @discord.ui.button(label="Leave Queue", custom_id="leave_queue", emoji="\U0001f494")
    async def leave_queue(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        try:
            match_json["general_queue"].remove(str(interaction.user.id))

        except ValueError:
            return await interaction.response.send_message(
                "You are not currently in the queue!", ephemeral=True
            )

        if (
            interaction.guild.get_role(verification_json["male_role"])
            in interaction.user.roles
            or interaction.guild.get_role(verification_json["trans_m_role"])
            in interaction.user.roles
        ):
            if (
                interaction.guild.get_role(match_json["male_pref_role"])
                in interaction.user.roles
            ):
                match_json["m_pref_m_queue"].remove(str(interaction.user.id))
            else:
                match_json["m_pref_f_queue"].remove(str(interaction.user.id))
        else:
            if (
                interaction.guild.get_role(match_json["male_pref_role"])
                in interaction.user.roles
            ):
                match_json["f_pref_m_queue"].remove(str(interaction.user.id))
            else:
                match_json["f_pref_f_queue"].remove(str(interaction.user.id))

        dump_match_json(match_json)
        await interaction.user.remove_roles(
            interaction.guild.get_role(match_json["matchmaking_role"]),
            reason="User left machmaking queue",
        )
        await interaction.response.send_message(
            "You have been removed from the queue successfully!", ephemeral=True
        )


class Match(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.add_view()

    match = app_commands.Group(
        name="match", description="Create and manage the matchmaking functionality"
    )

    @match.command()
    @commands.has_permissions(manage_guild=True)
    async def message(self, interaction: discord.Interaction, msg: str | None):
        with open("match.json", "r") as f:
            match = json.load(f)

        if msg is None:
            if match["message"] is None:
                return await interaction.response.send_message(
                    "There is no message set!"
                )

            return await interaction.response.send_message(
                "``The current message is set to:\n``" + match["message"]
            )

        match["message"] = msg

        with open("match.json", "w") as f:
            json.dump(match, f)

        await interaction.response.send_message("Your message has been set!")

    @match.command()
    @commands.has_permissions(manage_channels=True)
    async def channel(
        self, interaction: discord.Interaction, channel: discord.TextChannel | None
    ):
        with open("match.json", "r") as f:
            match = json.load(f)

        if channel is None:
            if match["channel"] is None:
                return await interaction.response.send_message(
                    "The channel has not been set!"
                )

            return await interaction.response.send_message(
                f'The current channel is set to: {interaction.guild.get_channel(match["channel"]).mention}'
            )

        match["channel"] = channel.id

        with open("match.json", "w") as f:
            json.dump(match, f)

        await interaction.response.send_message(
            f"The channel has been set to: {channel.mention}"
        )

    @match.command()
    async def link(self, interaction: discord.Interaction, url: str | None):
        with open("match.json", "r") as f:
            match = json.load(f)

        if url is None:
            if match["link"] is None:
                return await interaction.response.send_message(
                    "There is no image/link stored"
                )

            return await interaction.response.send_message(
                "The current image is: " + match["link"]
            )

        match["link"] = url

        with open("match.json", "w") as f:
            json.dump(match, f)

        await interaction.response.send_message("The link has been set to " + url)

    @match.command()
    async def create(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        with open("match.json", "r") as f:
            match = json.load(f)


async def setup(bot: commands.Bot):
    await bot.add_cog(Match(bot))
