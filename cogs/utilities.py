import json, datetime, traceback
import discord
import utils.clock
from discord import app_commands
from discord.ext import commands
from dateutil import parser
from discord.app_commands import Choice


class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clock = utils.clock.Clock(self.bot)

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

    @app_commands.command(description="Set an AFK Status!")
    async def afk(self, interaction: discord.Interaction, status: str = ""):
        with open("utilities.json", "r") as f:
            util = json.load(f)

        util["afk_status"][str(interaction.user.id)] = {
            "status": status,
            "afk_since": str(interaction.created_at),
        }
        with open("utilities.json", "w") as f:
            json.dump(util, f, indent=1)

        await interaction.response.send_message(
            "Your AFK status has been set successfully."
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        with open("utilities.json", "r") as f:
            util = json.load(f)
        if message.guild is None or len(message.mentions) == 0:
            return

        if str(message.author.id) in util["afk_status"]:
            del util["afk_status"][str(message.author.id)]
            await message.reply(f"{message.author.mention} is no longer AFK!")
            with open("utilities.json", "w") as f:
                json.dump(util, f, indent=1)

        for mention in message.mentions:
            if str(mention.id) in util["afk_status"]:
                await message.reply(
                    f'{mention.mention} is currently AFK! Status: ``{util["afk_status"][str(mention.id)]["status"] if util["afk_status"][str(mention.id)]["status"] != "" else "None"}`` They have been AFK since <t:{int(parser.parse(util["afk_status"][str(mention.id)]["afk_since"]).timestamp())}:R>'
                )

    @app_commands.command(description="Set a reminder!")
    @app_commands.choices(
        unit=[
            Choice(name="Seconds", value="seconds"),
            Choice(name="Minutes", value="minutes"),
            Choice(name="Hours", value="hours"),
            Choice(name="Days", value="days"),
            Choice(name="Weeks", value="weeks"),
            Choice(name="Months", value="months"),
        ],
    )
    async def remindme(
        self, interaction: discord.Interaction, amount: int, unit: str, reminder: str
    ):
        try:
            until = datetime.datetime.now()
            if unit == "months":
                until += datetime.timedelta(weeks=amount * 4)
            if unit == "weeks":
                until += datetime.timedelta(weeks=amount)
            if unit == "days":
                until += datetime.timedelta(days=amount)

            if unit == "hours":
                until += datetime.timedelta(hours=amount)
            if unit == "minutes":
                until += datetime.timedelta(minutes=amount)
            if unit == "seconds":
                until += datetime.timedelta(seconds=amount)

            await interaction.response.send_message(
                f"Ok, I will remind you in {amount} {unit} about: {reminder}"
            )

            m = await interaction.original_response()

            await self.clock.create(
                reminder,
                interaction.channel_id,
                m.id,
                interaction.user.id,
                until,
            )
        except:
            traceback.print_exc()


async def setup(bot):
    await bot.add_cog(Utilities(bot))
