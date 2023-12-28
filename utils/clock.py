import discord

from discord.ext import commands

import datetime, typing, asyncio, json, traceback
from utils.vote_utils import *


class Clock:  # Due to the size of this script, we will make a seperate class for it
    """The class for interfacing with reminders"""

    instances = []

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.endtime: typing.Optional[
            datetime.datetime
        ] = None  # Our current closest endtime
        self._task: typing.Optional[
            asyncio.Task
        ] = None  # The task that is currently running
        self.reminder: dict = None
        Clock.instances.append(self)

        self.bot.setup_hook = self.setup_hook

    async def setup_hook(self):
        self.bot.loop.create_task(self.update())  # Telling our code to update

    def get_closest_reminder(self) -> dict | None:
        """This is just finding the closest ending reminder"""
        with open("reminders.json", "r") as f:
            reminders = json.load(f)

        if len(reminders["reminders"]) == 0:
            return None

        reminders["reminders"] = sorted(
            reminders["reminders"], key=lambda k: k["endtime"]
        )

        with open("reminders.json", "w") as f:
            json.dump(reminders, f, indent=1)

        return reminders["reminders"][0]

    async def create(
        self,
        reminder: str,
        channel_id: int,
        message_id: int,
        user_id: int,
        endtime: datetime.datetime,
    ) -> dict:
        """Creating a new reminder"""
        with open("reminders.json", "r") as f:
            reminders = json.load(f)
        reminders["reminders"].append(
            {
                "user_id": user_id,
                "reminder": reminder,
                "channel_id": channel_id,
                "message_id": message_id,
                "endtime": endtime.timestamp(),
            }
        )

        if (
            not self._task or self._task.done()
        ) or endtime < self.endtime:  # if the timer ends sooner then the current scheduled one
            if self._task and not self._task.done():
                self._task.cancel()
            self._task = self.bot.loop.create_task(self.end_timer(endtime))

            self.endtime = endtime
            self.reminder = reminders["reminders"][-1]

        with open("reminders.json", "w") as f:
            json.dump(reminders, f, indent=1)

        return self.reminder  # just return the id we want

    async def update(self):
        """Gets the closest reminder and schedules it"""
        reminder = self.get_closest_reminder()
        print(reminder)
        if not reminder:
            return
        if (
            not self._task or self._task.done()
        ):  # if the task is done or no task exists we just create the task
            self.endtime = datetime.datetime.fromtimestamp(
                reminder["endtime"]
            )  # store the endtime
            self._task = self.bot.loop.create_task(self.end_timer(self.endtime))
            self.reminder = reminder  # store the id
            return

        if (
            datetime.datetime.fromtimestamp(reminder["endtime"]) < self.endtime
        ):  # Otherwise, if the reminder ends sooner then the current closest endtime
            self._task.cancel()  # cancel the task
            self._task = self.bot.loop.create_task(
                self.end_timer(datetime.datetime.fromtimestamp(reminder["endtime"]))
            )
            self.endtime = datetime.datetime.fromtimestamp(
                reminder["endtime"]
            )  # store the endtime
            self.reminder = reminder  # store the id

    async def end_timer(self, endtime):
        try:
            print("Endtime 2: ", endtime)
            await discord.utils.sleep_until(endtime)  # sleeping until the endtime

            # send your message here
            user = self.bot.get_user(self.reminder["user_id"])
            if self.reminder["channel_id"] is None:
                await user.send(
                    embed=discord.Embed(
                        title="Vote Reminder",
                        description=f"It has been 12 hours since your last vote!\n\n [Click here to vote!]({vote_json['topgg_server_link']})",
                        color=discord.Color.pink(),
                        timestamp=datetime.datetime.now(),
                    )
                )
            else:
                channel = await self.bot.fetch_channel(self.reminder["channel_id"])
                msg = channel.get_partial_message(self.reminder["message_id"])
                await msg.reply(
                    f'{user.mention} to be reminded of: {self.reminder["reminder"]}'
                )

            with open("reminders.json", "r") as f:
                reminders = json.load(f)

            reminders["reminders"].remove(self.reminder)
            with open("reminders.json", "w") as f:
                json.dump(reminders, f, indent=1)
            self.bot.loop.create_task(self.update())  # re update
        except:
            traceback.print_exc()

    def stop(self):
        self._task.cancel()
