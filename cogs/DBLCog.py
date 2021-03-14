import dbl
import discord
from discord.ext import commands, tasks


class DBLcog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dbl = dbl.DBLClient(self.client, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjczMzQ2NzI5NzY2NjE3MDk4MCIsImJvdCI6dHJ1ZSwiaWF0IjoxNjEzMDY4NzU0fQ.Bt-jFijumhiF3GKXHBAiRxO6Vseehqa2105BU1wkQwQ")
    
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        print(data)

    @commands.command()
    async def gcount(self, ctx):
        await ctx.send(self.dbl.guild_count())
    
    @commands.command()
    async def votes(self, ctx):
        vote = await self.dbl.get_bot_upvotes()
        await ctx.send(vote)

def setup(client):
    client.add_cog(DBLcog(client))
