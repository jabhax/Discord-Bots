import discord
import json
import os
import random
from discord.ext import commands


# Roles
ADMIN_ROLE = {
    'name': 'Admin',
    'desc': ('The Administrator role has unrestricted privileges and surpasses '
             'all Roles and/or Ranks.'),
    'privileges': ['All Role Privileges', 'All Admin Privileges'],
    'rarity': 'Unique'
}
GOD_ROLE = {
    'name': 'God',
    'desc': ('O\'Mighty Role, Bestower of all Roles from the tales of Old & New.'),
    'privileges': ['Everything...literally everything!'],
    'rarity': '???'
}
HIGH_RANKER_ROLE = {
    'name': 'High Ranker',
    'desc': ('The role of High Ranker greatly surpasses that of Ranker and is '
            'given to those who have exeeded the expectations of the God Role.'),
    'privileges': [
        'All Ranker Privileges', 'Manage Channels', 'Ban Members',
        'Manage Webhooks', 'Priority Speaker',
        ('The Mention @-everyone, @-here, and All Roles will NOT be able to '
         'ping this Role')
    ],
    'rarity': 'Very Rare'
}
RANKER_ROLE = {
    'name': 'Ranker',
    'desc': ('The role of Ranker are given to those who have earned a rank in '
            'the Heavens above.'),
    'privileges': [
        'All Regular privileges', 'Kick Members', 'Manage Nicknames',
        'Manage Emojis', 'Send TTS Messages', 'Manages Messages',
        'Mention @-everyone, @-here, and All Roles', 'Use External Emojis',
        'Mute Members', 'Deafen Members', 'Move Members'
    ],
    'rarity': 'Rare'
}
REGULAR_ROLE = {
    'name': 'Regular',
    'desc': ('The role of Regular is bestowed upon the most basic of fellows. '
             'Climb to reach higher ranks!'),
    'privileges': [
        'Create Invites', 'Change Nickname','Read Text & See Voice Channels',
        'Send Messages', 'Embed Links', 'Attach Files', 'Read Message History',
        'Add Reactions', 'Connect', 'Speak', 'Video', 'Use Voice Activity'
    ],
    'rarity': 'Common'
}


# Role Groups

def admin_or_owner():
    def predicate(ctx):
        return commands.check_any(
            commands.is_owner(),
            commands.has_role(ADMIN_ROLE))
    return commands.check(predicate)

def high_ranker():
    def predicate(ctx):
        return commands.check_any(
            commands.is_owner(),
            commands.has_role(HIGH_RANKER_ROLE),
            commands.has_role(ADMIN_ROLE))
    return commands.check(predicate)

def ranker():
    def predicate(ctx):
        return commands.check_any(
            commands.is_owner(),
            commands.has_role(RANKER_ROLE),
            commands.has_role(HIGH_RANKER_ROLE),
            commands.has_role(ADMIN_ROLE))
    return commands.check(predicate)

def regular():
    def predicate(ctx):
        return commands.check_any(
            commands.is_owner(),
            commands.has_role(REGULAR_ROLE),
            commands.has_role(RANKER_ROLE),
            commands.has_role(HIGH_RANKER_ROLE),
            commands.has_role(ADMIN_ROLE))
    return commands.check(predicate)

def get_roles():
    return [ADMIN_ROLE, HIGH_RANKER_ROLE, RANKER_ROLE, REGULAR_ROLE]
