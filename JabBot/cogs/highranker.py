import discord
from discord.ext import commands

from settings import PREFIX
from utils.roles import high_ranker
from utils.utils import mention, embedded, create_field, notify_user


class HighRanker(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    @high_ranker()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member=None, reason: str='No Reason'):
        '''
        Bans a member
        Description:
            Can be used by High Rankers, Admin, and Owners.
            WARNING! This is a destructive command; use with caution!
        Usage:
            [PREFIX]ban @member
            [PREFIX]ban @member "Reason for banning"
        '''
        error = 'Please specify user to ban via mention'
        if member:
            msg = f'{member} has been banned for {reason}'
            try:
                async with ctx.channel.typing():
                    await notify_user(member, msg)
                    await ctx.guild.ban(member, reason=reason)
                    await ctx.send(msg)
            except Exception as e:
                await ctx.send(e)
        else:
            async with ctx.channel.typing():
                await ctx.send(error)

    @commands.command()
    @high_ranker()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: str='', reason: str='No Reason'):
        '''
        Unbans a member
        Description:
            Can be used by High Rankers, Admin, and Owners.
            WARNING! This is a destructive command; use with caution!
        Usage:
            [PREFIX]unban @member
            [PREFIX]unban @member "Reason for unbanning"
        '''
        err1 = 'Please specify user to unban via mention'
        err2 = 'User was not found in banlist. Please checkbans!'
        if member == '':
            async with ctx.channel.typing():
                await ctx.send(err1)
                return
        bans = await ctx.guild.bans()
        for ban in bans:
            if ban.user.name in (member):
                msg = f'{member} has been unbanned for {reason}'
                async with ctx.channel.typing():
                    await ctx.guild.unban(ban.user, reason=reason)
                    # await notify_user(ban.user, msg)
                    await ctx.send(msg)
                    return
        else:
            await ctx.send(err2)

    @commands.command()
    @high_ranker()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def checkbans(self, ctx):
        '''
        Shows the list of banned users from the server
        Description:
            Will show all banned users on the server.
            Can also be viewed on the server settings ban-list.
        Usage:
            [PREFIX]checkbans
        '''
        bans, fields = await ctx.guild.bans(), []
        for ban in bans:
            fields.append(create_field('User', ban.user, True))
            fields.append(create_field('ID', ban.user.id, True))
            fields.append(create_field('Reason', ban.reason, True))
        embed = embedded(title='Bans', desc='List of banned members',
                         fields=fields, color=discord.Colour.dark_red())
        async with ctx.channel.typing():
            await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(HighRanker(bot))
