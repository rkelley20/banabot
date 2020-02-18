import discord
from discord.ext import commands
from colorama import Fore, Style
import config
from os import listdir, getcwd
from os.path import isfile, join
import traceback


class BanaContext(commands.Context):
    async def tick(self, value = True):
        # reacts to the message with an emoji
        # depending on whether value is True or False
        # if its True, it'll add a green check mark
        # otherwise, it'll add a red cross mark
        emoji = '\N{WHITE HEAVY CHECK MARK}' if value else '\N{CROSS MARK}'
        try:
            await self.message.add_reaction(emoji)
        except discord.HTTPException:
            pass

    
    async def check(self):
        self.tick()
    
    async def cross(self):
        self.tick(False)


class BanaBot(commands.Bot):
    async def get_context(self, message, *, cls=BanaContext):
        return await super().get_context(message, cls=cls)
    
    async def on_command_error(self, ctx, error):
        await ctx.cross()
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}', file=sys.stderr)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)

bot = BanaBot(command_prefix='$', description='BanaBot: A bot build on SQLite.')
bot.cfg = config

@bot.event
async def on_ready():
    print(f'\n{Fore.RED}------------------------------{Style.RESET_ALL}')
    print(f'{Fore.GREEN}Logged in as:{Style.RESET_ALL}')
    print(f'{Fore.CYAN}{bot.user.name} {Fore.YELLOW}-{Fore.CYAN} {bot.user.id}{Style.RESET_ALL}')
    print(f'{Fore.RED}------------------------------{Style.RESET_ALL}\n')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':

    # Grab every .py file in the directory excluding some...
    exclude = {'config.py', 'bot.py'}
    cogs_folder = 'cogs'

    def valid_cog(fname: str):
        return isfile(fname not in exclude and join(cogs_folder, fname)) and fname.endswith('.py')

    cogs = ['cogs.' + fname.rstrip('.py') for fname in listdir(cogs_folder) if valid_cog(fname)]

    cogstr = '\n'.join(cogs)
    print(f'\n{Fore.GREEN}Loading the following cogs:{Style.RESET_ALL}\n{Fore.YELLOW}{cogstr}{Style.RESET_ALL}')

    for cog in cogs:
        bot.load_extension(cog)

    try:
        bot.run(config.token, bot=True)
    except KeyboardInterrupt:
        bot.logout()