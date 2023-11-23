import traceback
import datetime
import asyncio
import typing

import discord
from discord import app_commands
from discord.ext import commands
from discord.interactions import Interaction
from discord.app_commands import Choice
from discord.app_commands import AppCommandError

from utils.moderation_utils import moderation_json, dump_moderation_json


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        description="Ban a user from the server! Optionally, provide a reason for the ban."
    )
    @commands.has_permissions(ban_members=True)
    @app_commands.choices(
        reason=[
            Choice(name=item, value=count)
            for count, item in enumerate(moderation_json["rules"])
        ]
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        user: typing.Union[discord.Member, discord.User],
        reason: int,
        proof: discord.Attachment,
    ):
        if moderation_json["log_channel"] is None:
            return await interaction.response.send_message(
                "The log channel has not been set up."
            )

        if not interaction.guild.me.guild_permissions.ban_members:
            return await interaction.response.send_message(
                "I do not have permission to ban members."
            )

        log = interaction.guild.get_channel(moderation_json["log_channel"])
        if log is None:
            return await interaction.response.send_message(
                "The log channel was not found! Make sure the channel exists and I have access to it!"
            )

        embed = discord.Embed(
            description=f"You've been banned from **{interaction.guild.name}**!",
            color=0xFF6666,
        )

        embed.add_field(
            name="Reason", value=f"{moderation_json['rules'][reason]}", inline=False
        )

        embed.add_field(
            name="Think we've made a mistake?",
            value="[Appeal for a ban!](https://discord.gg/SpMhwZcsHs)",
            inline=False,
        )

        embed.set_footer(text=user, icon_url=user.display_avatar.url)

        await user.send(embed=embed)
        await interaction.guild.ban(
            user,
            reason=moderation_json["rules"][reason],
        )
        await interaction.response.send_message(
            f"{user.mention} has been banned from **{interaction.guild.name}**!"
        )

        embed = discord.Embed(
            timestamp=interaction.created_at,
            description=f"{user.mention} has been banned.",
            color=0xFF6666,
        )

        embed.set_author(name=user, icon_url=user.display_avatar.url)

        embed.add_field(name="User ID", value=user.id, inline=False)

        embed.add_field(name="Banned by", value=interaction.user.mention, inline=False)

        embed.add_field(
            name="Reason", value=moderation_json["rules"][reason], inline=False
        )
        proof = await proof.to_file()

        await log.send(file=proof, embed=embed)

        if str(user.id) in moderation_json["history"]:
            del moderation_json["history"][str(user.id)]

        dump_moderation_json(moderation_json)

    @app_commands.command(description="Timeout a user!")
    @commands.has_permissions(moderate_members=True)
    @app_commands.choices(
        unit=[
            Choice(name="Seconds", value="seconds"),
            Choice(name="Minutes", value="minutes"),
            Choice(name="Hours", value="hours"),
            Choice(name="Days", value="days"),
            Choice(name="Weeks", value="weeks"),
        ],
        reason=[
            Choice(name=item, value=count)
            for count, item in enumerate(moderation_json["rules"])
        ],
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        user: discord.Member | discord.User,
        amount: int,
        unit: str,
        reason: int,
        proof: discord.Attachment,
    ):
        if user.is_timed_out():
            return await interaction.response.send_message(
                "This user is already timed out!"
            )

        until = datetime.datetime.now()

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
        try:
            await user.timeout(until, reason=reason)
        except:
            return await interaction.response.send_message(
                "Unable to timeout user. Make sure you formatted the command correctly and the time is less than 28 days, and try again."
            )
        else:
            log = interaction.guild.get_channel(moderation_json["log_channel"])
            embed = discord.Embed(
                timestamp=interaction.created_at,
                description=f"{user.mention} has been put in timeout.",
                color=0xFF6666,
            )
            embed.set_author(name=user, icon_url=user.display_avatar.url)

            embed.add_field(name="User ID", value=user.id, inline=False)

            embed.add_field(
                name="Put in timeout by", value=interaction.user.mention, inline=False
            )
            embed.add_field(name="Reason", value=reason, inline=False)

            proof = await proof.to_file()
            await log.send(file=proof, embed=embed)
            log = interaction.guild.get_channel(moderation_json["log_channel"])
            embed = discord.Embed(
                timestamp=interaction.created_at,
                description=f"You have been put in timeout.",
                color=0xFF6666,
            )
            embed.set_author(name=user, icon_url=user.display_avatar.url)

            embed.add_field(name="Reason", value=reason, inline=False)

            embed.add_field(
                name="Put in timeout by", value=interaction.user.mention, inline=False
            )

            await user.send(embed=embed)
            await interaction.response.send_message(
                "The user has been put in timeout successfully!"
            )

    @app_commands.command(description="Remove timeout from a user!")
    @commands.has_permissions(moderate_members=True)
    async def timeout(
        self, interaction: discord.Interaction, user: discord.Member | discord.User
    ):
        if not user.is_timed_out():
            return await interaction.response.send_message(
                "This user is not already timed out!"
            )

        await user.timeout(None, reason=f"Removed timeout by {interaction.user.name}")
        log = interaction.guild.get_channel(moderation_json["log_channel"])
        embed = discord.Embed(
            timestamp=interaction.created_at,
            description=f"{user.mention} has been taken out of timeout.",
            color=0xFF6666,
        )
        embed.set_author(name=user, icon_url=user.display_avatar.url)

        embed.add_field(name="User ID", value=user.id, inline=False)

        embed.add_field(
            name="Removed timeout by", value=interaction.user.mention, inline=False
        )

        await log.send(embed=embed)
        log = interaction.guild.get_channel(moderation_json["log_channel"])
        embed = discord.Embed(
            timestamp=interaction.created_at,
            description=f"You have been removed from timeout.",
            color=0xFF6666,
        )
        embed.set_author(name=user, icon_url=user.display_avatar.url)

        embed.add_field(
            name="Removed from timeout by", value=interaction.user.mention, inline=False
        )

        await user.send(embed=embed)
        await interaction.response.send_message(
            "The user has been removed from timeout successfully!"
        )

    @app_commands.command(description="Unban a user from the server!")
    @commands.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: discord.User):
        try:
            if moderation_json["log_channel"] is None:
                return await interaction.response.send_message(
                    "The log channel has not been set up."
                )
            log = interaction.guild.get_channel(moderation_json["log_channel"])
            if log is None:
                return await interaction.response.send_message(
                    "The log channel was not found! Make sure the channel exists and I have access to it!"
                )

            await interaction.guild.fetch_ban(user)
            await interaction.guild.unban(user)
            try:
                await user.send(
                    f"You've been unbanned from **{interaction.guild.name}**!"
                )
            except:
                pass
            await interaction.response.send_message(
                "The user has been unbanned from the server!"
            )
            embed = discord.Embed(
                timestamp=interaction.created_at,
                description=f"{user.mention} has been unbanned.",
                color=0xFF6666,
            )
            embed.set_author(name=user, icon_url=user.display_avatar.url)

            embed.add_field(name="User ID", value=user.id, inline=False)

            embed.add_field(
                name="Unbanned by", value=interaction.user.mention, inline=False
            )

            await log.send(embed=embed)

        except discord.NotFound:
            return await interaction.response.send_message(
                f"{user.mention} is not banned!"
            )

    @app_commands.command(description="Warn a user!")
    @commands.has_permissions(manage_roles=True)
    @app_commands.choices(
        reason=[
            Choice(name=item, value=count)
            for count, item in enumerate(moderation_json["rules"])
        ]
    )
    async def warn(
        self,
        interaction: discord.Interaction,
        user: typing.Union[discord.Member, discord.User],
        reason: int,
        proof: discord.Attachment,
    ):
        if moderation_json["log_channel"] is None:
            return await interaction.response.send_message(
                "The log channel has not been set up."
            )

        log = interaction.guild.get_channel(moderation_json["log_channel"])
        if log is None:
            return await interaction.response.send_message(
                "The log channel was not found! Make sure the channel exists and I have access to it!"
            )
        try:
            moderation_json["history"][str(user.id)].append(
                {
                    "reason": reason,
                    "created": interaction.created_at,
                    "warned_by": interaction.user.id,
                }
            )

        except KeyError:
            moderation_json["history"][str(user.id)] = [
                {
                    "reason": reason,
                    "created": interaction.created_at,
                    "warned_by": interaction.user.id,
                }
            ]

        warn_embed = discord.Embed(
            description=f"You've been warned in **{interaction.guild.name}**!",
            color=0xFF6666,
        )

        warn_embed.add_field(name="Reason", value=f"{reason}", inline=False)

        warn_embed.set_footer(text=user, icon_url=user.display_avatar.url)

        await user.send(embed=embed)

        await interaction.response.send_message(
            f'`{user}` has been warned. They now have `{len(moderation_json["history"][str(user.id)])}` warnings!'
        )

        embed = discord.Embed(
            description=f"{user.mention} has been warned! They now have `{len(moderation_json['history'][str(user.id)])}` warnings!",
            color=0xFF6666,
        )

        embed.set_author(name=user, icon_url=user.display_avatar.url)

        embed.add_field(name="User ID", value=f"{user.id}", inline=False)

        embed.add_field(
            name="Warned by", value=f"{interaction.user.mention}", inline=False
        )

        embed.add_field(name="Warn reason", value=f"{reason}", inline=False)

        embed.timestamp = interaction.created_at
        proof = await proof.to_file()

        await log.send(file=proof, embed=embed)
        dump_moderation_json(moderation_json)

    @app_commands.command(description="Access your or a user's moderation history!")
    @commands.has_permissions(manage_messages=True)
    async def history(
        self,
        interaction: discord.Interaction,
        user: typing.Union[discord.Member, discord.User] = None,
    ):
        warns = 0
        try:
            warns = len(
                moderation_json["history"][
                    str(user.id) if user is not None else str(interaction.user.id)
                ]
            )
        except KeyError:
            pass

        embed = discord.Embed(
            description=f"{user.mention} has **{warns}** warnings!", color=0xFF6666
        )

        embed.set_author(name=user, icon_url=user.display_avatar.url)

        embed.timestamp = interaction.created_at

        embed.set_footer(text="\u200b")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        description="Mute users!",
    )
    @app_commands.choices(
        unit=[
            Choice(name="Seconds", value="seconds"),
            Choice(name="Minutes", value="minutes"),
            Choice(name="Hours", value="hours"),
            Choice(name="Days", value="days"),
            Choice(name="Weeks", value="weeks"),
        ],
        reason=[
            Choice(name=item, value=count)
            for count, item in enumerate(moderation_json["rules"])
        ],
    )
    @commands.has_permissions(manage_roles=True)
    async def mute(
        self,
        interaction: discord.Interaction,
        user: discord.Member,
        time: float,
        unit: str,
        reason: int,
        proof: discord.Attachment,
    ):
        if moderation_json["log_channel"] is None:
            return await interaction.response.send_message(
                "The log channel has not been set up."
            )

        if moderation_json["mute_role"] is None:
            return await interaction.response.send_message(
                "The mute role has not been set up."
            )
        mute_role = interaction.guild.get_role(moderation_json["mute_role"])

        log = interaction.guild.get_channel(moderation_json["log_channel"])
        if log is None:
            return await interaction.response.send_message(
                "The log channel was not found! Make sure the channel exists and I have access to it!"
            )
        total_time = 0
        if unit == "seconds":
            total_time = time

        if unit == "minutes":
            total_time = time * 60

        if unit == "hours":
            total_time = time * 3600

        if unit == "days":
            total_time = time * 86400

        if unit == "weeks":
            total_time = time * 604800

        if mute_role in user.roles:
            return await interaction.response.send_message(
                f"{user.mention} is already muted!"
            )

        await user.add_roles(mute_role, reason=reason)
        embed = discord.Embed(
            description=f"You have been muted in **{interaction.guild.name}**!",
            color=0xFF6666,
        )
        embed.set_author(name=user, icon_url=user.display_avatar.url)
        embed.add_field(name="Reason", value=f"{reason}", inline=False)
        embed.timestamp = interaction.created_at

        await user.send(embed=embed)

        moderation_json["muted"].append(user.id)

        try:
            moderation_json["history"][str(user.id)].append(
                {
                    "reason": reason,
                    "created": interaction.created_at,
                    "warned_by": interaction.user.id,
                }
            )

        except KeyError:
            moderation_json["history"][str(user.id)] = [
                {
                    "reason": reason,
                    "created": interaction.created_at,
                    "warned_by": interaction.user.id,
                }
            ]

        embed = discord.Embed(
            description=f"{user.mention} has been muted!", color=0xFF6666
        )

        embed.set_author(name=user, icon_url=user.display_avatar.url)

        embed.add_field(name="User ID", value=f"{user.id}", inline=False)

        embed.add_field(name="Muted by", value=f"{interaction.user}", inline=False)

        embed.add_field(name="Mute reason", value=f"{reason}", inline=False)

        embed.timestamp = interaction.created_at
        proof = await proof.to_file()

        await log.send(file=proof, embed=embed)
        dump_moderation_json(moderation_json)

        await asyncio.sleep(total_time)

        try:
            moderation_json["muted"].remove(user.id)
            await user.remove_roles(mute_role, reason="Time elapsed")
            embed = discord.Embed(
                description=f"You have been unmuted in **{interaction.guild.name}**!",
                color=0xFF6666,
            )
            embed.set_author(name=user, icon_url=user.display_avatar.url)
            embed.add_field(name="Reason", value=f"{reason}", inline=False)
            embed.timestamp = interaction.created_at
            await user.send(embed=embed)

            embed = discord.Embed(
                description=f"{user.mention} has been unmuted!", color=0xFF6666
            )

            embed.set_author(name=user, icon_url=user.display_avatar.url)

            embed.add_field(name="User ID", value=f"{user.id}", inline=False)

            embed.add_field(name="Unmute reason", value=f"Time elapsed", inline=False)

            embed.timestamp = interaction.created_at

            await log.send(embed=embed)
            dump_moderation_json(moderation_json)

        except:
            embed = discord.Embed(
                description=f"Error unmuting {user.mention} ({user.name})!",
                color=0xFF6666,
            )

            embed.set_author(name=user, icon_url=user.display_avatar.url)

            embed.add_field(name="User ID", value=f"{user.id}", inline=False)

            embed.add_field(name="Muted by", value=f"{interaction.user}", inline=False)

            embed.add_field(name="Mute reason", value=f"{reason}", inline=False)

            embed.timestamp = interaction.created_at

            await log.send(embed=embed)

    @app_commands.command(
        description="Unmute users! If no users are provided, unmutes everyone!"
    )
    @commands.has_permissions(manage_roles=True)
    async def unmute(
        self, interaction: discord.Interaction, user: discord.Member = None
    ):
        if moderation_json["mute_role"] is None:
            return await interaction.response.send_message(
                "The mute role has not been set up.`"
            )

        if moderation_json["log_channel"] is None:
            return await interaction.response.send_message(
                "The log channel has not been set up."
            )
        mute_role = interaction.guild.get_role(moderation_json["mute_role"])
        log = interaction.guild.get_channel(moderation_json["log_channel"])

        if log is None:
            return await interaction.response.send_message(
                "The log channel was not found! Make sure the channel exists and I have access to it!"
            )

        if mute_role is None:
            return await interaction.response.send_message(
                "The mute role was not found! Set a new role as the Mute role!"
            )

        failed = 0

        if user is None:
            for user in mute_role.members:
                try:
                    await user.remove_roles(
                        mute_role, reason=f"Unmute by {interaction.user.name}"
                    )
                    embed = discord.Embed(
                        description=f"You have been unmuted in **{interaction.guild.name}**!",
                        color=0xFF6666,
                    )
                    embed.set_author(name=user, icon_url=user.display_avatar.url)
                    embed.add_field(
                        name="Reason",
                        value=f"Unmute by {interaction.user.name}",
                        inline=False,
                    )
                    embed.timestamp = interaction.created_at
                    await user.send(embed=embed)
                    moderation_json["muted"].remove(user.id)
                    embed = discord.Embed(
                        description=f"{user.mention} has been unmuted!", color=0xFF6666
                    )
                    embed.set_author(name=user, icon_url=user.display_avatar.url)
                    embed.add_field(name="User ID", value=f"{user.id}", inline=False)
                    embed.add_field(
                        name="Unmute reason",
                        value=f"Unmute by {interaction.user.name}",
                        inline=False,
                    )
                    embed.timestamp = interaction.created_at
                    await log.send(embed=embed)
                    dump_moderation_json(moderation_json)

                except:
                    embed = discord.Embed(
                        description=f"Error unmuting {user.mention}!", color=0xFF6666
                    )
                    embed.set_author(name=user, icon_url=user.display_avatar.url)
                    embed.add_field(name="User ID", value=f"{user.id}", inline=False)
                    embed.add_field(
                        name="Muted by", value=f"{interaction.user}", inline=False
                    )
                    embed.add_field(
                        name="Mute reason",
                        value=f"Unmute by {interaction.user.name}",
                        inline=False,
                    )
                    embed.timestamp = interaction.created_at
                    await log.send(embed=embed)
                    failed += 1

            return await interaction.response.send_message(
                f"Unmuted **{len(mute_role.members) - failed}/{len(mute_role.members)}** users!"
            )

        failed = 0

        try:
            await user.remove_roles(
                mute_role,
                reason=f"Unmute by {interaction.user.name}",
            )
            embed = discord.Embed(
                description=f"You have been unmuted in **{interaction.guild.name}**!",
                color=0xFF6666,
            )
            embed.set_author(name=user, icon_url=user.display_avatar.url)
            embed.add_field(
                name="Reason", value=f"Unmute by {interaction.user.name}", inline=False
            )
            embed.timestamp = interaction.created_at
            await user.send(embed=embed)
            moderation_json["muted"].remove(user.id)
            embed = discord.Embed(
                description=f"{user.mention} has been unmuted!", color=0xFF6666
            )
            embed.set_author(name=user, icon_url=user.display_avatar.url)
            embed.add_field(name="User ID", value=f"{user.id}", inline=False)
            embed.add_field(
                name="Unmute reason",
                value=f"Unmute by {interaction.user.name}",
                inline=False,
            )
            embed.timestamp = interaction.created_at
            await log.send(embed=embed)
            dump_moderation_json(moderation_json)

        except:
            embed = discord.Embed(
                description=f"Error unmuting {user.mention}!", color=0xFF6666
            )
            embed.set_author(name=user, icon_url=user.display_avatar.url)
            embed.add_field(name="User ID", value=f"{user.id}", inline=False)
            embed.add_field(name="Muted by", value=f"{interaction.user}", inline=False)
            embed.add_field(
                name="Mute reason",
                value=f"Unmute by {interaction.user.name}",
                inline=False,
            )
            embed.timestamp = interaction.created_at
            await log.send(embed=embed)
            return await interaction.response.send_message(
                f"Error unmuting {user.mention}!"
            )

        return await interaction.response.send_message(f"Unmuted {user.mention}!")

    @app_commands.command(description="Purge messages!")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, interaction: discord.Interaction, amount: int):
        await interaction.channel.purge(limit=amount + 1)
        await interaction.response.send_message(f"Purged **{amount}** messages!")

    @app_commands.command(
        description="Set or view the moderation log channel. Requires Manage Channels permission"
    )
    @app_commands.describe(
        channel="The channel to set as the new log channel. If no channel is provided, the current log channel wil be shown"
    )
    @commands.has_permissions(manage_channels=True)
    async def log(
        self, interaction: discord.Interaction, channel: discord.TextChannel | None
    ):
        if channel is None:
            if moderation_json["log_channel"] is None:
                return await interaction.response.send_message(
                    "The log channel has not been set up. Please set up the log channel using the command ``log channel``"
                )
            return await interaction.response.send_message(
                f"The log channel is set to {interaction.guild.get_channel(moderation_json['log_channel']).mention}"
            )

        moderation_json["log_channel"] = channel.id
        dump_moderation_json(moderation_json)

        await interaction.response.send_message(
            f"The log channel has been set to {channel.mention}", ephemeral=True
        )

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.id in moderation_json["muted"]:
            await member.add_roles(member.guild.get_role(moderation_json["mute_role"]))
            embed = discord.Embed(
                description=f"{member.mention} has been auto-muted!", color=0xFF6666
            )
            embed.set_author(name=member, icon_url=member.display_avatar.url)
            embed.add_field(name="User ID", value=f"{member.id}", inline=False)
            embed.add_field(name="Muted by", value=f"Re-join to server", inline=False)
            embed.timestamp = datetime.datetime.now()
            await member.guild.get_channel(moderation_json["log_channel"]).send(
                embed=embed
            )

    async def cog_app_command_error(
        self, interaction: Interaction, error: AppCommandError
    ):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message(
                "You do not have permission to use this command.",
                ephemeral=True,
            )

        if isinstance(error, discord.Forbidden):
            await interaction.response.send_message(
                "You do not have permission to use this command.",
                ephemeral=True,
            )

        if isinstance(error, commands.BadArgument):
            await interaction.response.send_message(
                "The user you provided was invalid!"
            )
        else:
            traceback.print_exc()


async def setup(bot):
    """Load the Moderation cog."""
    await bot.add_cog(Moderation(bot))
