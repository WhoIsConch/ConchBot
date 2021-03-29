import dbl
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os

load_dotenv('.env')
dbltoken = os.getenv('DBLTOKEN')

class DBLcog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dbl = dbl.DBLClient(self.client, dbltoken, autopost=True, webhook_path='/dblwebhook', webhook_auth='password', webhook_port=5000)
    
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print(data)
    
    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count successfully posted!")

    @commands.command()
    async def gcount(self, ctx):
        await ctx.send(self.dbl.guild_count())
    
    @commands.command()
    async def votes(self, ctx):
        vote = await self.dbl.get_bot_upvotes()
        await ctx.send(vote)


def setup(client):
    client.add_cog(DBLcog(client))
