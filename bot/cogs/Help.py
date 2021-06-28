import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client
 
    @commands.command()
    async def help(self, ctx, *, value=None):
        cogs = self.client.cogs
        print(cogs)
        if value is None:
            embed = discord.Embed(title="ConchBot Commands", colour=discord.Colour.green(), description="ConchBot is a small bot trying to grow, so your support would"
            " be amazing! Even as much as a vote on Top.gg or DBL can help greatly.\nMy command prefix is `cb `.\n"
            "You can see my latest updates via \"cb updates\"")
            for cog in cogs:
                print(cog)
                cmdlist = []
                commands = ""
                blacklist = ['Jishaku', 'Help', 'Config', 'Owner', 'Misc']
                if cog in blacklist:
                    continue

                flag = False

                if cog == 'NSFW' and not ctx.channel.is_nsfw():
                    commands = "`[COMMANDS EXPUNGED]`"
                    flag = True

                for command in cogs[cog].walk_commands():
                    if flag is True:
                        break
                    cmdlist.append(command)
                    commands += f"{command}, "

                if len([command for command in cmdlist]) < 1:
                    continue

                if flag is False:
                    finalcmds = commands[:-2]
                else:
                    finalcmds = commands

                embed.add_field(name=f"{cog} Commands", value=f"`{finalcmds}`", inline=False)

            embed.add_field(name="Extra Links", value="[Invite Me!](https://top.gg/bot/733467297666170980/invite/)"
            " | [Support Server](https://discord.gg/PyAcRfukvc) | [Website](https://conch.glitch.me) "
            "| [Vote on Top.gg](https://top.gg/bot/733467297666170980/vote/)"
            " | [Vote on Discord Bot List](https://discordbotlist.com/bots/conchbot/upvote)", inline=False)
            embed.set_footer(text = "Discord ConchBot | Made by UnsoughtConch")

            await ctx.send(embed=embed)

        else:
            command = self.client.get_command(value.lower())

            if command.cog.qualified_name == "NSFW":
                return await ctx.send("You can only view NSFW commands in NSFW-marked channels.")

            if command is not None:
                params = ""

                for thing in command.clean_params:
                    params += f"[{thing}] "
                embed = discord.Embed(title=f"{value} Command", color=discord.Color.random())
                embed.add_field(name="Description:", value=command.description, inline=False)
                if len(command.aliases) < 1:
                    aliases = '*No Aliases*'
                else:
                    aliases = command.aliases
                embed.add_field(name="Aliases:", value=aliases, inline=False)
                embed.add_field(name="How to use:", value=f"`cb {command.qualified_name} {params}`", inline=False)

                return await ctx.send(embed=embed)

            else:
                cog = self.client.get_cog(value)

                if cog is None:
                    embed = discord.Embed(title=f"No groups or commands by the name `{value}`", color=discord.Color.red(), description="Command categories are case-sensitive.")
                    return await ctx.send(embed=embed)

                if cog.qualified_name == "NSFW" and not ctx.channel.is_nsfw():
                    return await ctx.send("You can only view the NSFW category in NSFW-marked channels.")

                embed = discord.Embed(title=f"{cog.qualified_name} Category", color=discord.Color.random(), description=cog.description)
                commands = ""
                for command in cog.walk_commands():
                    commands += f"{command}, "
                embed.add_field(name="Commands:", value=f"`{commands[:-2]}`")

                await ctx.send(embed=embed)
                
def setup(client):
    client.add_cog(Help(client))
