import os
import platform
import datetime
import discord
from discord.ext import commands
import aiosqlite
from dotenv import load_dotenv

env = load_dotenv()

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def get_update_info(self, version=None):
        db = await aiosqlite.connect("./bot/db/updates.db")
        cursor = await db.cursor()

        if version is None:
            await cursor.execute("SELECT MAX(version) FROM updates")
            result = await cursor.fetchone()
            version = result[0]
        else:
            pass

        await cursor.execute(f"SELECT name FROM updates WHERE version = '{version}'")
        name = await cursor.fetchone()
        await cursor.execute(f"SELECT desc FROM updates WHERE version = '{version}'")
        desc = await cursor.fetchone()
        await cursor.execute(f"SELECT updates FROM updates WHERE version = '{version}'")
        updates = await cursor.fetchone()
        await cursor.execute(f"SELECT published FROM updates WHERE version = '{version}'")
        published = await cursor.fetchone()

        return version, name[0], desc[0], updates[0], published[0]

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.dark_red(),
            title=f"Pong! **__{round(self.client.latency * 1000)}__**"
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def guilds(self, ctx):
        servers = list(self.client.guilds)
        embed = discord.Embed(title="Guilds", colour=ctx.author.colour)
        for x in range(len(servers)):
            embed.add_field(name=servers[x-1].name, value=servers[x-1].member_count, inline=False)
        embed.add_field(name="Total Guilds:", value=len(self.client.guilds))
        embed.add_field(name="Total Members:", value=len(set(self.client.get_all_members())))
        await ctx.send(embed=embed)
        await ctx.send(f"Total Guilds: {len(self.client.guilds)}\nTotal Members: {len(set(self.client.get_all_members()))}")

    @commands.command()
    @commands.is_owner()
    async def servers(self, ctx):
        await ctx.send({len(self.client.guilds)})

    @commands.command(aliases=["purge"])
    @commands.cooldown(1, 5, commands.BucketType.user) 
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount:int):
        if amount < 1:
            await ctx.send("You can't clear a negative amount.")
        embed = discord.Embed(
            colour = discord.Colour.purple(),
        )
        embed.add_field(name="Messages Cleared", value=f"{amount} messages cleared.")

        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=embed, delete_after=5)
    
    @commands.command(aliases=["statistics", "info", "information"])
    @commands.cooldown(1, 5, commands.BucketType.user) 
    async def stats(self, ctx):
        embed = discord.Embed(
            colour=ctx.author.colour,
            title=f'{self.client.user.name} Stats'
        )
        embed.add_field(name="Bot Version:", value="1.0")
        embed.add_field(name="Python Version:", value=platform.python_version())
        embed.add_field(name="Discord.py Version:", value=discord.__version__)
        embed.add_field(name="Total Guilds:", value=len(self.client.guilds))
        embed.add_field(name="Total Users:", value=len(set(self.client.get_all_members())))
        embed.add_field(name="Bot Developers:", value="UnsoughtConch")
        await ctx.send(embed=embed)

    @commands.command()
    async def leave(self, ctx):
        check = ctx.author.guild_permissions.kick_members
        if check is True or ctx.author.id == 579041484796461076:
            await ctx.send("Are you sure you want me to leave the server? `yes` or `no.`")
            msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30)
            if "yes" in msg.content.lower():
                await ctx.send("I'm sorry you don't want me here anymore. If there was a problem or annoyance, you"
                " can feel free to join my support server. (https://discord.gg/PyAcRfukvc)")
                await ctx.guild.leave()
            elif "no" in msg.content.lower():
                await ctx.send("Thanks for deciding to keep me!")
            else:
                await ctx.send("Incorrect value. Aborting...")
        else:
            await ctx.send("You don't have permissions to make me leave!")

    @commands.group(invoke_without_command=True, aliases=["update"])
    async def updates(self, ctx):
        db = await aiosqlite.connect("./bot/db/updates.db")
        cursor = await db.cursor()

        version, name, desc, updates, published = await self.get_update_info()
        
        embed = discord.Embed(title=f"**__ConchBot Update {name}__**", colour=ctx.author.colour)
        embed.add_field(name="**Update Name:**", value=name, inline=False)
        embed.add_field(name="**Description:**", value=desc, inline=False)
        embed.add_field(name="**Updates:**", value=updates, inline=False)
        embed.set_footer(text=f"ConchBot Update {version} | Published {published}")
        await ctx.send(embed=embed)

    @updates.command()
    @commands.is_owner()
    async def publish(self, ctx, version, *, content):
        db = await aiosqlite.connect("./bot/db/updates.db")
        cursor = await db.cursor()
        now = datetime.datetime.now()
        td = datetime.datetime.today()
        currenttime = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
        name, desc, updates = content.split(", ")

        await ctx.send("This is how it will look. Good?")

        embed = discord.Embed(title=name, colour=ctx.author.colour)
        embed.add_field(name="**Update Name:**", value=name, inline=False)
        embed.add_field(name="**Description:**", value=desc, inline=False)
        embed.add_field(name="**Updates:**", value=updates, inline=False)
        embed.set_footer(text=f"ConchBot Update {version} | Published {td.month}/{td.day}/{td.year} at {currenttime}")
        await ctx.send(embed=embed)

        msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)

        if "yes" in msg.content.lower():
            await cursor.execute(f"INSERT INTO updates (version, name, desc, updates, published) VALUES "
            f"('{version}', '{name}', '{desc}', '{updates}', '{td.month}/{td.day}/{td.year} at {currenttime}')")
            await ctx.send("Update published!")
        else:
            await ctx.send("Aborting...")
        
        await db.commit()
        await cursor.close()
        await db.close()

    @updates.command()
    async def list(self, ctx):
        db = await aiosqlite.connect("./bot/db/updates.db")
        cursor = await db.cursor()

        await cursor.execute("SELECT version FROM updates")
        versions = await cursor.fetchall()

        embed = discord.Embed(title="ConchBot Updates", color=ctx.author.color)

        for version in versions:
            name = await self.get_update_info(version[0])
            embed.add_field(name=name[1], value=f"Update {version[0]}")
        embed.set_footer(text="To view a certain update, use 'cb update {version}.'")

        await ctx.send(embed=embed)

    @updates.command()
    async def info(self, ctx, version: int):
        db = await aiosqlite.connect("./bot/db/updates.db")
        cursor = await db.cursor()

        version, name, desc, updates, published = await self.get_update_info(version)

        embed = discord.Embed(title=f"**__ConchBot Update {name}__**", colour=ctx.author.colour)
        embed.add_field(name="**Update Name:**", value=name, inline=False)
        embed.add_field(name="**Description:**", value=desc, inline=False)
        embed.add_field(name="**Updates:**", value=updates, inline=False)
        embed.set_footer(text=f"ConchBot Update {version} | Published {published}")
        await ctx.send(embed=embed)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify an amount of messages to clear.")
            return
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions required to purge messages.")
            return
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send("Your amount must be an integer greater than one.")
            return
        else:
            await ctx.send("Reporting this error...")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')
            return

def setup(client):
    client.add_cog(Utility(client))
