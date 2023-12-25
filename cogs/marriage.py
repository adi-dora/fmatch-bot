import json
import random
import traceback
import discord
from discord.ext import commands
from discord.interactions import Interaction
from dateutil import parser


from discord import app_commands
from datetime import datetime as dt


class MarriageView(discord.ui.View):
    def __init__(self, proposer: discord.Member, user: discord.Member):
        super().__init__(timeout=600)
        self.proposer = proposer
        self.user = user

    @discord.ui.button(
        label="I do!",
        style=discord.ButtonStyle.green,
        custom_id="accept",
        emoji=discord.PartialEmoji(name="\U00002764"),
    )
    async def accept(self, interaction: Interaction, button: discord.ui.Button):
        with open("marriage.json", "r") as f:
            marriage = json.load(f)

        await interaction.message.edit(view=None)

        if marriage[str(self.proposer.id)]["spouse"] is not None:
            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Already Married",
                    description=f"{self.proposer.mention} already married someone else!",
                    color=discord.Color.red(),
                    timestamp=interaction.created_at,
                ).set_thumbnail(url=self.proposer.avatar.url)
            )
        if marriage[str(self.user.id)]["spouse"] is not None:
            await self.proposer.send(
                embed=discord.Embed(
                    title="Already Married",
                    description=f"{self.user.mention} is already married to someone else!",
                    color=discord.Color.red(),
                    timestamp=interaction.created_at,
                ).set_thumbnail(url=self.user.avatar.url)
            )

            return await interaction.response.send_message(
                embed=discord.Embed(
                    title="Already Married",
                    description=f"You are already married to someone else!",
                    color=discord.Color.red(),
                    timestamp=interaction.created_at,
                ).set_thumbnail(url=self.user.avatar.url)
            )

        marriage[str(self.proposer.id)]["spouse"] = {
            "user": self.user.id,
            "married": str(dt.now()),
        }
        marriage[str(self.user.id)]["spouse"] = {
            "user": self.proposer.id,
            "married": str(dt.now()),
        }
        with open("marriage.json", "w") as f:
            json.dump(marriage, f, indent=1)

        await interaction.response.send_message(
            f"You have accepted {self.proposer.name}'s proposal for marrige!"
        )
        await self.proposer.send(
            embed=discord.Embed(
                title="Accepted!",
                description=f"{self.user.name} has accepted your proposal for marrige! Congratulations! :heart:",
                color=discord.Color.pink(),
                timestamp=interaction.created_at,
            ).set_thumbnail(url=self.user.avatar.url)
        )

    @discord.ui.button(
        label="No!",
        style=discord.ButtonStyle.gray,
        custom_id="decline",
        emoji=discord.PartialEmoji(name="\U0001f494"),
    )
    async def decline(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.message.edit(view=None)
        await interaction.response.send_message(
            f"You have declined {self.proposer.mention}'s proposal for marrige!"
        )
        await self.proposer.send(
            embed=discord.Embed(
                title="Declined",
                description=f"{self.user.mention} has declined your proposal for marrige!",
                color=discord.Color.red(),
                timestamp=interaction.created_at,
            ).set_thumbnail(url=self.user.avatar.url)
        )


class DivorceView(discord.ui.View):
    def __init__(self, proposer: discord.Member, user: discord.Member):
        super().__init__(timeout=600)
        self.proposer = proposer
        self.user = user

    @discord.ui.button(
        label="Sign the Papers",
        style=discord.ButtonStyle.grey,
        custom_id="divorce",
        emoji=discord.PartialEmoji(name="\U0001f4dd"),
    )
    async def accept(self, interaction: Interaction, button: discord.ui.Button):
        with open("marriage.json", "r") as f:
            marriage = json.load(f)

        await interaction.message.edit(view=None)

        marriage[str(self.proposer.id)]["spouse"] = None
        marriage[str(self.user.id)]["spouse"] = None
        with open("marriage.json", "w") as f:
            json.dump(marriage, f, indent=1)

        await interaction.response.send_message("The divorce has been finalized!")
        await self.proposer.send("The divorce has been finalized!")

    @discord.ui.button(
        label="Work Through the Differences",
        style=discord.ButtonStyle.blurple,
        emoji=discord.PartialEmoji(name="\U0001f46b"),
    )
    async def decline(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.message.edit(view=None)
        await interaction.response.send_message("The divorce has been cancelled!")
        await self.proposer.send(
            f"The divorce was not accepted! {interaction.user.name} wants to work through the differences!"
        )


class Marriage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Propose to marry a user!")
    @app_commands.describe(member="The user you want to marry")
    async def propose(self, interaction: Interaction, member: discord.Member):
        with open("marriage.json", "r") as f:
            marriage = dict(json.load(f))

        if str(interaction.user.id) not in marriage.keys():
            marriage[str(interaction.user.id)] = {
                "spouse": None,
                "children": [],
                "parents": [],
            }

        if str(member.id) not in marriage.keys():
            marriage[str(member.id)] = {
                "spouse": None,
                "children": [],
                "parents": [],
            }

        if member.id == interaction.user.id:
            return await interaction.response.send_message(
                "You cannot marry yourself!", ephemeral=True
            )

        if marriage[str(interaction.user.id)]["spouse"] is not None:
            spouse = interaction.guild.get_member(
                marriage[str(interaction.user.id)]["spouse"]["user"]
            )
            return await interaction.response.send_message(
                f"You are already married to {spouse.mention}. No cheating!",
                ephemeral=True,
            )

        if marriage[str(member.id)]["spouse"] is not None:
            spouse = interaction.guild.get_member(
                marriage[str(member.id)]["spouse"]["user"]
            )
            return await interaction.response.send_message(
                f"{spouse.mention} is already married!", ephemeral=True
            )

        if member.id in [
            user["user"] for user in marriage[str(interaction.user.id)]["parents"]
        ]:
            return await interaction.response.send_message(
                f"You cannot marry your parent!", ephemeral=True
            )

        if member.id in [
            user["user"] for user in marriage[str(interaction.user.id)]["children"]
        ]:
            return await interaction.response.send_message(
                f"You cannot marry your child!", ephemeral=True
            )

        with open("marriage.json", "w") as f:
            json.dump(marriage, f, indent=1)

        await member.send(
            embed=discord.Embed(
                title="New Marriage Proposal",
                description=f"{interaction.user.name} wants to marry you! :ring:\nDo you want this person as your life partner?",
                color=discord.Color.pink(),
                timestamp=interaction.created_at,
            ).set_thumbnail(url=interaction.user.avatar.url),
            view=MarriageView(interaction.user, member),
        )

        await interaction.response.send_message(
            f"A proposal for marriage has been sent to {member.mention}.",
            ephemeral=True,
        )

    @app_commands.command(description="View your current spouse!")
    async def spouse(self, interaction: Interaction):
        with open("marriage.json", "r") as f:
            marriage = json.load(f)

        try:
            spouse = marriage[str(interaction.user.id)]["spouse"]

        except KeyError:
            marriage[str(interaction.user.id)] = {
                "spouse": None,
                "children": [],
                "parents": [],
            }
            with open("marriage.json", "w") as f:
                json.dump(marriage, f, indent=1)
            return await interaction.response.send_message(
                f"You are not married.", ephemeral=True
            )

        if spouse is None:
            return await interaction.response.send_message(
                f"You are not married.", ephemeral=True
            )

        spouse = interaction.guild.get_member(spouse['user'])
        if spouse is None:
            return await interaction.response.send_message(
                f"Your partner was not found!", ephemeral=True
            )

        return await interaction.response.send_message(
            f"Your spouse is {spouse.mention}.", ephemeral=True
        )

    @app_commands.command(description="View the children of you or another user!")
    async def children(self, interaction: Interaction, member: discord.Member | None):
        if member is None:
            member = interaction.user
        with open("marriage.json", "r") as f:
            marriage = json.load(f)

        try:
            children = marriage[str(member.id)]["children"]

        except KeyError:
            marriage[str(member.id)] = {
                "spouse": None,
                "children": [],
                "parents": [],
            }
            with open("marriage.json", "w") as f:
                json.dump(marriage, f, indent=1)
            return await interaction.response.send_message(
                f"You do not have any children.", ephemeral=True
            )

        if len(children) == 0:
            return await interaction.response.send_message(
                f"You do not have any children.", ephemeral=True
            )

        children = [interaction.guild.get_member(x["user"]) for x in children]

        embed = discord.Embed(
            title=f"Children of {member.display_name}",
            description="\n".join(
                item.mention for item in children if item is not None
            ),
            color=discord.Color.pink(),
            timestamp=interaction.created_at,
        ).set_thumbnail(url=member.avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="View the parents of you or another user!")
    async def parents(self, interaction: Interaction, member: discord.Member | None):
        if member is None:
            member = interaction.user

        with open("marriage.json", "r") as f:
            marriage = json.load(f)

        try:
            parents = marriage[str(member.id)]["parents"]

        except KeyError:
            marriage[str(member.id)] = {
                "spouse": None,
                "children": [],
                "parents": [],
            }
            with open("marriage.json", "w") as f:
                json.dump(parents, f, indent=1)

            return await interaction.response.send_message(
                f"You do not have any parents.", ephemeral=True
            )

        if len(parents) == 0:
            return await interaction.response.send_message(
                f"You do not have any parents.", ephemeral=True
            )

        parents = [interaction.guild.get_member(x["user"]) for x in parents]

        embed = discord.Embed(
            title=f"Parents of {member.display_name}",
            description="\n".join(item.mention for item in parents if item is not None),
            color=discord.Color.pink(),
            timestamp=interaction.created_at,
        ).set_thumbnail(url=member.avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="Emancipate from your parents!")
    async def emancipate(self, interaction: discord.Interaction):
        with open("marriage.json", "r") as f:
            marriage = json.load(f)

        try:
            parents = marriage[str(interaction.user.id)]["parents"]

        except KeyError:
            marriage[str(interaction.user.id)] = {
                "spouse": None,
                "children": [],
                "parents": [],
            }
            with open("marriage.json", "w") as f:
                json.dump(parents, f, indent=1)

            return await interaction.response.send_message(
                f"You do not have any parents.", ephemeral=True
            )

        if len(parents) == 0:
            return await interaction.response.send_message(
                f"You do not have any parents.", ephemeral=True
            )

        parents = [
            interaction.guild.get_member(x["user"]) for x in parents if x is not None
        ]

        marriage[str(interaction.user.id)]["parents"].clear()

        with open("marriage.json", "w") as f:
            json.dump(marriage, f, indent=1)

        await interaction.response.send_message(
            f"You have emancipated from your parents: {'& '.join(parent.mention for parent in parents)} .",
            ephemeral=True,
        )

        for parent in parents:
            for child in marriage[parent.id]["children"]:
                if child["user"] == interaction.user.id:
                    marriage[str(parent.id)]["children"].remove(child)

            await parent.send(
                embed=discord.Embed(
                    title=f"Child Emancipated",
                    description=f"{interaction.user.mention} has emancipated from you. You are no longer their parent",
                    color=discord.Color.pink(),
                    timestamp=interaction.created_at,
                )
            )

    @app_commands.command(description="Disown a child you adopted!")
    async def disown(self, interaction: discord.Interaction, child_id: str):
        with open("marriage.json", "r") as f:
            marriage = json.load(f)

        selected = interaction.guild.get_member(int(child_id))
        if selected is None:
            return await interaction.response.send_message(
                "The user was not found!", ephemeral=True
            )

        for child in marriage[str(interaction.user.id)]["children"]:
            if child["user"] == int(child_id):
                marriage[str(interaction.user.id)]["children"].remove(child)

                for parent in marriage[child_id]["parents"]:
                    if parent["user"] == interaction.user.id:
                        marriage[child_id]["parents"].remove(parent)
                with open("marriage.json", "w") as f:
                    json.dump(marriage, f, indent=1)

                await interaction.guild.get_member(child["user"]).send(
                    f"{interaction.user.mention} has disowned you!"
                )
                return await interaction.response.send_message(
                    f"You have disowned {interaction.guild.get_member(child['user']).mention}.",
                    ephemeral=True,
                )

        return await interaction.response.send_message(
            f"You do not have this user as a child.",
            ephemeral=True,
        )

    @disown.autocomplete("child_id")
    async def disown_autocomplete(self, interaction: discord.Interaction, current: str):
        with open("marriage.json", "r") as f:
            marriage = json.load(f)

        return [
            app_commands.Choice(
                name=interaction.guild.get_member(child["user"]).display_name,
                value=str(interaction.guild.get_member(child["user"]).id),
            )
            for child in marriage[str(interaction.user.id)]["children"]
            if current.lower()
            in interaction.guild.get_member(child["user"]).name.lower()
            and interaction.guild.get_member(child["user"]) is not None
        ]

    @app_commands.command(description="Divorce your significant other!")
    @app_commands.describe(reason="Why did it all fall apart?")
    async def divorce(self, interaction: discord.Interaction, reason: str | None):
        with open("marriage.json", "r") as f:
            marriage = json.load(f)

        try:
            spouse = marriage[str(interaction.user.id)]["spouse"]

        except KeyError:
            marriage[str(interaction.user.id)] = {
                "spouse": None,
                "children": [],
                "parents": [],
            }
            with open("marriage.json", "w") as f:
                json.dump(marriage, f, indent=1)

            return await interaction.response.send_message(
                f"You are not married!", ephemeral=True
            )
        
        if spouse is None:
            return await interaction.response.send_message("You are not married!", ephemeral=True)

        spouse = interaction.guild.get_member(spouse["user"])

        divorce_papers = discord.Embed(
            title="Filed for Divorce",
            description=f"{interaction.user.name} wishes to file for divorce. Do you accept?",
            color=discord.Color.pink(),
            timestamp=interaction.created_at,
        ).add_field(
            name="Reason",
            value=reason if reason else "No reason provided",
            inline=False,
        )

        await spouse.send(
            embed=divorce_papers, view=DivorceView(interaction.user, spouse)
        )
        await interaction.response.send_message(
            "You have filed for divorce!", ephemeral=True
        )

    @app_commands.command(description="Adopt a user!")
    async def adopt(self, interaction: discord.Interaction, child: discord.Member):
        try:
            with open("marriage.json", "r") as f:
                marriage = json.load(f)

            if str(interaction.user.id) not in marriage:
                marriage[str(interaction.user.id)] = {
                    "spouse": None,
                    "children": [],
                    "parents": [],
                }

            if str(child.id) not in marriage:
                marriage[str(child.id)] = {
                    "spouse": None,
                    "children": [],
                    "parents": [],
                }

            if child.id == interaction.user.id:
                return await interaction.response.send_message(
                    "You cannot adopt yourself!", ephemeral=True
                )

            if (
                marriage[str(interaction.user.id)]["spouse"] is not None
                and child.id == marriage[str(interaction.user.id)]["spouse"]["user"]
            ):
                return await interaction.response.send_message(
                    "You cannot adopt your spouse!", ephemeral=True
                )

            if child.id in [
                child["user"]
                for child in marriage[str(interaction.user.id)]["children"]
            ]:
                return await interaction.response.send_message(
                    "You are already this person's parent!", ephemeral=True
                )

            if child.id in [
                parent["user"]
                for parent in marriage[str(interaction.user.id)]["parents"]
            ]:
                return await interaction.response.send_message(
                    "You cannot adopt your parent!", ephemeral=True
                )

            if len(marriage[str(child.id)]["parents"]) == 2:
                return await interaction.response.send_message(
                    "You cannot adopt someone who has 2 loving parents!", ephemeral=True
                )

            if len(marriage[str(interaction.user.id)]["children"]) == 10:
                return await interaction.response.send_message(
                    "You cannot adopt more than 10 children!", ephemeral=True
                )

            marriage[str(interaction.user.id)]["children"].append(
                {
                    "user": child.id,
                    "adopted": str(dt.now()),
                }
            )

            marriage[str(child.id)]["parents"].append(
                {
                    "user": interaction.user.id,
                    "adopted": str(dt.now()),
                }
            )

            with open("marriage.json", "w") as f:
                json.dump(marriage, f, indent=1)

            await interaction.response.send_message(
                f"You have adopted {child.mention}. Make sure to provide a loving home for them!",
                ephemeral=True,
            )
            await child.send(
                embed=discord.Embed(
                    title=f"Adopted",
                    description=f"{interaction.user.mention} has adopted you. You are now their child!",
                    color=discord.Color.pink(),
                    timestamp=interaction.created_at,
                )
            )
        except:
            traceback.print_exc()

    @app_commands.command(description="View your relationship profile!")
    async def profile(
        self, interaction: discord.Interaction, user: discord.Member = None
    ):
        with open("marriage.json", "r") as f:
            marriage = json.load(f)

        if user is None:
            user = interaction.user

        if str(user.id) not in marriage:
            marriage[str(user.id)] = {
                "spouse": None,
                "children": [],
                "parents": [],
            }

        profile = discord.Embed(
            title=f"{user.name} Profile",
            color=discord.Color.pink(),
            timestamp=interaction.created_at,
        )
        profile.set_thumbnail(url=user.avatar.url)
        profile.add_field(
            name="Spouse",
            value=interaction.guild.get_member(
                marriage[str(user.id)]["spouse"]["user"]
            ).mention
            + f" <t:{int(parser.parse(marriage[str(user.id)]['spouse']['married']).timestamp())}:R>"
            if marriage[str(user.id)]["spouse"] is not None
            else "Single",
            inline=False,
        )
        profile.add_field(
            name=f"Children ({len(marriage[str(user.id)]['children'])})",
            value="\n".join(
                interaction.guild.get_member(child["user"]).mention
                + f" <t:{int(parser.parse(child['adopted']).timestamp())}:R>"
                for child in marriage[str(user.id)]["children"]
            ),
            inline=False,
        )

        profile.add_field(
            name=f"Parents ({len(marriage[str(user.id)]['parents'])})",
            value="\n".join(
                interaction.guild.get_member(parent["user"]).mention
                + f" <t:{int(parser.parse(parent['adopted']).timestamp())}:R>"
                for parent in marriage[str(user.id)]["parents"]
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=profile)


async def setup(bot):
    await bot.add_cog(Marriage(bot))
