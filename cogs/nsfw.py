import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncpraw
import os
import random

load_dotenv('.env')

reddit = asyncpraw.Reddit(client_id = os.getenv("redditid"),
            client_secret = os.getenv("redditsecret"),
            username = "UnsoughtConch",
            password = os.getenv('redditpassword'),
            user_agent = "ConchBotPraw")

class NSFW(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hentai(self, ctx):
        msg = await ctx.send("Getting your meme...")
        subreddit = await reddit.subreddit('hentai')
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
    

def setup(client):
    client.add_cog(NSFW(client))
