import discord
from discord.ext import commands
import random
import datetime

class Embeds:
    def __init__(self):
        self.cooldown_choices = [
        "Woah, slow down man",
        "A little too quick there",
        "Too fast man",
        "Spamming is cool"
    ]
        self.time = datetime.datetime.utcnow().strftime('%Y:%m:%d %H:%M:%S')

    def OnError(self, command_name : str, time : str, *, reason : str):
        self.Embed = discord.Embed(title="Oh no an error occurred", color=discord.Color.red())
        self.Embed.add_field(name="Command Name: ", value=command_name)
        self.Embed.add_field(name="At: ", value=time)
        self.Embed.add_field(name="Reason", value=reason)
        return self.Embed

    def OnCooldown(self, *, ctx=commands.Context, error : str):
        self.cooldown_name = random.choice(self.cooldown_choices)
        self.Embed = discord.Embed(title=self.cooldown_name, description="You need to slow down and don't spam the bot\n Retry after {:.2f}".format(ctx.command.name, error.retry_after), color=discord.Color.blue())
        return self.Embed

    def OnApiError(self, *, command_name : str, status : int):
        self.Embed = discord.Embed(title="Oh no an error occurred", color=discord.Color.red(), description="Sorry but something went wrong. DM Jerry.py#4249 if it keeps happening")
        self.Embed.add_field(name="Command Name: ", value=command_name)
        self.Embed.add_field(name="At: ", value=self.time)
        self.Embed.add_field(name="API Status", value=status)
        return self.Embed

