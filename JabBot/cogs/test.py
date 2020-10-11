import discord
from discord.ext import commands

from settings import PREFIX


class Test(commands.Cog):

    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    async def hello(self, ctx):
        '''
        Say hello mofo!
        Description:
            Show bot greeting',
        Usage:
            [PREFIX]hello'
        '''
        async with ctx.channel.typing():
            await ctx.send('Hello!')

    @commands.command()
    async def ping(self, ctx):
        '''
        Ping JabBot
        Description:
            Pings JabBot to say Pong
        Usage:
            [PREFIX]ping'
        '''
        async with ctx.channel.typing():
            await ctx.send(f'Pong! {round(self._bot.latency * 1000, 2)}')

    @commands.command()
    async def marco(self, ctx):
        '''
        Marco-Pollo
        Description:
            Pings JabBot to say Pollo
        Usage:
            [PREFIX]marco
        '''
        async with ctx.channel.typing():
            await ctx.send('Pollo!')


def setup(bot):
    bot.add_cog(Test(bot))
