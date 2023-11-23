import discord
import random
from discord import app_commands
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @app_commands.command(description="Give a hug!")
    @app_commands.describe(member="Select a member!")
    async def hug(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            bug = [
                "https://cdn.weeb.sh/images/rkIK_u7Pb.gif",
                "https://cdn.weeb.sh/images/r1v2_uXP-.gif",
                "https://cdn.weeb.sh/images/rJnKu_XwZ.gif",
                "https://cdn.weeb.sh/images/rJl3BcTuG.gif",
                "https://cdn.weeb.sh/images/HJ7lY_QwW.gif",
                "https://cdn.weeb.sh/images/B10Tfknqf.gif",
                "https://cdn.weeb.sh/images/rkYetOXwW.gif",
                "https://cdn.weeb.sh/images/SyQ0_umD-.gif",
                "https://cdn.weeb.sh/images/Hyec_OmDW.gif",
                "https://cdn.weeb.sh/images/H1ui__XDW.gif",
                "https://cdn.weeb.sh/images/Hk4qu_XvZ.gif",
                "https://cdn.weeb.sh/images/SJZ-Qy35f.gif",
                "https://cdn.weeb.sh/images/r1G3xCFYZ.gif",
                "https://cdn.weeb.sh/images/ryuhhuJdb.gif",
                "https://cdn.weeb.sh/images/r1kC_dQPW.gif",
                "https://cdn.weeb.sh/images/r1bAksn0W.gif",
                "https://cdn.weeb.sh/images/rkx1dJ25z.gif",
                "https://cdn.weeb.sh/images/BkHA_O7v-.gif",
                "https://cdn.weeb.sh/images/rJ_slRYFZ.gif",
                "https://cdn.weeb.sh/images/BkZngAYtb.gif",
                "https://cdn.weeb.sh/images/HJU2OdmwW.gif",
                "https://cdn.weeb.sh/images/S1qhfy2cz.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} is lonely! Here's a hug!",
                color=0xFF6666,
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(bug))

            await ctx.send(embed=embed)

        else:
            bug = [
                "https://cdn.weeb.sh/images/rkIK_u7Pb.gif",
                "https://cdn.weeb.sh/images/r1v2_uXP-.gif",
                "https://cdn.weeb.sh/images/rJnKu_XwZ.gif",
                "https://cdn.weeb.sh/images/rJl3BcTuG.gif",
                "https://cdn.weeb.sh/images/HJ7lY_QwW.gif",
                "https://cdn.weeb.sh/images/B10Tfknqf.gif",
                "https://cdn.weeb.sh/images/rkYetOXwW.gif",
                "https://cdn.weeb.sh/images/SyQ0_umD-.gif",
                "https://cdn.weeb.sh/images/Hyec_OmDW.gif",
                "https://cdn.weeb.sh/images/H1ui__XDW.gif",
                "https://cdn.weeb.sh/images/Hk4qu_XvZ.gif",
                "https://cdn.weeb.sh/images/SJZ-Qy35f.gif",
                "https://cdn.weeb.sh/images/r1G3xCFYZ.gif",
                "https://cdn.weeb.sh/images/ryuhhuJdb.gif",
                "https://cdn.weeb.sh/images/r1kC_dQPW.gif",
                "https://cdn.weeb.sh/images/r1bAksn0W.gif",
                "https://cdn.weeb.sh/images/rkx1dJ25z.gif",
                "https://cdn.weeb.sh/images/BkHA_O7v-.gif",
                "https://cdn.weeb.sh/images/rJ_slRYFZ.gif",
                "https://cdn.weeb.sh/images/BkZngAYtb.gif",
                "https://cdn.weeb.sh/images/HJU2OdmwW.gif",
                "https://cdn.weeb.sh/images/S1qhfy2cz.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} hugs {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(bug))

            await ctx.send(embed=embed)

    @hug.error
    async def hug_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to hug!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

    @app_commands.command(name="kiss", description="Give a kiss!")
    @app_commands.describe(member="Select a member!")
    async def kiss(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            kuss = [
                "https://cdn.weeb.sh/images/rkFSiEedf.gif",
                "https://cdn.weeb.sh/images/ByVQha_w-.gif",
                "https://cdn.weeb.sh/images/r1cB3aOwW.gif",
                "https://cdn.weeb.sh/images/rJeB2aOP-.gif",
                "https://cdn.weeb.sh/images/HJYghpOP-.gif",
                "https://cdn.weeb.sh/images/rJoL2pdvb.gif",
                "https://cdn.weeb.sh/images/rkde2aODb.gif",
                "https://cdn.weeb.sh/images/HklBtCvTZ.gif",
                "https://cdn.weeb.sh/images/rJ_U2p_Pb.gif",
                "https://cdn.weeb.sh/images/SJn43adDb.gif",
                "https://cdn.weeb.sh/images/H1e7nadP-.gif",
                "https://cdn.weeb.sh/images/H1a42auvb.gif",
                "https://cdn.weeb.sh/images/BJMX2TuPb.gif",
                "https://cdn.weeb.sh/images/S1VEna_v-.gif",
                "https://cdn.weeb.sh/images/ry-r3TuD-.gif",
                "https://cdn.weeb.sh/images/rJ_U2p_Pb.gif",
                "https://cdn.weeb.sh/images/S1E1npuvb.gif",
                "https://cdn.weeb.sh/images/HkZyXs3A-.gif",
                "https://cdn.weeb.sh/images/B1yv36_PZ.gif",
                "https://cdn.weeb.sh/images/r1VWnTuPW.gif",
                "https://cdn.weeb.sh/images/BJSdQRtFZ.gif",
                "https://cdn.weeb.sh/images/Sy6Ai6ODb.gif",
                "https://cdn.weeb.sh/images/B12LhT_Pb.gif",
                "https://cdn.weeb.sh/images/Skc42pdv-.gif",
                "https://cdn.weeb.sh/images/ryFdQRtF-.gif",
            ]

            embed = discord.Embed(
                description=f"No one kissed {ctx.author.mention} :( Here's a quick kiss for you!",
                color=0xFF6666,
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(kuss))

            await ctx.send(embed=embed)

        else:
            kuss = [
                "https://cdn.weeb.sh/images/rkFSiEedf.gif",
                "https://cdn.weeb.sh/images/ByVQha_w-.gif",
                "https://cdn.weeb.sh/images/r1cB3aOwW.gif",
                "https://cdn.weeb.sh/images/rJeB2aOP-.gif",
                "https://cdn.weeb.sh/images/HJYghpOP-.gif",
                "https://cdn.weeb.sh/images/rJoL2pdvb.gif",
                "https://cdn.weeb.sh/images/rkde2aODb.gif",
                "https://cdn.weeb.sh/images/HklBtCvTZ.gif",
                "https://cdn.weeb.sh/images/rJ_U2p_Pb.gif",
                "https://cdn.weeb.sh/images/SJn43adDb.gif",
                "https://cdn.weeb.sh/images/H1e7nadP-.gif",
                "https://cdn.weeb.sh/images/H1a42auvb.gif",
                "https://cdn.weeb.sh/images/BJMX2TuPb.gif",
                "https://cdn.weeb.sh/images/S1VEna_v-.gif",
                "https://cdn.weeb.sh/images/ry-r3TuD-.gif",
                "https://cdn.weeb.sh/images/rJ_U2p_Pb.gif",
                "https://cdn.weeb.sh/images/S1E1npuvb.gif",
                "https://cdn.weeb.sh/images/HkZyXs3A-.gif",
                "https://cdn.weeb.sh/images/B1yv36_PZ.gif",
                "https://cdn.weeb.sh/images/r1VWnTuPW.gif",
                "https://cdn.weeb.sh/images/BJSdQRtFZ.gif",
                "https://cdn.weeb.sh/images/Sy6Ai6ODb.gif",
                "https://cdn.weeb.sh/images/B12LhT_Pb.gif",
                "https://cdn.weeb.sh/images/Skc42pdv-.gif",
                "https://cdn.weeb.sh/images/ryFdQRtF-.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} kisses {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(kuss))

            await ctx.send(embed=embed)

    @kiss.error
    async def kiss_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to kiss!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

    @app_commands.command(name="cuddle", description="Give a cuddle!")
    @app_commands.describe(member="Select a member!")
    async def cuddle(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            cud = [
                "https://cdn.weeb.sh/images/rylgIUmPW.gif",
                "https://cdn.weeb.sh/images/Byd1IUmP-.gif",
                "https://cdn.weeb.sh/images/B1SzeshCW.gif",
                "https://cdn.weeb.sh/images/r1VzDkmjW.gif",
                "https://cdn.weeb.sh/images/ByXs1AYKW.gif",
                "https://cdn.weeb.sh/images/HJMv_k7iW.gif",
                "https://cdn.weeb.sh/images/SJLkLImPb.gif",
                "https://cdn.weeb.sh/images/SkeHkUU7PW.gif",
                "https://cdn.weeb.sh/images/rJ6zAkc1f.gif",
                "https://cdn.weeb.sh/images/SJceIU7wZ.gif",
                "https://cdn.weeb.sh/images/SyUYOJ7iZ.gif",
                "https://cdn.weeb.sh/images/H1SfI8XwW.gif",
                "https://cdn.weeb.sh/images/SJLkLImPb.gif",
                "https://cdn.weeb.sh/images/HkzArUmvZ.gif",
                "https://cdn.weeb.sh/images/BkN0rIQDZ.gif",
                "https://cdn.weeb.sh/images/BJkABImvb.gif",
                "https://cdn.weeb.sh/images/SJbGLUQwZ.gif",
                "https://cdn.weeb.sh/images/r1A77CZbz.gif",
                "https://cdn.weeb.sh/images/BywGX8caZ.gif",
                "https://cdn.weeb.sh/images/rkBl8LmDZ.gif",
                "https://cdn.weeb.sh/images/SyZk8U7vb.gif",
                "https://cdn.weeb.sh/images/HkZDkeamf.gif",
                "https://cdn.weeb.sh/images/r1Q0HImPZ.gif",
                "https://cdn.weeb.sh/images/rJlMU87vb.gif",
                "https://cdn.weeb.sh/images/SJYxIUmD-.gif",
                "https://cdn.weeb.sh/images/r1XEOymib.gif",
                "https://cdn.weeb.sh/images/SykzL87D-.gif",
                "https://cdn.weeb.sh/images/By03IkXsZ.gif",
                "https://cdn.weeb.sh/images/ryURHLXP-.gif",
                "https://cdn.weeb.sh/images/BkTe8U7v-.gif",
                "https://cdn.weeb.sh/images/rylgIUmPW.gif",
                "https://cdn.weeb.sh/images/r1s9RqB7G.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} is lonely! Here's some cuddles!",
                color=0xFF6666,
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(cud))

            await ctx.send(embed=embed)

        else:
            cud = [
                "https://cdn.weeb.sh/images/rylgIUmPW.gif",
                "https://cdn.weeb.sh/images/Byd1IUmP-.gif",
                "https://cdn.weeb.sh/images/B1SzeshCW.gif",
                "https://cdn.weeb.sh/images/r1VzDkmjW.gif",
                "https://cdn.weeb.sh/images/ByXs1AYKW.gif",
                "https://cdn.weeb.sh/images/HJMv_k7iW.gif",
                "https://cdn.weeb.sh/images/SJLkLImPb.gif",
                "https://cdn.weeb.sh/images/SkeHkUU7PW.gif",
                "https://cdn.weeb.sh/images/rJ6zAkc1f.gif",
                "https://cdn.weeb.sh/images/SJceIU7wZ.gif",
                "https://cdn.weeb.sh/images/SyUYOJ7iZ.gif",
                "https://cdn.weeb.sh/images/H1SfI8XwW.gif",
                "https://cdn.weeb.sh/images/SJLkLImPb.gif",
                "https://cdn.weeb.sh/images/HkzArUmvZ.gif",
                "https://cdn.weeb.sh/images/BkN0rIQDZ.gif",
                "https://cdn.weeb.sh/images/BJkABImvb.gif",
                "https://cdn.weeb.sh/images/SJbGLUQwZ.gif",
                "https://cdn.weeb.sh/images/r1A77CZbz.gif",
                "https://cdn.weeb.sh/images/BywGX8caZ.gif",
                "https://cdn.weeb.sh/images/rkBl8LmDZ.gif",
                "https://cdn.weeb.sh/images/SyZk8U7vb.gif",
                "https://cdn.weeb.sh/images/HkZDkeamf.gif",
                "https://cdn.weeb.sh/images/r1Q0HImPZ.gif",
                "https://cdn.weeb.sh/images/rJlMU87vb.gif",
                "https://cdn.weeb.sh/images/SJYxIUmD-.gif",
                "https://cdn.weeb.sh/images/r1XEOymib.gif",
                "https://cdn.weeb.sh/images/SykzL87D-.gif",
                "https://cdn.weeb.sh/images/By03IkXsZ.gif",
                "https://cdn.weeb.sh/images/ryURHLXP-.gif",
                "https://cdn.weeb.sh/images/BkTe8U7v-.gif",
                "https://cdn.weeb.sh/images/rylgIUmPW.gif",
                "https://cdn.weeb.sh/images/r1s9RqB7G.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} cuddles {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(cud))

            await ctx.send(embed=embed)

    @cuddle.error
    async def cuddle_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to cuddle!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

    @app_commands.command(name="bite", description="Give a bite!")
    @app_commands.describe(member="Select a member!")
    async def bite(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            bit = [
                "https://cdn.weeb.sh/images/rJAlbgXsb.gif",
                "https://cdn.weeb.sh/images/Hk1sxlQjZ.gif",
                "https://cdn.weeb.sh/images/H1_Jbemjb.gif",
                "https://cdn.weeb.sh/images/ByWuR1q1M.gif",
                "https://cdn.weeb.sh/images/S1o6egmjZ.gif",
                "https://cdn.weeb.sh/images/rk8illmiW.gif",
                "https://cdn.weeb.sh/images/rkakblmiZ.gif",
                "https://cdn.weeb.sh/images/Sys3xg7jW.gif",
                "https://cdn.weeb.sh/images/H1gYelQjZ.gif",
                "https://cdn.weeb.sh/images/BJXRmfr6-.gif",
                "https://cdn.weeb.sh/images/S1FOllQj-.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} got bitten by...No one :(",
                color=0xFF6666,
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(bit))

            await ctx.send(embed=embed)

        else:
            bit = [
                "https://cdn.weeb.sh/images/rJAlbgXsb.gif",
                "https://cdn.weeb.sh/images/Hk1sxlQjZ.gif",
                "https://cdn.weeb.sh/images/H1_Jbemjb.gif",
                "https://cdn.weeb.sh/images/ByWuR1q1M.gif",
                "https://cdn.weeb.sh/images/S1o6egmjZ.gif",
                "https://cdn.weeb.sh/images/rk8illmiW.gif",
                "https://cdn.weeb.sh/images/rkakblmiZ.gif",
                "https://cdn.weeb.sh/images/Sys3xg7jW.gif",
                "https://cdn.weeb.sh/images/H1gYelQjZ.gif",
                "https://cdn.weeb.sh/images/BJXRmfr6-.gif",
                "https://cdn.weeb.sh/images/S1FOllQj-.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} bites {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(bit))

            await ctx.send(embed=embed)

    @bite.error
    async def bite_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to bite!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command(name="pat", description="Give a pat!")
    @app_commands.describe(member="Select a member!")
    async def pat(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            pot = [
                "https://media.discordapp.net/attachments/852831439460368416/1046673941432913980/cdc99142ee366b37.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046673952317124619/c7d3184eb9af77dd.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046673964153438288/cdc99142ee366b37.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046673977306791946/663e1a1c99cec4dd.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046673989755490364/preview.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674004448137226/bc5fd5b5f324f8a5.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674013369405500/c14d03ec8f956db3.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674024043917322/81e752858b204683.gif",
            ]

            embed = discord.Embed(description=f"There there...", color=0xFF6666)

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(pot))

            await ctx.send(embed=embed)

        else:
            pot = [
                "https://media.discordapp.net/attachments/852831439460368416/1046673941432913980/cdc99142ee366b37.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046673952317124619/c7d3184eb9af77dd.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046673964153438288/cdc99142ee366b37.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046673977306791946/663e1a1c99cec4dd.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046673989755490364/preview.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674004448137226/bc5fd5b5f324f8a5.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674013369405500/c14d03ec8f956db3.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674024043917322/81e752858b204683.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} pats {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(pot))

            await ctx.send(embed=embed)

    @pat.error
    async def pat_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to pat!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command(name="poke", description="Give a poke!")
    @app_commands.describe(member="Select a member!")
    async def poke(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            pok = [
                "https://media.discordapp.net/attachments/852831439460368416/1046674609111576616/2b5c02ea72dabd21.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674612601237595/04a1b7dd2853687c.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674630615765002/4232ac933260ce34.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674653403422720/f4ddad238ca147f0.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674675788431390/preview.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674699318468658/10110b88511e3a2b.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674723356033054/053e0ed8eb6d19ce.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674745413869618/2b5c02ea72dabd21.gif",
            ]

            embed = discord.Embed(description=f"Here lemme poke you!", color=0xFF6666)

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(pok))

            await ctx.send(embed=embed)

        else:
            pok = [
                "https://media.discordapp.net/attachments/852831439460368416/1046674609111576616/2b5c02ea72dabd21.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674612601237595/04a1b7dd2853687c.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674630615765002/4232ac933260ce34.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674653403422720/f4ddad238ca147f0.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674675788431390/preview.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674699318468658/10110b88511e3a2b.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674723356033054/053e0ed8eb6d19ce.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046674745413869618/2b5c02ea72dabd21.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} pokes {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(pok))

            await ctx.send(embed=embed)

    @poke.error
    async def poke_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to poke!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command(name="slap", description="Give a slap!")
    @app_commands.describe(member="Select a member!")
    async def slap(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            slap = [
                "https://media.discordapp.net/attachments/852831439460368416/1046675056945811456/fe1c50dfffaf4f59.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675058002763826/7339ae33841dcdbe.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675078655516732/953a6e0fb1f57b30.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675101191503942/preview.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675173639725187/afb8ddd5dae69da1.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675176244392007/fe1c50dfffaf4f59.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675197077491732/bbe902c9c3bc9f4b.gif",
            ]

            embed = discord.Embed(description=f"You've been bad...", color=0xFF6666)

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(slap))

            await ctx.send(embed=embed)

        else:
            slap = [
                "https://media.discordapp.net/attachments/852831439460368416/1046675056945811456/fe1c50dfffaf4f59.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675058002763826/7339ae33841dcdbe.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675078655516732/953a6e0fb1f57b30.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675101191503942/preview.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675173639725187/afb8ddd5dae69da1.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675176244392007/fe1c50dfffaf4f59.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675197077491732/bbe902c9c3bc9f4b.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} slaps {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(slap))

            await ctx.send(embed=embed)

    @slap.error
    async def slap_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to slap!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command(name="highfive", description="Give a highfive!")
    @app_commands.describe(member="Select a member!")
    async def highfive(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            high = [
                "https://media.discordapp.net/attachments/852831439460368416/1046675409015672842/3475741c02441b04.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675413524553798/preview.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675436974907442/d9fcda1a5e2d8b87.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675456482607144/42e0061bbc01b34f.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675458349080626/8bec6b8887e984db.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675502619967558/c09b14844a36fd34.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675527286653008/b64980e55cd7b895.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675547939409920/ea210ef13704bb22.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675571905675264/e75cefc474cf56a7.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675640436408320/de3ecd98eaeab125.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675642747473920/51a6353b9f0b6b21.gif",
            ]

            embed = discord.Embed(description=f"Let's do it!", color=0xFF6666)

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(high))

            await ctx.send(embed=embed)

        else:
            high = [
                "https://media.discordapp.net/attachments/852831439460368416/1046675409015672842/3475741c02441b04.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675413524553798/preview.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675436974907442/d9fcda1a5e2d8b87.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675456482607144/42e0061bbc01b34f.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675458349080626/8bec6b8887e984db.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675502619967558/c09b14844a36fd34.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675527286653008/b64980e55cd7b895.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675547939409920/ea210ef13704bb22.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675571905675264/e75cefc474cf56a7.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675640436408320/de3ecd98eaeab125.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046675642747473920/51a6353b9f0b6b21.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} highfives {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(high))

            await ctx.send(embed=embed)

    @highfive.error
    async def highfive_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to highfive!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command(name="handhold", description="Hold some hands!")
    @app_commands.describe(member="Select a member!")
    async def handhold(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            handhold = [
                "https://cdn.weeb.sh/images/BkiRKrLBz.gif",
                "https://cdn.weeb.sh/images/rk5SMpq-M.gif",
                "https://cdn.weeb.sh/images/HkGuxacbf.gif",
                "https://cdn.weeb.sh/images/rJ2IfTq-f.gif",
                "https://cdn.weeb.sh/images/Sky0l65WM.gif",
                "https://cdn.weeb.sh/images/Hk5_ga5bG.gif",
                "https://cdn.weeb.sh/images/rJx5xa9bf.gif",
                "https://cdn.weeb.sh/images/SJ3nxT5Wz.gif",
                "https://cdn.weeb.sh/images/H1urgT5-f.gif",
                "https://cdn.weeb.sh/images/SJbTxT9Wz.gif",
            ]

            embed = discord.Embed(
                description=f"I'll hold your hands :(", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(handhold))

            await ctx.send(embed=embed)

        else:
            handhold = [
                "https://cdn.weeb.sh/images/BkiRKrLBz.gif",
                "https://cdn.weeb.sh/images/rk5SMpq-M.gif",
                "https://cdn.weeb.sh/images/HkGuxacbf.gif",
                "https://cdn.weeb.sh/images/rJ2IfTq-f.gif",
                "https://cdn.weeb.sh/images/Sky0l65WM.gif",
                "https://cdn.weeb.sh/images/Hk5_ga5bG.gif",
                "https://cdn.weeb.sh/images/rJx5xa9bf.gif",
                "https://cdn.weeb.sh/images/SJ3nxT5Wz.gif",
                "https://cdn.weeb.sh/images/H1urgT5-f.gif",
                "https://cdn.weeb.sh/images/SJbTxT9Wz.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} holds hands of {member}!",
                color=0xFF6666,
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(handhold))

            await ctx.send(embed=embed)

    @handhold.error
    async def handhold_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to handhold!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command(name="punch", description="Give a punch!")
    @app_commands.describe(member="Select a member!")
    async def punch(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            punch = [
                "https://images-ext-1.discordapp.net/external/w4pvWUqZ7DwYsphKvaSKMFXNarCngEd1cc_ZBTw0ISs/https/cdn.weeb.sh/images/rJHLDT-Wz.gif",
                "https://images-ext-1.discordapp.net/external/BXaocQWGvF1Pjhun0GPOZhZixuToMHTWVv2EzgWAhqs/https/cdn.weeb.sh/images/ByI7vTb-G.gif",
                "https://images-ext-2.discordapp.net/external/DcdB6jBiKoL7ISwmc7DIfe-WXONAIhCV2ibDPDRGNJw/https/cdn.weeb.sh/images/SJAfH5TOz.gif",
                "https://images-ext-2.discordapp.net/external/iRWrGzMiaVR5nZ_CzfNtaym7JVFOiY2EUDYUTrpBy-w/https/cdn.weeb.sh/images/B1rZP6b-z.gif",
                "https://images-ext-1.discordapp.net/external/06BzS6Z9jHMaHfNri98QM02Oj7yEsTdQXHkFjLNEbaw/https/cdn.weeb.sh/images/rJRUk2PLz.gif",
                "https://images-ext-1.discordapp.net/external/n0EA9Kkpnp9RciVhyDZLqTE9CyjX-IRP15oZFagxAf4/https/cdn.weeb.sh/images/SJR-PpZbM.gif",
                "https://images-ext-2.discordapp.net/external/iTf4fr_k8FyQDf_BtlcrfD0QbRN-Bm9v0YANz-N-0Rg/https/cdn.weeb.sh/images/SkFLH129z.gif",
            ]

            embed = discord.Embed(
                description=f"I'll punch you..for being bad!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(punch))

            await ctx.send(embed=embed)

        else:
            punch = [
                "https://images-ext-1.discordapp.net/external/w4pvWUqZ7DwYsphKvaSKMFXNarCngEd1cc_ZBTw0ISs/https/cdn.weeb.sh/images/rJHLDT-Wz.gif",
                "https://images-ext-1.discordapp.net/external/BXaocQWGvF1Pjhun0GPOZhZixuToMHTWVv2EzgWAhqs/https/cdn.weeb.sh/images/ByI7vTb-G.gif",
                "https://images-ext-2.discordapp.net/external/DcdB6jBiKoL7ISwmc7DIfe-WXONAIhCV2ibDPDRGNJw/https/cdn.weeb.sh/images/SJAfH5TOz.gif",
                "https://images-ext-2.discordapp.net/external/iRWrGzMiaVR5nZ_CzfNtaym7JVFOiY2EUDYUTrpBy-w/https/cdn.weeb.sh/images/B1rZP6b-z.gif",
                "https://images-ext-1.discordapp.net/external/06BzS6Z9jHMaHfNri98QM02Oj7yEsTdQXHkFjLNEbaw/https/cdn.weeb.sh/images/rJRUk2PLz.gif",
                "https://images-ext-1.discordapp.net/external/n0EA9Kkpnp9RciVhyDZLqTE9CyjX-IRP15oZFagxAf4/https/cdn.weeb.sh/images/SJR-PpZbM.gif",
                "https://images-ext-2.discordapp.net/external/iTf4fr_k8FyQDf_BtlcrfD0QbRN-Bm9v0YANz-N-0Rg/https/cdn.weeb.sh/images/SkFLH129z.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} punches {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(punch))

            await ctx.send(embed=embed)

    @punch.error
    async def punch_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to punch!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command(name="pout", description="Do a big pout!")
    @app_commands.describe(member="Select a member!")
    async def pout(self, ctx: commands.Context, *, member: str) -> None:
        if member is None:
            pout = [
                "https://media.discordapp.net/attachments/852831439460368416/1046678018132820038/6c9d83ee641da6c5.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678046939299970/7e5b5d08f0c466b8.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678064978985071/577fa43460acd05b.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678092216807434/ddf09161570dd984.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678113268027392/d81a78b8ebb6704f.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678115180609596/565b1850e3e91480.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678136806449182/87f4cc588bb16481.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678138064740412/974dd4f44aa7a93c.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678162739826739/53efc8eca26e6c70.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678183694581810/9d40224bb7757be1.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678185296801812/db12b849b6d044e5.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678206884884580/b64976075759865f.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} pouts!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(pout))

            await ctx.send(embed=embed)

        else:
            pout = [
                "https://media.discordapp.net/attachments/852831439460368416/1046678018132820038/6c9d83ee641da6c5.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678046939299970/7e5b5d08f0c466b8.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678064978985071/577fa43460acd05b.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678092216807434/ddf09161570dd984.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678113268027392/d81a78b8ebb6704f.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678115180609596/565b1850e3e91480.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678136806449182/87f4cc588bb16481.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678138064740412/974dd4f44aa7a93c.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678162739826739/53efc8eca26e6c70.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678183694581810/9d40224bb7757be1.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678185296801812/db12b849b6d044e5.gif",
                "https://media.discordapp.net/attachments/852831439460368416/1046678206884884580/b64976075759865f.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} pouts {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(pout))

            await ctx.send(embed=embed)

    @app_commands.command(name="lick", description="Give some lick!")
    @app_commands.describe(member="Select a member!")
    async def lick(self, ctx: commands.Context, *, member: str) -> None:
        if member == ctx.author:
            lic = [
                "https://cdn.weeb.sh/images/rktygCOD-.gif",
                "https://cdn.weeb.sh/images/HJRRyAuP-.gif",
                "https://cdn.weeb.sh/images/rJ6hrQr6-.gif",
                "https://cdn.weeb.sh/images/ryGpGsnAZ.gif",
                "https://cdn.weeb.sh/images/H13HS7S6-.gif",
                "https://cdn.weeb.sh/images/H1EJxR_vZ.gif",
                "https://cdn.weeb.sh/images/rykRHmB6W.gif",
                "https://cdn.weeb.sh/images/S1QzRJp7z.gif",
                "https://cdn.weeb.sh/images/Sk15iVlOf.gif",
                "https://cdn.weeb.sh/images/Bkxge0uPW.gif",
                "https://cdn.weeb.sh/images/Syg8gx0OP-.gif",
                "https://cdn.weeb.sh/images/Hkknfs2Ab.gif",
                "https://cdn.weeb.sh/images/BkvTBQHaZ.gif",
                "https://cdn.weeb.sh/images/HkEqiExdf.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} got licked by...No one :(",
                color=0xFF6666,
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(lic))

            await ctx.send(embed=embed)

        else:
            lic = [
                "https://cdn.weeb.sh/images/rktygCOD-.gif",
                "https://cdn.weeb.sh/images/HJRRyAuP-.gif",
                "https://cdn.weeb.sh/images/rJ6hrQr6-.gif",
                "https://cdn.weeb.sh/images/ryGpGsnAZ.gif",
                "https://cdn.weeb.sh/images/H13HS7S6-.gif",
                "https://cdn.weeb.sh/images/H1EJxR_vZ.gif",
                "https://cdn.weeb.sh/images/rykRHmB6W.gif",
                "https://cdn.weeb.sh/images/S1QzRJp7z.gif",
                "https://cdn.weeb.sh/images/Sk15iVlOf.gif",
                "https://cdn.weeb.sh/images/Bkxge0uPW.gif",
                "https://cdn.weeb.sh/images/Syg8gx0OP-.gif",
                "https://cdn.weeb.sh/images/Hkknfs2Ab.gif",
                "https://cdn.weeb.sh/images/BkvTBQHaZ.gif",
                "https://cdn.weeb.sh/images/HkEqiExdf.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} licks {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(lic))

            await ctx.send(embed=embed)

    @lick.error
    async def lick_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to lick!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

    @app_commands.command(name="spank", description="Spank someone!")
    @app_commands.describe(member="Select a member!")
    async def spank(self, ctx: commands.Context, *, member: str) -> None:
        if ctx.channel.id == 925466623668797490:
            spank = [
                "https://media.discordapp.net/attachments/756378270638800896/1048246243580706816/taritari-anime-spank.gif",
                "https://media.discordapp.net/attachments/756378270638800896/1048246243199033394/spank-anime.gif",
                "https://media.discordapp.net/attachments/756378270638800896/1048246241953325056/spank-bad.gif",
                "https://media.discordapp.net/attachments/756378270638800896/1048246521071673394/spank-slap_1.gif",
                "https://media.discordapp.net/attachments/756378270638800896/1048246709471420557/bad-spank_1.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} spanks {member}!", color=0xFFCCCC
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(spank))

            await ctx.send(embed=embed)

        else:
            await ctx.send("Please move to <#925466623668797490> to use this command!")

    @spank.error
    async def spank_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to spank!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command(name="fuck", description="Fuck someone!")
    @app_commands.describe(member="Select a member!")
    async def fuck(self, ctx: commands.Context, *, member: str) -> None:
        if ctx.channel.id == 925466623668797490:
            fuck = [
                "https://media.discordapp.net/attachments/756378270638800896/1048248170112634910/ezgif-3-bbff94600f.gif",
                "https://media.discordapp.net/attachments/756378270638800896/1048248170574000138/ezgif-3-76a13c2a4b.gif",
                "https://media.discordapp.net/attachments/756378270638800896/1048248171047944363/ezgif-3-d50679d56d.gif",
                "https://media.discordapp.net/attachments/756378270638800896/1048248171417063504/ezgif-3-94b9f00a2a.gif",
                "https://media.discordapp.net/attachments/756378270638800896/1048248172276875374/porno-anime-12.gif",
                "https://media.discordapp.net/attachments/756378270638800896/1048248172692131860/porno-anime-11.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} fucks {member}", color=0xFFCCCC
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(fuck))

            await ctx.send(embed=embed)

        else:
            await ctx.send("Please move to <#925466623668797490> to use this command!")

    @fuck.error
    async def fuck_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to fuck!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command(name="blowjob", description="Give a blowjob!")
    @app_commands.describe(member="Select a member!")
    async def blowjob(self, ctx: commands.Context, *, member: str) -> None:
        if ctx.channel.id == 925466623668797490:
            blowjob = [
                "https://media.discordapp.net/attachments/756378270638800896/1048250999011287050/ezgif-3-a3876aeedb.gif",
                "https://media.discordapp.net/attachments/756378270638800896/1048250999359422564/ezgif-3-2dab498bc8.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} blows {member}!", color=0xFFCCCC
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(blowjob))

            await ctx.send(embed=embed)

        else:
            await ctx.send("Please move to <#925466623668797490> to use this command!")

    @blowjob.error
    async def blowjob_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to give a blowjob!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command()
    @app_commands.describe(member="Select a member!")
    async def whip(self, ctx: commands.Context, *, member: str) -> None:
        """Whip someone"""

        gif_list = [
            "https://cdn.discordapp.com/attachments/760402160390373419/760434157133234186/whipping.gif",
            "https://cdn.discordapp.com/attachments/760402160390373419/760402205940645918/deJCBIjhVH3n2E4dyS9g2uo_7WWvVgjeImiTA5wT0SV9K8QGZVpeeW6IMtMOeyrEnzfM7GHQxVEG61UjdgxWPb0QNsRY7uWWxRUK.gif",
            "https://cdn.discordapp.com/attachments/760402160390373419/760409532974759976/giphy.gif",
            "https://cdn.discordapp.com/attachments/760402160390373419/760409924341334026/3e277ba0add9c21b90165e91c65406c92b6cdaf0_hq.gif",
            "https://cdn.discordapp.com/attachments/760402160390373419/760410311399964712/5b5.gif",
            "https://cdn.discordapp.com/attachments/730825643272568964/760399708068773918/image0.gif",
        ]
        embed = discord.Embed(
            description=f"{ctx.author.mention} whips {member}!", color=0xFF6666
        )
        embed.set_image(url=random.choice(gif_list))
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @whip.error
    async def whip_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention a user to whip!")

        else:
            await ctx.send(error)

    @app_commands.command()
    @app_commands.describe(member="Select a member!")
    async def titties(self, ctx: commands.Context, *, member: str) -> None:
        if ctx.channel.id == 925466623668797490:
            """Play with some titties!"""

            titties = [
                "https://media.discordapp.net/attachments/936876239837356042/1051316483587850321/245123_-_Ikki_Tousen_Ryofu_Housen_animated.gif?width=584&height=438",
                "https://media.discordapp.net/attachments/936876239837356042/1051316483222929418/anime-boobs.gif",
                "https://media.discordapp.net/attachments/936876239837356042/1051316482866425926/detail.gif",
                "https://media.discordapp.net/attachments/936876239837356042/1051316482480537721/tits_undress_gif-4431.gif?width=584&height=438",
                "https://media.discordapp.net/attachments/936876239837356042/1051315927972577361/giphy-2.gif",
                "https://media.discordapp.net/attachments/936876239837356042/1051315927548964944/indeed-she-is.gif",
                "https://media.discordapp.net/attachments/936876239837356042/1051315927079198780/268466e0b25bf2b7c1219a7b17bf56c9.gif?width=778&height=437",
                "https://media.discordapp.net/attachments/936876239837356042/1051315926659772427/3c6.gif",
                "https://media.discordapp.net/attachments/936876239837356042/1051315926252920925/29.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} tiddies {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(titties))

            await ctx.send(embed=embed)

        else:
            await ctx.send("Please move to <#925466623668797490> to use this command!")

    @titties.error
    async def titties_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to play with titties!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command()
    @app_commands.describe(member="Select a member!")
    async def peg(self, ctx: commands.Context, *, member: str) -> None:
        if ctx.channel.id == 925466623668797490:
            """Wanting to peg someone!"""

            pegging = [
                "https://cdn.discordapp.com/attachments/923130001312870410/1052098326834728960/2ab8f192a017ea32d4fddd074eb11923.gif",
                "https://cdn.discordapp.com/attachments/923130001312870410/1052098327212199946/bdc3afa50475ed6c927b66e0586668a5.gif",
                "https://cdn.discordapp.com/attachments/923130001312870410/1052098327606468618/l7kd8ncldd2a1.gif",
                "https://cdn.discordapp.com/attachments/923130001312870410/1052098327887482922/10470104.jpg.webp",
                "https://cdn.discordapp.com/attachments/923130001312870410/1052098328181100636/detail.gif",
                "https://cdn.discordapp.com/attachments/923130001312870410/1052098328487272539/wokada-futanari-pegging.gif",
                "https://cdn.discordapp.com/attachments/923130001312870410/1052098328797646948/aaa184aded96c5cef76574890a0ac281.gif",
                "https://cdn.discordapp.com/attachments/923130001312870410/1052098329099653180/artist-Buckethead-pictured-femdom-femdom-5200762.gif",
                "https://cdn.discordapp.com/attachments/923130001312870410/1052098329405825045/1becc080721ab1b76b6ec05bd135fb8c.gif",
            ]

            embed = discord.Embed(
                description=f"{ctx.author.mention} pegging {member}!", color=0xFF6666
            )

            embed.set_author(name=f"{ctx.guild.name}", icon_url=ctx.guild.icon.url)

            embed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)

            embed.set_image(url=random.choice(pegging))

            await ctx.send(embed=embed)

        else:
            await ctx.send("Please move to <#925466623668797490> to use this command!")

    @peg.error
    async def pegging_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention someone to peg them!")

        if isinstance(error, commands.BadArgument):
            await ctx.send("Couldn't find that user!")

        else:
            raise error

    @app_commands.command()
    async def role(self, ctx: commands.Context):
        """Posts a rolemenu"""

        embed = discord.Embed(color=0xFF6666)

        embed


async def setup(client):
    await client.add_cog(Misc(client))
