import asyncio
import datetime
import os
from itertools import cycle
import aiosqlite
import discord
from discord.ext import commands
from dotenv import load_dotenv

from cogs.utils import errors

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
	self.TOKEN = os.getenv("TOKEN")
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        super().__init__(command_prefix=prefix, intents=intents, allowed_mentions=allowed_mentions)
	

    def load_cogs(self):
        extensions = [
            "cogs.Help",
            "cogs.Misc",
            "cogs.Fun",
            "cogs.Support",
            "cogs.Utility",
            "cogs.Snipe",
            "cogs.Currency",
            "cogs.Image",
            "cogs.Secret",
            "cogs.owner",
            "cogs.tags",
            "cogs.nsfw"
        ]
        for extension in extensions:
            self.load_extension(extension)
            print(f"{extension} has been loaded.")
            self.remove_command('help')

    def status_loop(self):
        statuses = cycle(["New plethora of currency commands!", 
            "Revamped ConchBot!", "cb help", f"Watching {len(set(self.get_all_members()))} "
            f"users and {len(self.guilds)} servers.", "New memes and media commands!"])
        while True:
            self.change_presence(activity=discord.Game(next(statuses)))
            asyncio.sleep(15)

    def on_ready(self):
        print("ConchBot is online!")
        self.loop.create_task(self.status_loop)

    def run(self): 
	super().run(self.TOKEN, reconnect=True)

    def before_command(ctx):
        db = aiosqlite.connect("db/config.db")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS blacklist (id INT)")
        cursor.execute(f"SELECT id FROM blacklist WHERE id = {ctx.author.id}")
        memcheck = cursor.fetchone()
        if memcheck is not None:
            raise errors.Blacklisted(ctx).memsend()
        else:
            cursor.execute(f"SELECT id FROM blacklist WHERE id = {ctx.guild.id}")
            guildcheck = cursor.fetchone()
            if guildcheck is not None:
                raise errors.Blacklisted(ctx).guildsend()
        if ctx.cog.qualified_name == "NSFW" and not ctx.channel.is_nsfw():
            raise errors.NSFWCmd(ctx).send()

            


