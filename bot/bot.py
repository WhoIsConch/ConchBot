import asyncio
import os
from itertools import cycle
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime
from bot.cogs.tags import Tags
from bot.cogs.Currency import Currency
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio
import time
import aiohttp

async def get_prefix(bot, message):
    prefixes = []
    prefixes.append('cb!')
    prefixes.append('cB ')
    prefixes.append('CB ')
    prefixes.append('Cb ')
    id = bot.user.id
    prefixes.append(f'<@!{id}> ')
    prefixes.append(f'<@!{id}>')
    return prefixes

load_env = load_dotenv()

class ConchBot(commands.Bot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        intents = discord.Intents.all()
        prefix = get_prefix
        super().__init__(command_prefix=prefix, intents=intents, allowed_mentions=allowed_mentions, case_insensitive=True, strip_after_prefix=True)
        self.launch_time = datetime.utcnow()
        os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
        os.environ['JISHAKU_RETAIN'] = "True"

        @self.before_invoke
        async def before_command(ctx):
            if ctx.command.cog.qualified_name == "NSFW" and not ctx.channel.is_nsfw():
                await ctx.send("This command can only be used in NSFW channels.")
                raise
            await Tags.create_table(self, ctx.guild.id)
            await Currency.open_account(self, ctx.author)


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
        statuses = cycle([f"{len(set(self.get_all_members()))} "
            f"users and {len(self.guilds)} servers.", "cb help"])
        while True:
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(statuses)))
            await asyncio.sleep(20)

    async def on_ready(self):
        print("------")
        print("ConchBot is online!")
        print("Note:The fact that in owner.py cog in bot/cogs folder. We used @commands.has_role(). You could replacing whats inside () with your owner role id/name or use @commands.is_owner() for only the owner can use.")
        self.up()
        await self.status_loop()

    async def create_aiohttp_session(self):
        self.aiohttp = aiohttp.ClientSession()
        print("AIOHTTP connection established.")

    def up(self):
        print("------")
        email_pass = os.getenv("EMAIL_PASS")
        from_address = os.getenv("EMAIL")
        to_address = os.getenv("STATUSEMAIL")
        message = MIMEMultipart('UP')
        message['Subject'] = 'UP'
        message['From'] = from_address
        message['To'] = to_address
        content = MIMEText(f'ConchBot is Up!', 'plain')
        message.attach(content)
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(from_address, email_pass)
        mail.sendmail(from_address,to_address, message.as_string())
        mail.close()
        print("Successfully sent email")

    def down(self):
        print("------")
        email_pass = os.getenv("EMAIL_PASS")
        from_address = os.getenv("EMAIL")
        to_address = os.getenv("STATUSEMAIL")
        message = MIMEMultipart('DOWN')
        message['Subject'] = 'DOWN'
        message['From'] = from_address
        message['To'] = to_address
        content = MIMEText(f'ConchBot is Down!', 'plain')
        message.attach(content)
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(from_address, email_pass)
        mail.sendmail(from_address,to_address, message.as_string())
        mail.close()
    
    async def shutdown(self):
        print("------")
        print("Conch Bot Closing connection to Discord...")
        print("------")
        self.down()

    async def close(self):
        print("------")
        print("Conch Bot Closing on keyboard interrupt...\n")
        print("------")
        self.down()

    async def on_connect(self):
        print("------")
        print(f"Conch Bot Connected to Discord (latency: {self.latency*1000:,.0f} ms).")
        self.up()

    async def on_resumed(self):
        print("------")
        print("Conch Bot resumed.")
        self.up()

    async def on_disconnect(self):
        print("------")
        print("Conch Bot disconnected.")
        self.down()


    def run(self):
        time.sleep(2)
        self.load_cogs()
        print("Running bot...")

        TOKEN = os.getenv("TOKEN")
        
        super().run(TOKEN, reconnect=True)
