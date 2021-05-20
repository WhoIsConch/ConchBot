import random
import textwrap
from io import BytesIO

import asyncpraw
import discord
import PIL.Image
from aiohttp_requests import requests
import os
from discord.ext import commands
from PIL import ImageDraw, ImageFont

eupvote = '<:Upvote:822667264406192198>'
edownvote = '<:Downvote:822667263571525664>'
ecomment = '<:Comment:822668322293940224> '

class Image(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def text(self, ctx):
        img = PIL.Image.open("bot/src/MemeTemplates/IdPutMy.png")
        font = ImageFont.truetype("bot/src/arial.ttf", 22)
        draw = ImageDraw.Draw(img)
        fill_color = (255, 255, 255)
        stroke_color = (0, 0, 0)
        draw.text((12, 11), "And here's where I'd put my", font = font, fill=fill_color, stroke_width=2, stroke_fill=stroke_color)
        draw.text((71, 387), "IF I HAD ONE", font = font, fill=fill_color, stroke_width=2, stroke_fill=stroke_color)
        img.save("text.png")
        await ctx.send(file = discord.File("text.png"))
        file = 'text.png'
        location = "./"
        path = os.path.join(location, file)
        os.remove(path)


    @commands.command()
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

    @commands.command()
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
    
    @commands.command()
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
        # offset = ((img2_w - img1_w) // 2, (img2_h - img1_h) // 2)
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

    @commands.command()
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

    @commands.command()
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

    @commands.command()
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

    @commands.command()
    async def getout(self, ctx, *, text):
        msg = await ctx.send("Creating your meme...")
        img = PIL.Image.open("bot/src/MemeTemplates/stayout.jpg")
        font = ImageFont.truetype("bot/src/arial.ttf", 40)
        draw = ImageDraw.Draw(img)
        text = textwrap.fill(text, width=20)
        draw.text((26, 45), text, font=font, fill="Black", stroke_width=2, stroke_fill="whitre")
        img.save("Meme.png")
        await msg.delete()
        await ctx.send(file=discord.File("Meme.png"))
        file = 'Meme.png'
        location = "./"
        path = os.path.join(location, file)
        os.remove(path)

    @fuck.error
    async def fuck_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need at least one value, maximum two, separated by a comma.")
    
    @brain.error
    async def brain_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to provide one value, something that the brain says.")
        
    @mentalillness.error
    async def mentalillness_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must provide an image URL or attach an image to your message.")
        
    @idputmy.error
    async def idputmy_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify something to put in the meme.")
        
    @isthis.error
    async def isthis_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must provide a few things to put in your meme.")

def setup(client):
    client.add_cog(Image(client))
