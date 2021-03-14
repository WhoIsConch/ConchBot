import asyncio
import os

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

prefixes = ['cb ', 'cB', 'CB', 'Cb']
client = commands.Bot(command_prefix=prefixes)
client.remove_command('help')
extensions = [
    "cogs.Help",
    "cogs.Misc",
    "cogs.Fun",
    "cogs.Support",
    "cogs.Utility",
    "cogs.DBLCog",
    "cogs.Snipe"
]

for extension in extensions:
    client.load_extension(extension)
    print(f"{extension} has been loaded.")

@client.event
async def on_ready():
    print("ConchBot is online!")
    await client.loop.create_task(status_loop())

async def status_loop():
    while True:
        await client.change_presence(activity=discord.Game(name=f"with {len(client.guilds)} awesome servers!"))
        await asyncio.sleep(300)
        
load_dotenv('.env')
client.run(os.getenv('TOKEN'))
