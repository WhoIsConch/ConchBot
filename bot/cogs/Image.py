import textwrap
from io import BytesIO
import aiohttp
from aiohttp import request
import discord
import PIL.Image
from aiohttp_requests import requests
import os
from discord.ext import commands
from PIL import ImageDraw, ImageFont
from dotenv import load_dotenv
import io

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
