import asyncio
import datetime
import os
import traceback
from itertools import cycle

import aiosqlite
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from extras.errors import Blacklisted

# prefixes = ['cb!']
prefixes = ['cb ', 'Cb ', 'CB ', 'cB ']

client = commands.Bot(command_prefix=prefixes, intents=discord.Intents.all())
client.remove_command('help')
extensions = [
    "cogs.Help",
    "cogs.Misc",
    "cogs.Fun",
    "cogs.Support",
    "cogs.Utility",
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

@client.before_invoke
async def before_command(ctx):
    db = await aiosqlite.connect("config.db")
    cursor = await db.cursor()
    await cursor.execute("CREATE TABLE IF NOT EXISTS blacklist (id INT)")
    await cursor.execute(f"SELECT id FROM blacklist WHERE id = {ctx.author.id}")
    memcheck = await cursor.fetchone()
    if memcheck is not None:
        raise await Blacklisted(ctx).memsend()
    else:
        await cursor.execute(f"SELECT id FROM blacklist WHERE id = {ctx.guild.id}")
        guildcheck = await cursor.fetchone()
        if guildcheck is not None:
            raise await Blacklisted(ctx).guildsend()

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, but that command does not exist.")
    elif isinstance(error, commands.CommandOnCooldown):
        pass
    else:
        ctx.command.reset_cooldown(ctx)
        channel = client.get_channel(833508151802069002)
        now = datetime.datetime.now()
        time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
        await channel.send(f"Error occured at {time} invoked by {ctx.author} in {ctx.guild}. Error:\n```py\n{error}```")

async def status_loop():
    statuses = cycle(["New plethora of currency commands!", 
        "Revamped ConchBot!", "cb help", f"Watching {len(set(client.get_all_members()))} "
        f"users and {len(client.guilds)} servers.", "New memes and media commands!"])
    while True:
        await client.change_presence(activity=discord.Game(next(statuses)))
        await asyncio.sleep(15)
        
load_dotenv('.env')
client.run(os.getenv('TOKEN'))
