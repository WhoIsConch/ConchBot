import discord
from discord.ext import commands
import DiscordUtils

cmds = {
    "joke" : {
        "title" : "Joke Command",
        "desc" : "Returns a joke from the r/jokes subreddit!",
        "htu" : "cb joke",
        "aliases" : "*No Aliases*"
    },
    "ai" : {
        "title" : "AI Command",
        "desc" : "Set up a channel where you can talk to ConchBot's chatbot!",
        "htu" : "\"cb ai,\" or manually by naming a channel \"conchchat\"",
        "aliases" : "\"chatbot\""
    },
    "echo" : {
        "title" : "Echo Command",
        "desc" : "Sends a message to the specified channel.",
        "htu" : "cb echo {channel mention} {message}",
        "aliases" : "\"repeat\""
    },
    "8Ball" : {
        "title" : "8Ball Command",
        "desc" : "Ask the 8ball a question and it will return an answer.",
        "htu" : "cb 8ball {question}",
        "aliases" : "*No Aliases*"
    },
    "google" : {
        "title" : "Google Command",
        "desc" : "Googles something for you! This does *not* return a description, just a link.",
        "htu" : "cb google {query}",
        "aliases" : "\"lmgtfy\""
    },
    "chance" : {
        "title" : "Chance Command",
        "desc" : "Rates the chances of something happening on a scale ranging from 1 to 10",
        "htu" : "cb chance {question}",
        "aliases" : "\"chances,\" \"odds,\" \"odd\""
    },
    "avatar" : {
        "title" : "Avatar Command",
        "desc" : "Enlarges you or a friend's profile photo!",
        "htu" : "cb avatar {[optional]:member mention}",
        "aliases" : "\"pfp\""
    },
    "meme" : {
        "title" : "Meme Command",
        "desc" : "Returns a meme from the r/memes subreddit.",
        "htu" : "cb meme",
        "aliases" : "*No Aliases*"
    },
    "reddit" : {
        "title" : "Reddit Command",
        "desc" : "Returns a post from the specified subreddit.",
        "htu" : "cb reddit {subreddit}",
        "aliases" : "*No Aliases*"
    },
    "itft" : {
        "title" : "It's This For That Command",
        "desc" : "Returns a result from https://itsthisforthat.com",
        "htu" : "cb itft",
        "aliases" : "*No Aliases*"
    },
    "lyrics" : {
        "title" : "Lyrics Command [BETA]",
        "desc" : "Get the lyrics of your favorite song!",
        "htu" : "cb lyrics {band}, {song}",
        "aliases" : "*No Aliases*"
    },
    "fbi" : {
        "title" : "FBI Command",
        "desc" : "Search through the FBI Most Wanted database!",
        "htu" : "cb fbi",
        "aliases" : "*No Aliases*"
    },
    "fbi details" : {
        "title" : "FBI Details Command",
        "desc" : "Get more details of an entry via a UID.",
        "htu" : "cb fbi details {uid}",
        "aliases" : "*No Aliases*"
    },
    "covid" : {
        "title" : "COVID Command",
        "desc" : "Get COVID statistics for the specified country!",
        "htu" : "cb covid {country}",
        "aliases" : "*No Aliases*"
    },
    "snipe" : {
        "title" : "Snipe and Snipe Edit Commands",
        "desc" : "\"Snipe\" gets a previously deleted message, while \"snipe edit\" gets a previously edited message.",
        "htu" : "\"cb snipe\" or \"cb snipe edit\"",
        "alaises" : "*No Aliases"
    },
    "ping" : {
        "title" : "Ping Command",
        "desc" : "Gives you the bot's ping.",
        "htu" : "cb ping",
        "aliases" : "*No Aliases*"
    },
    "clear" : {
        "title" : "Clear Command",
        "desc" : "Clears the spevidied amount of messages.",
        "htu" : "cb clear {amount}",
        "aliases" : "\"purge\""
    },
    "stats" : {
        "title" : "Stats Command",
        "desc" : "Returns bot statistics, such as its server count, the bot version, Python version, and more.",
        "htu" : "cb stats",
        "aliases" : "\"statistics,\" \"info,\" \"information\""
    },
    "inventory" : {
        "title" : "Inventory Command",
        "desc" : "Shows you the items in your inventory, as well as your wallet and bank balance.",
        "htu" : "cb inventory",
        "aliases" : "\"inv,\" \"bal,\" \"balance,\" \"bag\""
    },
    "deposit" : {
        "title" : "Deposit Command",
        "desc" : "Deposit moners from your wallet into your bank.",
        "htu" : "cb deposit {amount or \"all\"}",
        "aliases" : "\"dep\""
    },
    "withdraw" : {
        "title" : "Withdraw Command",
        "desc" : "Withdraw moners from your bank into your wallet.",
        "htu" : "cb withdraw {amount}",
        "aliases" : "\"with\""
    },
    "buy" : {
        "title" : "Buy Command",
        "desc" : "Buy something from the shop!",
        "htu" : "cb buy {item} {[optional]: amount}",
        "aliases" : "*No Aliases*"
    },
    "sell" : {
        "title" : "Sell Command",
        "desc" : "Sell the items in your inventory.",
        "htu" : "cb sell {item} {[optional]: amount}",
        "aliases" : "*No Aliases*"
    },
    "shop" : {
        "title" : "Shop Command",
        "desc" : "View the currently available shop items.",
        "htu" : "cb shop",
        "aliases" : "*No Aliases*"
    },
    "beg" : {
        "title" : "Beg Command",
        "desc" : "Beg for some moners!",
        "htu" : "cb beg",
        "aliases" : "*No Aliases*"
    },
    "steal" : {
        "title" : "Steal Command",
        "desc" : "Steal moners from another user.",
        "htu" : "cb steal {user mention or ID}",
        "aliases" : "\"rob,\" \"yoink\""
    },
    "give" : {
        "title" : "Give Command",
        "desc" : "A highly interactive command to give others moners or items",
        "htu" : "cb give {user mention} {\"moners\" or \"item\"}",
        "aliases" : "\"gift\""
    },
    "slots" : {
        "title" : "Slots Command",
        "desc" : "Bet your moners on some slots. Your amount could be doubled, pentupled, or dectupled.",
        "htu" : "cb slots {amount}",
        "aliases" : "*No Aliases*"
    },
    "daily" : {
        "title" : "Daily Command",
        "desc" : "Collect your daily moners!",
        "htu" : "cb daily",
        "aliases" : "*No Aliases*"
    },
    "use" : {
        "title" : "Use Command",
        "desc" : "Use an item in your inventory.",
        "htu" : "cb use {item}",
        "aliases" : "*No Aliases*"
    },
    'task' : {
        "title" : "Task Command",
        "desc" : "Complete listed tasks!",
        "htu" : "cb task",
        "aliases" : "\"tasks\""
    },
    "supportc" : {
        "title" : "SupportC Command",
        "desc" : "Returns some extra support information, along with a link to ConchBot's server.",
        "htu" : "cb supportc",
        "aliases" : "*No Aliases*"
    },
    "report" : {
        "title" : "Report Command",
        "desc" : "Report a bug found within ConchBot",
        "htu" : "cb report {bug or problem, as much detail as possible}",
        "aliases" : "*No Aliases*"
    },
    "suggest" : {
        "title" : "Suggest Command",
        "desc" : "Suggests an idea to the ConchBot support server.",
        "htu" : "cb suggest {suggestion}",
        "aliases" : "*No Aliases*"
    },
    "invite" : {
        "title" : "Invite Command",
        "desc" : "Returns an invite to ConchBot's support server and a link to invite him to another server.",
        "htu" : "cb invite",
        "aliases" : "*No Aliases*"
    },
    "vote" : {
        "title" : "Vote Command",
        "desc" : "Returns links where you can vote for ConchBot!",
        "htu" : "cb vote",
        "aliases" : "*No Aliases*"
    },
    "vote claim" : {
        "title" : "Vote Claim Command",
        "desc" : "claim your ConchBot vote!",
        "htu" : "cb vote claim",
        "aliases" : "*No Aliases*"
    },
    "fuck" : {
        "title" : "Fuck Command",
        "desc" : "Creates a meme in the \"All My Homies Hate\" meme format!",
        "htu" : "cb fuck {value1}, {[optional]: value2}",
        "aliases" : "*No Aliases*"
    },
    "brain" : {
        "title" : "Brain Command",
        "desc" : "Creates a meme in the \"You Still Awake?\" meme format!",
        "htu" : "cb brain {value}",
        "aliases" : "*No Aliases*"
    },
    "mentalillness" : {
        "title" : "Mental Illness Command",
        "desc" : "Creates a meme in the \"Drawings Made by People with Mental Illnesses\" meme format!",
        "htu" : "cb mentalillness {image URL or attachment}",
        "aliases" : "*No Aliases*"
    },
    "idputmy" : {
        "title" : "I'd Put My Command",
        "desc" : "Creates a meme in the \"This is Where I'd Put My Trophy, if I Had One\" meme format!",
        "htu" : "cb idputmy {value}",
        "aliases" : "*No Aliases*"
    },
    "isthis" : {
        "title" : "Is This Command",
        "desc" : "Creates a meme in the \"Is This a Pigeon?\" meme format!",
        "htu" : "cb isthis {value1}, {value2}, {value3}",
        "aliases" : "*No Aliases*"
    },
    "tradeoffer" : {
        "title" : "Trade Offer Command",
        "desc" : "Creates a meme in the \"Trade Offer\" format!",
        "htu" : "cb tradeoffer {ireceive}, {youreceive}",
        "aliases" : "*No Aliases*"
    },
    "tag" : {
        "title" : "Tag Command Group",
        "desc" : "You can create, edit, and delete tags, or custom commands!",
        "htu" : "\"cb tag {create, edit, or delete} {name[create and edit], ID[delete]}, {content[create and edit]}\"",
        "aliases" : "tags"
    },
    "updates" : {
        "title" : "Updates Command",
        "desc" : "Shows you ConchBot's latest updates!",
        "htu" : "cb updates",
        "aliases" : "\"update\""
    },
    "leave" : {
        "title" : "Leave Command",
        "desc" : "Removes ConchBot from your server.",
        "htu" : "cb leave",
        "aliases" : "*No Aliases*"
    }
}

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def help(self, ctx, command=None):
        if command is None:
            embed0 = discord.Embed(
                title="ConchBot Commands",
                colour=ctx.author.colour
            )
            embed0.add_field(name="ConchBot Help", value="ConchBot is a small bot trying to grow, so your support would"
            " be amazing! Even as much as a vote on Top.gg or DBL can help greatly.\nMy command prefix is `cb `.\n"
            "You can see my latest updates via \"cb updates\"", inline=False)
            embed0.add_field(name="Fun Commands", value="`AI, Echo, 8ball, Google, Chance, Pfp, Joke, Meme, Reddit`\n"
            "View more information on page `1`.")
            embed0.add_field(name="Utility Commands", value="`Ping, Clear, Stats`\nView more information on page `2`.")
            embed0.add_field(name="Economy Commands", value="`Inventory, Deposit, Withdraw, Buy, Sell, Shop, Beg, "
            "Steal, Give, Slots, Daily, Use`\nView more information on page `3`.")
            embed0.add_field(name="Image Commands", value="`Fuck, Brain, MentalIllness, idputmy, isthis`\nView more"
            " information on page `4`.")
            embed0.add_field(name="Support Commands", value="`Report, Suggest, Invite, Vote, Vote Claim`\nView more"
            " information on page `5`.")
            embed0.add_field(name="Extra Links", value="[Invite Me!](https://top.gg/bot/733467297666170980/invite/)"
            " | [Support Server](https://discord.gg/PyAcRfukvc) | [Website](https://conch.glitch.me) "
            "| [Vote on Top.gg](https://top.gg/bot/733467297666170980/vote/)"
            " | [Vote on Discord Bot List](https://discordbotlist.com/bots/conchbot/upvote)", inline=False)
            embed0.set_footer(text = "Discord ConchBot | Made by UnsoughtConch")
            
            
            embed1 = discord.Embed(
                title="ConchBot Fun Commands",
                colour = ctx.author.colour
            )
            embed1.add_field(name="AI", value="Tells you how to talk to ConchBot's AI!", inline=False)
            embed1.add_field(name="Echo", value="Sends a message in a specified channel.", inline=False)
            embed1.add_field(name="8ball", value="Ask the 8ball a question!", inline=False)
            embed1.add_field(name="Google", value="Googles something for you!", inline=False)
            embed1.add_field(name="Chance", value="Rates the chance of something happening", inline=False)
            embed1.add_field(name="Pfp", value="Shows you or someone else's profile photo.", inline=False)
            embed1.add_field(name="Joke", value="Get a joke from the r/jokes subreddit.", inline=False)
            embed1.add_field(name="Meme", value="Get a nice little meme from the r/memes subreddit.", inline=False)
            embed1.add_field(name="Reddit", value="Specify a subreddit and get a post from there!", inline=False)
            embed1.add_field(name="Snipe", value="Snipe a previously deleted message, or an edited message with \"snipe edit!\"")
            embed1.add_field(name="FBI", value="Look through the FBI watchlist! \"fbi details\" gives you a more descriptive"
            "version of the person you are looking at.")
            embed1.set_footer(text="For more information on a certain command, please use 'cb help command.'")
            
            embed2 = discord.Embed(
                title="ConchBot Utility Commands",
                colour = ctx.author.colour
            )
            embed2.add_field(name="Ping", value="To see my ping. Maybe you're into knowing how long it'll take me"
            " to respond.", inline=False)
            embed2.add_field(name="Clear", value="Clear a certain amount of messages from a channel.", inline=False)
            embed2.add_field(name="Stats", value="View ConchBot's stats, such as server count, bot version, "
            "Python version and more.", inline=False)
            embed2.add_field(name="Tag", value="Creates a custom command, or tag!")
            embed2.add_field(name="Updates", value="Shows ConchBot's latest updates!")
            embed2.add_field(name="Leave", value="Makes ConchBot leave your server.")
            embed2.set_footer(text="For more information on a certain command, please use 'cb help command'")

            embed3 = discord.Embed(
                title="Currency Commands",
                colour=ctx.author.colour
                )
            embed3.add_field(name="Inventory", value="Shows your bank and wallet balance, as well as what items you own.", inline=False)
            embed3.add_field(name="Deposit", value="Deposit moners from your wallet to your bank.", inline=False)
            embed3.add_field(name="Withdraw", value="Withdraws moners from your bank to your wallet.", inline=False)
            embed3.add_field(name="Buy", value="Buy something from the shop.", inline=False)
            embed3.add_field(name="Sell", value="Sell something you have in your inventory.", inline=False)
            embed3.add_field(name="Shop", value="View the items in the shop available for purchase.", inline=False)
            embed3.add_field(name="Beg", value="Beg for some moners.", inline=False)
            embed3.add_field(name="Steal", value="Steal from other people!", inline=False)
            embed3.add_field(name="Give", value="A highly interactive command to let you give people either"
            " moners or items!", inline=False)
            embed3.add_field(name="Slots", value="Bet your money, can get doubled, pentupled, or dectupled!", inline=False)
            embed3.add_field(name="Daily", value="Collect your daily moners.", inline=False)
            embed3.add_field(name="Use", value="Use an item in your inventory!", inline=False)
            embed3.set_footer(text="For more information on a command, please use 'cb help command'")
            
            embed4 = discord.Embed(title="Image Commands", colour=ctx.author.colour)
            embed4.add_field(name="Fuck Command", value="Creates a meme in the 'all my homies hate' format!", inline=False)
            embed4.add_field(name="Brain Command", value="Creates a meme in the 'are you going to sleep?' format!", inline=False)
            embed4.add_field(name="Mentalillness", value="Creates a meme in the 'drawings made by people with mental "
            "ilness' format!", inline=False)
            embed4.add_field(name="idputmy", value="Creates a meme in the 'this is where I'd put my trophy, if I had one'"
            " format!", inline=False)
            embed4.add_field(name="isthis", value="Creates a meme in the 'is this a pigeon?' format!", inline=False)
            embed4.add_field(name="tradeoffer", value="Creates a meme in the 'Trade Offer' format!", inline=False)
            embed4.set_footer(text="For more information on a command, please use 'cb help command.'")
            
            embed5 = discord.Embed(title="Support Commands", colour=ctx.author.colour)
            embed5.add_field(name="Supportc", value="Kind of like a second support help command, but with more" 
            " information.")
            embed5.add_field(name="Report", value="Report a ConchBot bug.", inline=False)
            embed5.add_field(name="Suggest", value="Give a ConchBot suggestion!", inline=False)
            embed5.add_field(name="Invite", value="Invite ConchBot to your server, and gain an invite to the Support server!", inline=False)
            embed5.add_field(name="Vote", value="Returns links where you can vote for ConchBot", inline=False)
            embed5.set_footer(text="For more information on a command, please use 'cb help command.'")

            embeds = [embed0, embed1, embed2, embed3, embed4, embed5]

            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('0️⃣', "first")
            paginator.add_reaction('1️⃣', "page 1")
            paginator.add_reaction('2️⃣', "page 2")
            paginator.add_reaction('3️⃣', "page 3")
            paginator.add_reaction('4️⃣', "page 4")
            paginator.add_reaction('5️⃣', "page 5")
            paginator.add_reaction('⏩', "next")
            
            await paginator.run(embeds)

        else:
            try:
                embed = discord.Embed(title=cmds[command].get("title"))
                embed.add_field(name="Description:", value=cmds[command].get("desc"), inline=False)
                embed.add_field(name="How to Use:", value=cmds[command].get("htu"), inline=False)
                embed.add_field(name="Aliases:", value=cmds[command].get("aliases"), inline=False)
                embed.set_footer(text="For a list of command categories, use cb help.")
                await ctx.send(embed=embed)
            except:
                await ctx.send("Invalid Help Command")

def setup(client):
    client.add_cog(Help(client))
