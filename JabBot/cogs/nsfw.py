import discord
from discord.ext import commands
import time

from settings import PREFIX
from utils.utils import mention, get_random_joke


class NSFW(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    async def yomama(self, ctx, member=None, amount=1):
        '''
        Yomama Jokes
        Description:
            Have JabBot say "Yo Mama" jokes
            Sometimes the bot will not have a joke to tell.
            In that case, try again.
        Usage:
            [PREFIX]yomama
            [PREFIX]yomama 5
        '''
        if member:
            try:
                if type(eval(member)) is type(1):
                    amount, member = int(eval(member)), None
            except:
                print(f'type: {type(member)}, member: {member}')
        async with ctx.channel.typing():
            for i in range(amount):
                if member:
                    reply = (f'{member} {get_random_joke()}' if amount == 1 else
                             f'{i+1}. {member} {get_random_joke()}')
                else:
                    reply = f'{i+1}. {get_random_joke()}'
                await ctx.send(reply)
                time.sleep(1)


def setup(bot):
    bot.add_cog(NSFW(bot))
