import discord
from discord.ext import commands
from aiohttp import ClientSession
from io import BytesIO
import asyncio

class Utils(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.latex_api = 'https://chart.googleapis.com/chart?cht=tx&chl='
        self.weather_api = 'https://api.openweathermap.org/data/2.5/weather'

    
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

        params = {
            'APPID': self.bot.cfg.weather_api_key,
            'q': query,
            'units': 'imperial'
        }

        async with ClientSession() as cs:
            async with cs.get(self.weather_api, params=params) as r:
                data = await r.json()
                if r.status != 200:
                    await ctx.send(data['message'])
                await ctx.tick(r.status == 200)
        
        current_temp = data['main']['temp']
        low_temp = data['main']['temp_min']
        high_temp = data['main']['temp_max']
        clouds = data['weather'][0]['description']
        await ctx.send(f'In {query} it is {current_temp}° with a high of {high_temp}° and a low of {low_temp}° with {clouds}.')
    
    @commands.command()
    async def morse(self, ctx, *, phrase: str):

        await ctx.tick()
        morse_map = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'}
        
        encoded = ''.join(morse_map.get(c.upper(), c) for c in phrase)
        await ctx.send(encoded)
    
    @commands.command(name='eval')
    async def code_eval(self, ctx, *, code: str):
        lines = code.split('\n')

        # Only allow for python code
        if not lines[0].lower().endswith('python'):
            await ctx.cross()
            await ctx.send(f'Only able to execute python code at this point in time, sorry!')
        else:
            # Remove the ```python and closing ``` lines.
            code = '\n'.join(lines[1:-1])
            
            proc = await asyncio.create_subprocess_shell(
                f'python3 -c "{code}"',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
        
            stdout, stderr = await proc.communicate()

            await ctx.send(f'Your job exited with return code {proc.returncode}.')
            if stderr:
                await ctx.cross()
                await ctx.send(f'```\n{stderr.decode()}\n```')
            elif stdout:
                await ctx.check()
                await ctx.send(f'```\n{stdout.decode()}\n```')



def setup(bot):
    bot.add_cog(Utils(bot))