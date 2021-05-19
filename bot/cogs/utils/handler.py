import discord
from discord.ext import commands
import sys
import traceback

class CommandErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        else:
            error_channel = self.client.get_channel(833508151802069002)
            error_traceback = traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            await error_channel.send('''Error Occured at {ctx.guild.name} by {ctx.author.name}#{ctx.author.discriminator}: 
            ```
            Ignoring exception in command {}:')
            ```'''.format(ctx.command), file=sys.stderr)                
            await error_traceback.send(f'''Traceback:
            ```
            {error_traceback}
            ```''')

def setup(client):
    client.add_cog(CommandErrorHandler(client))
        
