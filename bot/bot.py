import asyncio
import os
from itertools import cycle
import discord
from discord.ext import commands, tasks
from discord.ext.commands.bot import when_mentioned_or
from dotenv import load_dotenv
from datetime import datetime

load_env = load_dotenv()

class ConchBot(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents = discord.Intents.all()
        super().__init__(command_prefix=when_mentioned_or('cb ', 'cB ', 'Cb ', 'CB ', 'cb', 'cB', 'Cb', 'CB'), intents=intents, allowed_mentions=allowed_mentions, case_insensitive=True)
        self.launch_time = datetime.utcnow()


    def load_cogs(self):
        self.remove_command('help')
        print("Loading All cogs...")
        print("------")
        for filename in os.listdir(f"./bot/cogs"):
            if filename.endswith(f".py"):
                self.load_extension(f"bot.cogs.{filename[:-3]}")
                print(f"Loaded `{filename[:20]}` Cog")
        print("------")   
        self.load_extension('bot.cogs.utils.handler')
        print("Loaded Error Handler")
        print("------")
        self.load_extension('jishaku')
        print("Loaded `jishaku`")
        print("------")

    @tasks.loop(seconds=15.0)
    async def status_loop(self):
        statuses = cycle(["New plethora of currency commands!", 
            "Revamped ConchBot!", "cb help", f"Watching {len(set(self.get_all_members()))} "
            f"users and {len(self.guilds)} servers.", "New memes and media commands!"])
        while True:
            await self.change_presence(activity=discord.Game(next(statuses)))
            await asyncio.sleep(15)
            
    async def on_ready(self):
        print("------")
        print("ConchBot is online!")
        print("Note:The fact that in owner.py cog in bot/cogs folder. We used @commands.has_role(). You could replacing whats inside () with your owner role id/name or use @commands.is_owner() for only the owner can use.")
        await self.status_loop()
    
    async def shutdown(self):
        print("------")
        print("Conch Bot Closing connection to Discord...")
        print("------")

    async def close(self):
        print("------")
        print("Conch Bot Closing on keyboard interrupt...\n")
        print("------")

    async def on_connect(self):
        print("------")
        print(f"Conch Bot Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("------")
        print("Conch Bot resumed.")

    async def on_disconnect(self):
        print("------")
        print("Conch Bot disconnected.")

    def run(self):
        self.load_cogs()
        print("Running bot...")

        TOKEN = os.getenv("TOKEN")
        
        super().run(TOKEN, reconnect=True)
