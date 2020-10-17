import datetime
import discord
from discord.ext import commands

from settings import PREFIX, JABHAX_ICON, PIXEL_PLAYGROUND_LOGO
from utils.utils import embedded, create_field
from utils.roles import admin_or_owner, ranker


class Admin(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog: str):
        '''
        Unloads cogs
        Ask your Admin for more information.
        Usage:
            [PREFIX]unload cogs.gamble
            [PREFIX]unload cogs.basic
        '''
        try:
            self._bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'Could not unload cog {cog}')
            return
        await ctx.send(f'{cog} cog unloaded')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog: str):
        '''
        Loads cogs
        Ask your Admin for more information.
        Usage:
            [PREFIX]load cogs.test
            [PREFIX]load cogs.basic
        '''
        try:
            self._bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Could not load cog {cog}')
            return
        await ctx.send(f'{cog} cog loaded')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog: str):
        '''
        Reloads cogs
        Ask your Admin for more information.
        Usage:
            [PREFIX]reload cogs.admin
            [PREFIX]reload cogs.test
        '''
        try:
            self._bot.unload_extension(cog)
            self._bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Could not reload cog {cog}')
            return
        await ctx.send(f'{cog} cog reloaded')

    @commands.command()
    @ranker()
    async def status(self, ctx):
        '''
        admin server status command
        Description:
            Display current server status, voice, text, emoji,
            and other details.
        Usage:
            [PREFIX]status
        '''
        num_voice_chs = len(ctx.guild.voice_channels)
        num_text_chs = len(ctx.guild.text_channels)
        fields = [
            create_field('Server Name', ctx.guild.name),
            create_field('# Voice Channels', num_voice_chs, True),
            create_field('# Text Channels', num_text_chs, True),
            create_field('AFK Channel', ctx.guild.afk_channel, True)
        ]
        num_emoji_fields, emoji_str = 0, ''
        num_emojis_in_field = 0
        for e in ctx.guild.emojis:
            if e.is_usable() and len(emoji_str) <= 990:
                emoji_str += str(e)
                num_emojis_in_field += 1
            else:
                num_emoji_fields += 1
                num_emojis_in_field = 0
                field_name = f'Custom Emojies {num_emoji_fields} ({num_emojis_in_field} emojis)'
                fields.append(create_field(field_name, emoji_str))
                emoji_str = ''
        if len(emoji_str) > 0: num_emoji_fields += 1
        if num_emoji_fields == 0: emoji_str = 'No Custom Emojies'
        img_file = discord.File(PIXEL_PLAYGROUND_LOGO);
        embed = embedded(author=self._bot.user.name,
            fields=fields, thumbnail=self._bot.user.avatar_url,
            image=f'attachment://{img_file.filename}',
            color=discord.Colour.dark_purple(),
            footer_text=datetime.datetime.now())
        async with ctx.channel.typing():
            await ctx.send(embed=embed, file=img_file)

def setup(bot):
    bot.add_cog(Admin(bot))
