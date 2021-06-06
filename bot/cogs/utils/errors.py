import discord

class Blacklisted(Exception):
    def __init__(self,ctx):
        super().__init__("error")
        self.ctx = ctx
    
    async def memsend(self):
        embed = discord.Embed(title="User Blacklisted", description="It looks like you have been blacklisted from using ConchBot.", color=discord.Color.red())
        embed.set_footer(text="If you think this is a mistake, please join the ConchBot Support server via \"cb support\" - blacklisted users can use that command.")

        await self.ctx.send(embed=embed)

    async def guildsend(self):
        embed = discord.Embed(title="Server Blacklisted", description="It looks like this guild has been blacklisted from using ConchBot.", color=discord.Color.red())
        embed.set_footer(text="If you think this is a mistake, please join the ConchBot Support server via \"cb support\" - blacklisted guilds can use that command.")

        await self.ctx.send(embed=embed)


    