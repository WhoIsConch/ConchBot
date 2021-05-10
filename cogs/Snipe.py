from datetime import datetime

from discord import Color, Embed
from discord.ext import commands

class Snipe(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot
        self.delete_snipes = dict()
        self.edit_snipes = dict()
        self.delete_snipes_attachments = dict()
        
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.delete_snipes[message.channel] = message
        self.delete_snipes_attachments[message.channel] = message.attachments

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.edit_snipes[after.channel] = (before, after)

    @commands.group(name='snipe')
    async def snipe_group(self, ctx):
        if ctx.invoked_subcommand is None:
            try:
                sniped_message = self.delete_snipes[ctx.channel]
            except KeyError:
                await ctx.send('There are no deleted messages in this channel to snipe!')
            else:
                result = Embed(
                    color=Color.red(),
                    description=sniped_message.content,
                    timestamp=sniped_message.created_at
                )
                result.set_author(name=sniped_message.author.display_name, icon_url=sniped_message.author.avatar_url)
                result.set_image(url=self.delete_snipes_attachments[ctx.channel][0].url)
                await ctx.send(embed=result)
                
    @snipe_group.command(name='edit')
    async def snipe_edit(self, ctx):
        try:
            before, after = self.edit_snipes[ctx.channel]
        except KeyError:
            await ctx.send('There are no message edits in this channel to snipe!')
        else:
            result = Embed(
                color=Color.red(),
                timestamp=after.edited_at
            )
            result.add_field(name='Before', value=before.content, inline=False)
            result.add_field(name='After', value=after.content, inline=False)
            result.set_author(name=after.author.display_name, icon_url=after.author.avatar_url)
            await ctx.send(embed=result)

def setup(client, *args, **kwargs):
    client.add_cog(Snipe(client, *args, **kwargs))