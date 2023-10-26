import json
import random
import traceback
from typing import Optional
from unicodedata import name
import discord
import datetime
from discord.ext import commands, tasks
from discord.interactions import Interaction
import uuid
from dateutil import parser
import typing

from typing_extensions import Annotated


from discord import Permissions, app_commands
from datetime import datetime as dt

from discord.app_commands import Choice
from discord.app_commands import AppCommandError



class Checklist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    checklist = app_commands.Group(name = 'checklist', description='Create and manage a checklist!')

    @checklist.command()
    async def list(self, interaction: discord.Interaction):
        try:
            with open('checklist.json', 'r') as f:
                checklist = json.load(f)
            embed = discord.Embed(title='Checklist', color=discord.Color.green(), timestamp=interaction.created_at)

            checklist["needed"].sort()
            checklist["done"].sort()
            checklist["removed"].sort()
            checklist["order"].sort()
            needed = "\n".join(item.title() for item in checklist["needed"])
            done = "\n".join(item.title() for item in checklist['done'])
            removed = "\n".join(item.title() for item in checklist['removed'])
            order = "\n".join(item.title() for item in checklist['order'])
            embed.add_field(name=f'Needed ({len(checklist["needed"])})', value=needed)
            embed.add_field(name=f'Done ({len(checklist["done"])})', value=done)
            embed.add_field(name=f'Removed ({len(checklist["removed"])})', value=removed)
            embed.add_field(name=f'To be Bought {len(checklist["order"])}', value=order)

            await interaction.response.send_message(embed=embed)
        except:
            traceback.print_exc()

    @checklist.command()
    async def unorder(self, interaction: discord.Interaction, item: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        checklist['needed'].append(checklist['order'].pop(checklist['order'].index(item)))

        with open('checklist.json', 'w') as f:
            json.dump(checklist, f)
        
        await interaction.response.send_message(f'Moved {item.title()} from the ``Order`` tab to the ``Needed`` tab')
        

        
    
    @unorder.autocomplete('item')
    async def unorder_autocomplete(self, interaction: discord.Interaction, query: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        return [app_commands.Choice(name=item.title(), value=item) for item in checklist['order'] if query.lower() in item.lower()]

    @checklist.command()
    async def add(self, interaction: discord.Interaction, item: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        if item.lower() in checklist['needed']:
            return await interaction.response.send_message(f'{item.title()} is already in the ``Needed`` tab!')
        
        if item.lower() in checklist['done']:
            return await interaction.response.send_message(f'{item.title()} is already in the ``Done`` tab!')
        if item.lower() in checklist['removed']:
            checklist['removed'].remove(item.lower())
            checklist['needed'].append(item.lower())
            with open('checklist.json', 'w') as f:
                json.dump(checklist, f)
            
            return await interaction.response.send_message(f'Moved {item.title()} from the ``Removed`` tab to the ``Needed`` tab!')
        
        checklist['needed'].append(item.lower())
        with open('checklist.json', 'w') as f:
            json.dump(checklist, f)
        
        await interaction.response.send_message(f'Added {item.title()} to the ``Needed`` tab.')


    @checklist.command()
    async def check(self, interaction: discord.Interaction, item: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        

        try:
        
            checklist['done'].append(checklist['needed'].pop(checklist['needed'].index(item)))

            with open('checklist.json', 'w') as f:
                json.dump(checklist, f)
            
            await interaction.response.send_message(f'Moved {item.title()} from the ``Needed`` tab to the ``Done`` tab')
        
        except:
            await interaction.response.send_message('The item provided was invalid!')

    @checklist.command()
    async def uncheck(self, interaction: discord.Interaction, item: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        try:
        
            checklist['needed'].append(checklist['done'].pop(checklist['done'].index(item)))

            with open('checklist.json', 'w') as f:
                json.dump(checklist, f)
            
            await interaction.response.send_message(f'Moved {item.title()} from the ``Done`` tab to the `` Needed`` tab')
        
        except:
            await interaction.response.send_message('The item provided was invalid!')

    @checklist.command()
    async def delete(self, interaction: discord.Interaction, item: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        if item in checklist['needed']:
            checklist['needed'].remove(item)
        
        if item in checklist['done']:
            checklist['done'].remove(item)
        
        if item in checklist['removed']:
            checklist['done'].remove(item)
        
        with open('checklist.json', 'w') as f:
            json.dump(checklist, f)
        
        await interaction.response.send_message(f'{item.title()} has been deleted from the list.')
    
    @checklist.command()
    async def remove(self, interaction: discord.Interaction, item: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        try:
        
            checklist['removed'].append(checklist['needed'].pop(checklist['needed'].index(item)))

            with open('checklist.json', 'w') as f:
                json.dump(checklist, f)
            
            await interaction.response.send_message(f'Moved {item.title()} from the ``Needed`` tab to the `` Removed`` tab')
        
        except:
            await interaction.response.send_message('The item provided was invalid!')
        

        

    @checklist.command()
    async def buy(self, interaction: discord.Interaction, item: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        checklist['order'].append(checklist['needed'].pop(checklist['needed'].index(item)))

        with open('checklist.json', 'w') as f:
            json.dump(checklist, f)

        await interaction.response.send_message(f'Moved {item.title()} from the ``Needed`` tab to the ``To Be Bought`` tab')     
        





    @check.autocomplete('item')
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        return [app_commands.Choice(name=item.title(), value=item) for item in checklist['needed'] if current.lower() in item]
    
    @buy.autocomplete('item')
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        return [app_commands.Choice(name=item.title(), value=item) for item in checklist['needed'] if current.lower() in item]
    
    @remove.autocomplete('item')
    async def remove_callback(self, interaction: discord.Interaction, current: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        return [app_commands.Choice(name=item.title(), value=item) for item in checklist['needed'] if current.lower() in item]


    @uncheck.autocomplete('item')
    async def uncheck_callback(self, interaction: discord.Interaction, current: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        return [app_commands.Choice(name=item.title(), value=item) for item in checklist['done'] if current.lower() in item]
    
    @delete.autocomplete('item')
    async def delete_callback(self, interaction: discord.Interaction, current: str):
        with open('checklist.json', 'r') as f:
            checklist = json.load(f)
        
        needed = [app_commands.Choice(name=item.title(), value=item) for item in checklist['needed'] if current.lower() in item]
        
        done = [app_commands.Choice(name=item.title(), value=item) for item in checklist['done'] if current.lower() in item]

        removed = [app_commands.Choice(name=item.title(), value=item) for item in checklist['removed'] if current.lower() in item]

        final_list = []
        for item in needed:
            final_list.append(item)
        
        for item in done:
            final_list.append(item)
        
        for item in removed:
            final_list.append(item)
        
        return final_list
        


async def setup(bot):
    await bot.add_cog(Checklist(bot))