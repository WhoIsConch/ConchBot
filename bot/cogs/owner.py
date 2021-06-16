import discord
from discord.ext import commands
import asyncio
import sqlite3
import sys
import os
from bot.cogs.Currency import Currency
from dotenv import load_dotenv
from jishaku.codeblocks import codeblock_converter
import aiosqlite


load_env = load_dotenv()

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def commit(self, ctx, db=None):
        if db is None:
            await ctx.send("Pick one of these db `./bot/db/currency.db`, `./bot/db/config.db`, `./bot/db/tasks.db`, `./bot/db/tags.db`")
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
        await ctx.send("OK")

    @commands.command(aliases=["close"])
    @commands.has_role(794015347018956821)
    async def shutdown(self, ctx):
        await ctx.send("Ending Python process ConchBot... Goodbye")
        await self.client.logout()

    @commands.command(aliases=["pull"])
    @commands.has_role(794015347018956821)
    async def refresh(self, ctx):
        cog = self.client.get_cog("Jishaku")
        github_repo = os.getenv("GITHUB_REPO_LINK")
        github_repo_branch = os.getenv("GITHUB_REPO_BRANCH")
        await cog.jsk_git(ctx, argument=codeblock_converter(f'stash'))
        await asyncio.sleep(2)
        await cog.jsk_git(ctx, argument=codeblock_converter(f'pull --ff-only {github_repo} {github_repo_branch}'))
        await asyncio.sleep(2)
        restart = self.client.get_command('restart')
        await ctx.invoke(restart)

    @commands.command()
    @commands.has_role(794015347018956821)
    async def restart(self, ctx):
        def restarter():
            python = sys.executable
            os.execl(python, python, * sys.argv)

        embed = discord.Embed(title="Bot Restarting...")
        embed.add_field(name="I'll be back soon...", value="Don't worry", inline=True)
        await ctx.send(embed=embed)
        restarter()
        
    
    @commands.command()
    @commands.is_owner()
    async def editmoners(self, ctx, user:discord.Member, amount:int):
        await Currency.open_account(self, user)
        await Currency.update_bank(self, user, amount)
        await ctx.send(f"Successfully given {user.name} {amount} moners.")
    
    @commands.command()
    @commands.is_owner()
    async def edititems(self, ctx, user:discord.Member, item, amount:int):
        await Currency.open_account(self, user)
        await Currency.item_func(self, user, item, amount)
        await ctx.send(f"Successfully given {user.name} {amount} {item}s.")
    
    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def blacklist(self, ctx, val=None):
        if val is not None:
            await ctx.invoke(self.client.get_command(f'blacklist add {val}'))
        else:
            return await ctx.send("You can add or remove")
    
    @blacklist.command()
    async def add(self, ctx, id=None):
        if id is None:
            await ctx.send("You need the id of that user")
        else:
            db = await aiosqlite.connect("./bot/db/config.db")
            cursor = await db.cursor()
            await cursor.execute(f"SELECT id FROM blacklist WHERE id = {id}")
            result = await cursor.fetchone()
            if result is None:
                await cursor.execute(f"INSERT INTO blacklist (id) VALUES ({id})")
                await ctx.send("Member blacklisted.")
            else:
                await ctx.send("That Member is already blacklisted.")
            await db.commit()
            await cursor.close()
            await db.close()

    @blacklist.command()
    async def remove(self, ctx, id):
        if id is None:
            await ctx.send("You need the id of that user")
        else:
            db = await aiosqlite.connect("./bot/db/config.db")
            cursor = await db.cursor()
            await cursor.execute(f"SELECT id FROM blacklist WHERE guild_id = {ctx.guild.id}")
            result = await cursor.fetchone()
            blacklisted = result[0]
            if id not in blacklisted:
                await ctx.send("That ID is not blacklisted.")
            else:
                await cursor.execute(f"DELETE FROM blacklist WHERE guild_id = {ctx.guild.id}")
                await ctx.send("ID removed from blacklist.")
            await db.commit()
            await cursor.close()
            await db.close()


def setup(client):
    client.add_cog(Owner(client))
