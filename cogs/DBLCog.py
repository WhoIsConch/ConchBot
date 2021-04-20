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
        self.dbl = dbl.DBLClient(self.client, dbltoken, autopost=True, webhook_path='/dblwebhook', webhook_auth='password', webhook_port=5000)
            
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.loop.create_task(self.dblvote())

    async def dblvote(self):
        while True:
            print("dblvote")
            votes = await self.dbl.get_bot_upvotes()
            db = await aiosqlite.connect('config.db')
            cursor = await db.cursor()
            await cursor.execute("SELECT userid FROM dblvote")
            check = await cursor.fetchall()
            for item in votes:
                print(item)
                print(votes)
                if "id" in item.keys():
                    print("thing in item keys")
                    id = item["id"]
                    for thing in check:
                        flag = False
                        await cursor.execute(f"SELECT time FROM dblvote WHERE userid = {id}")
                        check0 = await cursor.fetchone()
                        if check0 is None:
                            if thing[0] == int(id):
                                flag = True
                                continue
                        else:
                            break
                    if flag == True:
                        await cursor.execute(f"INSERT INTO dblvote (userid) VALUES ({id})")
            await cursor.execute("SELECT time FROM dblvote")
            check1 = await cursor.fetchall()
            now = datetime.datetime.now()
            currenttime = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            ntime = currenttime.replace(':', '')
            for time in check1:
                if time[0] == int(ntime):
                    await cursor.execute(f"DELETE FROM dblvote WHERE time = {ntime}")
            await db.commit()
            await cursor.close()
            await db.close()
            await asyncio.sleep(60)
    
    @commands.group(invoke_without_command=True)
    async def vote(self, ctx):
        embed = discord.Embed(title="Vote for ConchBot", colour=discord.Colour.blue())
        embed.add_field(name="Top.gg", value="You can vote for ConchBot on Top.gg [here!](https://top.gg/bot/733467297666170980/vote)")
        embed.add_field(name="Discord Bot List", value="You can vote for ConchBot on Discord Bot List [here!](https://discord.ly/conchbot)")
        embed.set_footer(text="When you're done voting, please use the \"cb vote claim\" command to claim your reward!")
        await ctx.send(embed=embed)

    @vote.command()
    async def claim(self, ctx):
        votes = await self.dbl.get_bot_upvotes()
        flag = False
        db = await aiosqlite.connect("config.db")
        cursor = await db.cursor()
        now = datetime.datetime.now()
        await cursor.execute(f"SELECT time FROM dblvote WHERE userid = {ctx.author.id}")
        timecheck = await cursor.fetchone()
        await cursor.execute(f"SELECT userid FROM dblvote WHERE userid = {ctx.author.id}")
        idcheck = await cursor.fetchone()
        if idcheck is None:
            embed = discord.Embed(title="Vote Not Found", colour=discord.Colour.red())
            embed.add_field(name="Sorry, it looks like we have not found your vote yet.", value="It may take up "
            "to two minutes for ConchBot to recognize your vote. Please be patient.")
            embed.set_footer(text="If you are certain you voted and are not able to redeem your vote, please "
            "join ConchBot's support server via 'cb support' and open a ticket.")
            await ctx.send(embed=embed)
        elif timecheck[0] is not None:
            time = str(timecheck[0])
            newtime = str(time[:2]) + ':' + str(time[2:])
            embed = discord.Embed(title="Vote Already Claimed", colour=ctx.author.colour)
            embed.add_field(name="It seems as you have already claimed your vote reward for today!",
            value=f"You have claimed your reward at {newtime} EST, military time.")
            embed.set_footer(text="If you think this is a mistake, please join ConchBot's support server via 'cb support'")
            await ctx.send(embed=embed)
        else:
            currenttime = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            time = currenttime.replace(':', '')
            ntime = int(time) + 1200
            if ntime > 2400:
                ntime -= 2400
            await Currency.item_func(self, ctx.author, "Bronze Conch", 1)
            await cursor.execute(f"UPDATE dblvote SET time = '{ntime}' WHERE userid = {ctx.author.id}")
            await ctx.send("You have claimed your vote and have been rewarded with one **Bronze Conch**! Please use it via \"cb use bronze.\"")
        await db.commit()
        await cursor.close()
        await db.close()

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
        db = await aiosqlite.connect('config.db')
        cursor = await db.cursor()
        await cursor.execute("SELECT userid FROM dblvote")
        check = await cursor.fetchall()
        print(check)
        
    

def setup(client):
    client.add_cog(DBLcog(client))
