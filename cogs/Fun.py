import random

import aiosqlite
import discord
from discord.ext import commands
from prsaw import RandomStuff

rs = RandomStuff(async_mode=True)

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def connect_to_db(self, message):
        db = await aiosqlite.connect('aichannels.db')
        cursor = await db.cursor()
        await cursor.execute(f'SELECT channel_id FROM main WHERE guild_id = {message.channel.guild.id}')
        result = await cursor.fetchone()
        return result

    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     result = await self.connect_to_db(message)
    #     if message.author.bot:
    #         return
    #     else:
    #         if result is None:
    #             return
    #         else:
    #             if message.channel.id == result[0]:
    #                 await message.channel.trigger_typing()
    #                 response = await rs.get_ai_response(message.content)
    #                 await message.reply(response)
    #             else:
    #                 return
    #     await self.client.process_commands(message)
    #     await cursor.close()
    #     await db.close()

    @commands.group(invoke_without_command=True, enabled=False)
    async def joke(self, ctx):
        anyjoke = await rs.get_joke(_type="any")
        await ctx.send(anyjoke)
        await rs.close()
    
    @joke.command(aliases=['developer', 'programmer'], enabled=False)
    async def dev(self, ctx):
        devjoke = await rs.get_joke(_type="dev")
        await ctx.send(devjoke)
        await rs.close()

    @joke.command(aliases=['scary', 'spook'], enabled=False)
    async def spooky(self, ctx):
        spookjoke = await rs.get_joke(_type="spooky")
        await ctx.send(spookjoke)
        await rs.close()
    
    @joke.command(enabled=False)
    async def pun(self, ctx):
        punjoke = await rs.get_joke(_type="pun")
        await ctx.send(punjoke)
        await rs.close()

    @commands.command(aliases=['chatbot'])
    async def ai(self, ctx, channel:discord.TextChannel, disabled=True):
        db = await aiosqlite.connect('aichannels.db')
        cursor = await db.cursor()
        await cursor.execute(f'SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}')
        result = await cursor.fetchone()
        if result is None:
            await cursor.execute(f'INSERT INTO main (guild_id, channel_id) VALUES ({ctx.guild.id}, {channel.id})')
        else:
            await cursor.execute(f'UPDATE main SET channel_id = {channel.id} WHERE guild_id = {ctx.guild.id}')
        await ctx.send(f"AI bot channel set to {channel.mention}.")
        await db.commit()
        await cursor.close()
        await db.close()

    @commands.command(aliases=['repeat'])
    async def echo(self, ctx, channel:discord.TextChannel=None, *, msg):
        if channel is None:
            await ctx.send(msg)
        else:
            await channel.send(msg)

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, msg):
        responses = ['As I see it, yes.',
                        'Ask again later.',
                        'Better not tell you now.',
                        'Cannot predict now.',
                        'Concentrate and ask again.',
                        'Don’t count on it.',
                        'It is certain.',
                        'It is decidedly so.',
                        'Most likely.',
                        'My reply is no.',
                        'My sources say no.',
                        'Outlook not so good.',
                        'Outlook good.',
                        'Reply hazy, try again.',
                        'Signs point to yes.',
                        'Very doubtful.',
                        'Without a doubt.',
                        'Yes.',
                        'Yes – definitely.',
                        'You may rely on it.']
        embed = discord.Embed(
            title="Magic 8 Ball",
            colour=discord.Colour.blurple()
        )
        embed.add_field(name="Question:", value=msg)
        embed.add_field(name="Answer:", value=random.choice(responses))
        await ctx.send(embed=embed)

    @commands.command(aliases=["LMGTFY"])
    async def google(self, ctx, *, query):
        nquery = query.replace(' ', '+').lower()
        await ctx.send(f"https://www.google.com/search?q={nquery}")

    @commands.command(aliases=['chances', 'odds', 'odd'])
    async def chance(self, ctx, *, msg):
        chancenum = random.randint(0, 10)
        embed = discord.Embed(
            title="What are the Chances?",
            colour = ctx.author.colour
        )
        embed.add_field(name="Question:", value=msg)
        embed.add_field(name="The chances are...", value=chancenum)
        await ctx.send(embed=embed)

    @commands.command(aliases=['avatar'])
    async def pfp(self, ctx, member: discord.Member=None):
        if member is None:
            embed = discord.Embed(
                title=f"{ctx.author}'s Avatar",
                colour=ctx.author.colour
            )
            embed.set_image(url=ctx.author.avatar_url)
            ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{member}'s Avatar",
                colour=member.colour
            )
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)

    @joke.error
    async def joke_error(self, ctx, error):
        if isinstance(error, commands.DisabledCommand):
            await ctx.send("Sorry! The joke commands have been disabled until further notice.")
    
    @dev.error
    async def dev_error(self, ctx, error):
        if isinstance(error, commands.DisabledCommand):
            await ctx.send("Sorry! The joke commands have been disabled until further notice.")

    @spooky.error
    async def spooky_error(self, ctx, error):
        if isinstance(error, commands.DisabledCommand):
            await ctx.send("Sorry! The joke commands have been disabled until further notice.")

    @pun.error
    async def pun_error(self, ctx, error):
        if isinstance(error, commands.DisabledCommand):
            await ctx.send("Sorry! The joke commands have been disabled until further notice.")

    @ai.error
    async def ai_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must mention a channel for me to set the chatbot to.")

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify a message to send!")

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to give me a question for the magic 8 ball to answer.")

    @google.error
    async def google_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must include a query for me to Google.")

    @chance.error
    async def chance_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify what I am rating the chances of.")

    @pfp.error
    async def pfp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("How the fuck are you getting this error? Please contact UnsoughtConch via `cb support`.")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("I could not find that member. Please make sure your ID is correct and you are mentioning an existing user.")

def setup(client):
    client.add_cog(Fun(client))
