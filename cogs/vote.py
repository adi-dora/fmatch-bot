import json
import random
import traceback
import discord
import datetime
from discord.ext import commands
from discord.interactions import Interaction
import uuid
from dateutil import parser
import topgg
import os
import ngrok
import math
from discord import app_commands
from datetime import datetime as dt


from utils.level_utils import *
from utils.vote_utils import *
from utils import clock


class Votes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            self.bot.topgg = topgg.WebhookManager(self.bot).dsl_webhook(
                route="/dsl", auth_key="abcd"
            )
            await self.bot.topgg.run(5000)

            lis = await ngrok.forward(
                5000,
                authtoken=os.getenv("NGROK_AUTHTOKEN"),
                domain="vulture-shining-routinely.ngrok-free.app",
            )

            print("initialized vote")
        except:
            traceback.print_exc()

    @app_commands.command()
    async def votereminder(self, interaction: discord.Interaction):
        if str(interaction.user.id) not in vote_json["votes"]:
            return await interaction.response.send_message(
                "You have not voted for the bot yet!"
            )

        if vote_json["votes"][str(interaction.user.id)]["remind"]:
            vote_json["votes"][str(interaction.user.id)]["remind"] = False
            await interaction.response.send_message(
                "You have opted out of vote reminders successfully!"
            )

        else:
            vote_json["votes"][str(interaction.user.id)]["remind"] = True
            await interaction.response.send_message(
                "You have opted into vote reminders successfully! You will be notified 12 hours after your next vote!"
            )

        dump_vote_json(vote_json)

    @commands.Cog.listener()
    async def on_dsl_vote(self, data):
        try:
            guild = self.bot.get_guild(data["guild"])
            chan = guild.get_channel(vote_json["vote_channel"])
            user = guild.get_member(int(data["user"]))
            if data["user"] not in vote_json["votes"]:
                vote_json["votes"][data["user"]] = {
                    "num_votes": 1,
                    "last_vote": str(dt.now()),
                    "remind": False,
                }
            else:
                vote_json["votes"][data["user"]]["num_votes"] += 1

            try:
                level_json[data["user"]]["experience"] += 100

            except KeyError:
                level_json[data["user"]] = {
                    "level": math.floor(100 ** (1 / 3)),
                    "experience": 100,
                    "position": len(level_json),
                    "last_message": str(dt.now()),
                }
            if vote_json["votes"][data["user"]]["num_votes"] == 10:
                level_json[data["user"]]["experience"] += 1000

            if vote_json["votes"][data["user"]]["num_votes"] == 30:
                role = guild.get_role(vote_json["30_votes_role"])
                await user.add_roles(role, reason="User voted 30 times")

            if vote_json["votes"][data["user"]]["num_votes"] == 50:
                role = guild.get_role(vote_json["50_votes_role"])
                await user.add_roles(role, reason="User voted 50 times")

            if (
                level_json[data["user"]]["experience"]
                > (level_json[data["user"]]["level"] + 1) ** 3
            ):
                level_json[data["user"]]["level"] = math.floor(
                    level_json[data["user"]]["experience"] ** (1 / 3)
                )

            dump_level_json(level_json)
            dump_vote_json(vote_json)

            await chan.send(
                embed=discord.Embed(
                    title="User Voted for Server",
                    description=f'{user.mention} has voted for the server and received rewards! \n\n [Click here to vote!]({vote_json["topgg_server_link"]})',
                    color=discord.Color.pink(),
                    timestamp=dt.now(),
                )
            )

            embed = discord.Embed(
                title="Thank You for Voting",
                description=f'Thank you for voting Flirtcord! Your rewards have been added! Your current vote count is ``{vote_json["votes"][str(user.id)]["num_votes"]}``!',
                color=discord.Color.pink(),
                timestamp=dt.now(),
            )

            if vote_json["votes"][str(user.id)]["remind"]:
                embed.description += (
                    " You will be reminded to vote again after 12 hours!"
                )
            else:
                embed.description += " You will be able to vote again after 12 hours! If you would like to be reminded, please enable vote reminders!"

            await user.send(embed=embed)

            if vote_json["votes"][str(user.id)]["remind"]:
                clock_inst: clock.Clock = clock.Clock.instances[0]
                await clock_inst.create(
                    "vote reminder",
                    None,
                    None,
                    user.id,
                    dt.now() + datetime.timedelta(hours=12),
                )
        except:
            traceback.print_exc()


async def setup(bot: commands.Bot):
    await bot.add_cog(Votes(bot))
