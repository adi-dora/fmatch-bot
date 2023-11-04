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
from verification_utils import verification_json, dump_verification_json


class DeniedModal(discord.ui.Modal):
    def __init__(self, message: discord.Message):
        super().__init__(title="Denied Reason", timeout=300, custom_id="denied_modal")
        self.message = message

        self.reason = discord.ui.TextInput(label="Reason Denied", min_length=5)
        self.add_item(self.reason)

    async def on_submit(self, interaction: Interaction):
        try:
            user = interaction.guild.get_member(
                verification_json["verifications"][str(self.message.id)]["user"]
            )
            await interaction.response.send_message(
                f"{user.mention} has been denied for the reason: ``{self.reason.value}``"
            )
            await user.send(
                embed=discord.Embed(
                    title="Verification Denied",
                    color=discord.Color.red(),
                    timestamp=interaction.created_at,
                )
                .add_field(name="Reason", value=self.reason.value)
                .set_footer(text="Reapply for verification by running /verify!")
            )
            del verification_json["verifications"][str(self.message.id)]
            dump_verification_json(verification_json)
            await self.message.edit(view=discord.ui.View())
        except:
            traceback.print_exc()


class MutedModal(discord.ui.Modal):
    def __init__(self, message: discord.Message):
        super().__init__(title="Muted Reason", timeout=300, custom_id="muted_modal")
        self.message = message

        self.reason = discord.ui.TextInput(label="Reason Muted", min_length=5)
        self.add_item(self.reason)

    async def on_submit(self, interaction: Interaction):
        try:
            with open('moderation.json', 'r') as f:
                mod = json.load(f)
            user = interaction.guild.get_member(
                verification_json["verifications"][str(self.message.id)]["user"]
            )
            mute_role = interaction.guild.get_role(mod['mute_role'])

            talk_role = interaction.guild.get_role(verification_json['talking_role'])

            await user.remove_roles(talk_role, reason=f'Muted for Verification Request')            
            await user.add_roles(mute_role, reason=f'Muted for Verification Request')
            await interaction.response.send_message(
                f"{user.mention} has been muted for the reason: ``{self.reason.value}``"
            )
            await user.send(
                embed=discord.Embed(
                    title="Muted for Verification Request",
                    color=discord.Color.red(),
                    timestamp=interaction.created_at,
                )
                .add_field(name="Reason", value=self.reason.value)
                .set_footer(text="Reapply for verification by running /verify!")
            )
            
        except:
            traceback.print_exc()




class VerificationView(discord.ui.View):
    def __init__(
        self,
    ):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Gender Verified",
        custom_id="gender_button",
        style=discord.ButtonStyle.green,
    )
    async def gender_verified_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        # TODO: Get gender data then verify gender
        await interaction.response.send_message("Not yet implemented; need gender data")

    @discord.ui.button(label="18+ Verified", custom_id="age_button")
    async def age_verified_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        try:
            adult_role = interaction.guild.get_role(
                verification_json["18_verified_role"]
            )
            user = interaction.guild.get_member(
                verification_json["verifications"][str(interaction.message.id)]["user"]
            )

            await user.add_roles(adult_role)
            await user.send(
                embed=discord.Embed(
                    title="Verification Accepted",
                    description="Your age and gender have been verified",
                    color=discord.Color.green(),
                    timestamp=interaction.created_at,
                )
            )
            del verification_json["verifications"][str(interaction.message.id)]
            dump_verification_json(verification_json)
            await interaction.response.send_message(
                "The user has been successfully age verified"
            )
            await interaction.message.edit(view=discord.ui.View())

        except KeyError:
            await interaction.response.send_message(
                "There was an error with this verification request! Please ask the user to resubmit."
            )
            await interaction.message.edit(view=discord.ui.View())

    @discord.ui.button(label="Denied", custom_id="denied_button")
    async def denied_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        modal = DeniedModal(interaction.message)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="Mute user", custom_id="mute_button")
    async def mute_button(
        self, interaction: discord.Interaction, button: discord.Button
    ):
        print("mute")


class Verification(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        for verification in verification_json["verifications"]:
            self.bot.add_view(VerificationView(), message_id=int(verification))

        print("added current verifications")

    @app_commands.command()
    @app_commands.choices(
        verification_type=[
            Choice(name="Gender Verified", value="gender"),
            Choice(name="Age Verified", value="age")
        ]
    )
    async def verify(
        self,
        interaction: discord.Interaction,
        verification_type: str,
        pose: discord.Attachment | None,
        id: discord.Attachment | None,
    ):
        if verification_type == 'age' and (pose is None or id is None):
            return await interaction.response.send_message('You must provide a pose and an ID to verify both gender and age!', ephemeral=True)
        
        if verification_type == 'gender' and pose is None:
            return await interaction.response.send_message('You must provide a pose to verify your gender!', ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        try:
            chan = interaction.guild.get_channel(
                verification_json["verification_channel"]
            )
            files = []
            pose = await pose.to_file()
            if verification_type == 'age':
                id = await id.to_file()
                files.append(id)
            files.append(pose)
            roles = [
                interaction.guild.get_role(role)
                for role in verification_json["staff_roles"]
            ]

            embed = (
                discord.Embed(
                    title="New Verification Request", timestamp=interaction.created_at
                )
                .add_field(name="User", value=f"{interaction.user.mention}")
                .set_author(
                    name=f"{interaction.user.name}",
                    icon_url=interaction.user.avatar.url,
                )
            )
            if verification_type == 'age':
                embed.set_image(url=f"attachment://{id.filename}").set_thumbnail(
                    url=f"attachment://{pose.filename}"
                )
            else:
                embed.set_image(url=f"attachment://{pose.filename}")
            m = await chan.send(
                " ".join(role.mention for role in roles),
                embed=embed,
                view=VerificationView(),
                files=files,
            )
            verification_json["verifications"][str(m.id)] = {
                "user": interaction.user.id
            }
            dump_verification_json(verification_json)
            await interaction.followup.send("Successfully sent verification request")
        except:
            traceback.print_exc()


async def setup(bot):
    await bot.add_cog(Verification(bot))
