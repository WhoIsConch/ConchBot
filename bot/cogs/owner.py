import discord
from discord.ext import commands
import asyncio
import sqlite3
import sys
import os
from dotenv import load_dotenv
from jishaku.codeblocks import codeblock_converter
import logging
import psutil


load_env = load_dotenv()

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def commit(self, ctx, db=None):
        if db is None:
            await ctx.send("db/currency.db, db/config.db, db/tasks.db, db/tags.db")
        db = sqlite3.connect(db)
        cursor = db.cursor()
        await ctx.send("Committing database...")
        db.commit()
        
        cursor.execute(f"INSERT INTO u{579041484796461076} (item) VALUES (0)")
        db.commit()
        cursor.execute(f"DELETE FROM u{579041484796461076} WHERE item = 0")
        db.commit()
        await ctx.send("Database successfully committed.")
        cursor.close()
        db.close()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Ending Python process ConchBot... Goodbye")
        await self.client.logout()

    @commands.command()
    @commands.is_owner()
    async def refresh(self, ctx):
        cog = self.client.get_cog("Jishaku")
        await cog.jsk_git(ctx, argument=codeblock_converter('pull'))
        await asyncio.sleep(2)  # allow jsk git pull to finish
        restart = self.client.get_command('restart')
        await ctx.invoke(restart)

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, code: codeblock_converter):
        cog = self.client.get_cog("Jishaku")
        await cog.jsk_python(ctx, argument=code)

    @commands.command()
    @commands.is_owner()
    async def restart(self, ctx):
        def restarter():
            python = sys.executable
            os.execl(python, python, * sys.argv)

        embed = discord.Embed(title="Bot Restarting...")
        embed.add_field(name="I'll be back soon...", value="Don't worry", inline=True)
        await ctx.send(embed=embed)
        restarter()

def setup(client):
    client.add_cog(Owner(client))
