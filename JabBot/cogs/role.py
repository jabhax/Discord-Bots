import discord
from discord.ext import commands

from settings import PREFIX
from utils.roles import (get_roles, ADMIN_ROLE, HIGH_RANKER_ROLE, RANKER_ROLE,
    REGULAR_ROLE, GOD_ROLE)
from utils.utils import embedded, create_field



class Role(commands.Cog):

    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    async def myroles(self, ctx):
        '''
        Show current user's roles
        Description:
            Displays the current user's current roles.
        Usage:
            [PREFIX]myroles
        '''
        roles = ", ".join([role.name for role in ctx.author.roles if role.name != '@everyone'])
        async with ctx.channel.typing():
            await ctx.send(f'Current roles are:{roles}')

    @commands.command()
    async def allroles(self, ctx):
        '''
        Show available roles
        Description:
            List all available roles.
        Usage:
            [PREFIX]allroles
        '''
        roles, other_roles, fields = {}, [], []
        for role in get_roles(): roles[role['name']] = role
        other_roles, fields = [], []
        for role in ctx.guild.roles:
            if role.name in roles.keys():
                fields.append(create_field(role.name, roles[role.name]['desc'], True))
                fields.append(create_field('Privileges', ', '.join(roles[role.name]['privileges']), True))
                fields.append(create_field('Rarity', roles[role.name]['rarity'], True))
            else:
                if role.name != '@everyone':
                    other_roles.append(role.name)
        other_roles = ', '.join(other_roles)
        fields.append(create_field('Other Roles', other_roles))
        embed = embedded(
            title='Server Roles',
            desc='Below are the current server roles:',
            fields=fields)
        async with ctx.channel.typing():
            await ctx.send(embed=embed)

    @commands.command()
    async def roleinfo(self, ctx, *args):
        '''
        '''
        rolename = ' '.join(args)
        roles, fields = {}, []
        for role in get_roles(): roles[role['name'].lower()] = role
        for role in ctx.guild.roles:
            if role.name.lower() in roles.keys():
                roles[role.name.lower()]['color'] = role.colour
        if rolename.lower() in roles.keys():
            fields = []
            for i in range(len(roles[rolename]['privileges'])):
                priv = roles[rolename]['privileges'][i]
                fields.append(create_field(f'PR{i}', priv, True))
            embed = embedded(
                title=rolename.upper(),
                desc=roles[rolename]['desc'],
                fields=fields,
                color=roles[rolename]['color'])
            async with ctx.channel.typing():
                await ctx.send(embed=embed)
        else:
            if rolename == GOD_ROLE['name']:
                async with ctx.channel.typing():
                    msg = ('You are too weak to even view this info. Do not try'
                           'this again! This is a forbidden role; do not try '
                           'this again!')
                    await ctx.send(msg)
            else:
                async with ctx.channel.typing():
                    await ctx.send('Unknown Role')


def setup(bot):
    bot.add_cog(Role(bot))
