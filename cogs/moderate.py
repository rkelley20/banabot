import discord
from discord.ext import commands

class Moderate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def kick(self, ctx, member: discord.Member, reason: str = None):
        await ctx.check()
        await member.kick(reason=reason)
        


def setup(bot):
    bot.add_cog(Moderate(bot))