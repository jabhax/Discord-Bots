import os
import json
import random
import discord
from discord.ext import commands

from settings import (PREFIX, USER_RANKS_PATH, RANKS_CONFIG_DIR,
    load_resource, write_resource)
from utils.roles import admin_or_owner, regular, ranker, high_ranker
from ranks.model import Ranks as RK
from utils.utils import embedded, create_field


EMPTY = discord.Embed.Empty
EMPTY_FV = '\u200b'

class Ranks(commands.Cog):

    def __init__(self, bot):
        self._bot = bot
        self.rk = RK(client=self._bot)

    @commands.Cog.listener()
    async def on_ready(self):
        config = load_resource(RANKS_CONFIG_DIR)
        if 'guilds' not in config:
            config['guilds'] = {}
        for guild in self._bot.guilds:
            if guild.name not in config['guilds']:
                config['guilds'][guild.name] = {
                    'announcement_channels': [], 'ranks_roles': [],
                    'activated': False
                }
            else:
                print(f'{guild.name} is already in the ranks config json')
        write_resource(RANKS_CONFIG_DIR, config)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        USERS = load_resource(USER_RANKS_PATH)
        await self.rk.update_data(USERS, member)
        write_resource(USER_RANKS_PATH, USERS)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self._bot.user: return
        if message.author.bot: return

        # If the guild has ranks activated then load and update_data
        config = load_resource(RANKS_CONFIG_DIR)
        if config['guilds'][message.guild.name]['activated']:
            USERS = load_resource(USER_RANKS_PATH)
            xp_gain, ts = 100, message.created_at
            await self.rk.update_data(USERS, message.author)
            ULOGS = self.rk.get_user_logs(message.author)
            await self.rk.add_xp(USERS, ULOGS, message.author, xp_gain, ts)
            await self.rk.lvl_up(USERS, ULOGS, message.author, message.channel, ts)
            write_resource(USER_RANKS_PATH, USERS)
        else:
            print('Ranks is deactivated for this server. Please type .activateranks to create the rank roles and to activate xp gain')

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

    @commands.command()
    async def profile(self, ctx):
        '''
        Show user's logs
        Description:
            Displays the user's current log file details
        Usage:
            [PREFIX]logs
        '''
        user, fields = ctx.message.author, []
        ULOGS, id = self.rk.get_user_logs(user), str(user.id)
        title = f'{user.name}\'s Profile Card'
        desc = 'shows your Ranks profile & stats'
        USERS = load_resource(USER_RANKS_PATH)
        rank, lvl = USERS[id]['rank'], USERS[id]['level']
        hi_rank = self.get_highest_rank(user)
        xp, lxp = USERS[id]['experience'], USERS[id]['lifetime_experience']
        xp2lvl = USERS[id]['experience_to_next_level']
        lms = USERS[id]['last_sent_message_ts']

        msg_ctr, mtn_ctr = ULOGS['message_counter'], ULOGS['mention_counter']
        game_wins, game_loss = ULOGS['game_wins'], ULOGS['game_loss']
        game_draws, pkmn_wins = ULOGS['game_wins'], ULOGS['pokemon_battle_wins']
        pkmn_loss, pkmn_draws = ULOGS['pokemon_battle_loss'], ULOGS['pokemon_battle_draws']
        fields.append(create_field('Rank', hi_rank, True))
        fields.append(create_field('Level', lvl, True))
        fields.append(create_field(EMPTY_FV, EMPTY_FV))
        fields.append(create_field('XP', xp, True))
        fields.append(create_field('Lifetime XP', lxp, True))
        fields.append(create_field('XP to level', xp2lvl, True))
        fields.append(create_field(f'Last Message Sent on', lms, True))
        fields.append(create_field(f'Messages Sent: {msg_ctr}', EMPTY_FV, True))
        fields.append(create_field(f'Mentions Sent: {mtn_ctr}', EMPTY_FV, True))
        fields.append(create_field(f'Wins: {game_wins}', EMPTY_FV, True))
        fields.append(create_field(f'Losses: {game_loss}', EMPTY_FV, True))
        fields.append(create_field(f'Draws: {game_draws}', EMPTY_FV, True))
        fields.append(create_field(f'Pokemon Battle Wins: {pkmn_wins}', EMPTY_FV, True))
        fields.append(create_field(f'Pokemon Battle Losses: {pkmn_loss}', EMPTY_FV, True))
        fields.append(create_field(f'Pokemon Battle Draws: {pkmn_draws}', EMPTY_FV, True))

        logs_embed = embedded(title=title, desc=desc, fields=fields,
                              thumbnail=ctx.message.author.avatar_url,
                              footer_text=f'shows your log/logs details',
                              footer_icon=self._bot.user.avatar_url)
        async with ctx.channel.typing():
            await ctx.channel.send(embed=logs_embed)

    @commands.command()
    async def logs(self, ctx, log_category=None, limit=5):
        '''
        Show user's logs
        Description:
            Displays the user's current log file details
        Usage:
            [PREFIX]logs
        '''
        user = ctx.message.author
        ULOGS = self.rk.get_user_logs(user)
        title, fields = f'{user.name}\'s Logs Card', []
        if log_category:
            category_logs = ULOGS[log_category]
            n = len(category_logs)
            if n <= limit: limit = n
            i = 1
            for log in category_logs[n-limit:n]:
                print(f'{limit-i}  log: {log}')
                msg, ts = log[0], log[1]
                css_mark = "```"
                fields.append(create_field(f'{limit-i}', EMPTY_FV, True))
                fields.append(create_field(f'{css_mark}{msg}{css_mark}', EMPTY_FV, True))
                fields.append(create_field(f'{css_mark}{ts}{css_mark}', EMPTY_FV, True))
                i += 1
            desc = f'{user.name}\'s {log_category} logs'
        else:
            xp_ctr, rc_ctr = len(ULOGS['xp']), len(ULOGS['rank_change'])
            ca_ctr, a_ctr = len(ULOGS['command_activity']), len(ULOGS['activity'])
            msg_ctr, mtn_ctr = ULOGS['message_counter'], ULOGS['mention_counter']
            fields.append(create_field(f'Messages Sent: {msg_ctr}', EMPTY_FV, True))
            fields.append(create_field(f'Mentions Sent: {mtn_ctr}', EMPTY_FV, True))
            fields.append(create_field(f'[PREFIX]logs xp', f'{xp_ctr} logs', True))
            fields.append(create_field(f'[PREFIX]logs rank_change', f'{rc_ctr} logs', True))
            fields.append(create_field(f'[PREFIX]logs command_activity', f'{ca_ctr} logs', True))
            fields.append(create_field(f'[PREFIX]logs activity', f'{a_ctr} logs', True))
            desc = f'{user.name}\'s logs overview'

        logs_embed = embedded(title=title, desc=desc, fields=fields,
                              thumbnail=ctx.message.author.avatar_url,
                              footer_text=f'shows your log/logs details',
                              footer_icon=self._bot.user.avatar_url)
        async with ctx.channel.typing():
            await ctx.channel.send(embed=logs_embed)

    @commands.command()
    async def setrankschannels(self, ctx, *args):
        input_chs, anc_chs = [a for a in args], []
        for input_ch in input_chs:
            for text_ch in ctx.guild.text_channels:
                if input_ch == text_ch.id:
                    anc_chs.append((text_ch.id, text_ch.name))
                    break
                elif input_ch == text_ch.name:
                    anc_chs.append((text_ch.id, text_ch.name))
                    break
            else:
                print(f'no channel found called {input_ch}')
        config = load_resource(RANKS_CONFIG_DIR)
        config['guilds'][ctx.guild.name]['announcement_channels'] = anc_chs
        write_resource(RANKS_CONFIG_DIR, config)
        announcements = config['guilds'][ctx.guild.name]['announcement_channels']
        anc_msg = '\n'.join([f'({a[1]}, {a[0]})' for a in announcements])
        async with ctx.channel.typing():
            msg = f'Ranks Announcement Channels set to:\n{anc_msg}'
            await ctx.channel.send(msg)

    @commands.command()
    async def unsetrankschannels(self, ctx):
        config = load_resource(RANKS_CONFIG_DIR)
        config['guilds'][ctx.guild.name]['announcement_channels'] = []
        write_resource(USER_RANKS_PATH, config)
        async with ctx.channel.typing():
            msg = f'Ranks Announcement Channels have been unset'
            await ctx.channel.send(msg)

    @commands.command()
    async def announcements(self, ctx):
        config = load_resource(RANKS_CONFIG_DIR)
        announcements = config['guilds'][ctx.guild.name]['announcement_channels']
        anc_msg = '\n'.join([f'({a[1]}, {a[0]})' for a in announcements])
        async with ctx.channel.typing():
            msg = f'Ranks Announcement Channels are:\n{anc_msg}'
            await ctx.channel.send(msg)

    @commands.command()
    async def roles(self, ctx):
        all_roles = {}
        msg = ''
        for guild in self._bot.guilds:
            all_roles[guild.name] = []
            for role in guild.roles:
                all_roles[guild.name].append(role)
                if len(msg) <= 1900:
                    msg += f'{guild.name}  --  role: {role.name}, {role.id}, {role.colour}\n'
                else:
                    async with ctx.channel.typing():
                        await ctx.channel.send(msg)
                    msg = ''

    @commands.command()
    async def activateranks(self, ctx):
        config, guild = load_resource(RANKS_CONFIG_DIR), ctx.message.guild
        if guild.name in config['guilds']:
            if len(config['guilds'][guild.name]['ranks_roles']) == 0:
                config['guilds'][guild.name]['ranks_roles'] = await self.rk.create_guild_ranks(guild)
                config['guilds'][guild.name]['activated'] = True
                write_resource(RANKS_CONFIG_DIR, config)
            else:
                print(f'{guild.name} already has Ranks Activated!')
        else:
            print(f'{guild.name} not configured!')

    @commands.command()
    async def deactivateranks(self, ctx):
        config, guild = load_resource(RANKS_CONFIG_DIR), ctx.message.guild
        await self.rk.remove_rank_roles(config, ctx.guild)
        config['guilds'][guild.name]['activated'] = False
        write_resource(RANKS_CONFIG_DIR, config)

    @commands.command()
    async def stackranks(self, ctx):
        USERS, guild = load_resource(USER_RANKS_PATH), ctx.message.guild
        uid = str(ctx.message.author.id)
        USERS[uid]['stack_ranks'] = not USERS[uid]['stack_ranks']
        write_resource(USER_RANKS_PATH, USERS)
        async with ctx.channel.typing():
            msg = f'{ctx.message.author.name}\'s ranks switched to '
            msg += 'stacked' if USERS[uid]['stack_ranks'] else 'unstacked'
            await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Ranks(bot))
