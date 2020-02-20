import discord
from discord.ext import commands

class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def color(self, ctx, hex_code: str):
        try:
            hex_code = str(int(hex_code.lstrip('#'), 16))
        except ValueError:
            await ctx.cross()
            await ctx.send(f'{ctx.author.mention}, {hex_code} is not a valid hex code.')
        else:
            await ctx.check()
        
        roles = [role for role in ctx.guild.roles if role.name == hex_code]
        
        if roles:   
            await ctx.author.add_roles(roles[0])
        else:
            role = await ctx.guild.create_role(name=hex_code, colour=discord.Color(int(hex_code)))
            await ctx.author.add_roles(role)
    
    @commands.group()
    async def role(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f'{ctx.author.mention}, you must specify a subcommand.')
    
    @role.command(name='add')
    async def role_add(self, ctx, member: discord.Member = None, role: discord.Role = None):
        author = ctx.author

        if member is None and role is None:
            await ctx.cross()
            await ctx.send('Usage: $role add <member|id> <role_name>')
        else:
            await ctx.check()
            await member.add_roles(role)
            await ctx.send(f'{member.mention} has been added to the role {role.name}!')


def setup(bot):
    bot.add_cog(Roles(bot))