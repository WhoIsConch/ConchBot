import discord
from discord.ext import commands
import os
import aiosqlite
import sqlite3
import sys

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog=None):
        if cog is None:
            await ctx.send("Available cogs:\nBotConfig\nCurrency\nDBLCog\nFun\nHelp\nImage\nMisc\nOwner\nSecret\n"
            "Snipe\nSupport\nUtility")
        else:
            try:
                await self.client.load_extension(f"cogs.{cog}")
                await ctx.send(f"{cog} loaded.")
            except discord.ext.commands.ExtensionNotFound:
                await ctx.send("Invalid extension.")
            except discord.ext.commands.ExtensionAlreadyLoaded:
                await ctx.send("Extension already loaded.")
            except:
                await ctx.send("Okay")

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog=None):
        if cog is None:
            await ctx.send("Available cogs:\nBotConfig\nCurrency\nDBLCog\nFun\nHelp\nImage\nMisc\nOwner\nSecret\n"
            "Snipe\nSupport\nUtility")
        else:
            try:
                await self.client.unload_extension("cogs." + cog)
                await ctx.send(f"{cog} unloaded.")
            except discord.ext.commands.ExtensionNotFound:
                await ctx.send("Invalid extension.")
            except discord.ext.commands.ExtensionNotLoaded:
                await ctx.send("Extension not loaded.")
            except:
                await ctx.send("Okay")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if cog is None:
            await ctx.send("Available cogs:\nBotConfig\nCurrency\nDBLCog\nFun\nHelp\nImage\nMisc\nOwner\nSecret\n"
            "Snipe\nSupport\nUtility")
        else:
            try:
                await self.client.unload_extension("cogs." + cog)
                await self.client.load_extension("cogs." + cog)
                await ctx.send(f"{cog} reloaded.")
            except discord.ext.commands.ExtensionNotFound:
                await ctx.send("Invalid extension.")
            except discord.ext.commands.ExtensionNotLoaded:
                await ctx.send("Extension not loaded.")
            except:
                await ctx.send("Okay")

    @commands.command()
    @commands.is_owner()
    async def commit(self, ctx, db=None):
        if db is None:
            await ctx.send("currency.db, config.db, tasks.db, tags.db")
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
        sys.exit()

def setup(client):
    client.add_cog(Owner(client))
