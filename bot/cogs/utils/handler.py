import discord
from discord.ext import commands
import sys
import asyncio
from dotenv import load_dotenv
import os
import datetime
from bot.cogs.tags import Tags
from bot.cogs.utils.embed import Embeds

env = load_dotenv()

class CommandErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.time = datetime.datetime.utcnow().strftime('%Y:%m:%d %H:%M:%S')

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

        if isinstance(error, IndexError):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The number value you input was invalid")
            await ctx.send(embed=embed)        
        elif isinstance(error, commands.NoPrivateMessage):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The command can not be used in private messages")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.DisabledCommand):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The command is currently disabled and cannot be used")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            embed = Embeds().OnCooldown(ctx, error)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.errors.NotOwner):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The command is only used by the owner")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.ChannelNotFound):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The channel couldn't be found")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "The user couldn't be found")
            await ctx.send(embed=embed)
        elif isinstance(error, discord.Forbidden):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "I am forbidden to do this")
            await ctx.send(embed=embed)
        elif isinstance(error, discord.NotFound):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "Couldn't find what you need")
            await ctx.send(embed=embed)
        elif isinstance(error, asyncio.TimeoutError):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "You have been timed out because you didn't respond in time")
            await ctx.send(embed=embed)          
        elif isinstance(error, discord.HTTPException):
            embed = Embeds().OnError(ctx.command.qualified_name, self.time, "Something went wrong... Please Contact: Jerry.py#4249 or UnsoughtConch#9225 if it keeps happening")
            await ctx.send(embed=embed)
        if not isinstance(error, discord.HTTPException):
            try:
                print(error, file=sys.stderr)
            except:
                print(error, file=sys.stderr)
        else:
            creator = await self.bot.fetch_user(os.getenv("OWNER_ID"))
            embed = discord.Embed(title="Oh no. An error occurred")
            embed.add_field(
                name=f"In {ctx.command.qualified_name}:", 
                value=f"""```py
            {error.__class__.__name__}: {error} - {sys.stderr}
            ```"""
            )
            await creator.send(embed=embed)

def setup(client):
    client.add_cog(CommandErrorHandler(client))
        
