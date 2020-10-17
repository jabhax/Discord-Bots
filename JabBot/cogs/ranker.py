import discord
import random
import asyncio
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

    @commands.command()
    @commands.guild_only()
    @ranker()
    async def purgeuser(self, ctx, user: discord.Member, amount: int=1):
        '''
        Purge a mentioned user's messages on chat channel
        Description:
            Deletes the latest message. If a number is provided
            then it will delete the last n messages.
        Usage:
            Params:
                user: The user being mentioned
                amount: Number of messages to be purged from mentioned user

            [PREFIX]purgeuser user amount
            [PREFIX]purgeuser @someone
            [PREFIX]purgeuser @someone 5
            [PREFIX]purgeuser @someone 5
        '''
        user_msgs, counter = [], 0
        history_limit = amount if amount > 200 else 200
        if user == self._bot.user: amount += 1
        async with ctx.channel.typing():
            await ctx.channel.purge(
                limit=amount,
                check=lambda msg: (not msg.pinned and msg.author.id == user.id))
            await ctx.send(f'{mention(user)}\'s previous {amount} messages have been purged!')
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1, check=lambda msg: not msg.pinned)
        if random.randint(1, 8) == 5:
            async with ctx.channel.typing():
                await ctx.send(f'It seems a Ranker is here.')

def setup(bot):
    bot.add_cog(Ranker(bot))
