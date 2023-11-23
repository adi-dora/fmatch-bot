import json
import discord
from discord.ext import commands


from discord import app_commands


class MatchView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    # TODO: Add functionality to the Enter and Leave Queue buttons to keep track of who's in queue and whether they are eligble to enter. Then send profile to matches

    @discord.ui.button(label="Enter Queue", custom_id="enter_queue", emoji="\U00002764")
    async def enterQueue(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        with open("match.json", "r") as f:
            match = json.load(f)

    @discord.ui.button(label="Leave Queue", custom_id="leave_queue", emoji="\U0001f494")
    async def leave_queue(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        with open("match.json", "r") as f:
            match = json.load(f)


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
