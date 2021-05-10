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
    },
    "sauce" : {
        "title" : "Sauce Command",
        "desc" : "\"cb sauce\" grabs a random image from nhentai.com, while \"cb sauce {id}\" searches for a certain comic!",
        "htu" : "cb sauce {[optional]: ID}",
        "aliases" : "*No Aliases*"
    },
    "rule34" : {
        "title" : "Rule34 Command",
        "desc" : "\"cb rule34\" grabs a random image from rule34.xxx, while \"cb rule34 {tag}\" searches for posts with that tag!",
        "htu" : "cb rule34 {[optional]: tag}",
        "aliases" : "\"r34\""
    },
    "hentai" : {
        "title" : "Hentai Command",
        "desc" : "Grabs a random post from r/hentai!",
        "htu" : "cb hentai",
        "aliases" : "*No Aliases*"
    },
    "porn" : {
        "title" : "Porn Command",
        "desc" : "Grabs a random post from r/porn!",
        "htu" : "cb porn",
        "aliases" : "*No Aliases*"
    },
    "boobs" : {
        "title" : "Boobs Command",
        "desc" : "Grabs a random post from r/boobs!",
        "htu" : "cb boobs",
        "aliases" : "\"boob,\" \"tits,\" \"tit\""
    },
    "pussy" : {
        "title" : "Pussy Command",
        "desc" : "Grabs a random post from r/pussy!",
        "htu" : "cb pussy",
        "aliases" : "\"vagina\""
    },
    "boobdrop" : {
        "title" : "Boob Drop Command",
        "desc" : "Get a boob drop post from r/tittydrop!",
        "htu" : "cb boobdrop",
        "aliases" : "\"tittydrop,\" \"boobdrop\""
    },
    "feet" : {
        "title" : "Feet Command",
        "desc" : "What type of cretin unironically has a foot fetish?",
        "htu" : "You don't.",
        "aliases" : "*No Aliases*"
    },
    "gay" : {
        "title" : "Gay Command",
        "desc" : "Get a porn post from r/gayporn!",
        "htu" : "cb gay",
        "aliases" : "*No Aliases*"
    },
    "lesbian" : {
        "title" : "Lesbian Command",
        "desc" : "Get a post from r/lesbians!",
        "htu" : "cb lesbian",
        "aliases" : "\"lesbo\""
    },
    "overwatch" : {
        "title" : "Overwatch Command",
        "desc" : "Get a porn post from r/Overwatch_porn!",
        "htu" : "cb overwatch",
        "aliases" : "*No Aliases*"
    },
    "sfm" : {
        "title" : "SFM Command",
        "desc" : "Get a post from r/SFMCompileClub!",
        "htu" : "cb sfm",
        "aliases" : "*No Aliases*"
    },
    "waifu" : {
        "title" : "Waifu Command",
        "desc" : "Get a post from r/WaifusGoneWild!",
        "htu" : "cb waifu",
        "aliases" : "*No Aliases*"
    },
    "futa" : {
        "title" : "Futa Command",
        "desc" : "Get a post from r/futanari!",
        "htu" : "cb futa",
        "aliases" : "\"futanari\""
    },
    "bdsm" : {
        "title" : "BDSM Command",
        "desc" : "Get a post from r/BDSM!",
        "htu" : "cb bdsm",
        "aliases" : "*No Aliases*"
    }
}

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    async def getembed(self, type):
        if type == "help":
            embed = discord.Embed(title="ConchBot Commands", colour=discord.Colour.green())
            embed.add_field(name="ConchBot Help", value="ConchBot is a small bot trying to grow, so your support would"
            " be amazing! Even as much as a vote on Top.gg or DBL can help greatly.\nMy command prefix is `cb `.\n"
            "You can see my latest updates via \"cb updates\"", inline=False)
            embed.add_field(name="Fun Commands", value="`AI, Echo, 8ball, Google, Chance, Pfp, Joke, Meme, Reddit`\n"
            "View more information on page `1`.")
            embed.add_field(name="Utility Commands", value="`Ping, Clear, Stats`\nView more information on page `2`.")
            embed.add_field(name="Economy Commands", value="`Inventory, Deposit, Withdraw, Buy, Sell, Shop, Beg, "
            "Steal, Give, Slots, Daily, Use`\nView more information on page `3`.")
            embed.add_field(name="Image Commands", value="`Fuck, Brain, MentalIllness, idputmy, isthis`\nView more"
            " information on page `4`.")
            embed.add_field(name="Support Commands", value="`Report, Suggest, Invite, Vote, Vote Claim`\nView more"
            " information on page `5`.")
            embed.add_field(name="NSFW Commands", value="`Sauce, Rule34, Hentai, Porn, Boobs, Pussy, Boobdrop, Feet, Gay, "
            "Overwatch, SFM, Waifu, Lesbain, Futanari, BDSM`\nView more information on page `6`.")
            embed.add_field(name="Extra Links", value="[Invite Me!](https://top.gg/bot/733467297666170980/invite/)"
            " | [Support Server](https://discord.gg/PyAcRfukvc) | [Website](https://conch.glitch.me) "
            "| [Vote on Top.gg](https://top.gg/bot/733467297666170980/vote/)"
            " | [Vote on Discord Bot List](https://discordbotlist.com/bots/conchbot/upvote)", inline=False)
            embed.set_footer(text = "Discord ConchBot | Made by UnsoughtConch")

        elif type == "fun":
            embed = discord.Embed(title="ConchBot Fun Commands", colour=discord.Color.gold())
            embed.add_field(name="AI", value="Tells you how to talk to ConchBot's AI!")
            embed.add_field(name="Echo", value="Sends a message in a specified channel.")
            embed.add_field(name="8ball", value="Ask the 8ball a question!")
            embed.add_field(name="Google", value="Googles something for you!")
            embed.add_field(name="Chance", value="Rates the chance of something happening")
            embed.add_field(name="Pfp", value="Shows you or someone else's profile photo.")
            embed.add_field(name="Joke", value="Get a joke from the r/jokes subreddit.")
            embed.add_field(name="Meme", value="Get a nice little meme from the r/memes subreddit.")
            embed.add_field(name="Reddit", value="Specify a subreddit and get a post from there!")
            embed.add_field(name="Snipe", value="Snipe a previously deleted message, or an edited message with \"snipe edit!\"")
            embed.add_field(name="FBI", value="Look through the FBI watchlist! \"fbi details\" gives you a more descriptive"
            "version of the person you are looking at.")
            embed.set_footer(text="For more information on a certain command, please use 'cb help command.'")

        elif type == "utility":
            embed = discord.Embed(title="ConchBot Utility Commands", colour=discord.Color.greyple())
            embed.add_field(name="Ping", value="To see my ping. Maybe you're into knowing how long it'll take me"
            " to respond.")
            embed.add_field(name="Clear", value="Clear a certain amount of messages from a channel.")
            embed.add_field(name="Stats", value="View ConchBot's stats, such as server count, bot version, "
            "Python version and more.")
            embed.add_field(name="Tag", value="Creates a custom command, or tag!")
            embed.add_field(name="Updates", value="Shows ConchBot's latest updates!")
            embed.add_field(name="Leave", value="Makes ConchBot leave your server.")
            embed.set_footer(text="For more information on a certain command, please use 'cb help command'")
        
        elif type == "economy":
            embed = discord.Embed(title="Economy Commands", colour=discord.Color.green())
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

        elif type == "image":
            embed = discord.Embed(title="Image Commands", colour=discord.Color.magenta())
            embed.add_field(name="Fuck Command", value="Creates a meme in the 'all my homies hate' format!")
            embed.add_field(name="Brain Command", value="Creates a meme in the 'are you going to sleep?' format!")
            embed.add_field(name="Mentalillness", value="Creates a meme in the 'drawings made by people with mental "
            "ilness' format!")
            embed.add_field(name="idputmy", value="Creates a meme in the 'this is where I'd put my trophy, if I had one'"
            " format!")
            embed.add_field(name="isthis", value="Creates a meme in the 'is this a pigeon?' format!")
            embed.add_field(name="tradeoffer", value="Creates a meme in the 'Trade Offer' format!")
            embed.set_footer(text="For more information on a command, please use 'cb help command.'")

        elif type == "support":
            embed = discord.Embed(title="Support Commands", colour=discord.Color.red())
            embed.add_field(name="Supportc", value="Kind of like a second support help command, but with more" 
            " information.")
            embed.add_field(name="Report", value="Report a ConchBot bug.")
            embed.add_field(name="Suggest", value="Give a ConchBot suggestion!")
            embed.add_field(name="Invite", value="Invite ConchBot to your server, and gain an invite to the Support server!", inline=False)
            embed.add_field(name="Vote", value="Returns links where you can vote for ConchBot")
            embed.set_footer(text="For more information on a command, please use 'cb help command.'")

        elif type == "nsfw":
            embed = discord.Embed(title="NSFW Commands", color=0xFFFAFA)
            embed.add_field(name="Sauce", value="Search for source codes on nhentai.com, or don't provide a code for a "
            "random nhentai.com image!")
            embed.add_field(name="Rule34", value="Search for posts on Rule34.xxx, or don't provide a search term for "
            "a random post!")
            embed.add_field(name="Hentai", value="Get a random hentai image from r/hentai!")
            embed.add_field(name="Porn", value="get a porn post from r/porn!")
            embed.add_field(name="Boobs", value="Get a boob post from r/boobs!")
            embed.add_field(name="Pussy", value="Get a pussy post from r/pussy!")
            embed.add_field(name="Boobdrop", value="Get a boob drop post from r/tittydrop!")
            embed.add_field(name="Feet", value="What type of cretin unironically has a foot fetish?")
            embed.add_field(name="Gay", value="Get a porn post from r/gayporn!")
            embed.add_field(name="Overwatch", value="Get a porn post from r/Overwatch_porn!")
            embed.add_field(name="SFM", value="Get a post from r/SFMCompileClub!")
            embed.add_field(name="Waifu", value="Get a post from r/WaifusGoneWild!")
            embed.add_field(name="Lesbian", value="Get a post from r/lesbians!")
            embed.add_field(name="Futanari", value="Get a post from r/futanari!")
            embed.add_field(name="BDSM", value="Get a post from r/BSDM!")
            embed.set_footer(text="For more information on a command, please use 'cb help command.'")
            
        return embed

    @commands.group(invoke_without_command=True)
    async def help(self, ctx, command=None):
        if command is None:
            embed0 = await self.getembed("help")
            embed1 = await self.getembed("fun")
            embed2 = await self.getembed("utility")
            embed3 = await self.getembed("economy")
            embed4 = await self.getembed("image")
            embed5 = await self.getembed("support")
            embed6 = await self.getembed("nsfw")

            embeds = [embed0, embed1, embed2, embed3, embed4, embed5, embed6]

            paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('0️⃣', "first")
            paginator.add_reaction('1️⃣', "page 1")
            paginator.add_reaction('2️⃣', "page 2")
            paginator.add_reaction('3️⃣', "page 3")
            paginator.add_reaction('4️⃣', "page 4")
            paginator.add_reaction('5️⃣', "page 5")
            paginator.add_reaction('6️⃣', "page 6")
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
                try:
                    embed = await self.getembed(command)
                    await ctx.send(embed=embed)
                except:
                    await ctx.send("Invalid help value.")

def setup(client):
    client.add_cog(Help(client))
