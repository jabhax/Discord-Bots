import discord
from discord.ext import commands
import aiohttp
import praw
import random

from utils.utils import mention, embedded
from settings import (PREFIX, REDDIT_APP_ID, REDDIT_APP_SECRET,
    REDDIT_ENABLED_MEME_SUBREDDITS, REDDIT_ENABLED_NSFW_SUBREDDITS)


class Images(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self._reddit = None
        if REDDIT_APP_ID and REDDIT_APP_SECRET:
            self._reddit = praw.Reddit(
                client_id=REDDIT_APP_ID,
                client_secret=REDDIT_APP_SECRET,
                user_agent=f'JabBot:{REDDIT_APP_ID}:1.0')

    @commands.command()
    async def random(self, ctx, subreddit: str=''):
        '''
        Random images/gifs
        Description:
            Display random images.
        Usage:
            [PREFIX]random
            [PREFIX]random funny
            [PREFIX]random memes
            [PREFIX]random wtf
        '''
        async with ctx.channel.typing():
            if self._reddit:
                sub, nsfw = REDDIT_ENABLED_MEME_SUBREDDITS[0], False
                if subreddit:
                    if subreddit in REDDIT_ENABLED_MEME_SUBREDDITS:
                        sub = subreddit
                    elif subreddit in REDDIT_ENABLED_NSFW_SUBREDDITS:
                        sub, nsfw = subreddit, True
                    else:
                        list_memes = ", ".join(REDDIT_ENABLED_MEME_SUBREDDITS)
                        list_nsfw = ", ".join(REDDIT_ENABLED_NSFW_SUBREDDITS)
                        title = 'Please select a subreddit from the following list:\n'
                        channel_fields = [
                            create_field(name='Meme Channels', value=list_memes),
                            create_field(name='NSFW Channels', value=list_nsfw)
                        ]
                        embed = embedded(title=title, fields=channel_fields)
                        await ctx.send(embed=embed)
                        return
                if nsfw and not ctx.channel.is_nsfw():
                    await ctx.send('This is NSFW content, which is not allowed '
                                   'on this channel.')
                    return
                hot_submissions = self._reddit.subreddit(sub).hot()
                for i in range(0, random.randint(1, 10)):
                    hot_sub = next(x for x in hot_submissions if not x.stickied)
                await ctx.send(hot_sub.url)
            else:
                await ctx.send('Random Reddit not working. Contact your Admin!')

    @commands.command()
    async def cat(self, ctx):
        '''
        Cat images/gifs
        Description:
            Display random cat images.
        Usage:
            [PREFIX]cat'
        '''
        random_url = 'https://aws.random.cat/meow'
        footer_url = 'https://random.cat/'
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(random_url) as req:
                    data = await req.json()
                    embed = embedded(title='Meow', image=data['file'],
                                     color=discord.Embed.Empty,
                                     footer_text=footer_url)
                    await ctx.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        '''
        Dog images/gifs
        Description:
            Display random dog images.
        Usage:
            [PREFIX]dog'
        '''
        random_url = 'https://random.dog/woof.json'
        footer_url = 'https://random.dog/'
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(random_url) as req:
                    data = await req.json()
                    embed = embedded(title='Woof', image=data['url'],
                                     color=discord.Embed.Empty,
                                     footer_text=footer_url)
                    await ctx.send(embed=embed)

    @commands.command()
    async def fox(self, ctx):
        '''
        Fox images/gifs
        Description:
            Display random fox images.
        Usage:
            [PREFIX]fox'
        '''
        random_url = 'https://randomfox.ca/floof'
        footer_url = 'https://randomfox.ca/'
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(random_url) as req:
                    data = await req.json()
                    embed = embedded(title='Floof', image=data['image'],
                                     color=discord.Embed.Empty,
                                     footer_text=footer_url)
                    await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Images(bot))
