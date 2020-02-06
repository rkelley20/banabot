import discord
from discord.ext import commands
import asyncio
from functools import partial

class Games(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def count(self, ctx, num: int = 10):
        await ctx.tick()
        await ctx.send(f'Count to {num} without messing up...')

        def check(msg):
            return msg.channel == ctx.channel and not msg.author.bot
        
        for i in range(1, num + 1):
            try:
                msg = await self.bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send(f'Failed to count {num} in time 👎!')
                break
            else:
                if msg.content.strip() == str(i):
                    await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                else:
                    await msg.add_reaction('\N{CROSS MARK}')
                    await ctx.send(f'Failed to count to {num} 👎!')
                    break
        else:
            await ctx.send('Congrats you guys did it 👍!')

    

def setup(bot):
    bot.add_cog(Games(bot))