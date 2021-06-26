import aiosqlite
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from dotenv import load_dotenv
import dbl
import os
from bot.cogs.Currency import Currency


env = load_dotenv()


class Support(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dbl = dbl.DBLClient(self.client, os.getenv('DBLTOKEN'), autopost=True, webhook_path='/dblwebhook', webhook_auth='69420', webhook_port=5000)

    async def getvotes(self):
        return await self.dbl.get_bot_upvotes()
    
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        channel = self.client.get_channel(724050498847506436)
        user = self.client.get_user(int(data['user']))
        if user is None:
            pass
        else:
            await user.send("Thanks for voting for ConchBot! Due to this, you'll get awesome perks, such as:"
            "\nUnlocked image commands!\nNo message on the AI!\nA `bronze conch` currency item! (Use with `cb use bronze`)")
        await Currency.item_func(self, user, "Bronze Conch", 1)

        await channel.send(data)

    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count successfully posted!")

    @commands.command(description="Displays an embed of where you can get support for ConchBot.")
    async def support(self, ctx):
        embed = discord.Embed(
            title="ConchBot Support",
            colour=discord.Colour.gold()
        )
        embed.add_field(name="You Just Used the Support Command!", value="This means you either have a question about ConchBot,"
        " would like to report an error or bug, or just want to join the ConchBot community!")
        embed.add_field(name="ConchBot Discord Server", value="You can join ConchBot's support server [here](https://discord.gg/PyAcRfukvc)")
        embed.add_field(name="Or, if you don't want to join a server...", value="You can submit bugs or errors via 'cb report {description of bug}.")
        await ctx.send(embed=embed)
    
    @commands.command(description="Report a bug to the ConchBot developers.")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def report(self, ctx, *, content):
        channel = self.client.get_channel(795711741606101024)
        db = await aiosqlite.connect('./bot/db/config.db')
        cursor = await db.cursor()
        await cursor.execute('SELECT num FROM bugnum WHERE placeholder = 1')
        result = await cursor.fetchone()
        num = result[0]+1
        embed = discord.Embed(
            title=f"Bug Report #{num}",
            colour=discord.Colour.red()
        )
        embed.add_field(name="Submitted By:", value=ctx.author)
        embed.add_field(name="Bug Description:", value=content)
        embed.set_footer(text=f"User ID: {ctx.author.id}")
        await cursor.execute(f'UPDATE bugnum SET num = {num} WHERE placeholder = 1')
        await channel.send(embed=embed)
        await ctx.send("Thank you for the bug report! Our team will identify and fix the problem as soon as possible!")
        await db.commit()
        await cursor.close()
        await db.close()

    # @commands.command()
    # @commands.is_owner()
    # async def respond(self, ctx, *, content):
    #     user, content = content.split(':;')

    #     user = self.client.get_user(user.id)

    #     if user is None:
    #         return await ctx.send("Failed.")

    #     embed=discord.Embed(title="Bug Report Response", color=discord.Color.random(), description="*You are receiving this message because you have recently submitted a bug about ConchBot.*")
    #     embed.add_field(name="Response:", value=content)
    #     embed.set_footer(text="*If this response asks for more information, you can just use the report command again.*")

    #     await user.send(embed=embed)

    #     await ctx.send("User contacted.")

    @commands.command(description="Suggest a feature!")
    @commands.cooldown(1, 86400, BucketType.user)
    async def suggest(self, ctx, *, suggestion):
        channel = self.client.get_channel(819029394534039604)
        if channel is None:
            await ctx.guild.create_text_channel('suggestions')
            channel = discord.utils.get(ctx.guild.channels, name="suggestions")
        if len(suggestion)>100:
            await ctx.send("Please keep your suggestion under 100 characters as to not flood the suggestions channel.")
        elif len(suggestion)<10:
            await ctx.send("That suggestion is too short. Your suggestion must be more than 10 characters long.")
        else:
            embed = discord.Embed(
                title=f"{ctx.author.name}#{ctx.author.discriminator} has a suggestion!",
                colour=ctx.author.colour
            )
            embed.add_field(name="Submitted by:", value=ctx.author.name)
            embed.add_field(name="Suggestion:", value=suggestion)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            await ctx.send("Your suggestion has been submitted!")
            suggestion_message = await channel.send(embed=embed)
            await suggestion_message.add_reaction("⬆️")
            await suggestion_message.add_reaction("⬇️")

    @commands.group(invoke_without_command=True, description="Vote for ConchBot on Top.gg or DBL!")
    async def vote(self, ctx):
        embed = discord.Embed(title="Vote for ConchBot", colour=discord.Colour.blue())
        embed.add_field(name="Perks", value="Voting for ConchBot gets you awesome perks, such as unlocked commands and currency items!")
        embed.add_field(name="Top.gg", value="You can vote for ConchBot on Top.gg [here!](https://top.gg/bot/733467297666170980/vote)")
        embed.add_field(name="Discord Bot List", value="You can vote for ConchBot on Discord Bot List [here!](https://discord.ly/conchbot)")
        embed.set_footer(text="When you're done voting, please use the \"cb vote claim\" command to claim your reward!")
        await ctx.send(embed=embed)

    @commands.command(description="Get a link to invite ConchBot to your server!")
    async def invite(self, ctx):
        embed = discord.Embed(
            title="ConchBot Invites",
            colour=ctx.author.colour
        )
        embed.add_field(name="ConchBot Invite:", value="You can invite ConchBot to your server "
        "[here](https://discord.com/api/oauth2/authorize?client_id=733467297666170980&permissions=388102&scope=bot)")
        embed.add_field(name="Support Server Invite:", value="You can join ConchBot Support "
        "[here](https://discord.gg/PyAcRfukvc)")
        embed.add_field(name="ConchBot's creator (UnsoughtConch)'s community server:",
        value="You can join Conch's community server [here](https://discord.gg/n8XyytfxMk)")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Support(client))
