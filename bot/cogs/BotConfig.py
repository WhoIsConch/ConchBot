import discord
from discord.ext import commands
import aiosqlite

class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def check_ff(self, guild):
        db = await aiosqlite.connect('.bot/db/config.db')
        cursor = await db.cursor()
        await cursor.execute(f"SELECT familyfriendly FROM config WHERE guild_id = {guild.id}")
        check = await cursor.fetchone()
        if check == None:
            await cursor.execute(f"SELECT guild_id FROM config WHERE guild_id = {guild.id}")
            check0 = await cursor.fetchone()
            if check0 is None:
                await cursor.execute(f"INSERT INTO config (guild_id, familyfriendly) VALUES ({guild.id}, 0)")
            else:
                await cursor.execute(f"UPDATE config SET familyfriendly = 0 WHERE guild_id = {guild.id}")
            await db.commit()
            await cursor.close()
            await db.close()  
            return "Inactive"
        if check[0] == 1:  
            return "Active"
        elif check[0] == 0:
            return "Inactive"      
        elif check[0] == 2:
            return "fuf"

    @commands.group(invoke_without_command=True, disasbled=True)
    async def config(self, ctx):
        embed = discord.Embed(title="Configuration Settings", colour=discord.Colour.gold())
        embed.add_field(name="Family Friendly Mode", value=f"Status: {await self.check_ff(ctx.guild)}\n "
        "DISCLAIMER: Family friendly mode does not apply to the bot's AI function.")
        await ctx.send(embed=embed)
    
    @config.command(disabled=True)
    async def ff(self, ctx, mode):
        db = await aiosqlite.connect('.bot/db/config.db')
        cursor = await db.cursor()
        status = await self.check_ff(ctx.guild)
        if mode == "activate" or "on":
            if status == "Active":
                await ctx.send("Family friendly mode is already active!")
            else:
                await cursor.execute(f"UPDATE config SET familyfriendly = 1 WHERE guild_id = {ctx.guild.id}")
                await ctx.send("Family friendly mode now active!")
        elif mode == "deactivate":
            if status == "Inactive":
                await ctx.send("Family friendly mode is already inactive!")
            else:
                await cursor.execute(f"UPDATE config SET familyfriendly = 0 WHERE guild_id = {ctx.guild.id}")
                await ctx.send("Family friendly mode deactivated.")
        elif mode == "fuf" or "off" or "deactivate":
            if status == "fuf":
                await ctx.send("Your forgetfull ass forgot that family unfriendly mode was already on.")
            else:
                embed = discord.Embed(name="⚠YOU ARE ABOUT TO TURN ON FAMILY **UN**FRIENDLY MODE⚠")
                embed.add_field(name="What is it?", value="Family unfriendly mode is a version of Conchbot in which "
                "every single message has some sort of insult or other content labeled Not Safe For Work. (Curses, "
                "innapropriate naming schemes, etc.)")
                embed.add_field(name="Effects:", value="All of the begging command's names are now NSFW, every message "
                "sent by ConchBot has innapropriate language in it, etc.")
                embed.add_field(name="ARE YOU SURE?", value="After this message, you are required to send either 'yes' "
                "or 'no,' the prompt being if you want to turn on family unfriendly mode or not.")
                embed.set_footer(text="You better make the right choice.")
                embed.set_thumbnail(url="https://i.imgur.com/OJwc0yL.jpeg")
                await ctx.send(embed=embed)
                msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=60)
                if "no" in msg.content.lower():
                    await ctx.send("Alright. No family unfriendly mode for you.")
                elif "yes" in msg.content.lower():
                    await cursor.execute(f"UPDATE config SET familyfriendly = 2 WHERE guild_id = {ctx.guild.id}")
                    await ctx.send("Alrighty motherfucker. Family unfriendly mode is now activated, bitch.")
                else:
                    await ctx.send("Invalid answer.")
        else:
            await ctx.send("Invalid argument. Your argument should either be `activate`,`deactivate`, or `fuf`, or `off`, `on`.")
        await db.commit()
        await cursor.close()
        await db.close()

def setup(client):
    client.add_cog(Config(client))