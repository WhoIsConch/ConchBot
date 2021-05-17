from io import BytesIO

import discord
from discord.ext import commands
from PIL import ImageFont,ImageDraw
import PIL.Image

class Secret(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 811308446372069436:
            img = PIL.Image.open("AllMyHomiesHateTemplate.jpg")
            font = ImageFont.truetype("arial.ttf", 50)
            draw = ImageDraw.Draw(img)
            text = member.name
            fill_color = (255, 255, 255)
            stroke_color = (0, 0, 0)
            draw.text((285, 29), text, font = font, fill=fill_color, stroke_width=2, stroke_fill=stroke_color)
            draw.text((32, 538), text, font = font, fill=fill_color, stroke_width=2, stroke_fill=stroke_color)
            img.save("text.png")
            channel = self.client.get_channel(811345201729372205)
            await channel.send(file = discord.File("text.png"))

def setup(client):
    client.add_cog(Secret(client))

