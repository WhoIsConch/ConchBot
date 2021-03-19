import asyncio
import os

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle

prefixes = ['cb ', 'Cb ', 'cB ']
client = commands.Bot(command_prefix=prefixes)
client.remove_command('help')
extensions = [
    "cogs.Help",
    "cogs.Misc",
    "cogs.Fun",
    "cogs.Support",
    "cogs.Utility",
    "cogs.DBLCog",
    "cogs.Snipe",
    "cogs.Currency"
]

for extension in extensions:
    client.load_extension(extension)
    print(f"{extension} has been loaded.")

@client.event
async def on_ready():
    print("ConchBot is online!")
    await client.loop.create_task(status_loop())

statuses = cycle(["NEW plethora of currency commands!", 
        "Revamped ConchBot!", "cb help"])

async def status_loop():
    while True:
        await client.change_presence(activity=discord.Game(next(statuses)))
        await asyncio.sleep(15)
        
load_dotenv('.env')
client.run(os.getenv('TOKEN'))
