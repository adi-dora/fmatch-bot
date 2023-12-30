from asyncio.exceptions import CancelledError
import io
import json
import textwrap
import traceback

import discord
import asyncio
from discord import message


import aiohttp
import os
from contextlib import redirect_stdout
from textwrap import indent

import datetime


from discord.ext import commands
from discord import app_commands
from discord.ext import tasks
from discord.ext.commands import when_mentioned_or
from datetime import datetime
from typing import Any, List, Optional, Type, Union

client = commands.Bot(
    command_prefix=when_mentioned_or("!"),
    intents=discord.Intents.all(),
    case_insensitive=True,
    description="General purpose bot for Tickets, Activity Management and Moderation, along with miscellaneous features.",
)

@client.event
async def on_ready():
    print("Up and running...")
    guild = client.get_guild(647209569285701642)
    channel = discord.utils.get(guild.text_channels, name="allton-3443")
    await channel.send(
        f"Up and running...\nBot ID:\n{client.user.id}\nLatency:"
        + str(client.latency * 1000)
        + " ms"
    )

    counter = 0

    for server in client.guilds:
        counter += server.member_count or 0

    activity = discord.Game(
        name=f"on {len(client.guilds)} servers with {counter} members!"
    )

    await client.change_presence(
        status=discord.Status.do_not_disturb, activity=activity
    )


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
    await client.start(os.getenv('BOT_TOKEN')
    )


@client.command(name="sync")
async def sync_slash_commands(ctx):
    try:
        x = await client.tree.sync()
        await ctx.message.add_reaction("✅")
        # print(x)
    except:
        traceback.print_exc()


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")
    await ctx.send(f"The {extension} cog has been loaded!")


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    await client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"The {extension} cog has been unloaded!")


@client.command()
@commands.is_owner()
async def reload(ctx, extension: Optional[str]):
    print("-" * 40)
    if extension is not None:
        await client.unload_extension(f"cogs.{extension}")
        await client.load_extension(f"cogs.{extension}")
        return await ctx.send(f"The {extension} cog has been reloaded!")

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.unload_extension(f"cogs.{filename[:-3]}")
            await client.load_extension(f"cogs.{filename[:-3]}")

    return await ctx.send("All cogs have been reloaded!")


@client.command()
async def link(ctx):
    e = discord.Embed(colour=0x1FBDAC)
    e.description = f" bruh (https://reddit.com)"
    await ctx.send(embed=e)


@client.command()
async def hastebin(ctx, *, data):
    data = bytes(str(data), "utf-8")
    async with aiohttp.ClientSession() as cs:
        async with cs.post("https://hastebin.com/documents", data=data) as r:
            res = await r.json()
            key = res["key"]
            return await ctx.send(f"https://hastebin.com/{key}")


@client.command(hidden=True, name="eval")
async def eval_(ctx: commands.Context, *, body: str):
    """Evaluates Python code."""

    env = {
        "ctx": ctx,
        "bot": client,
        "channel": ctx.channel,
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message,
        "discord": __import__("discord"),
    }

    env.update(globals())

    stdout = io.StringIO()

    to_compile = f'async def func():\n{indent(body, "  ")}'

    def paginate(text: str):
        """Simple generator that paginates text."""
        last = 0
        pages = []
        appd_index = curr = None
        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr
        if appd_index != len(text) - 1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != "", pages))

    try:
        exec(to_compile, env)  # pylint: disable=exec-used
    except Exception as exc:
        await ctx.send(f"```py\n{exc.__class__.__name__}: {exc}\n```")
        return await ctx.message.add_reaction("\u2049")

    func = env["func"]
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception:
        value = stdout.getvalue()
        await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        return await ctx.message.add_reaction("\u2049")

    else:
        value = stdout.getvalue()
        if ret is None:
            if value:
                try:
                    await ctx.send(f"```py\n{value}\n```")
                except Exception:
                    paginated_text = paginate(value)
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            await ctx.send(f"```py\n{page}\n```")
                            break
                        await ctx.send(f"```py\n{page}\n```")
        else:
            try:
                await ctx.send(f"```py\n{value}{ret}\n```")
            except Exception:
                paginated_text = paginate(f"{value}{ret}")
                for page in paginated_text:
                    if page == paginated_text[-1]:
                        await ctx.send(f"```py\n{page}\n```")
                        break
                    await ctx.send(f"```py\n{page}\n```")

    await ctx.message.add_reaction("\u2705")





    




try:
    loop = asyncio.get_running_loop()
except Exception:
    loop = None

if loop and loop.is_running():
    loop.create_task(load_extensions())
else:
    asyncio.run(load_extensions())
