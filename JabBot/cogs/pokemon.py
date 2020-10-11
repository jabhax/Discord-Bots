import discord
import time
import random
from discord.ext import commands

from settings import PREFIX, PKMN_SPRITE_MENU
from utils.roles import regular
from utils.utils import embedded, create_field
from pokemon.model import Pokedex

from settings import PKMN_SPRITE_MENU, DEX_ID_TO_NAME_JSON, PK_JSON



class Pokemon(commands.Cog):
    GEN1 = (1, 151)
    GEN2 = (152, 251)
    GEN3 = (252, 386)
    GEN4 = (387, 493)
    GEN5 = (494, 649)
    GEN6 = (650, 721)
    GEN7 = (722, 809)
    GEN8 = (810, 893)

    def __init__(self, bot):
        self._bot = bot
        # dirs = "\n".join([d for d in dir(self._bot)])
        # print(f'{dirs}')
        self.pd = Pokedex()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        emoji = reaction.emoji
        ch = reaction.message.channel
        guild = reaction.message.guild
        print(f'emoji.name: {emoji.name}')
        if user.bot: return
        async with ch.typing():
            pk_embed, files, pkmn, prv, nxt = await self.pd.embed_pokemon(guild, emoji.name)
            msg = await ch.send(embed=pk_embed, files=files)
            await msg.add_reaction(prv)
            await msg.add_reaction(nxt)

    @commands.command()
    async def deleteanimated(self, ctx):
        '''
        just do it....
        Description:
            Deletes every fucking animated emoji
        Usage:
            [PREFIX]deleteAllAnimatedEmojis
        '''
        for emoji in ctx.guild.emojis:
            if emoji.animated:
                messages = []
                start = time.time()
                await ctx.send(f'Clearing channel of emoji {emoji}...')
                for ch in ctx.guild.text_channels:
                    messages += await ch.history(limit=200).flatten()
                for msg in messages:
                    if len(msg.reactions) > 0:
                        reaction = discord.utils.get(msg.reactions, emoji=emoji.name)
                        await msg.clear_reaction(emoji)
                start = time.time()
                await ctx.send(f'Cleared in {(time.time()-start):.4f}s. Deleting {emoji}...')
                await emoji.delete()
                await ctx.send(f'Delete took {(time.time()-start):.4f}s, bot latency: {self._bot.latency}')
        else:
            await ctx.send(f'Good job! There are no more animated emojis!')

    @commands.command()
    async def populate(self, ctx, *args):
        '''
        Populate the Pokedex
        Description:
            Populates the pokedex by reteriving all of them from the Pokebase API
        Usage:
            [PREFIX]populate
        '''
        # Need to fix:
        #   - Deoxys (386)
        #   - Type-Null (772)
        #   - Silvary (773)
        #   - Tapu-Koko (785)
        #   - Tapu-Lele (786)
        #   - Tapu-Bulu (787)
        #   - Tapu-Fini (788)
        self.pd.PK_CH = discord.utils.get(ctx.guild.text_channels, name="pokedex")
        for id in range(102, 807):
            # id = random.randint(1, 807)
            async with ctx.channel.typing():
                pk_embed, files, pkmn, prv, nxt = (
                    await self.pd.embed_pokemon(ctx.guild, str(id)))
                msg = await ctx.send(embed=pk_embed, files=files)
                await msg.add_reaction(prv)
                await msg.add_reaction(nxt)

    @commands.command()
    async def dex(self, ctx, *args):
        '''
        Search the pokedex
        Description:
            Queries the pokedex for a pokemon by name or pokedex entry id
        Usage:
            [PREFIX]dex charizard
            [PREFIX]dex 006
            [PREFIX]dex 6
            [PREFIX]dex Charizard
        '''
        self.pd.PK_CH = discord.utils.get(ctx.guild.text_channels, name="pokedex")
        pkmn = ' '.join(args).strip()
        async with ctx.channel.typing():
            pk_embed, files, pkmn, prv, nxt = (
                await self.pd.embed_pokemon(ctx.guild, pkmn, detailed=False))
            msg = await ctx.send(embed=pk_embed, files=files)
            await msg.add_reaction(prv)
            await msg.add_reaction(nxt)

    @commands.command()
    async def ddex(self, ctx, *args):
        '''
        Search the detailed dex
        Description:
            Queries the pokedex for a pokemon by name or pokedex entry id and
            displays more details than [PREFIX]dex.
        Usage:
            [PREFIX]ddex charizard
            [PREFIX]ddex 006
            [PREFIX]ddex 6
            [PREFIX]ddex Charizard
        '''
        self.pd.PK_CH = discord.utils.get(ctx.guild.text_channels, name="pokedex")
        pkmn = ' '.join(args).strip()
        async with ctx.channel.typing():
            pk_embed, files, pkmn, prv, nxt = (
                await self.pd.embed_pokemon(ctx.guild, pkmn))
            msg = await ctx.send(embed=pk_embed, files=files)
            await msg.add_reaction(prv)
            await msg.add_reaction(nxt)


def setup(bot):
    bot.add_cog(Pokemon(bot))
