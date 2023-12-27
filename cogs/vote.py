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
import ngrok
from discord import app_commands
from datetime import datetime as dt
import server

from discord.app_commands import Choice
from discord.app_commands import AppCommandError


class Votes(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # server.keep_alive()
        self.bot.topgg = topgg.WebhookManager(self.bot).dsl_webhook(route="/dsl")
        await self.bot.topgg.run(5000)

        lis = await ngrok.forward(
            5000, authtoken="2a8QYDhQqhs3upeUqSQ7DgArT1U_5BEUtGjrRT8DtZXSDn3Gn"
        )

        print(lis.url())

        print("initialized vote")

    # try:
    #     server.keep_alive()
    # #     print('keeping alive')
    # except:
    #     traceback.print_exc()

    @commands.Cog.listener()
    async def on_dsl_vote(self, data):
        print(data)


async def setup(bot: commands.Bot):
    await bot.add_cog(Votes(bot))
