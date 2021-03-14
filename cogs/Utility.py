import asyncio
import platform

import discord
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
    
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
            embed.add_field(name=servers[x-1].name, value="Serber", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def servers(self, ctx):
        await ctx.send({len(self.client.guilds)})

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member:discord.Member, *, reason=None):
        embed = discord.Embed(
            colour = discord.Colour.red(),
            title="**Member Kicked**"
        )
        embed.add_field(name="User:", value=member.name)
        embed.add_field(name="Reason:", value=reason)
        embed.set_footer(text="ConchBot Moderation")

        await member.kick(reason=reason)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member:discord.Member, *, reason=None):
        embed = discord.Embed(
            colour=discord.Colour.red(),
            title="**Member Banned**"
        )
        embed.add_field(name="User:", value=member.name)
        embed.add_field(name="Reason:", value=reason)
        
        await member.ban(reason=reason)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_descriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member.member_descriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{member_name}{member_descriminator} has been unbanned.")
            else:
                await ctx.send("Member not found. Make sure they are banned, and that you have used the correct format.")

    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount:int):
        embed = discord.Embed(
            colour = discord.Colour.purple(),
        )
        embed.add_field(name="Messages Cleared", value=f"{amount} messages cleared.")

        await ctx.channel.purge(limit=amount+1)
        await ctx.send(embed=embed, delete_after=5)
    
    @commands.command(aliases=["statistics", "info", "information"])
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

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify a user to kick.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permissions required to kick other users.")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify a user to ban.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permissions required to ban other users.")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found.")
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify a user to kick in the correct `username+descriminator` format.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions required to unban other users.")
   
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify an amount of messages to clear.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have the permissions required to purge messages.")

def setup(client):
    client.add_cog(Utility(client))
