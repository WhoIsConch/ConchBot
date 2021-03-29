import asyncio
import multiprocessing
import os
import random
import sqlite3
import threading

import aiosqlite
import asyncpraw
import discord
import httpx
from discord.ext import commands
from dotenv import load_dotenv
from prsaw import RandomStuff

load_dotenv('.env')

reddit = asyncpraw.Reddit(client_id = os.getenv("redditid"),
                    client_secret = os.getenv("redditsecret"),
                    username = "UnsoughtConch",
                    password = os.getenv('redditpassword'),
                    user_agent = "ConchBotPraw")

rs = RandomStuff(async_mode=True)

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            if message.channel.name == "conchchat":
                await message.channel.trigger_typing()
                aimsg = await rs.get_ai_response(message.content)
                await message.reply(aimsg)
                return

    @commands.command(aliases=["chatbot"])
    @commands.has_permissions(manage_guild=True)
    async def ai(self, ctx):
        await ctx.send("You can set up a chatbot channel by naming any channel 'conchchat,' or I can do it for you! "
        "would you like me to do it for you? `Yes` or `no`.")
        msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)
        if "yes" in msg.content.lower():
            await ctx.send("What category would you like this channel in? Channel categories ***must be the exact "
            "name, capitalization and all.***")
            msg0 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)
            category = discord.utils.get(ctx.guild.categories, name=msg0.content)
            try:
                channel = await ctx.guild.create_text_channel('conchchat', category=category)
            except:
                await ctx.send("I'm sorry, but I do not have the `manage guild` requirement needed to create channels.")
                return
            await ctx.send(f"Done! The channel `conchchat` was created in the category `{msg0.content}`")
        elif "no" in msg.content.lower():
            await ctx.send("Okay. Cancelling...")
        else:
            await ctx.send("That's not a valid option.")

    @commands.command()
    async def meme(self, ctx):
        msg = await ctx.send("Getting your meme...")
        subreddit = await reddit.subreddit('memes')
        top = subreddit.top(limit=50)
        all_subs = []

        async for submission in top:
            all_subs.append(submission)
        
        ransub = random.choice(all_subs)

        embed = discord.Embed(title=ransub.title, colour=ctx.author.colour, url=ransub.url)
        embed.set_image(url=ransub.url)
        embed.set_footer(text=f"Posted by {ransub.author} on Reddit. | ❤ {ransub.ups} | 💬 {ransub.num_comments}")
        await msg.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def reddit(self, ctx, subreddit):
        message = await ctx.send("This may take a hot minute... Sit tight!")
        subreddit = await reddit.subreddit(subreddit)
        top = subreddit.top(limit=50)
        all_subs = []

        async for submission in top:
            all_subs.append(submission)
        
        ransub = random.choice(all_subs)
        if ransub.over_18:
            if ctx.channel.is_nsfw() == True:
                pass
            else:
                await ctx.send("Looks like that post is marked over 18, meaning you need to be in an NSFW marked"
                " channel to look at that post.")
                return
        if ransub.is_self:
            embed = discord.Embed(title=f"{ransub.author}'s Post", colour=ctx.author.colour)
            embed.add_field(name=ransub.title, value=ransub.selftext)
            embed.set_footer(text=f"❤ {ransub.ups} | 💬 {ransub.num_comments}")
        else:
            embed = discord.Embed(title=ransub.title, colour=ctx.author.colour, url=ransub.url)
            embed.set_footer(text=f"Posted by {ransub.author} on Reddit. | ❤ {ransub.ups} | 💬 {ransub.num_comments}")
            embed.set_image(url=ransub.url)
        await message.delete()
        await ctx.send(embed=embed)

    @commands.command()
    async def joke(self, ctx):
        msg = await ctx.send("Grabbing your joke...")
        subreddit = await reddit.subreddit("jokes")
        top = subreddit.top(limit=50)
        all_subs = []

        async for submission in top:
            all_subs.append(submission)
        
        ransub = random.choice(all_subs)

        embed = discord.Embed(name=f"{ransub.author}'s Joke", colour=ctx.author.colour)
        embed.add_field(name=ransub.title, value=ransub.selftext)
        embed.set_footer(text=f"❤ {ransub.ups} | 💬 {ransub.num_comments}")
        await msg.delete()
        await ctx.send(embed=embed)

    @commands.command(aliases=['repeat'])
    async def echo(self, ctx, channel:discord.TextChannel=None, *, msg):
        if channel is None:
            await ctx.send(msg)
        else:
            await channel.send(msg)

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, msg):
        responses = ['As I see it, yes.',
                        'Ask again later.',
                        'Better not tell you now.',
                        'Cannot predict now.',
                        'Concentrate and ask again.',
                        'Don’t count on it.',
                        'It is certain.',
                        'It is decidedly so.',
                        'Most likely.',
                        'My reply is no.',
                        'My sources say no.',
                        'Outlook not so good.',
                        'Outlook good.',
                        'Reply hazy, try again.',
                        'Signs point to yes.',
                        'Very doubtful.',
                        'Without a doubt.',
                        'Yes.',
                        'Yes – definitely.',
                        'You may rely on it.']
        embed = discord.Embed(
            title="Magic 8 Ball",
            colour=discord.Colour.blurple()
        )
        embed.add_field(name="Question:", value=msg)
        embed.add_field(name="Answer:", value=random.choice(responses))
        await ctx.send(embed=embed)

    @commands.command(aliases=["LMGTFY"])
    async def google(self, ctx, *, query):
        nquery = query.replace(' ', '+').lower()
        await ctx.send(f"https://www.google.com/search?q={nquery}")

    @commands.command(aliases=['chances', 'odds', 'odd'])
    async def chance(self, ctx, *, msg):
        chancenum = random.randint(0, 10)
        embed = discord.Embed(
            title="What are the Chances?",
            colour = ctx.author.colour
        )
        embed.add_field(name="Question:", value=msg)
        embed.add_field(name="The chances are...", value=chancenum)
        await ctx.send(embed=embed)

    @commands.command(aliases=['avatar'])
    async def pfp(self, ctx, member: discord.Member=None):
        if member is None:
            embed = discord.Embed(
                title=f"{ctx.author}'s Avatar",
                colour=ctx.author.colour
            )
            embed.set_image(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{member}'s Avatar",
                colour=member.colour
            )
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)

    @ai.error
    async def ai_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permissions to do that! Please contact a server admin to do that for you.")

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify a message to send!")

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to give me a question for the magic 8 ball to answer.")

    @google.error
    async def google_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must include a query for me to Google.")

    @chance.error
    async def chance_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify what I am rating the chances of.")

    @pfp.error
    async def pfp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("How the fuck are you getting this error? Please contact UnsoughtConch via `cb support`.")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("I could not find that member. Please make sure your ID is correct and you are mentioning an existing user.")

def setup(client):
    client.add_cog(Fun(client))
