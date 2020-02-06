import discord
from discord.ext import commands
from colorama import Fore, Style
import config
from os import listdir, getcwd
from os.path import isfile, join


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


class BanaBot(commands.Bot):
    async def get_context(self, message, *, cls=BanaContext):
        return await super().get_context(message, cls=cls)

bot = BanaBot(command_prefix='$', description='BanaBot: A bot build on SQLite.')
bot.cfg = config

@bot.event
async def on_ready():
    print(f'\n{Fore.RED}--------------------{Style.RESET_ALL}')
    print(f'{Fore.GREEN}Logged in as:{Style.RESET_ALL}')
    print(f'{Fore.CYAN}{bot.user.name} {Fore.YELLOW}-{Fore.CYAN} {bot.user.id}{Style.RESET_ALL}')
    print(f'{Fore.RED}--------------------{Style.RESET_ALL}\n')

# Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':

    # Grab every .py file in the directory excluding some...
    exclude = {'config.py', 'bot.py'}
    cogs_folder = 'cogs'

    def valid_cog(fname: str):
        return isfile(join(cogs_folder, fname)) and fname not in exclude and fname.endswith('.py')

    cogs = ['cogs.' + fname.rstrip('.py') for fname in listdir(cogs_folder) if valid_cog(fname)]

    print(f'Loading the following cogs:\n {cogs}')

    for cog in cogs:
        bot.load_extension(cog)

    try:
        bot.run(config.token, bot=True)
    except KeyboardInterrupt:
        bot.logout()