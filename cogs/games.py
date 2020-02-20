import discord
from discord.ext import commands
import asyncio
from functools import partial
import random

class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def count(self, ctx, num: int = 10):

        def check(msg):
            return msg.channel == ctx.channel and not msg.author.bot
        
        await ctx.tick(num > 0)

        if num > 0:
            await ctx.send(f'Count to {num} without messing up...')

            for i in range(1, num + 1):
                try:
                    msg = await self.bot.wait_for('message', timeout=10.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send(f'Failed to count {num} in time 👎')
                    break
                else:
                    if msg.content.strip() == str(i):
                        await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                    else:
                        await msg.add_reaction('\N{CROSS MARK}')
                        await ctx.send(f'Failed to count to {num} 👎')
                        break
            else:
                await ctx.send('Congrats you guys did it 👍')
        else:
            await ctx.send('The number must be greater than 0')
    
    @commands.command(name='guessnum')
    async def guess_number(self, ctx, num: int = 100):
        n = str(random.randint(1, num))

        await ctx.send(f'I am thinking of a number between 1 and {num}, can you guess it?')

        def check(msg):
            return msg.channel == ctx.channel and not msg.author.bot
        
        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f'Failed to guess the number in time, it was {n}!')
                break
            else:
                if msg.content.strip() == n:
                    await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                    await ctx.send(f'Congrats {msg.author.mention}, you guessed the numer, it was {n}!')
                    break


    

def setup(bot):
    bot.add_cog(Games(bot))