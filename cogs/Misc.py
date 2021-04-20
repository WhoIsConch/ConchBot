import aiosqlite
import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db = await aiosqlite.connect('config.db')
        cursor = await db.cursor()
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="Thanks for inviting me to your server!",
                    colour=discord.Colour.green()
                )
                embed.add_field(name="What am I?", value="I'm a Discord bot who focuses on fun!", inline=False)
                embed.add_field(name="What can I do?", value="Tons of things! I have currency commands, fun commands, and more!")
                embed.add_field(name="Links:", value="You can join my support server [here](https://discord.gg/PyAcRfukvc), "
                "invite me [here]((https://discord.com/api/oauth2/authorize?client_id=733467297666170980&permissions=388102&scope=bot)"
                ", or join the creator's community server [here](https://discord.gg/n8XyytfxMk).")
                embed.set_footer(text="For any support regarding Conchbot, please run cb support.")
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                embed.set_image(url=self.client.user.avatar_url)
                await channel.send(embed=embed)
            break
        channel1 = self.client.get_channel(793927796354449459)
        await channel1.send(f"ConchBot has joined a server called {guild.name}!")
        await cursor.execute(f"SELECT guild_id FROM config WHERE guild_id = {guild.id}")
        check = await cursor.fetchone()
        if check is None:
            await cursor.execute(f"INSERT INTO config (guild_id) VALUES ({guild.id})")

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title="ConchBot Invites",
            colour=ctx.author.colour
        )
        embed.add_field(name="ConchBot Invite:", value="You can invite ConchBot to your server "
        "[here](https://discord.com/api/oauth2/authorize?client_id=733467297666170980&permissions=388102&scope=bot)")
        embed.add_field(name="Support Server Invite:", value="You can join ConchBot Support "
        "[here](https://discord.gg/PyAcRfukvc)")
        embed.add_field(name="ConchBot's creator (UnsoughtConch)'s community server:",
        value="You can join Conch's community server [here](https://discord.gg/n8XyytfxMk)")
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def blacklist(self, ctx):
        await ctx.send("You can `add` or `remove` users.")
    
    @blacklist.command()
    async def add(self, ctx, id):
        db = await aiosqlite.connect("config.db")
        cursor = await db.cursor()
        await cursor.execute(f"SELECT id FROM blacklist WHERE id = {id}")
        result = await cursor.fetchone()
        if result is None:
            await cursor.execute(f"INSERT INTO blacklist (id) VALUES ({id})")
            await ctx.send("ID blacklisted.")
        else:
            await ctx.send("That ID is already blacklisted.")
        await db.commit()
        await cursor.close()
        await db.close()

    @blacklist.command()
    async def remove(self, ctx, id):
        db = await aiosqlite.connect("config.db")
        cursor = await db.cursor()
        await cursor.execute(f"SELECT id FROM blacklist WHERE id = {id}")
        result = await cursor.fetchone()
        if result is None:
            await ctx.send("That ID is not blacklisted.")
        else:
            await cursor.execute(f"DELETE FROM blacklist WHERE id = {id}")
            await ctx.send("ID removed from blacklist.")
        await db.commit()
        await cursor.close()
        await db.close()

def setup(client):
    client.add_cog(Misc(client))
