import aiosqlite
import discord
import os
from discord.ext import commands

dbltoken = os.getenv('DBLTOKEN')

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                embed = discord.Embed(
                    title="Thanks for inviting me to your server!",
                    colour=discord.Colour.green()
                )
                embed.add_field(name="What am I?", value="I'm a Discord bot who focuses on fun!", inline=False)
                embed.add_field(name="What can I do?", value="Tons of things! I have currency commands, fun commands, and more!")
                embed.add_field(name="Links:", value="You can join my support server [here](https://discord.gg/PyAcRfukvc), "
                "invite me [here]((https://discord.com/api/oauth2/authorize?client_id=733467297666170980&permissions=388102&scope=bot)"
                ", or join the creator's community server [here](https://discord.gg/n8XyytfxMk).")
                embed.set_footer(text="For any support regarding Conchbot, please run cb support.")
                embed.set_author(name=self.client.user.name, icon_url=self.client.user.avatar_url)
                embed.set_image(url=self.client.user.avatar_url)
                await channel.send(embed=embed)
            break
        channel1 = self.client.get_channel(793927796354449459)
        await channel1.send(f"ConchBot has joined a server called {guild.name}!")

def setup(client):
    client.add_cog(Misc(client))
