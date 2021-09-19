import discord
from discord.ext import commands
import random

class Embeds:
    def __init__(self):
        self.cooldown_choices = [
        "Woah, slow down man",
        "A little too quick there",
        "Too fast man",
        "Spamming is cool"
    ]

    def OnError(self, command_name, time, *, reason : str):
        self.Embed = discord.Embed(title="Oh no an error occurred", color=discord.Color.red())
        self.Embed.add_field(name="Command Name: ", value=command_name)
        self.Embed.add_field(name="At: ", value=time)
        self.Embed.add_field(name="Reason", value=reason)
        return self.Embed



    def OnCooldown(self, *, ctx, error):
        self.cooldown_name = random.choice(self.cooldown_choices)
        self.Embed = discord.Embed(title=self.cooldown_name, description="You need to slow down and don't spam the bot\n Retry after {:.2f}".format(ctx.command.name, error.retry_after), color=discord.Color.red())
        return self.Embed

