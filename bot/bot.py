import asyncio
import os
from itertools import cycle
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from bot.cogs.utils import errors

load_env = load_dotenv()





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
        super().__init__(command_prefix=self.prefix, intents=intents, allowed_mentions=allowed_mentions)
    
    def prefix(self):
        user_id = self.user.id
        base = [f'<@!{user_id}> ', f'<@{user_id}> ', 'cb ', 'Cb ', 'CB ', 'cB ']
        return base


    def load_cogs(self):
        self.remove_command('help')
        print("Loading All cogs...")
        print("------")
        for filename in os.listdir(f"./bot/cogs"):
            if filename.endswith(f".py"):
                self.load_extension(f"bot.cogs.{filename[:-3]}")
                print(f"Loaded `{filename[:20]}` Cog")
        print("------")
        self.load_extension('jishaku')
        print("Loaded `jishaku`")

    @tasks.loop(seconds=15.0)
    async def status_loop(self):
        statuses = cycle(["New plethora of currency commands!", 
            "Revamped ConchBot!", "cb help", f"Watching {len(set(self.get_all_members()))} "
            f"users and {len(self.guilds)} servers.", "New memes and media commands!"])
        while True:
            await self.change_presence(activity=discord.Game(next(statuses)))
            await asyncio.sleep(15)


            
    async def on_ready(self):
        print("ConchBot is online!")
        await self.status_loop()

    def run(self):
        self.load_cogs()
        print("Running bot...")

        TOKEN = os.getenv("TOKEN")
        
        super().run(TOKEN, reconnect=True)


        

    
            


