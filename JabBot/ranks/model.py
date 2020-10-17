import discord
import os

from settings import (USER_RANKS_PATH, RANKS_CONFIG_DIR, USER_LOGS_DIR,
    load_resource, write_resource)
from utils.utils import embedded, mention


EMPTY = discord.Embed.Empty
EMPTY_FV = '\u200b'
RANKS_PRIORITY = {
    'god': { 'priority': 0 },
    'Admin': { 'priority': 1 },
    'High Ranker': { 'priority': 2 },
    'Ranker': { 'priority': 3 },
    'Regular': { 'priority': 4 },
    'Noob': { 'priority': 5 }
}
ROLES = {
    'High Ranker': {
        'color': 0xe91e63, 'hoist': False, 'mentionable': False,
        'permissions': [
            'create_instant_invite', 'change_nickname', 'read_messages',
            'send_messages', 'embed_links', 'attach_files',
            'read_message_history', 'add_reactions', 'connect', 'speak',
            'voice_activation', 'kick_members', 'manage_nicknames',
            'manage_emojis', 'send_tts_messages', 'manage_messages',
            'mention_everyone', 'external_emojis', 'mute_members',
            'deafen_members', 'move_members', 'manage_channels', 'ban_members',
            'manage_webhooks'
        ]
    },
    'Ranker': {
        'color': 0x1abc9c, 'hoist': False, 'mentionable': True,
        'permissions': [
            'create_instant_invite', 'change_nickname', 'read_messages',
            'send_messages', 'embed_links', 'attach_files',
            'read_message_history', 'add_reactions', 'connect', 'speak',
            'voice_activation', 'kick_members', 'manage_nicknames',
            'manage_emojis', 'send_tts_messages', 'manage_messages',
            'mention_everyone', 'external_emojis', 'mute_members',
            'deafen_members', 'move_members'
        ]
    },
    'Regular': {
        'color': 0x1f8b4c, 'hoist': False, 'mentionable': True,
        'permissions': [
            'create_instant_invite', 'change_nickname', 'read_messages',
            'send_messages', 'embed_links', 'attach_files',
            'read_message_history', 'add_reactions', 'connect', 'speak',
            'voice_activation'
        ]
    },
    'Noob': {
        'color': 0xa9e2e2, 'hoist': False, 'mentionable': True,
        'permissions': [
            'change_nickname', 'read_messages', 'send_messages', 'attach_files',
            'read_message_history', 'add_reactions', 'connect', 'speak',
            'voice_activation'
        ]
    }
}

class Ranks:
    announcement_channels = None

    def __init__(self, client):
        self.client = client

    async def update_data(self, USERS, user):
        uid = str(user.id)
        if not uid in USERS:
            USERS[uid] = {}
            USERS[uid]['experience'] = 0
            USERS[uid]['lifetime_experience'] = 0
            USERS[uid]['level'] = 0
            USERS[uid]['rank'] = []
            USERS[uid]['last_sent_message_ts'] = 0
            USERS[uid]['stack_ranks'] = False
            self.get_user_logs(user)  # creates them if not there

    def get_highest_rank(self, user):
        ranks = self.get_user_ranks_json(user)
        highest, role_name = 5, 'Noob'
        for r in ranks:
            if r[1] in RANKS_PRIORITY:
                priority = RANKS_PRIORITY[r[1]]['priority']
                if priority <= highest:
                    role_name, highest = r[1], priority
        return (role_name, highest)

    async def add_xp(self, USERS, ULOGS, user, xp, ts):
        uid = str(user.id)
        if uid in USERS:
            USERS[uid]['experience'] += xp
            USERS[uid]['lifetime_experience'] += xp
            xp_msg = f'{user.name} gained {xp} xp'
            ULOGS['xp'].append((xp_msg, str(ts)))
            self.save_user_logs(user, ULOGS)
        else:
            print(f'{uid} not in {USERS.keys()}')

    async def lvl_up(self, USERS, ULOGS, user, ch, ts):
        uid = str(user.id)
        xp = USERS[uid]['experience']
        lvl_start = USERS[uid]['level']
        # lvl_end = int(xp ** float(1.0/4))
        xp_to_next_level = 5 * (lvl_start ** 2) + 50 * lvl_start + 100
        USERS[uid]['experience_to_next_level'] = xp_to_next_level
        # if lvl_start < lvl_end:
        if xp >= xp_to_next_level:
            lvl_end = lvl_start + 1
            USERS[uid]['level'] = lvl_end
            USERS[uid]['experience'] = 0
            lvl_msg = f'has leveled up to {lvl_end}'
            lvl_msg_dm = f'you have leveled up to {lvl_end}'
            ULOGS['xp'].append((f'{user.name} {lvl_msg}', str(ts)))
            self.save_user_logs(user, ULOGS)
            announce_embed = embedded(title=EMPTY, desc=f'Level up card',
                                      footer_text=lvl_msg,
                                      footer_icon=user.avatar_url)
            await self.make_announcement(user, announce_embed)
            await self.assign_rank_role(USERS, user, lvl_end)

    async def make_announcement(self, user, announce_embed):
        chs = self.get_announcement_channels(user.guild)
        if len(chs) > 0:
            for ch in chs:
                announce_ch = discord.utils.get(user.guild.text_channels, name=ch[1])
                await announce_ch.send(embed=announce_embed)
            return
        dm_ch = await user.create_dm()
        await dm_ch.send(embed=announce_embed)

    def is_announcement_channels_set(self, guild):
        config = self.get_announcement_channels(guild)
        if guild.name in config['guilds']:
            if len(config['guilds'][guild.name]['announcement_channels']) > 0:
                return True
        return False

    def get_guild_config(self, guild):
        config = load_resource(RANKS_CONFIG_DIR)
        if guild.name in config['guilds']:
            return config['guilds'][guild.name]
        else:
            err = f'Guild {guild.name} does not have its settings configured'
            raise ValueError(err)

    def save_user_logs(self, user, logs):
        user_logs_path = f'{USER_LOGS_DIR}{str(user.id)}.json'
        write_resource(user_logs_path, logs)

    def get_user_logs(self, user):
        user_logs_path = f'{USER_LOGS_DIR}{str(user.id)}.json'
        if os.path.isfile(user_logs_path):
            logs = load_resource(user_logs_path)
        else:
            logs = {
                'xp': [],
                'rank_change': [],
                'command_activity': [],
                'activity': [],
                'message_counter': 0,
                'mention_counter': 0,
                'game_wins': 0,
                'game_loss': 0,
                'game_draws': 0,
                'pokemon_battle_wins': 0,
                'pokemon_battle_loss': 0,
                'pokemon_battle_draws': 0
            }
            write_resource(user_logs_path, logs)
            logs = load_resource(user_logs_path)
        return logs

    def get_user_ranks_json(self, user):
        USERS = load_resource(USER_RANKS_PATH)
        return USERS[str(user.id)]

    def save_user_ranks_json(self, user, user_json):
        USERS = load_resource(USER_RANKS_PATH)
        USERS[str(user.id)] = user_json
        write_resource(USER_RANKS_PATH, USERS)

    def get_announcement_channels(self, guild):
        config = load_resource(RANKS_CONFIG_DIR)
        if guild.name:
            return config['guilds'][guild.name]['announcement_channels']
        else:
            err = f'Guild {guild.name} does not have its settings configured'
            raise ValueError(err)

    async def create_guild_ranks(self, guild):
        roles, role_names = [], ['Noob', 'Regular', 'Ranker', 'High Ranker']
        for n in role_names:
            if n == 'High Ranker': perms = discord.Permissions.all()
            elif n == 'Ranker': perms = discord.Permissions.voice()
            elif n == 'Regular': perms = discord.Permissions.text()
            elif n == 'Noob': perms = discord.Permissions.none()
            else:
                raise ValueError('Unsupported rank name')
            perms.update(**dict.fromkeys(ROLES[n]['permissions'], True))
            await guild.create_role(
                name=n, colour=discord.Colour(ROLES[n]['color']),
                hoist=ROLES[n]['hoist'], mentionable=ROLES[n]['mentionable'],
                permissions=perms)
            role = discord.utils.get(guild.roles, name=n)
            print(f'Created role ({role.name}, {role.id}) in {guild.name}')
            # guild.channel.send(embed=embedded(desc=f'Created role ({role.name}, {role.id}) in {guild.name}'))
            roles.append((role.id, role.name))
        return roles

    async def assign_rank_role(self, USERS, user, lvl):
        uid = str(user.id)
        if lvl >= 9000: new_rank = 'Administrator'
        if 9000 > lvl and lvl >= 1000: new_rank = 'High Ranker'
        elif 1000 > lvl and lvl >= 100: new_rank = 'Ranker'
        elif 100 > lvl and lvl >= 10: new_rank = 'Regular'
        elif 10 > lvl and lvl >= 0: new_rank = 'Noob'
        if new_rank:
            role = self.get_rank_role(name=new_rank)
            if not (role.name in USERS[uid]['rank']):
                USERS[uid]['rank'].append(role.name)
                await user.add_roles(role)

            if not USERS[uid]['stack_ranks']:
                gconfig = self.get_guild_config(user.guild)
                for rr in gconfig['ranks_roles']:
                    if rr[1] != role.name:
                        old_roles = self.get_rank_role(name=rr[1])
                        await user.remove_roles(old_roles)
            else:
                for rank in USERS[uid]['rank']:
                    rank_role = self.get_rank_role(name=rank)
                    await user.add_roles(rank_role)
            write_resource(USER_RANKS_PATH, USERS)
        else:
            old_rank = self.get_highest_rank(USERS[uid]['rank'])
            print(f'failed to assign new rank. Retaining {old_rank} rank')

    def get_rank_role(self, id=None, name=None):
        role = None
        try:
            for guild in self.client.guilds:
                for r in guild.roles:
                    if id:
                        if id == r.id:
                            role = discord.utils.get(guild.roles, id=int(id))
                    elif name:
                        config = self.get_guild_config(guild)
                        for rr in config['ranks_roles']:
                            if name in rr[1]:
                                role = discord.utils.get(guild.roles, id=rr[0])
                                break
                    if role: return role
            if role is None:
                raise ValueError(f'Could not find role: id: {id}, name: {name}')
        except:
            raise ValueError(f'Could not find role: id: {id}, name: {name}')

    async def remove_rank_roles(self, config, guild):
        for rr in config['guilds'][guild.name]['ranks_roles']:
            role = discord.utils.get(guild.roles, name=rr[1])
            print(f'Deleting role {role}')
            await role.delete()
        config['guilds'][guild.name]['ranks_roles'] = []
