import discord
from discord.ext import commands
from aiohttp import ClientSession
from io import BytesIO

class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.latex_api = 'https://chart.googleapis.com/chart?cht=tx&chl='

    
    @commands.command()
    async def latex(self, ctx, *, code: str):

        api = 'https://chart.googleapis.com/chart'
        params = {
            'cht': 'tx',
            'chl': code
        }

        async with ClientSession() as cs:
            async with cs.get(api, params=params) as r:
                await ctx.tick(r.status == 200)
                data = await r.read()
                
        img = discord.File(BytesIO(data), filename=f'{code}.jpg')
        
        await ctx.send(file=img)
    
    @commands.command()
    async def weather(self, ctx, city: str, state: str = None):
        
        query = city
        if state is not None:
            query += f', {state}'

        api = 'https://api.openweathermap.org/data/2.5/weather'
        params = {
            'APPID': self.bot.cfg.weather_api_key,
            'q': query,
            'units': 'imperial'
        }

        async with ClientSession() as cs:
            async with cs.get(api, params=params) as r:
                data = await r.json()
                if r.status != 200:
                    await ctx.send(data['message'])
                await ctx.tick(r.status == 200)
        
        current_temp = data['main']['temp']
        low_temp = data['main']['temp_min']
        high_temp = data['main']['temp_max']
        clouds = data['weather'][0]['description']
        await ctx.send(f'In {query} it is {current_temp}° with a high of {high_temp}° and a low of {low_temp}° with {clouds}.')


def setup(bot):
    bot.add_cog(Utils(bot))