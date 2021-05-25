import datetime
import json
from aiohttp import request
import random
import inspect
import os
import dbl
import aiohttp
import io
import asyncpraw
import discord
import DiscordUtils
import httpx
from discord.ext import commands
from dotenv import load_dotenv
from prsaw import RandomStuff
from dotenv import load_dotenv
import os
from io import BytesIO


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
    @commands.cooldown(1, 10, commands.BucketType.user) 
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
    @commands.cooldown(1, 10, commands.BucketType.user) 
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


    @commands.group(invoke_without_command=True)
    async def fbi(self, ctx):
        await ctx.send("What page?")
        msg = await self.client.wait_for('message', check=lambda message: message.author == ctx.author, timeout=10)
        page = int(msg.content)
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.fbi.gov/wanted/v1/list", params={'page': page}) as response:
                data = json.loads(await response.read())
                embeds = []
                try:
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
                 except IndexError:
                    return await ctx.send("Too high of a page") #added a handler just in case

    @fbi.command()
    @commands.cooldown(1, 10, commands.BucketType.user) 
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
    @commands.cooldown(1, 10, commands.BucketType.user) 
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
    @commands.cooldown(1, 10, commands.BucketType.user) 
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
    @commands.cooldown(1, 3, commands.BucketType.user) 
    async def echo(self, ctx, channel:discord.TextChannel=None, *, msg):
        if channel is None:
            await ctx.send(msg)
        else:
            await channel.send(msg)

    @commands.command(name='8ball')
    @commands.cooldown(1, 5, commands.BucketType.user) 
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
    @commands.cooldown(1, 3, commands.BucketType.user) 
    async def google(self, ctx, *, query):
        nquery = query.replace(' ', '+').lower()
        await ctx.send(f"https://www.google.com/search?q={nquery}")

    @commands.command(aliases=['chances', 'odds', 'odd'])
    @commands.cooldown(1, 5, commands.BucketType.user) 
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
    @commands.cooldown(1, 3, commands.BucketType.user) 
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
    

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def animal(self, ctx, animal=None):
        animal_options = ["dog", "cat", "panda", "fox", "bird", "koala", "red_panda"]
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


    @commands.command()
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


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def meme(self, ctx):
        meme_web = "https://some-random-api.ml/meme"

        async with ctx.typing():
            async with request("GET", meme_web, headers={}) as response:
                if response.status == 200:
                    api = await response.json()
                    image = api["image"]
                    await ctx.send(image)
                else:
                    await ctx.send(f"API returned a {response.status} status.")




    @commands.command()
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


    @commands.command()
    async def triggered(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as wastedSession:
                async with wastedSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage:
                    imageData = io.BytesIO(await wastedImage.read())
                    
                    await wastedSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'triggered.gif'))

    @commands.command()
    async def rainbow(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as gaySession:
                async with gaySession.get(f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format="png", size=1024)}') as gayImage:
                    imageData = io.BytesIO(await gayImage.read())
                    
                    await gaySession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'gay.gif'))

    @commands.command()
    async def wasted(self, ctx, member: discord.Member=None):
        if not member:
            member = ctx.author
        async with ctx.typing():
            async with aiohttp.ClientSession() as wastedSession:
                async with wastedSession.get(f'https://some-random-api.ml/canvas/wasted?avatar={member.avatar_url_as(format="png", size=1024)}') as wastedImage:
                    imageData = io.BytesIO(await wastedImage.read())
                    
                    await wastedSession.close()
                    
                    await ctx.reply(file=discord.File(imageData, 'wasted.gif'))

    @commands.command()
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

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def lyrics(self, ctx, *, search=None):
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

    @commands.command()
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


    @commands.command()
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


    @commands.command()
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

    @ai.error
    async def ai_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the permissions to do that! Please contact a server admin to do that for you.")
            return
        

    @echo.error
    async def echo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify a message to send!")
            return
        if isinstance(error, commands.ChannelNotFound):
            await ctx.send("Channel not found.")
            return
    
        
    @fbi.error
    async def fbi_error(self, ctx, error):
        if isinstance(error, ValueError):
            await ctx.send("That isn't a valid number.")
            return
        
    @details.error
    async def details_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to provide a valid **UID.** These can be found via the `cb fbi` command.")
            return
        

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to give me a question for the magic 8 ball to answer.")
            return

    @google.error
    async def google_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must include a query for me to Google.")
            return
       
    @chance.error
    async def chance_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You must specify what I am rating the chances of.")
            return
        
    @pfp.error
    async def pfp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("How the fuck are you getting this error? Please contact UnsoughtConch via `cb support`.")
            return
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("I could not find that member. Please make sure your ID is correct and you are mentioning an existing user.")
            return
        

def setup(client):
    client.add_cog(Fun(client))
