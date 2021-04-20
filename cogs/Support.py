import aiosqlite
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

class Support(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(
            title="ConchBot Support",
            colour=discord.Colour.gold()
        )
        embed.add_field(name="You Just Used the Support Command!", value="This means you either have a question about ConchBot,"
        " would like to report an error or bug, or just want to join the ConchBot community!")
        embed.add_field(name="ConchBot Discord Server", value="You can join ConchBot's support server [here](https://discord.gg/PyAcRfukvc)")
        embed.add_field(name="Or, if you don't want to join a server...", value="You can submit bugs or errors via 'cb report {description of bug}.")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def report(self, ctx, *, bug):
        if ctx.author.id in blacklist:
            await ctx.send("Sorry, but you are blacklisteed from reporting bugs and adding suggestions.")
            return
        channel = self.client.get_channel(795711741606101024)
        db = await aiosqlite.connect('config.db')
        cursor = await db.cursor()
        await cursor.execute('SELECT num FROM bugnum WHERE placeholder = 1')
        result = await cursor.fetchone()
        num = result[0]+1
        embed = discord.Embed(
            title=f"Bug Report #{num}",
            colour=discord.Colour.red()
        )
        embed.add_field(name="Submitted By:", value=ctx.author)
        embed.add_field(name="Bug Description:", value=bug)
        await cursor.execute(f'UPDATE bugnum SET num = {num} WHERE placeholder = 1')
        await channel.send(embed=embed)
        await ctx.send("Thank you for the bug report! Our team will identify and fix the problem as soon as possible!")
        await db.commit()
        await cursor.close()
        db.close

    @commands.command()
    @commands.cooldown(1, 86400, BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        channel = self.client.get_channel(819029394534039604)
        if len(suggestion)>100:
            await ctx.send("Please keep your suggestion under 100 characters as to not flood the suggestions channel.")
        elif len(suggestion)<10:
            await ctx.send("That suggestion is too short. Your suggestion must be more than 10 characters long.")
        else:
            embed = discord.Embed(
                title="Someone has a suggestion!",
                colour=ctx.author.colour
            )
            embed.add_field(name="Submitted by:", value=ctx.author.name)
            embed.add_field(name="Suggestion:", value=suggestion)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send("Your suggestion has been submitted!")
            await channel.send(embed=embed)
    
    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must add a description of the bug to report.")

    @suggest.error
    async def suggest_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must input a suggestion for ConchBot.")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send("You have already submitted a suggestion in the last 24 hours.")

def setup(client):
    client.add_cog(Support(client))
