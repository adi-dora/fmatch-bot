import json
import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import datetime as dt
import asyncio
import traceback


from discord import app_commands
from utils.profile_utils import *
from utils.verification_utils import *
from utils.match_utils import *


class DecideMatchView(discord.ui.View):
    users = {}
    matches = []

    def __init__(self, current_user: discord.Member, matched_user: discord.Member):
        super().__init__(timeout=600)
        self.matched_user = matched_user
        self.current_user = current_user
        DecideMatchView.users[self.current_user.id] = self

    @discord.ui.button(label="Accept Match", style=discord.ButtonStyle.green)
    async def accept_match_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        await interaction.message.edit(view=discord.ui.View())
        DecideMatchView.matches.append(interaction.user.id)
        await self.matched_user.send(
            embed=discord.Embed(
                title="Match Accepted",
                description=f"{interaction.user.mention} ({interaction.user.name}) has accepted the match request.",
                color=discord.Color.green(),
                timestamp=interaction.created_at,
            )
        )
        await interaction.response.send_message("You have accepted the match request.")
        if self.matched_user.id in DecideMatchView.matches:
            new_chan = await self.matched_user.guild.create_text_channel(
                f"match-{interaction.user.name}-{self.matched_user.name}",
                category=self.matched_user.guild.get_channel(
                    match_json["matchmaking_category"]
                ),
                reason="New match created",
            )
            overrides = new_chan.overwrites
            overrides[self.current_user] = discord.PermissionOverwrite(
                read_messages=True
            )
            overrides[self.matched_user] = discord.PermissionOverwrite(
                read_messages=True
            )
            await new_chan.edit(
                overwrites=overrides, reason="Give access to matched users"
            )
            await self.current_user.remove_roles(
                self.matched_user.guild.get_role(match_json["matchmaking_role"]),
                reason="Match found",
            )
            await self.matched_user.remove_roles(
                self.matched_user.guild.get_role(match_json["matchmaking_role"]),
                reason="Match found",
            )

            del DecideMatchView.users[self.matched_user.id]
            del DecideMatchView.users[interaction.user.id]
            DecideMatchView.matches.remove(interaction.user.id)
            DecideMatchView.matches.remove(self.matched_user.id)

            await new_chan.send(
                f"{self.current_user.mention} {self.matched_user.mention} you have matched with each other! You have ten minutes to mingle before this channel is deleted!"
            )
            for i in range(1, 11):
                await asyncio.sleep(60)
                await new_chan.send(f"{10 - i} minutes remaining!")

            await new_chan.delete(reason="10 minutes elapsed since match")

    @discord.ui.button(label="Reject Match", style=discord.ButtonStyle.red)
    async def reject_match_btn(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        try:
            if self.matched_user.id in DecideMatchView.users:
                DecideMatchView.users[self.matched_user.id].stop()
                del DecideMatchView.users[self.matched_user.id]
            if self.matched_user.id in DecideMatchView.matches:
                DecideMatchView.matches.remove(self.matched_user.id)

            await interaction.message.edit(view=discord.ui.View())

            if (
                self.current_user.guild.get_role(verification_json["male_role"])
                in self.current_user.roles
                or self.current_user.guild.get_role(verification_json["trans_m_role"])
                in self.current_user.roles
            ):
                if (
                    self.current_user.guild.get_role(match_json["male_pref_role"])
                    in self.current_user.roles
                ):
                    match_json["m_pref_m_queue"].append(str(interaction.user.id))
                else:
                    match_json["m_pref_f_queue"].append(str(interaction.user.id))
            else:
                if (
                    self.current_user.guild.get_role(match_json["male_pref_role"])
                    in self.current_user.roles
                ):
                    match_json["f_pref_m_queue"].append(str(interaction.user.id))
                else:
                    match_json["f_pref_f_queue"].append(str(interaction.user.id))

            match_json["general_queue"].append(str(interaction.user.id))

            if (
                self.matched_user.guild.get_role(verification_json["male_role"])
                in self.matched_user.roles
                or self.matched_user.guild.get_role(verification_json["trans_m_role"])
                in self.matched_user.roles
            ):
                if (
                    self.matched_user.guild.get_role(match_json["male_pref_role"])
                    in self.matched_user.roles
                ):
                    match_json["m_pref_m_queue"].append(str(self.matched_user.id))
                else:
                    match_json["m_pref_f_queue"].append(str(self.matched_user.id))
            else:
                if (
                    self.matched_user.guild.get_role(match_json["male_pref_role"])
                    in self.matched_user.roles
                ):
                    match_json["f_pref_m_queue"].append(str(self.matched_user.id))
                else:
                    match_json["f_pref_f_queue"].append(str(self.matched_user.id))

            match_json["general_queue"].append(str(self.matched_user.id))
            dump_match_json(match_json)
            await interaction.response.send_message(
                "You have rejected the match! You have been re-added to the queue successfully!"
            )
            await self.matched_user.send(
                "Your partner has rejected the match! You have been re-added to the queue successfully!"
            )
        except:
            traceback.print_exc()

    async def on_timeout(self) -> None:
        if (
            str(self.current_user.id) in match_json["general_queue"]
            and str(self.matched_user.id) in match_json["general_queue"]
        ):
            return
        if self.current_user.id in DecideMatchView.users:
            del DecideMatchView.users[self.current_user.id]
        if self.matched_user.id in DecideMatchView.users:
            del DecideMatchView.users[self.matched_user.id]

        if self.current_user.id in DecideMatchView.matches:
            DecideMatchView.matches.remove(self.current_user.id)
        if self.matched_user.id in DecideMatchView.matches:
            DecideMatchView.matches.remove(self.matched_user.id)

        if (
            self.current_user.guild.get_role(verification_json["male_role"])
            in self.current_user.roles
            or self.current_user.guild.get_role(verification_json["trans_m_role"])
            in self.current_user.roles
        ):
            if (
                self.current_user.guild.get_role(match_json["male_pref_role"])
                in self.current_user.roles
            ):
                match_json["m_pref_m_queue"].append(str(self.current_user.id))
            else:
                match_json["m_pref_f_queue"].append(str(self.current_user.id))
        else:
            if (
                self.current_user.guild.get_role(match_json["male_pref_role"])
                in self.current_user.roles
            ):
                match_json["f_pref_m_queue"].append(str(self.current_user.id))
            else:
                match_json["f_pref_f_queue"].append(str(self.current_user.id))

        match_json["general_queue"].append(str(self.current_user.id))

        if (
            self.matched_user.guild.get_role(verification_json["male_role"])
            in self.matched_user.roles
            or self.matched_user.guild.get_role(verification_json["trans_m_role"])
            in self.matched_user.roles
        ):
            if (
                self.matched_user.guild.get_role(match_json["male_pref_role"])
                in self.matched_user.roles
            ):
                match_json["m_pref_m_queue"].append(str(self.matched_user.id))
            else:
                match_json["m_pref_f_queue"].append(str(self.matched_user.id))
        else:
            if (
                self.matched_user.guild.get_role(match_json["male_pref_role"])
                in self.matched_user.roles
            ):
                match_json["f_pref_m_queue"].append(str(self.matched_user.id))
            else:
                match_json["f_pref_f_queue"].append(str(self.matched_user.id))

        match_json["general_queue"].append(str(self.matched_user.id))

        dump_match_json(match_json)
        await self.current_user.send(
            "You or your match did not respond in time! You have been re-added to the queue!"
        )
        await self.matched_user.send(
            "You or your match did not respond in time! You have been re-added to the queue!"
        )


class MatchView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Enter Queue", custom_id="enter_queue_btn", emoji="\U00002764"
    )
    async def enter_queue_btn(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        try:
            if str(interaction.user.id) not in profile_json["profiles"]:
                return await interaction.response.send_message(
                    "You do not have a profile! Please create one before you can enter the queue!",
                    ephemeral=True,
                    delete_after=300,
                )

            if str(interaction.user.id) in match_json["general_queue"]:
                return await interaction.response.send_message(
                    "You are already in the queue!", ephemeral=True, delete_after=300
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

            match_json["general_queue"].append(str(interaction.user.id))

            dump_match_json(match_json)
            await interaction.user.add_roles(
                interaction.guild.get_role(match_json["matchmaking_role"]),
                reason="User entered matchmaking queue",
            )
            await interaction.response.send_message(
                "You have been added to the matchmaking queue successfully!",
                ephemeral=True,
                delete_after=300,
            )
        except:
            traceback.print_exc()

    @discord.ui.button(
        label="Leave Queue", custom_id="leave_queue_btn", emoji="\U0001f494"
    )
    async def leave_queue(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        try:
            match_json["general_queue"].remove(str(interaction.user.id))

        except ValueError:
            return await interaction.response.send_message(
                "You are not currently in the queue!", ephemeral=True, delete_after=300
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
                print("removed user")
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
            "You have been removed from the queue successfully!",
            ephemeral=True,
            delete_after=300,
        )


class Match(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(MatchView(), message_id=match_json["match_view_id"])
        # self.create_matches_loop.start()

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def matchmessage(self, interaction: discord.Interaction, msg: str | None):
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

    @app_commands.command()
    @app_commands.checks.has_permissions(manage_channels=True)
    async def matchchannel(
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

    @app_commands.command()
    async def creatematch(self, interaction: discord.Interaction):
        chan = interaction.guild.get_channel(match_json["send_match_channel"])
        m = await chan.send(match_json["message"], view=MatchView())

        match_json["match_view_id"] = m.id
        dump_match_json(match_json)

    # @tasks.loop(minutes=2)
    @app_commands.command()
    async def create_matches_loop(self, interaction: discord.Interaction):
        await interaction.response.send_message("running loop", ephemeral=True)
        try:
            guild = self.bot.get_guild(match_json["server_id"])
            general_queue = match_json["general_queue"].copy()
            for user in general_queue:
                if user not in match_json["general_queue"]:
                    continue
                user = guild.get_member(int(user))
                if (
                    guild.get_role(verification_json["male_role"]) in user.roles
                    or guild.get_role(verification_json["trans_m_role"]) in user.roles
                ):
                    if guild.get_role(match_json["male_pref_role"]) in user.roles:
                        matched_user = self.get_match(guild, user, "m_pref_m")
                        user_pref = "m_pref_m"
                    else:
                        matched_user = self.get_match(guild, user, "f_pref_m")
                        user_pref = "m_pref_f"
                else:
                    if guild.get_role(match_json["male_pref_role"]) in user.roles:
                        matched_user = self.get_match(guild, user, "m_pref_f")
                        user_pref = "f_pref_m"
                    else:
                        matched_user = self.get_match(guild, user, "f_pref_f")
                        user_pref = "f_pref_f"

                if matched_user is not None:
                    match_json["general_queue"].remove(str(user.id))
                    match_json[user_pref + "_queue"].remove(str(user.id))
                    await user.send(
                        embed=discord.Embed(
                            title="Match Found!",
                            description=f"You have been successfully matched with {matched_user.mention} ({matched_user.name})",
                            color=discord.Color.pink(),
                            timestamp=dt.now(),
                        ).set_footer(
                            text="You have 10 minutes before this request times out and you are re-added to the queue"
                        )
                    )
                    file = discord.utils.MISSING
                    if "selfie" in profile_json["profiles"][str(matched_user.id)]:
                        file = get_selfie(matched_user)
                    await user.send(
                        embed=create_profile_embed(matched_user)[0],
                        view=DecideMatchView(user, matched_user),
                        file=file,
                    )

                    await matched_user.send(
                        embed=discord.Embed(
                            title="Match Found!",
                            description=f"You have been successfully matched with {user.mention} ({user.name})",
                            color=discord.Color.pink(),
                            timestamp=dt.now(),
                        ).set_footer(
                            text="You have 10 minutes before this request times out and you are re-added to the queue"
                        )
                    )

                    file = discord.utils.MISSING
                    if "selfie" in profile_json["profiles"][str(user.id)]:
                        file = get_selfie(user)
                    await matched_user.send(
                        embed=create_profile_embed(user)[0],
                        view=DecideMatchView(matched_user, user),
                        file=file,
                    )
                    dump_match_json(match_json)
        except:
            traceback.print_exc()

    def get_match(
        self, guild: discord.Guild, current_user: discord.Member, pref: str
    ) -> discord.Member | None:
        for user in match_json[pref + "_queue"]:
            user = guild.get_member(int(user))
            if user == current_user:
                continue
            if user.status != discord.Status.offline:
                match_json["general_queue"].remove(str(user.id))
                match_json[pref + "_queue"].remove(str(user.id))
                dump_match_json(match_json)

                return user
        return None


async def setup(bot: commands.Bot):
    await bot.add_cog(Match(bot))
