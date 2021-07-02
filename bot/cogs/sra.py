import discord
from discord.ext import commands
from aiohttp import request
import random
import DiscordUtils
import aiohttp
import io
from discord.ext.commands.core import command

class srapi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Show an image and a fact about the given animal!\n[animal] value is optional.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def animal(self, ctx, animal=None):
        animal_options = ["dog", "cat", "panda", "fox", "bird", "koala", "red_panda", "racoon", "kangaroo", "elephant", "giraffe", "whale"]
        if animal is None:
            animal = random.choice(animal_options)
        if (animal := animal.lower()) in animal_options:
            animal_fact_url = f"https://some-random-api.ml/facts/{animal}"
            animal_image_url = f"https://some-random-api.ml/img/{animal}"
            

            async with ctx.typing():

                async with request("GET", animal_image_url, headers={}) as response:
                    if response.status == 200:
                        animal_api = await response.json()
                        image_link = animal_api["link"]

                    else:
                        image_link = None

                async with request("GET", animal_fact_url, headers={}) as response:
                    if response.status == 200:
                        animal_api = await response.json()

                        embed = discord.Embed(title=f"{animal.title()} fact")
                        embed.add_field(name="Fact", value=animal_api["fact"])
                        if image_link is not None:
                            embed.set_image(url=image_link)
                        await ctx.send(embed=embed)

                    else:
                        await ctx.send(f"API returned a {response.status} status.")
        else:
            await ctx.send(f"Sorry but {animal} isn't in my api")

    @commands.command(description="Returns a real-looking Discord bot token.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def token(self, ctx):
        token_web = "https://some-random-api.ml/bottoken"

        async with ctx.typing():
            async with request("GET", token_web, headers={}) as response:
                if response.status == 200:
                    api = await response.json()
                    bottoken = api["token"]
                else:
                    await ctx.send(f"API returned a {response.status} status.")

            await ctx.send(bottoken)

    @commands.command(description="Get a random meme!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://www.reddit.com/r/memes/hot.json') as r:
                    res = await r.json()
                embed = discord.Embed(title="Meme")
                embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)
        except:
            meme_link = f"https://some-random-api.ml/meme"

            async with request("GET", meme_link, headers={}) as response:
                if response.status == 200:
                    api = await response.json()
                    image = api["image"]
                    caption = api["caption"]

                    embed = discord.Embed(title="Meme", description=caption)
                    embed.set_image(url=image)
                    await ctx.send(embed=embed)

    @commands.command(description="Get lyrics of a specific song!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lyrics(self, ctx, *, search):
        search = search.replace(' ', '%20')
        search_web = f"https://some-random-api.ml/lyrics?title={search}"

        await ctx.channel.trigger_typing()
        async with request("GET", search_web, headers={}) as response:
            if response.status == 200:
                api = await response.json()
                title = api["title"]
                author = api["author"]
                lyrics = api["lyrics"]
                
                embed = discord.Embed(title=f"{title} by {author}", description=lyrics)
                try:
                    await ctx.send(embed=embed)
                except:
                    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                    paginator.add_reaction('◀', 'back')
                    paginator.add_reaction('▶', 'next')
                    

                    embed1 = discord.Embed(title=f"{title} by {author} | Page 1", description=lyrics[:int(len(lyrics)/2)])
                    embed2 = discord.Embed(title=f"{title} by {author} | Page 2", description=lyrics[int(len(lyrics)/2):])

                    embeds = [embed1, embed2]

                    await paginator.run(embeds)
            else:
                await ctx.send(f"API returned a {response.status} status.")

    @commands.command(description="Define a word!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def define(self, ctx, word):
        word_lowered = word.lower()
        word_link = f"https://some-random-api.ml/dictionary?word={word_lowered}"

        async with request("GET", word_link, headers={}) as response:
            if response.status == 200:
                api = await response.json()
                word_name = api["word"]
                word_definition = api["definition"]
                paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                paginator.add_reaction('◀', 'back')
                paginator.add_reaction('▶', 'next')
                

                embed1 = discord.Embed(title=f"{word_name} | Page 1", description=word_definition[:int(len(word_definition)/2)])
                embed2 = discord.Embed(title=f"{word_name} | Page 2", description=word_definition[int(len(word_definition)/2):])

                embeds = [embed1, embed2]

                await paginator.run(embeds)
            else:
                await ctx.send(f"API returned a {response.status} status.")    


    @commands.command(description="This command makes anyone *glassed*.\n[member] value is optional.")
    async def glass(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as glassSession:
                async with glassSession.get(f'https://some-random-api.ml/canvas/glass?avatar={member.avatar_url_as(format="png", size=1024)}') as glassImage:
                    imageData = io.BytesIO(await glassImage.read())
                    
                    await glassSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'glass.gif'))

    @commands.command(description="This command makes anyone *inverted*.\n[member] value is optional.")
    async def invert(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as invertSession:
                async with invertSession.get(f'https://some-random-api.ml/canvas/invert?avatar={member.avatar_url_as(format="png", size=1024)}') as invertImage:
                    imageData = io.BytesIO(await invertImage.read())
                    
                    await invertSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'invert.gif'))


    @commands.command(description="This command makes anyone *glassed*.\n[member] value is optional.")
    async def bright(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as brightSession:
                async with brightSession.get(f'https://some-random-api.ml/canvas/bright?avatar={member.avatar_url_as(format="png", size=1024)}') as brightImage:
                    imageData = io.BytesIO(await brightImage.read())
                    
                    await brightSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'bright.gif'))

    @commands.command(description="This command convert rgb to hex")
    async def hex(self, ctx, hex):
        if not hex:
            await ctx.send("Put a hex code in")
        async with ctx.typing():
            async with aiohttp.ClientSession() as hexSession:
                async with hexSession.get(f'https://some-random-api.ml/canvas/colorviewer?hex={hex}') as hexImage:
                    imageData = io.BytesIO(await hexImage.read())
                    
                    await hexSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'hex.gif'))



    @commands.group(invoke_without_command=True)
    async def youtube(self, ctx):
        pass

    @youtube.command()
    async def comment(self, ctx, member: discord.Member, comment:str):
        member_avatar = member.avatar_url_as(format="png", size=256)
        api_link = f"https://some-random-api.ml/canvas/youtube-comment?avatar={member_avatar}&comment={comment}&username={member.name}"

        async with ctx.typing():
            async with aiohttp.ClientSession() as youtubeSession:
                async with youtubeSession.get(api_link) as youtubeComment:
                    imageData = io.BytesIO(await youtubeComment.read())
                    
                    await youtubeSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'youtube.gif'))


    @command()
    async def blur(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as blurSession:
                async with blurSession.get(f'https://some-random-api.ml/canvas/blur?avatar={member.avatar_url_as(format="png", size=1024)}') as blurImage:
                    imageData = io.BytesIO(await blurImage.read())
                    
                    await blurSession.close()

        await ctx.reply(file=discord.File(imageData, 'blur.gif'))

    @command()
    async def pixel(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as pixelSession:
                async with pixelSession.get(f'https://some-random-api.ml/canvas/pixelate?avatar={member.avatar_url_as(format="png", size=1024)}') as pixelImage:
                    imageData = io.BytesIO(await pixelImage.read())
                    
                    await pixelSession.close()

        await ctx.reply(file=discord.File(imageData, 'pixel.gif'))


    @commands.command(description="Returns an image of an anime pat!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pat(self, ctx):
        pat_image = "https://some-random-api.ml/animu/pat"

        async with ctx.typing():
            async with request("GET", pat_image, headers={}) as response:
                if response.status == 200:
                    api = await response.json()
                    image = api["link"]
                else:
                    await ctx.send(f"API returned a {response.status} status.")

            await ctx.send(image)

    @commands.command(description="This command makes anyone *triggered*.\n[member] value is optional.")
    async def triggered(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as wastedSession:
                async with wastedSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage:
                    imageData = io.BytesIO(await wastedImage.read())
                    
                    await wastedSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'triggered.gif'))

    @commands.command(description="This command makes you gay, basically.\n[member] value is optional.")
    async def rainbow(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as gaySession:
                async with gaySession.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format="png", size=1024)}') as gayImage:
                    imageData = io.BytesIO(await gayImage.read())
                    
                    await gaySession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'gay.gif'))

    @commands.command(aliases=['passed'], description="What you see when you vote for ConchBot on Top.gg\n[member] value is optional.")
    async def missionpassed(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as passSession:
                async with passSession.get(f'https://some-random-api.ml/canvas/passed?avatar={member.avatar_url_as(format="png", size=1024)}') as passedImage:
                    imageData = io.BytesIO(await passedImage.read())
                    
                    await passSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'passed.gif'))

    @commands.command(description="You're wasted.\n[member] value is optional.")
    async def wasted(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as wastedSession:
                async with wastedSession.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage:
                    imageData = io.BytesIO(await wastedImage.read())
                    
                    await wastedSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'wasted.gif'))

    @commands.command(description="Get an anime wink!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wink(self, ctx):
        wink_image = f"https://some-random-api.ml/animu/wink"

        async with ctx.typing():
            async with request("GET", wink_image, headers={}) as response:
                if response.status == 200:
                    api = await response.json()
                    image = api["link"]
                else:
                    await ctx.send(f"API returned a {response.status} status.")

            await ctx.send(image)
    
    @commands.command(description="Get an anime hug.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx):
        hug_image = f"https://some-random-api.ml/animu/hug"

        async with ctx.typing():
            async with request("GET", hug_image, headers={}) as response:
                if response.status == 200:
                    api = await response.json()
                    image = api["link"]
                else:
                    await ctx.send(f"API returned a {response.status} status.")

            await ctx.send(image)

    @commands.command(description="Get a random picture of Pikachu!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def pikachu(self, ctx):
        pikachu_image = f"https://some-random-api.ml/img/pikachu"

        async with ctx.typing():
            async with request("GET", pikachu_image, headers={}) as response:
                if response.status == 200:
                    api = await response.json()
                    image = api["link"]
                else:
                    await ctx.send(f"API returned a {response.status} status.")

            await ctx.send(image)

    @commands.command(aliases=["encoder"])
    async def encode(self, ctx, type, *, code):
        types = ["binary", "base64"]
        type = type.lower()
        if type in types:
            async with aiohttp.ClientSession() as encodeSession:
                if type == "binary":
                    async with encodeSession.get(f"https://some-random-api.ml/binary?text={code}") as encoder:
                        if encoder.status == 200:
                            api = await encoder.json()
                            encoded = api["binary"]
                            embed = discord.Embed(title="Binary Encoder")
                            embed.add_field(name="Input", value=f"```{code}```", inline=False)
                            embed.add_field(name="Output", value=f"```{encoded}```", inline=False)
                            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f"The api has troubles sorry try again later. Error code: {encoder.status}")
                else:
                    async with encodeSession.get(f"https://some-random-api.ml/base64?encode={code}") as encoder:
                        if encoder.status == 200:
                            api = await encoder.json()
                            encoded = api["base64"]
                            embed = discord.Embed(title="Base64 Encoder")
                            embed.add_field(name="Input", value=f"```{code}```", inline=False)
                            embed.add_field(name="Output", value=f"```{encoded}```", inline=False)
                            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f"The api has troubles sorry try again later. Error code: {encoder.status}")
        else:
            await ctx.send("Use binary or base64")


    @commands.command(aliases=["decoder"])
    async def decode(self, ctx, type, *, code):
        types = ["binary", "base64"]
        type = type.lower()
        if type in types:
            async with aiohttp.ClientSession() as decodeSession:
                if type == "binary":
                    async with decodeSession.get(f"https://some-random-api.ml/binary?decode={code}") as decoder:
                        if decoder.status == 200:
                            api = await decoder.json()
                            decoded = api["text"]
                            embed = discord.Embed(title="Binary Decoder")
                            embed.add_field(name="Input", value=f"```{code}```", inline=False)
                            embed.add_field(name="Output", value=f"```{decoded}```", inline=False)
                            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f"The api has troubles sorry try again later. Error code: {decoder.status}")
                else:
                    async with decodeSession.get(f"https://some-random-api.ml/base64?decode={code}") as decoder:
                        if decoder.status == 200:
                            api = await decoder.json()
                            decoded = api["text"]
                            embed = discord.Embed(title="Base64 Decoder")
                            embed.add_field(name="Input", value=f"```{code}```", inline=False)
                            embed.add_field(name="Output", value=f"```{decoded}```", inline=False)
                            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send(f"The api has troubles sorry try again later. Error code: {decoder.status}")
        else:
            await ctx.send("Use binary or base64")

def setup(client):
    client.add_cog(srapi(client))