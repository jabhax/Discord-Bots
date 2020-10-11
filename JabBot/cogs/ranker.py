import discord
from discord.ext import commands

from settings import PREFIX
from utils.roles import ranker
from utils.utils import mention, embedded, create_field, notify_user


class Ranker(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    @ranker()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, reason: str='No Reason'):
        '''
        Kicks a members
        Description:
            Can be used by Rankers, High Rankers, Admin, and Owners.
            WARNING! This is a destructive command; use with caution!
        Usage:
            [PREFI]kick @member "Reason for kicking"
        '''
        error = 'Please specify user to kick via mention'
        if member:
            msg = f'{member} has been kicked for {reason}'
            async with ctx.channel.typing():
                try:
                    await notify_user(member, msg)
                    await ctx.guild.kick(member, reason=reason)
                    await ctx.send(msg)
                except Exception as e:
                    await ctx.send(e)
        else:
            async with ctx.channel.typing():
                await ctx.send(error)


def setup(bot):
    bot.add_cog(Ranker(bot))
