from inspect import istraceback
import discord
from discord.ext import commands
import sys
import traceback
from dotenv import load_dotenv
import os
import datetime

env = load_dotenv()

class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Command: `{ctx.command.name}` doesn't exist")


        if isinstance(error, discord.errors.HTTPException):
            await ctx.send("Something went wrong. We'll report it. Note: The bot might be ratelimited")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')
        
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You are cooldown for the command `{ctx.command.name}`. Please try again in {error.retry_after:.2f}s")
        
        if isinstance(error, discord.ext.commands.errors.NotOwner):
            await ctx.send("You are not the owner of this bot so you can't use this command")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                await ctx.send("Something went wrong. We'll report it. Note: The bot might be ratelimited")
                now = datetime.datetime.now()
                time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
                error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
                await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')
        

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')
        


        else:
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')
            

def setup(client):
    client.add_cog(CommandErrorHandler(client))
        
