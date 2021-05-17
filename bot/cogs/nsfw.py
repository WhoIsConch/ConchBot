import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncpraw
import os
import random
import rule34
from hentai import Hentai, Format, Utils
import DiscordUtils

load_dotenv('.env')

rule34 = rule34.Rule34()
reddit = asyncpraw.Reddit(client_id = os.getenv("redditid"),
            client_secret = os.getenv("redditsecret"),
            username = "UnsoughtConch",
            password = os.getenv('redditpassword'),
            user_agent = "ConchBotPraw")

class NSFW(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def hentai(self, ctx):
        msg = await ctx.send("Getting your porn...")
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

    @commands.command()
    async def sauce(self, ctx, id=None):
        await ctx.send("Getting your porn...")
        if id is None:
            doujin = Utils.get_random_hentai()

        else:
            doujin = Hentai(id)

        if not Hentai.exists(doujin.id):
            await ctx.send("Nothing found.")

        else:
            try:
                artist = doujin.artist[0].name
            except:
                artist = "No artist"
            embeds = []
            num = 0
            for url in doujin.image_urls:
                num += 1
                embed = discord.Embed(title=doujin.title(Format.Pretty), color=ctx.author.color, url=doujin.url)
                embed.set_image(url=url)
                embed.set_footer(text=f"Author: {artist} | Upload date: {doujin.upload_date} | Page {num} of {len(doujin.image_urls)}")
                embeds.append(embed)
            
            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('⏩', "next")
            
            await paginator.run(embeds)

    @commands.command()
    async def porn(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('porn')
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

    @commands.command(aliases=["tits", "boob", "tit"])
    async def boobs(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('boobs')
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
    
    @commands.command(aliases=["tittydrop", "titdrop"])
    async def boobdrop(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('tittydrop')
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
    async def feet(self, ctx):
        await ctx.send("What the fuck is wrong with you? Fucking toe gobbling fuck.")
        
    @commands.command()
    async def gay(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('gayporn')
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
    async def overwatch(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('overwatch_porn')
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
    async def sfm(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('sfmcompileclub')
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

    @commands.command(aliases=["vagina"])
    async def pussy(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('pussy')
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
    async def waifu(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('waifusgonewild')
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

    @commands.command(aliases=["r34"])
    async def rule34(self, ctx, *, query=None):
        if query is None:
            msg = await ctx.send("Getting your porn...")
            subreddit = await reddit.subreddit('rule34')
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
        else:
            msg = await ctx.send("Grabbing your porn...")
            images = await rule34.getImages(tags=query)
            total = []

            for image in images:
                total.append(image)
            
            finalimg = random.choice(total)

            embed = discord.Embed(title="ID: " + finalimg.id, colour=ctx.author.colour, url=finalimg.file_url)
            embed.set_image(url=finalimg.file_url)
            embed.set_footer(text=f"Posted by {finalimg.creator_ID} on Rule 34. | Score: {finalimg.score}")
            await msg.delete()
            await ctx.send(embed=embed)

    @commands.command(aliases=["futa"])
    async def futanari(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('futanari')
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

    @commands.command(aliases=["lesbo"])
    async def lesbian(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('lesbians')
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
    async def bdsm(self, ctx):
        msg = await ctx.send("Getting your porn...")
        subreddit = await reddit.subreddit('bdsm')
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
