import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from ifunny import Client
from ifunny.objects import User, Post
import DiscordUtils
from dotenv import load_dotenv
import os 

load_dotenv()

ifclient = Client()

ifclient.login(os.getenv("iFunnyemail"), os.getenv("iFunnypass"))

class iFunny(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def ifunny(self, ctx):
        main = discord.Embed(title="Guide to the iFunny group of commands [BETA]", description="DISCLAIMER: All iFunny functionality is currently in beta, so commands may not work as"
        " expected.", color=discord.Color.gold())
        main.add_field(name="`feature` command", value="Using the `meme` command returns a new meme from the `feature` section.")
        main.add_field(name="`collective` command", value="Using the `meme` command returns a new meme from the `collective` section.")
        main.add_field(name="`user` command", value="The `user` command returns info of the provided iFunny user.")
        main.add_field(name="`post` command", value="Post something to the iFunny account `DiscordConchbot`.")
        main.add_field(name="Extra Information", value="This page hosts extra information about the iFunny module, such as why we smile posts.")
        main.set_footer(text="iFunny API wrapper made by Zero#5200 | Page 1")

        feature = discord.Embed(title="`feature` - `ifunny` subcommand", color=discord.Color.gold())
        feature.add_field(name="Information:", value="The `feature` command grabs all of the features in the `DiscordConchbot` iFunny profile feed. To show you as many non-repeated memes"
        " as possible, we mark the memes as read. If you know iFunny, though, there are only a certain amount of memes in featured for every feature set. This means that after a certain"
        " amount of memes, you might start seeing repeats. If you still want to see memes from iFunny, you can use the `collective` command, which rarely has repeats.")
        feature.add_field(name="How to use:", value="It's just `cb ifunny feature`, with two aliases, `featured` and `features`.", inline=False)
        feature.set_footer(text="iFunny Feature command | Page 2")

        collective = discord.Embed(title="`collective` - `ifunny` subcommand", color=discord.Color.dark_red())
        collective.add_field(name="Information:", value="If you use iFunny, you know all of the rumors about collective. Some people say it was way worse back in the day, some people say"
        " it's just as bad today. I'm just going to say this: ***be careful when using the collective command.*** iFunny collective is known for hosting NSFW and sometimes NSFL content."
        " It's not super abundant, while using iFunny, I don't see too much bad stuff. But every now and then it's there. So just be careful when using this subcommand.")
        collective.add_field(name="How to use:", value="`cb ifunny collective`, with no aliases.", inline=False)
        collective.set_footer(text="iFunny Collective command | Page 3")

        user = discord.Embed(title="`user` - `ifunny` subcommand", color=discord.Color.gold())
        user.add_field(name="Information:", value="This is used to get information about a user on iFunny. The following is the data it returns: `subscribers`, `subscriptions`, "
        "`total posts`, `total features`, `rank`, and `rating`. `rank` returns both `rank` and `days`, while `rating` returns both `level` and `exp`. `smiles` can be found in the footer.")
        user.add_field(name="How to use:", value="`cb ifunny user {username}`, gives error when no user is found.", inline=False)
        user.set_footer(text="iFunny User command | Page 4")

        post = discord.Embed(title="`post` - `ifunny` subcommand", color=discord.Color.gold())
        post.add_field(name="Information:", value="The `post` command is one of the most powerful `ifunny` subcommands. Why? Well, it posts an image to the iFunny account `DiscordConchBot`."
        " Posting items that go against iFunny's guidelines may get your account blacklisted from using ConchBot. When posting an image, ConchBot comments on the post. It comments who"
        " posted the image, so a post comment would look something like this: `Posted by UnsoughtConch#9225 on Discord using Discord ConchBot.")
        post.add_field(name="How to use:", value="`cb ifunny post {image URL}`. Image URL is optional. If there is no URL, it is expected that there be an attachment on the message for a "
        " image. If there is no URL or attached image, you get an error. If there is more than one attachment in an image, ConchBot gives you an error telling you that there can only be "
        " one attachment.")
        post.set_footer(text="iFunny Post command | Page 5")

        extra = discord.Embed(title="Extra Information for the `ifunny` Command Group", color=discord.Color.blue())
        extra.add_field(name="`feature` and `collective` commands:", value="When looking through posts, ConchBot smiles every post it sees as a courtesy to the meme author. If the meme author"
        " gets curious, he can look at ConchBot's iFunny account and the pinned post will be an informative post on why ConchBot smiled their post.")
        extra.add_field(name="Why This Exists", value="The iFunny module in ConchBot exists to make the bot more social. The main scope of ConchBot is to be a very featureful fun and social"
        " Discord bot, and an iFunny module was a module that a lot of bots don't have, if any. So this is a unique feature for enjoyment and social interaction.")
        extra.add_field(name="Who Made the Package?", value="This is possible because of Zero's iFunny API Wrapper. Sadly, chat functions no longer work, as his wrapper uses an older "
        "version of the Discord API, but I'm hoping to find a way to implement that in the future.")
        extra.add_field(name="Risks", value="iFunny isn't known for its friendly content and user base. That's why this entire module will soon be toggleable. There can sometimes be "
        "NSFW content in the featured section, and NSFL content in the collective section. There is no NSFW filter for any of this, due to the API and the way iFunny marks posts. That's"
        " why this will be toggleable in the future, so people won't have to worry about the risks.")
        extra.set_footer(text="iFunny Extra Information | Page 6")

        embeds = [main, feature, collective, user, post, extra]

        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        paginator.add_reaction("◀", "back")
        paginator.add_reaction("▶", "next")

        await paginator.run(embeds)

    @ifunny.command(aliases=["featured", 'features'])
    async def feature(self, ctx):
        msg = await ctx.send(embed=discord.Embed(title="Getting meme from iFunny collective...", color=discord.Color.random()))
        feed = ifclient.featured
        embeds = []
        for feature in feed:
            if "videos" in feature.content_url:
                continue
            print(hex(int("0x" + feature.author.nick_color, 16)))
            embed = discord.Embed(color=int("0x" + feature.author.nick_color, 16))
            try:
                embed.set_author(name=feature.author.nick, url=feature, icon_url=feature.author.profile_image.url)
            except:
                embed.set_author(name=feature.author.nick, url=feature, icon_url="https://ifunny.co/logo.jpg")
            embed.set_image(url=feature.content_url)
            embed.set_footer(text=f"👍 {feature.smile_count} | 💬 {feature.comment_count}")
            embeds.append(embed)
            print(feature)
            feature.read()
            feature.smile()
            break

        await ctx.send(embed=embed)
        await msg.delete()

    @ifunny.command()
    async def collective(self, ctx):
        msg = await ctx.send(embed=discord.Embed(title="Getting meme from iFunny collective...", color=discord.Color.random()))
        feed = ifclient.collective
        embeds = []
        for post in feed:
            if "videos" in post.content_url:
                continue
            print(hex(int("0x" + post.author.nick_color, 16)))
            embed = discord.Embed(color=int("0x" + post.author.nick_color, 16))
            try:
                embed.set_author(name=post.author.nick, url=post, icon_url=post.author.profile_image.url)
            except:
                embed.set_author(name=post.author.nick, url=post, icon_url="https://ifunny.co/logo.jpg")
            embed.set_image(url=post.content_url)
            embed.set_footer(text=f"👍 {post.smile_count} | 💬 {post.comment_count}")
            embeds.append(embed)
            print(post)
            post.read()
            post.smile()
            break

        await ctx.send(embed=embed)
        await msg.delete()

    @ifunny.command()
    async def user(self, ctx, *, name):
        user = User.by_nick(name)

        if not user:
            return await ctx.send(embed=discord.Embed(title=f"❌ User \"{user}\" does not exist.", color=discord.Color.red()))

        if user.is_verified:
            username = user.nick + " <a:verified:848709295851044884>"
        else:
            username = user.nick

        embed = discord.Embed(title=f"{username} iFunny Stats", color=int("0x" + user.nick_color, 16), description=user.about)

        if user.profile_image:
            embed.set_thumbnail(url=user.profile_image.url)
            embed.set_author(name=user.nick, icon_url=user.profile_image.url, url=f"https://ifunny.co/user/{user.nick}")
        
        embed.add_field(name="Subscribers:", value=user.subscriber_count)
        embed.add_field(name="Subscriptions:", value=user.subscription_count)
        embed.add_field(name="Total Posts:", value=user.post_count)
        embed.add_field(name="Total features:", value=user.feature_count)
        embed.add_field(name="Rank:", value=f"{user.rank} with {user.days} days on iFunny")
        embed.add_field(name="Rating:", value=f"Level: {user.rating.level} | EXP: {user.rating.points}")
        embed.set_footer(text=f"{user.smiles_count} smiles")

        await ctx.send(embed=embed)

    @ifunny.command()
    @commands.cooldown(1, 86400, BucketType.user)
    async def post(self, ctx, image=None):
        if image is None:
            if len(ctx.message.attachments) > 1:
                return await ctx.send(f"iFunny only supports one attachment.")
            else:
                image = image.attachments[0].url

        msg = await ctx.send(embed=discord.Embed(title="Posting image...", description="No, it didn't break! It just takes a while to make sure the post published.", color=discord.Color.random()))

        post = ifclient.post_image_url(image, wait=True)

        try:
            embed = discord.Embed(title="Click Here to Go to Post", url=post)
            embed.set_image(url=post.content_url)
            await ctx.send(embed=embed)
        except:
            await ctx.send(embed=discord.Embed(title="Posted!", description="Set title to go to iFunny page", url="https://ifunny.co/user/DiscordConchbot"))
        
        await msg.delete()
        post.add_comment(text=f"Posted by {ctx.author} on Discord using Discord ConchBot.")

def setup(client):
    client.add_cog(iFunny(client))
