import asyncio
import datetime
import os
from itertools import cycle
import aiosqlite
import discord
from discord.ext import commands
from discord.ext.commands.core import before_invoke
from dotenv import load_dotenv

from bot.cogs.utils import errors

load_env = load_dotenv()



def prefix(bot, message):
    prefixes = aiosqlite.connect('db/config.db')
    cursor = prefixes.cursor()
    cursor.execute(f"SELECT prefix from prefixes WHERE guildid = '{message.guild.id}'")
    result = cursor.fetchone()
    prefix = str(result[0])
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ', 'cb ', 'Cb ', 'CB ', 'cB ']
    base.append(prefix)
    return base

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            messages=True,
            reactions=True,
        )
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        super().__init__(command_prefix=prefix, intents=intents, allowed_mentions=allowed_mentions)
    

    def load_cogs(self):
        if discord.ext.commands.errors.ExtensionAlreadyLoaded:
            pass
        else:
            print("Loading All cogs...")
            print("------")
            for filename in os.listdir(f"./bot/cogs"):
                if filename.endswith(f".py"):
                    self.load_extension(f"bot.cogs.{filename[:-3]}")
                    print(f"Loaded `{filename[:20]}` Cog")
            self.remove_command('help')

    def on_ready(self):
        print("ConchBot is online!")

    


    def setup(self):
        self.load_cogs()
        self.on_ready()
        

    def run(self):
        self.setup()

        TOKEN = os.getenv("TOKEN")
        
        print("Running bot...")
        super().run(TOKEN, reconnect=True)
            


