import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(
            title="ConchBot Commands",
            colour=ctx.author.colour
        )
        embed.add_field(name="Fun Commands", value="For information on our fun commands, please use"
        " \"cb help fun\"", inline=False)
        embed.add_field(name="Utility Commands", value="For information on our fun commands, please "
        "use \"cb help utility\"", inline=False)
        embed.add_field(name="Currency Commands", value="Currency commands are temporarily disabled due to "
        "the new update. They will be available soon.", inline=False)
        embed.add_field(name="Support Commands", value="For information on our support commands, please use"
        " \"cb help misc\"", inline=False)
        embed.set_footer(text="You can get a support server invite and invite the bot with 'cb invite'")
        await ctx.send(embed=embed)
    
    @help.command()
    async def fun(self, ctx):
        embed = discord.Embed(
            title="ConchBot Fun Commands",
            colour = ctx.author.colour
        )
        embed.add_field(name="Joke", value="Command group that returns a joke. "
        "***Commands currently disabled.***", inline=False)
        embed.add_field(name="AI", value="Sets up an AI chatbot channel.", inline=False)
        embed.add_field(name="Echo", value="Sends a message in a specified channel.", inline=False)
        embed.add_field(name="8ball", value="Ask the 8ball a question!")
        embed.add_field(name="Google", value="Googles something for you!")
        embed.add_field(name="Chance", value="Rates the chance of something happening")
        embed.add_field(name="Pfp", value="Shows you or someone else's profile photo.")
        embed.set_footer(text="For more information on a certain command, please use 'cb help command.'")
        await ctx.send(embed=embed)
    
    @help.command()
    async def joke(self, ctx):
        embed = discord.Embed(
            title="Joke Command",
            colour = ctx.author.colour
        )
        embed.add_field(name="**COMMAND CURRENTLY DISABLED**", value="Due to some errors, the joke command and"
        " subcommands are currently disabled.", inline=False)
        embed.add_field(name="Description:", value="Command Group that returns a joke.", inline=False)
        embed.add_field(name="Subcommands:", value="JOKE: returns a joke. \nDEV: Returns a developer joke."
        "\nSPOOKY: returns a spooky joke.\nPUN: Returns a pun.", inline=False)
        embed.add_field(name="How to use:", value="'cb joke,' 'cb joke dev', 'cb joke spooky,' 'cb joke pun.'",
        inline=False)
        embed.add_field(name='Alaises:', value="DEV: 'developer,' 'programmer.'\nSPOOKY: 'scary,' 'spook'",
        inline=False)
        embed.set_footer(text="To see a list of fun commands, use 'cb help fun.'")
        await ctx.send(embed=embed)
    
    @help.command()
    async def ai(self, ctx):
        embed = discord.Embed(
            title="AI Command",
            colour=ctx.author.colour
        )
        embed.add_field(name="**COMMAND DISABLED**", value="Command is currently disabled due to "
        "threading issues.", inline=False)
        embed.add_field(name="Description:", value="Sets up an AI chatbot channel. After setting up the channel"
        ", you can speak to ConchBot's AI.", inline=False)
        embed.add_field(name="How to use:", value="cb ai #{channel you want chatbot to speak in}", inline=False)
        embed.add_field(name="Aliases:", value="'Chatbot'", inline=False)
        embed.set_footer(text="To see a list of fun commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def echo(self, ctx):
        embed = discord.Embed(
            title="Echo Command",
            colour=ctx.author.colour
        )
        embed.add_field(name="Description:", value="Sends a message to the specified channel.", inline=False)
        embed.add_field(name="How to use:", value="cb echo #{channel to send message} {message}", inline=False)
        embed.add_field(name="Aliases:", value="'repeat'", inline=False)
        embed.set_footer(text="To see a list of fun commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command(name="8ball")
    async def _8ball(self, ctx):
        embed = discord.Embed(
            title="8ball Command",
            colour=ctx.author.colour
        )
        embed.add_field(name="Description:", value="Ask the 8ball a question, and it will reply "
        "with an answer.", inline=False)
        embed.add_field(name="How to use:", value="cb 8ball {question}", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases.*", inline=False)
        embed.set_footer(text="To see a list of fun commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def google(self, ctx):
        embed = discord.Embed(
                title="Google Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Googles something for you! This does *not*"
        " Return a description, just a link. Kind of like that Let Me Google That For You"
        " website.", inline=False)
        embed.add_field(name="How to use:", value="cb google {what you want to google}", inline=False)
        embed.add_field(name="Aliases:", value="'LMGTFY'", inline=False)
        embed.set_footer(text="To see a list of fun commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def chance(self, ctx):
        embed = discord.Embed(
                title="Chance Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Rates the chances of something happening on a scale"
        " of 0 to 10.", inline=False)
        embed.add_field(name="How to use:", value="cb chance {question}", inline=False)
        embed.add_field(name="Aliases:", value="'chances,' 'odds,' 'odd.'", inline=False)
        embed.set_footer(text="To see a list of fun commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def pfp(self, ctx):
        embed = discord.Embed(
                title="PFP Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Shows the profile photo of you or someone else!",
        inline=False)
        embed.add_field(name="How to use:", value="cb pfp @{someone else[optional]}", inline=False)
        embed.add_field(name="Aliases:", value="'avatar'", inline=False)
        embed.set_footer(text="To see a list of fun commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def utility(self, ctx):
        embed = discord.Embed(
            title="ConchBot Utility Commands",
            colour = ctx.author.colour
        )
        embed.add_field(name="Ping", value="To see my ping. Maybe you're into knowing how long it'll take me"
        " to respond.")
        embed.add_field(name="Kick", value="Kick a member.")
        embed.add_field(name="Ban", value="Ban someone.")
        embed.add_field(name="Unban", value="Unban someone.")
        embed.add_field(name="Clear", value="Clear a certain amount of messages from a channel.")
        embed.add_field(name="Stats", value="View ConchBot's stats, such as server count, bot version, "
        "Python version and more.")
        embed.set_footer(text="For more information on a certain command, please use 'cb help command'")
        await ctx.send(embed=embed)
    
    @help.command()
    async def ping(self, ctx):
        embed = discord.Embed(
                title="Ping Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Gives you the bot's ping. ", inline=False)
        embed.add_field(name="How to use:", value="cb ping", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of utility commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def kick(self, ctx):
        embed = discord.Embed(
                title="Kick Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Kicks the specified user.", inline=False)
        embed.add_field(name="How to use:", value="cb kick @{person to kick}", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of utility commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def ban(self, ctx):
        embed = discord.Embed(
                title="Ban Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Bans the specified user.", inline=False)
        embed.add_field(name="How to use:", value="cb ban @{user to ban}", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of utility commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def unban(self, ctx):
        embed = discord.Embed(
                title="Unban Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Unbans the specified user.", inline=False)
        embed.add_field(name="How to use:", value="cb unban {user name}#{user tag}", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of utility commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def clear(self, ctx):
        embed = discord.Embed(
                title="Clear Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Clears the specified amount of messages.", inline=False)
        embed.add_field(name="How to use:", value="cb clear {amount of messages}", inline=False)
        embed.add_field(name="Aliases:", value="purge", inline=False)
        embed.set_footer(text="To see a list of utility commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def stats(self, ctx):
        embed = discord.Embed(
                title="Stats Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Returns the bot's stats, such as server count, "
        "bot version, Python version and more.", inline=False)
        embed.add_field(name="How to use:", value="cb stats", inline=False)
        embed.add_field(name="Aliases:", value="'statistics,' 'info,' 'information.'", inline=False)
        embed.set_footer(text="To see a list of utility commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def currency(self, ctx):
        embed = discord.Embed(
            title="Currency Commands",
            colour=ctx.author.colour
        )
        embed.add_field(name="Inventory", value="Shows your bank and wallet balance, as well as what items you own.")
        embed.add_field(name="Deposit", value="Deposit moners from your wallet to your bank.")
        embed.add_field(name="Withdraw", value="Withdraws moners from your bank to your wallet.")
        embed.add_field(name="Buy", value="Buy something from the shop.")
        embed.add_field(name="Sell", value="Sell something you have in your inventory.")
        embed.add_field(name="Shop", value="View the items in the shop available for purchase.")
        embed.add_field(name="Beg", value="Beg for some moners.")
        embed.add_field(name="Steal", value="Steal from other people!")
        embed.add_field(name="Give", value="A highly interactive command to let you give people either"
        " moners or items!")
        embed.add_field(name="Slots", value="Bet your money, can get doubled, pentupled, or dectupled!")
        embed.add_field(name="Daily", value="Collect your daily moners.")
        embed.add_field(name="Use", value="Use an item in your inventory!")
        embed.set_footer(text="For more information on a command, please use 'cb help command'")
        await ctx.send(embed=embed)
    
    @help.command()
    async def inventory(self, ctx):
        embed = discord.Embed(
                title="Inventory Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Shows your bank and wallet balance, as well as "
        "the items in your inventory.", inline=False)
        embed.add_field(name="How to use:", value="cb inventoty", inline=False)
        embed.add_field(name="Aliases:", value="'inv,' 'bal', 'balance', 'bag.'", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")
        await ctx.send(embed=embed)

    @help.command()
    async def deposit(self, ctx):
        embed = discord.Embed(
                title="Deposit Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Deposits moners from your wallet to "
        "your bank.", inline=False)
        embed.add_field(name="How to use:", value="cb deposit {amount to deposit, or 'ALL'}", inline=False)
        embed.add_field(name="Aliases:", value="'dep'", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")
        await ctx.send(embed=embed)

    @help.command()
    async def withdraw(self, ctx):
        embed = discord.Embed(
                title="Withdraw Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Withdraws moners from your bank to "
        "your wallet", inline=False)
        embed.add_field(name="How to use:", value="cb withdraw {amount to withdraw, or 'ALL'}", inline=False)
        embed.add_field(name="Aliases:", value="'with'", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")
        await ctx.send(embed=embed)

    @help.command()
    async def buy(self, ctx):
        embed = discord.Embed(
                title="Buy Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Buy something from the shop.", inline=False)
        embed.add_field(name="How to use:", value="cb buy {item}", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")
        await ctx.send(embed=embed)

    @help.command()
    async def sell(self, ctx):
        embed = discord.Embed(
                title="Sell Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Sell something you have in your inventory.", inline=False)
        embed.add_field(name="How to use:", value="cb sell {item} {amount[optional]}", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")
        await ctx.send(embed=embed)

    @help.command()
    async def shop(self, ctx):
        embed = discord.Embed(
            title="Shop Command",
            colour=ctx.author.colour
        )
        embed.add_field(name="Description:", value="View the items in the shop that are available for purchase.", inline=False)
        embed.add_field(name="How To Use:", value="cb shop", inline=False)
        embed.add_field(name="Aliases:", value="*No Aliases*", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")
        await ctx.send(embed=embed)

    @help.command()
    async def beg(self, ctx):
        embed = discord.Embed(
                title="Beg Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Beg for some moners.", inline=False)
        embed.add_field(name="How to use:", value="cb beg", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")
        await ctx.send(embed=embed)

    @help.command()
    async def steal(self, ctx):
        embed = discord.Embed(
            title="Steal Command",
            colour = ctx.author.colour
        )
        embed.add_field(name="Description:", value="Steal moners from other users!", inline=False)
        embed.add_field(name="How to use:", value="'cb steal {user or ID}'", inline=False)
        embed.add_field(name="Aliases:", value="'rob,' 'yoink.'", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")

    @help.command()
    async def give(self, ctx):
        embed = discord.Embed(
            title="Give Command",
            colour = ctx.author.colour
        )
        embed.add_field(name="Description:", value="A highly interactive command that lets you give "
        "moners and items to your friends!", inline=False)
        embed.add_field(name="How to use:", value="cb give @user {'item' **or** 'moners'}", inline=False)
        embed.add_field(name="Aliases:", value="'gift.'", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")

    @help.command()
    async def slots(self, ctx):
        embed = discord.Embed(
                title="Slots Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Bet your moners! It can get doubled, pentupled, "
        "or dectupled!", inline=False)
        embed.add_field(name="How to use:", value="cb slots {amount to bet}", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")
        await ctx.send(embed=embed)

    @help.command()
    async def daily(self, ctx):
        embed = discord.Embed(
                title="Daily Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Collect your daily moners.", inline=False)
        embed.add_field(name="How to use:", value="cb daily", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of currency commands, use 'cb help currency.'")
        await ctx.send(embed=embed)

    @help.command()
    async def use(self, ctx):
        embed = discord.Embed(
                title="Use Command",
                colour = ctx.author.colour
            )
        embed.add_field(name="Description:", value="Use an item in your inventory!", inline=False)
        embed.add_field(name="How to use:", value="'cb use {item}", inline=False)
        embed.add_field(name="Aliases:", value="*No Aliases*", inline=False)
        embed.set_footer(text="To see a list of fun commands, use 'cb help fun.'")

    @help.command()
    async def support(self, ctx):
        embed = discord.Embed(
            title="Support Commands",
            colour=ctx.author.colour
        )
        embed.add_field(name="Supportc", value="Kind of like a second support help command, but with more" 
        " information.")
        embed.add_field(name="Report", value="Report a ConchBot bug.")
        embed.add_field(name="Suggest", value="Give a ConchBot suggestion!")
        embed.set_footer(text="For more information on a command, please use 'cb help command.'")
        await ctx.send(embed=embed)

    @help.command()
    async def supportc(self, ctx):
        embed = discord.Embed(
                title="Support Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Gives some info about support, and a link to ConchBot's"
        " Discord server.", inline=False)
        embed.add_field(name="How to use:", value="cb support", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of support commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def report(self, ctx):
        embed = discord.Embed(
                title="Report Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Report a ConchBot bug.", inline=False)
        embed.add_field(name="How to use:", value="cb report {detailed description of bug, such as "
        "what happened to cause the bug, what happens, etc.}", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of support commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

    @help.command()
    async def suggest(self, ctx):
        embed = discord.Embed(
                title="Suggest Command",
                colour=ctx.author.colour
            )
        embed.add_field(name="Description:", value="Suggests an idea to the ConchBot dev!", inline=False)
        embed.add_field(name="How to use:", value="cb suggest {suggestion}", inline=False)
        embed.add_field(name="Aliases:", value="*No aliases*", inline=False)
        embed.set_footer(text="To see a list of support commands, use 'cb help fun.'")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))
