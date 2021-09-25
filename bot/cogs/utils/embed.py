from os import stat
import discord
from discord.ext import commands
import random
import datetime

class Embeds():
    def __init__(self):
        self.cooldown_choices = [
            "Woah, slow down man",
            "A little too quick there",
            "Too fast man",
            "Spamming is cool"
        ]
        self.time = datetime.datetime.utcnow().strftime('%Y:%m:%d %H:%M:%S')
        self.error_codes = {
            400 : "Bad request",
            401 : "Unauthorized",
            403 : "Forbidden",
            404 : "Page Not found",
            429 : "Too many requests",
        }

    def OnError(self, command_name : str, time : str, *, reason : str):
        self.Embed = discord.Embed(title="Oh no an error occurred", color=discord.Color.red())
        self.Embed.add_field(name="Command Name: ", value=command_name)
        self.Embed.add_field(name="At: ", value=time)
        self.Embed.add_field(name="Reason", value=reason)
        return self.Embed

    def OnCooldown(self, *, error : str):
        self.cooldown_name = random.choice(self.cooldown_choices)
        self.Embed = discord.Embed(title=self.cooldown_name, description=f"You need to slow down and don't spam the bot\n Retry after {int(error.retry_after)}s", color=discord.Color.blue())
        return self.Embed

    def OnApiError(self, *, command_name : str, status : int):
        self.Embed = discord.Embed(title="Oh no an error occurred", color=discord.Color.red(), description="Sorry but something went wrong. DM Jerry.py#4249 if it keeps happening")
        self.Embed.add_field(name="Command Name: ", value=command_name)
        self.Embed.add_field(name="At: ", value=self.time)
        if status in self.error_codes:
            status_reason = self.error_codes[status]
            self.Embed.add_field(name="API Status", value=f"{status} - {status_reason}")
        else:
            self.Embed.add_field(name="API Status", value=f"{status}")
        return self.Embed

    @staticmethod
    def get_error_codes():
        error_codes = {
            400 : "Bad request",
            401 : "Unauthorized",
            403 : "Forbidden",
            404 : "Page Not found",
            429 : "Too many requests",
        }
        return error_codes

    @staticmethod
    def get_all_cooldown_messages():
        cooldown_choices = [
            "Woah, slow down man",
            "A little too quick there",
            "Too fast man",
            "Spamming is cool"
        ]
        return cooldown_choices

    @staticmethod
    def time():
        return datetime.datetime.utcnow().strftime('%Y:%m:%d %H:%M:%S')
