from inspect import istraceback
import discord
from discord.ext import commands
import sys
import asyncio
from dotenv import load_dotenv
import os
import datetime
from bot.cogs.tags import Tags
import traceback

env = load_dotenv()

class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            error = error.original
        except:
            error = error
            
        if isinstance(error, commands.CommandNotFound):
            try:
                e = await Tags.get_tag(self, ctx.guild.id, ctx.message.content[3:])
                if e is False:
                    return
                else:
                    return await ctx.send(e[0])
                    
            except:
                return

        if isinstance(error, discord.errors.HTTPException):
            await ctx.send("Something went wrong. Note: The bot might be ratelimited")
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'The command has been disabled.')
            return
        
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You are cooldown. Please try again in **{error.retry_after:.2f}s**")
            return

        if isinstance(error, commands.errors.NotOwner):
            await ctx.send("This command is restricted to bot owners.")
            return

        if isinstance(error, IndexError):
            await ctx.send("That's not a valid number choice.")
            return

        if isinstance(error, ValueError):
            await ctx.send("You must seperate some values with a comma.")
            return

        if isinstance(error, commands.ChannelNotFound):
            print(f"| {error} | ")
            await ctx.send("Channel doesn't exist")

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permissions to do that! Please contact a server admin to do that for you.")
            return
        
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("That member doesn't exist.")
            return

        if isinstance(error, commands.MissingRole):
            await ctx.send("You don't have have the role to use this")

        if isinstance(error, discord.Forbidden):
            await ctx.send("I can't do this. I'm forbidden to do this.")

        if isinstance(error, discord.NotFound):
            await ctx.send("Couldn't find that sorry")
            return

        if isinstance(error, asyncio.TimeoutError):
            await ctx.send("You waited too long :(")
            return

        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send("There are required arguements/parameters you need to input")
            return

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'Command can not be used in Private Messages.')
                return
            except discord.HTTPException:
                await ctx.send("Something went wrong. We'll report it. Note: The bot might be ratelimited")
        

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')
                return
            else:
                await ctx.send("You were supposed to type that but you ended typing that")
                return

        else:
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(833508151802069002)
            e = traceback.format_exception(type(error), error, error.__traceback__)
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')
            return

def setup(client):
    client.add_cog(CommandErrorHandler(client))
        
