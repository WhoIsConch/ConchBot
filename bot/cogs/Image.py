import io
import os
import random
import textwrap
from io import BytesIO

import aiohttp
import discord
import DiscordUtils
import PIL.Image
from aiohttp import request
from aiohttp_requests import requests
from discord.ext import commands
from dotenv import load_dotenv
from PIL import ImageDraw, ImageFont

env = load_dotenv()

eupvote = '<:Upvote:822667264406192198>'
edownvote = '<:Downvote:822667263571525664>'
ecomment = '<:Comment:822668322293940224> '

class Image(commands.Cog):

    '''
    The commands here are used to make memes and show them to your friends!
    '''

    def __init__(self, client):
        self.client = client

    @commands.command(description="Fuck this meme, all my homies hate this meme.")
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def fuck(self, ctx, *, val):
        try:
            val1, val2 = val.split(',')
        except ValueError:
            val1 = val
            val2 = None
        img = PIL.Image.open("bot/src/MemeTemplates/AllMyHomiesHateTemplate.jpg")
        font = ImageFont.truetype("bot/src/arial.ttf", 50)
        draw = ImageDraw.Draw(img)
        fill_color = (255, 255, 255)
        stroke_color = (0, 0, 0)
        draw.text((311, 26), val1, font = font, fill=fill_color, stroke_width=2, stroke_fill=stroke_color)
        if val2 is not None:
            draw.text((153, 535), val2, font = font, fill=fill_color, stroke_width=2, stroke_fill=stroke_color)
        else:
            draw.text((153, 535), val1, font = font, fill=fill_color, stroke_width=2, stroke_fill=stroke_color)
        img.save("text.png")
        await ctx.send(file = discord.File("text.png"))
        file = 'text.png'
        location = "./"
        path = os.path.join(location, file)
        os.remove(path)

    @commands.command(description="\"Are you going to sleep?\" \"Yes, now shut up.\" \"You should go use ConchBot\"")
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def brain(self, ctx, *, content):
        msg = await ctx.send("Creating your meme...")
        img = PIL.Image.open("bot/src/MemeTemplates/Brain.png")
        font = ImageFont.truetype("bot/src/arial.ttf", 10)
        draw = ImageDraw.Draw(img)
        text = textwrap.fill(content, width=25)
        draw.text((17, 176), text, font=font, fill="Black")
        img.save("Meme.png")
        await msg.delete()
        await ctx.send(file=discord.File("Meme.png"))
        file = 'Meme.png'
        location = "./"
        path = os.path.join(location, file)
        os.remove(path)
    
    @commands.command(description="These drawings are made by people with mental illnesses.")
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def mentalillness(self, ctx, url=None):
        msg = await ctx.send("Creating your meme...")
        if url is None:
            url = ctx.message.attachments[0].url
        try:
            response = await requests.get(url)
        except:
            await ctx.send("You must provide a valid image URL.")
            return
        size = 128, 128
        img1 = PIL.Image.open(BytesIO(response.content))
        img1_w, img1_h = img1.size
        img2 = PIL.Image.open("bot/src/MemeTemplates/MentalIlness.png")
        img2_w, img2_h = img2.size
        offset = ((img2_w - img1_w) // 2, (img2_h - img1_h) // 2)
        basewidth = 175
        wpercent = (basewidth/float(img1.size[0]))
        hsize = int((float(img1.size[1])*float(wpercent)))
        img1 = img1.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
        img2.paste(img1, (227, 286))
        img2.save("Meme.png")
        await msg.delete()
        await ctx.send(file=discord.File("Meme.png"))
        file = 'Meme.png'
        location = "./"
        path = os.path.join(location, file)
        os.remove(path)

    @commands.command(description="This is where I'd put my meme, *IF I HAD ONE*")
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def idputmy(self, ctx, *, text):
        msg = await ctx.send("Creating your meme...")
        img = PIL.Image.open("bot/src/MemeTemplates/IdPutMy.png")
        font = ImageFont.truetype("bot/src/arial.ttf", 22)
        draw = ImageDraw.Draw(img)
        text = textwrap.fill(text, width=20)
        draw.text((45, 41), text, font=font, fill="White", stroke_width=2, stroke_fill="Black")
        img.save("Meme.png")
        await msg.delete()
        await ctx.send(file=discord.File("Meme.png"))
        file = 'Meme.png'
        location = "./"
        path = os.path.join(location, file)
        os.remove(path)

    @commands.command(description="Is this a meme?")
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def isthis(self, ctx, *, text):
        try:
            text_one, text_two, text_three = text.split(',')
        except ValueError:
            await ctx.send("You must separate three values by commas.")
            return
        msg = await ctx.send("Creating your meme...")
        img = PIL.Image.open("bot/src/MemeTemplates/IsThis.jpg")
        font = ImageFont.truetype("bot/src/arial.ttf", 100)
        draw = ImageDraw.Draw(img)
        text_one = textwrap.fill(text_one, width=11)
        text_two = textwrap.fill(text_two, width=8)
        draw.text((181, 841), text_one, font=font, fill="White", stroke_width=5, stroke_fill="Black")
        draw.text((1097, 165), text_two, font=font, fill="White", stroke_width=5, stroke_fill="Black")
        draw.text((345, 1317), text_three, font=font, fill="White", stroke_width=5, stroke_fill="Black")
        img.save("Meme.png")
        await msg.delete()
        await ctx.send(file=discord.File("Meme.png"))        
        file = 'Meme.png'
        location = "./"
        path = os.path.join(location, file)
        os.remove(path)

    @commands.command(description="I receive: Nothing. You receive: This meme!")
    @commands.cooldown(1, 10, commands.BucketType.user) 
    async def tradeoffer(self, ctx, *, text):
        try:
            text_one, text_two = text.split(',')
        except ValueError:
            await ctx.send("You must separate three values by commas.")
            return
        msg = await ctx.send("Creating your meme...")
        img = PIL.Image.open("bot/src/MemeTemplates/TradeOffer.jpg")
        font = ImageFont.truetype("bot/src/arial.ttf", 50)
        draw = ImageDraw.Draw(img)
        text_one = textwrap.fill(text_one, width=15)
        text_two = textwrap.fill(text_two, width=13)
        draw.text((32, 179), text_one, font=font, fill="White", stroke_width=5, stroke_fill="Black")
        draw.text((320, 184), text_two, font=font, fill="White", stroke_width=5, stroke_fill="Black")
        img.save("Meme.png")
        await msg.delete()
        await ctx.send(file=discord.File("Meme.png"))       
        file = 'Meme.png'
        location = "./"
        path = os.path.join(location, file)
        os.remove(path)

    @commands.command(description="\"My daughter tells me you like Discord bots\" \"Yes sir ConchBot is the worst\" \"You have six seconds to get the fuck out of my house\"")
    async def getout(self, ctx, *, text):
        msg = await ctx.send("Creating your meme...")
        img = PIL.Image.open("bot/src/MemeTemplates/stayout.jpg")
        font = ImageFont.truetype("bot/src/arial.ttf", 40)
        draw = ImageDraw.Draw(img)
        text = textwrap.fill(text, width=20)
        draw.text((26, 45), text, font=font, fill="black", stroke_width=2, stroke_fill="white")
        img.save("Meme.png")
        await msg.delete()
        await ctx.send(file=discord.File("Meme.png"))
        file = 'Meme.png'
        location = "./"
        path = os.path.join(location, file)
        os.remove(path)
    
    @commands.command(description="Make a picture of yourself or a friend in a WANTED poster!\n[member] value is optional.")
    async def wanted(self, ctx, member : discord.Member=None):
        if member is None:
            member = ctx.author

        wanted = Image.open("bot/src/MemeTemplates/wanted.jpg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((308, 306))
        wanted.paste(pfp, (69, 143))
        wanted.save("profile.jpg")
        await ctx.send(file = discord.File("profile.jpg"))
        file = 'profile.jpg'
        location = "./"
        path = os.path.join(location, file)
        os.remove(path)

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

    @commands.command(description="This command makes anyone *bright*.\n[member] value is optional.")
    async def bright(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as brightSession:
                async with brightSession.get(f'https://some-random-api.ml/canvas/bright?avatar={member.avatar_url_as(format="png", size=1024)}') as brightImage:
                    imageData = io.BytesIO(await brightImage.read())
                    
                    await brightSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'bright.gif'))

    @commands.command(description="This command converts rgb to hex")
    async def hex(self, ctx, hex):
        if not hex:
            await ctx.send("Put a hex code in")
        async with ctx.typing():
            async with aiohttp.ClientSession() as hexSession:
                async with hexSession.get(f'https://some-random-api.ml/canvas/colorviewer?hex={hex}') as hexImage:
                    imageData = io.BytesIO(await hexImage.read())
                    
                    await hexSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'hex.gif'))

    @commands.command(description="Make a YouTube comment!")
    async def comment(self, ctx, member: discord.Member, comment:str):
        member_avatar = member.avatar_url_as(format="png", size=256)
        api_link = f"https://some-random-api.ml/canvas/youtube-comment?avatar={member_avatar}&comment={comment}&username={member.name}"

        async with ctx.typing():
            async with aiohttp.ClientSession() as youtubeSession:
                async with youtubeSession.get(api_link) as youtubeComment:
                    imageData = io.BytesIO(await youtubeComment.read())
                    
                    await youtubeSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'youtube.gif'))

    @commands.command(description="Blur an avatar.\n[member] value is optional.")
    async def blur(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as blurSession:
                async with blurSession.get(f'https://some-random-api.ml/canvas/blur?avatar={member.avatar_url_as(format="png", size=1024)}') as blurImage:
                    imageData = io.BytesIO(await blurImage.read())
                    
                    await blurSession.close()

        await ctx.reply(file=discord.File(imageData, 'blur.gif'))

    @commands.command(description="Pixelate an avatar.\n[member] value is optional.")
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

def setup(client):
    client.add_cog(Image(client))
