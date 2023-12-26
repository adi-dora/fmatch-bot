import traceback
import discord
import random
from discord.ext import commands, tasks
from discord.interactions import Interaction
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFont, ImageDraw
import os
from dateutil import parser

from discord import app_commands
import datetime
from datetime import datetime as dt
import requests
from utils.level_utils import *


class Levels(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.sort_and_push_lb.start()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if message.content.startswith("!rank"):
            return
        try:
            level_json[str(message.author.id)]
        except KeyError:
            level_json[str(message.author.id)] = {
                "level": 1,
                "experience": 0,
                "position": len(level_json) + 1,
                "last_message": str(dt.now()),
            }
        else:
            if dt.now() - parser.parse(
                level_json[str(message.author.id)]["last_message"]
            ) < datetime.timedelta(minutes=2):
                return
            level_json[str(message.author.id)]["experience"] += random.randint(5, 10)
            level_json[str(message.author.id)]["last_message"] = str(dt.now())

            if (
                level_json[str(message.author.id)]["experience"]
                >= (level_json[str(message.author.id)]["level"] + 1) ** 3
            ):
                level_json[str(message.author.id)]["level"] += 1
                await message.reply(
                    f'{message.author.mention} has leveled up! They are now level {level_json[str(message.author.id)]["level"]}'
                )

    @tasks.loop(seconds=10)
    async def sort_and_push_lb(self):
        x = dict(
            sorted(level_json.items(), key=lambda k: k[1]["experience"], reverse=True)
        )
        for enum, val in enumerate(x):
            level_json[val]["position"] = enum + 1

        dump_level_json(level_json)

    @commands.command()
    async def rank(
        self,
        ctx: discord.Interaction,
        user: discord.Member | discord.User | None,
    ):
        try:
            if user is None:
                user = ctx.author

            if str(user.id) not in level_json:
                level = 1

                experience = 0

                position = len(level_json) + 1

                percentage = 0

                next_level = 8

                exp_format = f"{experience} / {next_level} Total EXP"

                current_format = f"{experience} / {next_level} EXP"
            else:
                user_data = level_json[str(user.id)]
                level = user_data["level"]

                experience = int(user_data["experience"])

                position = user_data["position"]

                last_level = int(level**3)

                next_level = int((level + 1) ** 3)

                difference_1 = next_level - last_level

                difference_2 = user_data["experience"] - last_level

                percentage_1 = difference_2 / difference_1

                percentage = int(percentage_1 * 100)

                exp_format = f"{experience} / {next_level} Total EXP"

                current_level_1 = next_level - last_level

                current_level_2 = experience - last_level

                current_format = f"{current_level_2} / {current_level_1} EXP"

            font_2 = ImageFont.truetype("./card/ArialCE.ttf", 40)

            font_1 = ImageFont.truetype("./card/ArialCE.ttf", 25)
            background = Image.open("./card/card.png").convert("RGBA")

            dot = Image.open("./card/dot.png").convert("RGBA")

            avatar = Image.open(
                requests.get(
                    user.display_avatar.with_format("png").with_size(1024).url,
                    stream=True,
                ).raw
            ).convert("RGBA")

            mask = Image.open("./card/mask.png").convert("L")

            output = ImageOps.fit(dot, mask.size, centering=(0.5, 0.5))

            output.putalpha(mask)

            if percentage == 0:
                pass

            elif percentage == 1:
                background.paste(dot, (113, 200), mask=output)

            else:
                x = 113

                background.paste(dot, (113, 200), mask=output)

                for i in range(2, percentage):
                    x += 7

                    background.paste(dot, (x, 200), mask=output)

            draw = ImageDraw.Draw(background)

            x = 1200 - ((1200 - 842) + font_2.getsize(str(level))[0])

            draw.text(
                (x, 80),
                str(level),
                font=font_2,
                stroke_width=1,
                stroke_fill=(255, 102, 102),
            )

            x = x - 120

            draw.text(
                (x, 80),
                f"Level:",
                font=font_2,
                stroke_width=1,
                stroke_fill=(255, 191, 225),
            )

            x = x - 40 - font_2.getsize(f"#{position}")[0]

            draw.text(
                (x, 80),
                f"#{position}",
                font=font_2,
                stroke_width=1,
                stroke_fill=(255, 191, 225),
            )

            x = x - 120

            draw.text(
                (x, 80),
                f"Rank:",
                font=font_2,
                stroke_width=1,
                stroke_fill=(255, 191, 225),
            )

            x = 1200 - ((1200 - 842) + font_1.getsize(f"{exp_format}")[0])

            draw.text(
                (x, 135),
                exp_format,
                font=font_1,
                stroke_width=1,
                stroke_fill=(207, 165, 165),
            )

            x = 1200 - ((1200 - 842) + font_1.getsize(f"{current_format}")[0])

            draw.text(
                (x, 170),
                current_format,
                font=font_1,
                stroke_width=1,
                stroke_fill=(207, 165, 165),
            )

            x = 120

            name = user.name

            y = 147

            font_3 = ImageFont.truetype("./card/ArialCE.ttf", 50)

            f = font_3.getsize(name)

            m = 18

            while f[0] >= 380:
                m -= 1

                name = name[0:m]

                f = font_3.getsize(name)

            draw.text(
                (x, y), name, font=font_3, stroke_width=1, stroke_fill=(255, 191, 225)
            )

            x = x + 15 + font_3.getsize(name)[0]

            mask2 = Image.open("./card/mask_2.png").convert("L")

            output2 = ImageOps.fit(avatar, mask2.size, centering=(0.5, 0.5))

            output2.putalpha(mask2)

            avatar = avatar.resize((229, 229))

            background.paste(avatar, (933, 46), mask=output2)

            x = user.id

            background.save(f"./cards/card_{x}.png", "PNG")

            await ctx.send(file=discord.File(f"./cards/card_{x}.png"))

            os.remove(f"./cards/card_{x}.png")
        except:
            traceback.print_exc()

    @commands.command()
    async def leaderboard(self, interaction: discord.Interaction):
        try:
            x = sorted(
                level_json.items(), key=lambda k: k[1]["experience"], reverse=True
            )
            if len(x) > 10:
                x = x[:10]

            x = dict(x)

            embed = discord.Embed(
                title="Current Leaderboard",
                timestamp=interaction.message.created_at,
                color=discord.Color.pink(),
            )
            embed.description = "\n".join(
                f"{num}. "
                + interaction.guild.get_member(int(user)).mention
                + f' ({x[user]["experience"]} EXP)'
                for num, user in enumerate(x.keys())
            )

            await interaction.send(embed=embed)
        except:
            traceback.print_exc()


async def setup(bot: commands.Bot):
    await bot.add_cog(Levels(bot))
