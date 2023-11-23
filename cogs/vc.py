import json
import traceback
import discord
from discord.ext import commands


from discord import app_commands
from datetime import datetime as dt


class DeleteVcConfirmation(discord.ui.View):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        with open("vc.json", "r") as f:
            vc = json.load(f)
        channel = interaction.guild.get_channel(self.channel["id"])
        vc["channels"].remove(self.channel)
        await channel.delete(reason=f"Private VC deleted by {interaction.user.name}")
        with open("vc.json", "w") as f:
            json.dump(vc, f)

        await interaction.message.delete()
        return await interaction.response.send_message(
            "Your channel has been deleted!", ephemeral=True
        )

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def decline(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.send_message("Request Cancelled!", ephemeral=True)
        await interaction.message.delete()


class VC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        with open("vc.json", "r") as f:
            vc = json.load(f)

        if before.guild.get_role(vc["role"]) not in after.roles:
            for channel in vc["channels"]:
                if channel["owner"] == after.id:
                    channel = before.guild.get_channel(channel["id"])
                    await channel.delete(reason="Lost required role")

    vc = app_commands.Group(
        name="vc", description="Manage your own private Voice Channels!"
    )

    @vc.command(
        description="Shows help and informtion about how to create and manage private VCs!"
    )
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Claim and manage your private VC!", color=0xFF6666)

        embed.description = "Claim a private VC of your own!"
        embed.set_author(
            name=interaction.user, icon_url=interaction.user.display_avatar.url
        )
        embed.add_field(name="/vc claim", value="Claim a Private VC!", inline=False)
        embed.add_field(name="/vc edit", value="Edit your VC name!", inline=False)

        embed.add_field(name="/vc delete", value="Unclaim your VC!", inline=False)

        embed.add_field(
            name="/vc users",
            value="Check which users have permissions to join your VC!",
            inline=False,
        )

        embed.add_field(name="/add", value="Add a user to your VC!", inline=False)

        embed.add_field(
            name="/remove", value="Remove a user from your VC!", inline=False
        )

        embed.timestamp = dt.utcnow()

        await interaction.response.send_message(embed=embed)

    @vc.command(description="Create a new private VC!")
    async def claim(self, interaction: discord.Interaction, channel_name: str):
        with open("vc.json", "r") as f:
            vc = json.load(f)

        role = interaction.guild.get_role(vc["role"])

        if role is not None:
            if not interaction.user._roles.has(vc["role"]):
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Missing Role",
                        description=f"You need the {role.mention} role to use this command!",
                        color=discord.Color.red(),
                    ),
                    ephemeral=True,
                )

        category = interaction.guild.get_channel(vc["category"])
        if category is None:
            return await interaction.response.send_message(
                "The category was not found! Make sure it exists and I have access to it!"
            )

        for chan in vc["channels"]:
            if (
                interaction.user.id == chan["owner"]
                or interaction.user.id in chan["users"]
            ):
                vc_chan = interaction.guild.get_channel(chan["id"])
                return await interaction.response.send_message(
                    f"You are already a part of another private VC! {vc_chan.jump_url}",
                    ephemeral=True,
                )

        channel = await interaction.guild.create_voice_channel(
            channel_name,
            reason=f"New private VC created by {interaction.user.name}",
            category=category,
            overwrites={
                interaction.guild.default_role: discord.PermissionOverwrite(
                    view_channel=False, connect=False, speak=False, stream=False
                ),
                interaction.guild.me: discord.PermissionOverwrite(
                    view_channel=True, connect=True, speak=True, stream=True
                ),
                interaction.user: discord.PermissionOverwrite(
                    view_channel=True, connect=True, speak=True, stream=True
                ),
            },
        )

        vc["channels"].append(
            {"owner": interaction.user.id, "id": channel.id, "users": []}
        )

        with open("vc.json", "w") as f:
            json.dump(vc, f)

        await interaction.response.send_message(
            f"Your channel has been created! {channel.jump_url}", ephemeral=True
        )

    @vc.command(
        description="Set the category into which your VC channels will be created!"
    )
    @commands.has_permissions(administrator=True)
    async def category(
        self, interaction: discord.Interaction, category: discord.CategoryChannel
    ):
        with open("vc.json", "r") as f:
            vc = json.load(f)

        channel = interaction.guild.get_channel(category.id)

        if channel is None:
            return await interaction.response.send_message(
                "The category was not found! Make sure it exists and I have access to it!"
            )

        vc["category"] = category.id

        with open("vc.json", "w") as f:
            json.dump(vc, f)

        await interaction.response.send_message(
            f"The category for VC channels has been set to {category.mention}",
            ephemeral=True,
        )

    @vc.command(
        description="Set the role that's required to claim and manage Voice Channels"
    )
    @commands.has_permissions(
        manage_roles=True, manage_channels=True, manage_guild=True
    )
    async def role(self, interaction: discord.Interaction, role: discord.Role | None):
        try:
            with open("vc.json", "r") as f:
                vc = json.load(f)

            if role is None:
                if vc["role"] is None:
                    return await interaction.response.send_message(
                        embed=discord.Embed(
                            title="Current VC Role",
                            description=f"The current VC role is: None",
                            color=discord.Color.blue(),
                            timestamp=interaction.created_at,
                        ),
                        ephemeral=True,
                    )

                vc_role = interaction.guild.get_role(vc["role"])
                return await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Current VC Role",
                        description=f"The current VC role is: {vc_role.mention}",
                        color=discord.Color.blue(),
                        timestamp=interaction.created_at,
                    ),
                    ephemeral=True,
                )

            vc["role"] = role.id
            with open("vc.json", "w") as f:
                json.dump(vc, f)

            await interaction.response.send_message(
                embed=discord.Embed(
                    title="Success",
                    description=f"The required role to create private VCs is now {role.mention}",
                    color=discord.Color.green(),
                    timestamp=interaction.created_at,
                ),
                ephemeral=True,
            )
        except:
            traceback.print_exc()

    @vc.command(description="Edit the name of your private VC!")
    async def edit(self, interaction: discord.Interaction, new_name: str):
        with open("vc.json", "r") as f:
            vc = json.load(f)

        for chan in vc["channels"]:
            if chan["owner"] == interaction.user.id:
                channel = interaction.guild.get_channel(chan["id"])
                await channel.edit(
                    name=new_name,
                    reason=f"Edited Private VC by {interaction.user.display_name}",
                )
                return await interaction.response.send_message(
                    "Your Voice channel has been updated!", ephemeral=True
                )

        return await interaction.response.send_message(
            "You do not own any private VCs!", ephemeral=True
        )

    @vc.command(description="Delete your private VC!")
    async def delete(self, interaction: discord.Interaction):
        with open("vc.json", "r") as f:
            vc = json.load(f)

        for chan in vc["channels"]:
            if chan["owner"] == interaction.user.id:
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Confirmation Required",
                        description=f"Are you sure you want to delete your VC?",
                        color=discord.Color.orange(),
                        timestamp=interaction.created_at,
                    ),
                    view=DeleteVcConfirmation(chan),
                )

    @vc.command(description="Add a user to your private VC!")
    async def add(self, interaction: discord.Interaction, user: discord.Member):
        with open("vc.json", "r") as f:
            vc = json.load(f)

        for chan in vc["channels"]:
            if chan["owner"] == interaction.user.id:
                if user.id in chan["users"]:
                    return await interaction.response.send_message(
                        f"{user.mention} is already a part of this VC!", ephemeral=True
                    )
                chan["users"].append(user.id)
                channel = interaction.guild.get_channel(chan["id"])
                overwrites = channel.overwrites
                overwrites[user] = discord.PermissionOverwrite(
                    view_channel=True, connect=True, speak=True, stream=True
                )
                await channel.edit(
                    overwrites=overwrites,
                    reason=f"Added {user.display_name} to private VC by {interaction.user.display_name}",
                )
                await interaction.response.send_message(
                    f"Added {user.mention} to private VC {channel.jump_url}!",
                    ephemeral=True,
                )
                with open("vc.json", "w") as f:
                    json.dump(vc, f)
                return

        return await interaction.response.send_message(
            "You do not own any private VCs!", ephemeral=True
        )

    @vc.command(description="Remove a user from your private VC!")
    async def remove(self, interaction: discord.Interaction, user: discord.Member):
        with open("vc.json", "r") as f:
            vc = json.load(f)

        for chan in vc["channels"]:
            if chan["owner"] == interaction.user.id:
                if user.id not in chan["users"]:
                    return await interaction.response.send_message(
                        f"{user.mention} is not a part of this VC!", ephemeral=True
                    )
                chan["users"].remove(user.id)
                channel = interaction.guild.get_channel(chan["id"])
                overwrites = channel.overwrites
                del overwrites[user]
                await channel.edit(
                    overwrites=overwrites,
                    reason=f"Removed {user.display_name} from private VC by {interaction.user.display_name}",
                    ephemeral=True,
                )
                await interaction.response.send_message(
                    f"Removed {user.mention} from private VC {channel.jump_url}!",
                    ephemeral=True,
                )
                with open("vc.json", "w") as f:
                    json.dump(vc, f)
                return

        return await interaction.response.send_message(
            "You do not own any private VCs!", ephemeral=True
        )

    @vc.command(description="List all users in your private VC!")
    async def users(self, interaction: discord.Interaction):
        with open("vc.json", "r") as f:
            vc = json.load(f)

        for chan in vc["channels"]:
            if chan["owner"] == interaction.user.id:
                users = []
                for user in chan["users"]:
                    users.append(interaction.guild.get_member(user))
                await interaction.response.send_message(
                    embed=discord.Embed(
                        title="Users in VC",
                        description="\n".join([f"{user.mention}" for user in users]),
                        color=discord.Color.blue(),
                        timestamp=interaction.created_at,
                    ).set_footer(text=f"Total users: {len(users)}"),
                    ephemeral=True,
                )
                return

        return await interaction.response.send_message(
            "You do not own any private VCs!", ephemeral=True
        )

    # @vc.command()
    # async def current(self, interaction: discord.Interaction):
    #     with open("vc.json", "r") as f:
    #         vc = json.load(f)

    #     owner_channel = []
    #     member_channels = []

    #     for chan in vc["channels"]:
    #         if chan["owner"] == interaction.user.id:
    #             owner_channel = interaction.guild.get_channel(chan["id"])

    # async def cog_app_command_error(
    #     self, interaction: Interaction, error: AppCommandError
    # ):
    #     await interaction.response.send_message(error, ephemeral=True)


async def setup(bot):
    """Load the Giveaway cog."""
    await bot.add_cog(VC(bot))
