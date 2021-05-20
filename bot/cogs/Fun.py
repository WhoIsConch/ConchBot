import asyncio
import json
import multiprocessing
import os
import random
import datetime
import threading
import dbl
import aiohttp
import aiosqlite
import asyncpraw
import discord
import DiscordUtils
import httpx
from discord.ext import commands
from dotenv import load_dotenv
from prsaw import RandomStuff
from dotenv import load_dotenv

load_dotenv('.env')

reddit = asyncpraw.Reddit(client_id = os.getenv("redditid"),
                    client_secret = os.getenv("redditsecret"),
                    username = "UnsoughtConch",
                    password = os.getenv('redditpassword'),
                    user_agent = "ConchBotPraw")

rs = RandomStuff(async_mode=True, api_key = os.getenv("aiapikey"))
dbltoken = os.getenv('DBLTOKEN')

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dbl = dbl.DBLClient(self.client, dbltoken)
        
    @commands.command()
    async def test(self, ctx):
        await ctx.send("Test")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.channel.name == "conchchat":
            try:
                flag = False
                votes = await self.dbl.get_bot_upvotes()
                for item in votes:
                    if int(item['id']) == int(message.author.id):
                        flag = True
                        break
                if flag is True:
                    await message.channel.trigger_typing()
                    aimsg = await rs.get_ai_response(message.content)
                    await message.reply(aimsg)
                else:
                    await message.channel.trigger_typing()
                    aimsg = await rs.get_ai_response(message.content)
                    await message.reply(f"{aimsg}\n\n*Consider voting for me on Top.gg! (<https://bit.ly/2PiLbwh>) "
                    "It only takes a second of your time and you won't see this message anymore!*")
            except AttributeError:
                await message.channel.trigger_typing()
                aimsg = await rs.get_ai_response(message.content)
                await message.reply(aimsg)
            except httpx.ReadTimeout:
                await message.channel.send("It seems my API has timed out. Please give me a few minutes, and if the problem "
                "continues, please contact UnsoughtConch via my `cb support` command.")
        else:
            pass
        try:
            if message.guild.id == 724050498847506433:
                if "retard" in message.content.lower():
                    await message.add_reaction("☹")
        except:
            pass

        if message.content == "<@!786620946412863538>":
            await message.channel.send("My prefix is `cb `")

    @commands.command(aliases=["chatbot"])
    @commands.has_permissions(manage_guild=True)
    async def ai(self, ctx, channel:discord.TextChannel):
        await ctx.send("You can set up a chatbot channel by naming any channel 'conchchat,' or I can do it for you! "
        "would you like me to do it for you? `Yes` or `no`.")
        msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30)
        if "yes" in msg.content.lower():
            await ctx.send("What category would you like this channel in? Channel categories ***must be the exact "
            "name, capitalization and all.***")
            msg0 = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=30)
            category = discord.utils.get(ctx.guild.categories, name=msg0.content)
            try:
                channel = await ctx.guild.create_text_channel('conchchat', category=category)
            except:
                await ctx.send("I'm sorry, but I do not have the `manage guild` requirement needed to create channels.")
                return
            await ctx.send(f"Done! The channel `conchchat` was created in the category `{msg0.content}`")
        elif "no" in msg.content.lower():
            await ctx.send("Okay. Cancelling...")
        else:
            await ctx.send("That's not a valid option.")

    @commands.command()
    async def meme(self, ctx):
        msg = await ctx.send("Getting your meme...")
        subreddit = await reddit.subreddit('memes')
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
    async def reddit(self, ctx, subreddit):
        message = await ctx.send("This may take a hot minute... Sit tight!")
        try:
            subreddit = await reddit.subreddit(subreddit)
            top = subreddit.top(limit=50)
            all_subs = []

            async for submission in top:
                all_subs.append(submission)
            
            ransub = random.choice(all_subs)
            if ransub.over_18:
                if ctx.channel.is_nsfw() == True:
                    pass
                else:
                    await ctx.send("Looks like that post is marked over 18, meaning you need to be in an NSFW marked"
                    " channel to look at that post.")
                    return
            if ransub.is_self:
                embed = discord.Embed(title=f"{ransub.author}'s Post", colour=ctx.author.colour)
                embed.add_field(name=ransub.title, value=ransub.selftext)
                embed.set_footer(text=f"❤ {ransub.ups} | 💬 {ransub.num_comments}")
            else:
                embed = discord.Embed(title=ransub.title, colour=ctx.author.colour, url=ransub.url)
                embed.set_footer(text=f"Posted by {ransub.author} on Reddit. | ❤ {ransub.ups} | 💬 {ransub.num_comments}")
                embed.set_image(url=ransub.url)
            await message.delete()
            await ctx.send(embed=embed)
        except:
            await ctx.send("Something went wrong. This may be the fact that the subreddit does not exist or is locked.")

    @commands.command()
    async def itft(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://itsthisforthat.com/api.php?json') as thing:
                try:
                    load = await thing.read()
                    jdata = json.loads(load)
                    embed = discord.Embed(title="Wait, what does your startup do?", colour=ctx.author.colour)
                    embed.add_field(name="So, basically, it's like a", value=f"**{jdata['this']}**", inline=False)
                    embed.add_field(name="For", value=f"**{jdata['that']}**", inline=False)
                    embed.set_footer(text="ItsThisForThat API | itsthisforthat.com")
                    await ctx.send(embed=embed)
                except:
                    await ctx.send("Woops! Something went wrong.")

    @commands.command()
    async def lyrics(self, ctx, *, values):
        band, song = values.split(",")
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.lyrics.ovh/v1/{band}/{song}") as lyrics:
                load = await lyrics.read()
                lyricdata = json.loads(load)
                lyricsraw = lyricdata["lyrics"]
                print(len(lyricsraw))
                try:
                    embeds = []
                    num1 = 0
                    lyrc = lyricsraw.split('\n\n\n\n')
                    for section in lyrc:
                        num1 += 1
                        num = discord.Embed().add_field(name=f"{song} Lyrics Part {num1}", value=section)
                        embeds.append(num)
                    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                    paginator.add_reaction('⏪', "back")
                    paginator.add_reaction('⏩', "next")
                    
                    await paginator.run(embeds)
            
                except KeyError:
                    await ctx.send("Invalid song or band name.")
                
                except:
                    await ctx.send("Sorry, something went wrong.")

    @commands.group(invoke_without_command=True)
    async def fbi(self, ctx):
        await ctx.send("What page?")
        msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)
        page = int(msg.content)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.fbi.gov/wanted/v1/list", params={'page': page}) as response:
                data = json.loads(await response.read())
                embeds = []
                for item in data["items"]:
                    embed = discord.Embed(title=f"FBI Wanted | {item['title']}")
                    embed.add_field(name="Details:", value=item['details'])
                    embed.add_field(name="Warning Message:", value=item['warning_message'])
                    embed.add_field(name="Reward:", value=item['reward_text'])
                    embed.add_field(name="UID:", value=item['uid'])
                    embed.set_footer(text="Data from FBI API | For more info on an entry, use 'cb fbi details {UID}'")
                    embeds.append(embed)
                
                paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
                paginator.add_reaction('⏪', "back")
                paginator.add_reaction('⏩', "next")
                    
                await paginator.run(embeds)

    @fbi.command()
    async def details(self, ctx, uid, value=None):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.fbi.gov/@wanted-person/{uid}") as response:
                data = json.loads(await response.read())
                
                details = data["details"]
                title = data["title"]
                desc = data["description"]
                reward = data["reward_text"]
                warnmsg = data["warning_message"]
                sex = data["sex"]
                if value is None:
                    pass
                else:
                    embed = discord.Embed(title=f"FBI Wanted | {title}", colour=discord.Colour.red(),
                    description=f"Published on {data['publication']}", url=data['url'])
                    try:
                        embed.add_field(name=value, value=data[value])
                        embed.set_footer(text="Data from FBI API | https://api.fbi.gov.docs")
                        await ctx.send(embed=embed)
                        return
                    except:
                        await ctx.send("That's an invalid value. Use 'cb help fbi' for more details.")
                        return
                    return
                embed = discord.Embed(title=f"FBI Wanted | {title}", colour=discord.Colour.red(),
                description=f"Published on {data['publication']}", url=data["url"])
                if details is not None:
                    embed.add_field(name="Details:",value=details, inline=False)
                else:
                    pass
                if desc is not None:
                    embed.add_field(name="Description", value=desc)
                else:
                    pass
                if warnmsg is not None:
                    embed.add_field(name="Warning Message:", value=warnmsg, inline=False)
                else:
                    pass
                if reward is not None:
                    embed.add_field(name="Reward:", value=reward)
                else:
                    pass
                if sex is not None:
                    embed.add_field(name="Sex:", value=sex, inline=False)
                else:
                    pass

                embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Seal_of_the_Federal_Bureau_of_Investigation.svg/300px-Seal_of_the_Federal_Bureau_of_Investigation.svg.png")
                try:
                    embed.set_image(url = data["images"][0]["large"])
                except:
                    pass

                await ctx.send(embed=embed)

    @commands.command()
    async def covid(self, ctx, country):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://covid-api.mmediagroup.fr/v1/cases") as response:
                data = json.loads(await response.read())
                try:
                    embed = discord.Embed(title=f"COVID-19 in {country}", colour=discord.Colour.gold(),)
                    embed.add_field(name="Cases:", value=data[country]['All']['confirmed'])
                    embed.add_field(name="Recovered Cases:", value=data[country]['All']['recovered'])
                    embed.add_field(name="Deaths:", value=data[country]['All']['deaths'])
                    embed.add_field(name="Country Population:", value=data[country]['All']['population'])
                    embed.add_field(name="Life Expectancy:", value=data[country]['All']['life_expectancy'])
                    embed.set_footer(text="Stats brought to you by M-Media-Group's COVID-19 API")
                    await ctx.send(embed=embed)
                except:
                    await ctx.send("Country not found. Country names ***are case-sensitive***.")

    @commands.command()
    async def joke(self, ctx):
        msg = await ctx.send("Grabbing your joke...")
        subreddit = await reddit.subreddit("jokes")
        top = subreddit.top(limit=50)
        all_subs = []

        async for submission in top:
            all_subs.append(submission)
        
        ransub = random.choice(all_subs)

        embed = discord.Embed(name=f"{ransub.author}'s Joke", colour=ctx.author.colour)
        embed.add_field(name=ransub.title, value=ransub.selftext)
        embed.set_footer(text=f"❤ {ransub.ups} | 💬 {ransub.num_comments}")
        await msg.delete()
        await ctx.send(embed=embed)

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
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{member}'s Avatar",
                colour=member.colour
            )
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)

    @ai.error
    async def ai_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permissions to do that! Please contact a server admin to do that for you.")
        else:
            await ctx.send("Reporting this error...")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify a message to send!")
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("Channel not found.")
        else:
            await ctx.send("Reporting this error...")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')

    @lyrics.error
    async def lyrics_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You didn't seem to tell me a song or a band.")
        if ValueError:
            await ctx.send("You need to tell me what person and song, separated by a comma.")
        else:
            await ctx.send("Reporting this error...")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')

    @fbi.error
    async def fbi_error(self, ctx, error):
        if isinstance(error, ValueError):
            await ctx.send("That isn't a valid number.")
        else:
            await ctx.send("Reporting this error...")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')
    
    @details.error
    async def details_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to provide a valid **UID.** These can be found via the `cb fbi` command.")
        else:
            await ctx.send("Reporting this error...")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to give me a question for the magic 8 ball to answer.")
        else:
            await ctx.send("Reporting this error...")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')

    @google.error
    async def google_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must include a query for me to Google.")
        else:
            await ctx.send("Reporting this error...")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')

    @chance.error
    async def chance_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify what I am rating the chances of.")
        else:
            await ctx.send("Reporting this error...")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')

    @pfp.error
    async def pfp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("How the fuck are you getting this error? Please contact UnsoughtConch via `cb support`.")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("I could not find that member. Please make sure your ID is correct and you are mentioning an existing user.")
        else:
            await ctx.send("Reporting this error...")
            now = datetime.datetime.now()
            time = datetime.time(hour=now.hour, minute=now.minute).isoformat(timespec='minutes')
            error_channel = self.client.get_channel(int(os.getenv("ERROR_CHANNEL")))
            await error_channel.send(f'Error Occured at {time} and in {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator} with the command `{ctx.command.name}`: ``` {error} ```')

def setup(client):
    client.add_cog(Fun(client))
