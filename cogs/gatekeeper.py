import json
import traceback
from unicodedata import name
import discord
from discord.ext import commands
from discord.interactions import Interaction


from discord import app_commands
from discord.ui.item import Item


class GenderView(discord.ui.View):
    def __init__(self, age_role: discord.Role, interaction: discord.Interaction):
        super().__init__(timeout=300)
        self.age = age_role
        self.interaction = interaction

    with open("gatekeeper.json", "r") as f:
        gate = json.load(f)

    @discord.ui.select(
        placeholder="Select your gender...",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label=gender["label"], value=gender["label"], emoji=gender["emoji"]
            )
            for gender in gate["gender"]
        ],
        custom_id="gender",
    )
    async def gender_select(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        with open("gatekeeper.json", "r") as f:
            gate = json.load(f)

        try:
            age_roles = [
                interaction.guild.get_role(a_data["role"]) for a_data in gate["age"]
            ]
            gender_roles = [
                interaction.guild.get_role(g_data["role"]) for g_data in gate["gender"]
            ]
            await interaction.user.remove_roles(*age_roles)
            await interaction.user.remove_roles(*gender_roles)

            for gender in gate["gender"]:
                if select.values[0] == gender["label"]:
                    gender_role = interaction.guild.get_role(gender["role"])

                    await interaction.user.add_roles(
                        *[gender_role, self.age], reason="Added age and gender roles"
                    )
                    await self.interaction.edit_original_response(
                        content="You have been granted access to the server!", view=None
                    )
                    # Add roles you want added to people after they verify in the "roles_after_verification" field in the json
                    await interaction.user.add_roles(
                        *[
                            interaction.guild.get_role(role)
                            for role in gate["roles_after_verification"]
                        ],
                        reason="Extra roles after verification",
                    )

                    break

        except:
            traceback.print_exc()


class AgeView(discord.ui.View):
    def __init__(self, interation: discord.Interaction):
        super().__init__(timeout=300)
        self.interaction = interation

    with open("gatekeeper.json", "r") as f:
        gate = json.load(f)

    @discord.ui.select(
        placeholder="Select your age...",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label=age["label"], value=age["label"], emoji=age["emoji"]
            )
            for age in gate["age"]
        ],
        custom_id="age",
    )
    async def age_select(
        self, interaction: discord.Interaction, select: discord.ui.Select
    ):
        try:
            with open("gatekeeper.json", "r") as f:
                gate = json.load(f)

            for age in gate["age"]:
                if select.values[0] == str(age["label"]):
                    role_to_give = interaction.guild.get_role(age["role"])

                    await self.interaction.delete_original_response()
                    await interaction.response.send_message(
                        "Select your gender",
                        view=GenderView(role_to_give, interaction),
                        ephemeral=True,
                    )

        except:
            traceback.print_exc()


class GatekeeperView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="I Agree", style=discord.ButtonStyle.green, custom_id="agree"
    )
    async def confirm(self, interaction: Interaction, button: discord.ui.Button):
        with open("gatekeeper.json", "r") as f:
            gate = json.load(f)

        await interaction.response.send_message(
            "Select your age", view=AgeView(interaction), ephemeral=True
        )

    @discord.ui.button(
        label="I Disagree", style=discord.ButtonStyle.red, custom_id="disagree"
    )
    async def deny(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.user.kick(reason="User disagreed to the rules")
        await interaction.user.send(
            "You have been kicked from the server for disagreeing to the rules!"
        )

    async def on_error(self, interaction: Interaction, error: Exception, item: Item):
        traceback.print_exc()


class ConfirmationView(discord.ui.View):
    def __init__(self, channel: discord.TextChannel, message: str, link: str):
        super().__init__(timeout=300)
        self.channel = channel
        self.message = message
        self.link = link

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: Interaction, button: discord.ui.Button):
        with open("gatekeeper.json", "r") as f:
            gate = json.load(f)
        if self.link:
            await self.channel.send(self.link)

        m = await self.channel.send(self.message, view=GatekeeperView())
        gate["msg_id"] = m.id
        await interaction.message.edit(view=None)
        await interaction.response.send_message("The Gatekeeper message has been sent!")
        with open("gatekeeper.json", "w") as f:
            json.dump(gate, f, indent=1)

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red)
    async def deny(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.message.edit(view=None)
        await interaction.response.send_message("The request has been cancelled!")


class Gatekeeper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        with open("gatekeeper.json", "r") as f:
            gate = json.load(f)
        await self.bot.add_view(GatekeeperView(), gate["msg_id"])

    gatekeeper = app_commands.Group(
        name="gatekeeper",
        description="Manage the way users first interact with your server",
    )

    @gatekeeper.command(
        description="Set the channel where the gatekeeper messages will be sent"
    )
    @app_commands.describe(
        channel="The channel where the gatekeeper messages will be sent. If none, the current will be shown"
    )
    @commands.has_permissions(administrator=True)
    async def channel(
        self, interaction: Interaction, channel: discord.TextChannel | None
    ):
        with open("gatekeeper.json", "r") as f:
            gate = json.load(f)

        if channel is None:
            if gate["channel"] is None:
                return await interaction.response.send_message(
                    "No channel has been set"
                )
            gate_channel = interaction.guild.get_channel(gate["channel"])
            if gate_channel is None:
                return await interaction.response.send_message(
                    "The channel was not found!"
                )
            return await interaction.response.send_message(
                f"The current Gatekeeper channel is: {gate_channel.mention}",
            )

        with open("gatekeeper.json", "w") as f:
            gate["channel"] = channel.id
            json.dump(gate, f, indent=1)

        await interaction.response.send_message(
            f"The Gatekeeper channel has been set to: {channel.mention}"
        )

    @gatekeeper.command()
    @commands.has_permissions(administrator=True)
    async def rules(self, interaction: Interaction, message: str):
        with open("gatekeeper.json", "r") as f:
            gate = json.load(f)

        gate["rules"] = message

        with open("gatekeeper.json", "w") as f:
            json.dump(gate, f, indent=1)

        await interaction.response.send_message(
            f"The rules have been set to: \n{message}", ephemeral=True
        )

    @gatekeeper.command(
        description="Provide the link for an image to be displayed with the rules"
    )
    @commands.has_permissions(administrator=True)
    async def link(self, interaction: Interaction, link: str):
        with open("gatekeeper.json", "r") as f:
            gate = json.load(f)

        gate["link"] = link

        with open("gatekeeper.json", "w") as f:
            json.dump(gate, f, indent=1)

        await interaction.response.send_message(
            f"The link for the gatekeeper functionality has been set to: \n{link}",
            ephemeral=True,
        )

    @gatekeeper.command(
        description="Review the settings for the Gatekeepeer and publish"
    )
    @commands.has_permissions(administrator=True)
    async def create(self, interaction: Interaction):
        with open("gatekeeper.json", "r") as f:
            gate = json.load(f)

        try:
            channel = interaction.guild.get_channel(gate["channel"])
            rules = gate["rules"]

            if (
                channel is None
                or rules is None
                or not gate["age"]
                or not gate["gender"]
            ):
                return await interaction.response.send_message(
                    "Please set the channel and rules for the Gatekeeper, and add roles for the Age and Gender menus!"
                )

            embed = (
                discord.Embed(
                    title="Gatekeeper Settings",
                    color=discord.Color.pink(),
                    timestamp=interaction.created_at,
                )
                .add_field(name="Channel", value=f"{channel.mention}", inline=False)
                .add_field(name="Rules", value=f"{rules}", inline=False)
                .add_field(
                    name="Ages",
                    value="\n".join(
                        interaction.guild.get_role(age["role"]).mention
                        for age in gate["age"]
                    ),
                )
                .add_field(
                    name="Genders",
                    value="\n".join(
                        interaction.guild.get_role(gender["role"]).mention
                        for gender in gate["gender"]
                    ),
                )
            ).set_image(url=gate["link"])

            await interaction.response.send_message(
                "Are you sure you want to create the Agree message with these settings?",
                embed=embed,
                view=ConfirmationView(channel, rules, gate["link"]),
            )
        except Exception as e:
            traceback.print_exc()

    @gatekeeper.command(
        description="Clear the message and link for the Gatekeeper functionality"
    )
    @commands.has_permissions(administrator=True)
    async def clear(self, interaction: Interaction):
        with open("gatekeeper.json", "r") as f:
            gate = json.load(f)

        gate["rules"] = None
        gate["link"] = None
        with open("gatekeeper.json", "w") as f:
            json.dump(gate, f, indent=1)

        await interaction.response.send_message(
            "The settings have been cleared!", ephemeral=True
        )

    @gatekeeper.command()
    @app_commands.choices(
        menu=[
            app_commands.Choice(name="Age", value="age"),
            app_commands.Choice(name="Gender", value="gender"),
        ]
    )
    async def add(
        self,
        interaction: discord.Interaction,
        menu: str,
        name: str,
        emoji: str,
        role: discord.Role,
    ):
        with open("gatekeeper.json", "r") as f:
            gate = json.load(f)

        if role >= interaction.guild.me.top_role:
            return await interaction.response.send_message(
                "This role is higher than my highest role, so I cannot give it to others!"
            )

        if menu == "age":
            try:
                name = int(name)
            except:
                return await interaction.response.send_message(
                    "This is not a valid age!", ephemeral=True
                )
            if name in [val["label"] for val in gate["age"]]:
                return await interaction.response.send_message(
                    "You have already set a role for this age!"
                )

            gate["age"].append({"label": name, "emoji": emoji, "role": role.id})

            with open("gatekeeper.json", "w") as f:
                json.dump(gate, f, indent=1)

            await interaction.response.send_message(
                f"The age ``{name}`` has been added!"
            )

        if menu == "gender":
            if name in [val["label"] for val in gate["gender"]]:
                return await interaction.response.send_message(
                    "You have already set a role for this gender!"
                )

            gate["gender"].append({"label": name, "emoji": emoji, "role": role.id})

            with open("gatekeeper.json", "w") as f:
                json.dump(gate, f, indent=1)

            await interaction.response.send_message(
                f"The gender ``{name}`` has been added!"
            )

    with open("gatekeeper.json", "r") as f:
        gate = json.load(f)

    final_names = []
    for age in gate["age"]:
        final_names.append(age)

    for gender in gate["gender"]:
        final_names.append(gender)

    # @gatekeeper.command()
    # @app_commands.choices(role = [Choice(name=item['label'], value=item['role']) for item in final_names])
    # async def remove(self, interaction: discord.Interaction, role: int):
    #     with open('gatekeeper.json', 'r') as f:
    #         gate = json.load(f)
    #     for age in gate['age']:
    #         if age['role'] == role:
    #             gate['age'].remove(age)

    #     for gender in gate['gender']:
    #         if gender['role'] == role:
    #             gate['gender'].remove(gender)

    #     with open('gatekeeper.json', 'w') as f:
    #         json.dump(gate,f)

    #     await interaction.response.send_message('The role has been removed from the menu!')


async def setup(bot):
    await bot.add_cog(Gatekeeper(bot))
