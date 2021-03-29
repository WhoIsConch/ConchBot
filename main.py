import asyncio
import os

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle

prefixes = ['cb ', 'cB ', 'Cb ', 'CB ']
client = commands.Bot(command_prefix=prefixes, intents=discord.Intents.all())
client.remove_command('help')
extensions = [
    "cogs.Help",
    "cogs.Misc",
    "cogs.Fun",
    "cogs.Support",
    "cogs.Utility",
    "cogs.DBLCog",
    "cogs.Snipe",
    "cogs.Currency",
    "cogs.Image",
    "cogs.Secret"
]

for extension in extensions:
    client.load_extension(extension)
    print(f"{extension} has been loaded.")

@client.event
async def on_ready():
    print("ConchBot is online!")
    await client.loop.create_task(status_loop())

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, but that command does not exist.")
    else:
        print(error)

async def status_loop():
    statuses = cycle(["New plethora of currency commands!", 
        "Revamped ConchBot!", "cb help", f"Watching {len(set(client.get_all_members()))} "
        f"users and {len(client.guilds)} servers.", "New memes and media commands!"])
    while True:
        await client.change_presence(activity=discord.Game(next(statuses)))
        await asyncio.sleep(15)
        
load_dotenv('.env')
client.run(os.getenv('TOKEN'))
