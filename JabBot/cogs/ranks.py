import os
import json
import discord
from discord.ext import commands

from settings import PREFIX, USER_RANKS_PATH, load_resource, write_resource
from utils.roles import admin_or_owner, regular, ranker, high_ranker
from ranks.model import Ranks as RK


class Ranks(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self.rk = RK()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        USERS = load_resource(USER_RANKS_PATH)
        await self.rk.update_data(USERS, member)
        write_resource(USER_RANKS_PATH, USERS)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self._bot.user: return
        if message.author.bot: return

        xp_gain, USERS = 5, load_resource(USER_RANKS_PATH)
        await self.rk.update_data(USERS, message.author)
        await self.rk.add_xp(USERS, message.author, xp_gain)
        await self.rk.lvl_up(USERS, message.author, message.channel)
        write_resource(USER_RANKS_PATH, USERS)

    @commands.command()
    async def xp(self, ctx):
        '''
        Show user's xp.
        Description:
            Displays the user's current experience points amount.
        Usage:
            [PREFIX]xp
        '''
        USERS = load_resource(USER_RANKS_PATH)
        xp = USERS[str(ctx.message.author.id)]['experience']
        async with ctx.channel.typing():
            await ctx.channel.send(f'{ctx.message.author.mention} you have {xp} XP')

    @commands.command()
    async def lvl(self, ctx):
        '''
        Show user's level.
        Description:
            Displays the user's current level.
        Usage:
            [PREFIX]lvl
        '''
        USERS = load_resource(USER_RANKS_PATH)
        lvl = USERS[str(ctx.message.author.id)]['level']
        async with ctx.channel.typing():
            await ctx.channel.send(f'{ctx.message.author.mention} is level {lvl}!')


def setup(bot):
    bot.add_cog(Ranks(bot))
