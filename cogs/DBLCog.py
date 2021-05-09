import asyncio
import datetime
import os

import aiosqlite
import dbl
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from .Currency import Currency

load_dotenv('.env')
dbltoken = os.getenv('DBLTOKEN')

class DBLcog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dbl = dbl.DBLClient(self.client, dbltoken, autopost=True, webhook_path='/dblwebhook', webhook_auth='69420', webhook_port=5000)

    async def getvotes(self):
        return await self.dbl.get_bot_upvotes()

    @commands.group(invoke_without_command=True)
    async def vote(self, ctx):
        embed = discord.Embed(title="Vote for ConchBot", colour=discord.Colour.blue())
        embed.add_field(name="Perks", value="Voting for ConchBot gets you awesome perks, such as unlocked commands and currency items!")
        embed.add_field(name="Top.gg", value="You can vote for ConchBot on Top.gg [here!](https://top.gg/bot/733467297666170980/vote)")
        embed.add_field(name="Discord Bot List", value="You can vote for ConchBot on Discord Bot List [here!](https://discord.ly/conchbot)")
        embed.set_footer(text="When you're done voting, please use the \"cb vote claim\" command to claim your reward!")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        channel = self.client.get_channel(724050498847506436)
        user = self.client.get_user(int(data['user']))
        if user is None:
            pass
        else:
            await user.send("Thanks for voting for ConchBot! Due to this, you'll get awesome perks, such as:"
            "\nUnlocked image commands!\nNo message on the AI!\nA `bronze conch` currency item! (Use with `cb use bronze`)")
        await Currency.item_func(self, user, "Bronze Conch", 1)

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count successfully posted!")

def setup(client):
    client.add_cog(DBLcog(client))
