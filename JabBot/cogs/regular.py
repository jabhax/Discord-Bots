import discord
from discord.ext import commands

from settings import PREFIX
from utils.roles import regular
from utils.utils import embedded, create_field


class Regular(commands.Cog):

    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    async def hey(self, ctx):
        '''
        Description:
            Regulars can say Hey in addition to Hello.
        Usage:
            [PREFIX]hey
        '''
        async with ctx.channel.typing():
            await ctx.send('Hey')


def setup(bot):
    bot.add_cog(Regular(bot))
