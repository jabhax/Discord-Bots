import discord
from discord.ext import commands

from settings import PREFIX, BOT_PROFILE_PIC, DEBUG_LOGS
from utils.utils import (mention, text_to_owo, embedded, create_fields,
    parse_embed_user_params, notify_user)


class Basic(commands.Cog):
    # Commands in the Basic Cogs Class
    def __init__(self, bot):
        self._bot = bot

    # @commands.Cog.listener()
    # async def on_command_error(self, ctx, ex):
    #     help_msg = ('Please check help for proper usage of this command or talk'
    #                 ' to your Admin.')
    #     server_msg = ('WARNING!!! BOT IS NOT IN PRODUCTION SERVER AND DEBUG '
    #                   'HAS BEEN TURNED ON!')
    #     names = ['Help Message', 'Server Message', 'Exception'] if DEBUG_LOGS else ['Help Message']
    #     values = [help_msg, server_msg, ex] if DEBUG_LOGS else [help_msg]
    #     inlines = [True, True, True] if DEBUG_LOGS else [True]
    #     fields = create_fields(names=names, values=values, inlines=inlines)
    #     embed = embedded(title='Command Help', desc='Incorrect Command Usage', fields=fields)
    #     r = (f'Please check help for proper usage of this command or talk to '
    #          f'your Admin.')
    #     await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        ## uncommenting this with-block will force the bot to change its avatar
        ## profile pic to the BOT_PROFILE_PIC from data/bot_profile_photo.jpeg
        # with open(BOT_PROFILE_PIC, 'rb') as f:
        #     image = f.read()
        #     await self._bot.user.edit(avatar=image)
        print(f'Connected!\nUsername: {self._bot.user.name}\n'
              f'ID: {self._bot.user.id}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.upper().startswith("."):
            # if message.author.bot: return
            # args = message.content.split(" ")
            # await message.channel.send("%s" % (" ".join(args[1:])))
            await message.delete()

    @commands.command()
    async def say(self, ctx, *args):
        '''
        Makes the bot quote you
        Description:
            Mentions user and says what user types.
        Usage:
            [PREFIX]say "some funny comment"
        '''
        r = mention(ctx.message.author) + ' says ' + ' '.join(args)
        await ctx.send(r)

    @commands.command()
    async def search(self, ctx, *args):
        '''
        Searches what you type
        Description:
            Searches using Google Search
        Usage:
            [PREFIX]search cats
        '''
        r = f'{mention(ctx.message.author)} here is what you searched for:\n'
        embed = embedded(title="".join(args), footer_text=f'https://google.com/search?q={"".join(args)}')
        await ctx.channel.send(r, embed=embed)

    @commands.command()
    async def embed(self, ctx, *args):
        '''
        Embeds what user types onto the channel
        Description:
        * Embed's 1st and 2nd input parameters are reserved for the
          Embedding Title and Embedding Description, respectively.
        * Embed's following input parameters are its fields, which
          are composed of a Field Name and Field Value. All
          parameters must follow this in alternating format
          from Name1, Val1, Name2, Val2, ...NameN, ValN.
        * After all field parameters, users can optionally specify
          a thumbnail url via thumbnail={YOUR_URL}
        Usage:
            [PREFIX]embed
            [PREFIX]embed Title
            [PREFIX]embed Title Desc
            [PREFIX]embed Title Desc Field1 v1
            [PREFIX]embed Title Desc Field1 v1 Field2 v2...
            [PREFIX]embed Title Desc Field1 v1... thumbnail=url
        '''
        args = [a for a in args]
        p = parse_embed_user_params(ctx, args)
        embed = embedded(title=p['title'], desc=p['desc'], fields=p['fields'],
                         thumbnail=p['thumbnail'],
                         inline=p['global_inline'],
                         footer_text=f'Added by {ctx.author.name}',
                         footer_icon=ctx.author.avatar_url)
        async with ctx.channel.typing():
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def poop(self, ctx, *args):
        '''
        Take a poop!
        Description:
            Poop on members on the server.
        Usage:
            [PREFIX]poop
            [PREFIX]poop @user1
            [PREFIX]poop @user1 @user2 ...
        '''
        async with ctx.channel.typing():
            await ctx.send(f'You took a dump on {", ".join(args)}!')

    @commands.command()
    async def owo(self, ctx):
        '''
        OWO-fy your text
        Description:
            Converts text to owo by replacing appropriate vowels.
        Usage:
            [PREFIX]owo some_text
        '''
        async with ctx.channel.typing():
            await ctx.send(text_to_owo(ctx.message.content))

    @commands.command()
    @commands.guild_only()
    async def invite(self, ctx):
        '''
        Have bot send invite to channel
        Description:
            Sends invite to server in guild channels only.
            (No D.M. channels)
        Usage:
            [PREFIX]invite @user1 @user2 ...
        '''
        link = await ctx.channel.create_invite(max_age=1)
        async with ctx.channel.typing():
            await ctx.send(link)

    @commands.command()
    async def purge(self, ctx, *args):
        '''
        Purge messages on chat channel
        Description:
            Deletes the latest message. If a number is provided
            then it will delete the last n messages.
        Usage:
            [PREFIX]purge 10'
        '''
        amount = int(eval(args[0])) if args else 2
        async with ctx.channel.typing():
            await ctx.channel.purge(limit=amount)

    @commands.command()
    async def poke(self, ctx, member: discord.Member=None):
        '''
        Poke someone on the server
        Description:
            Pokes a user of your choosing using @mention
        Usage:
            [PREFIX]poke @member
        '''
        msg, error = f'{mention(ctx.author)} poked you!', 'Use @mention to poke'
        if member:
            await notify_user(member, f'{mention(ctx.author)} poked you!')
        else:
            await ctx.send(error)

def setup(bot):
    bot.add_cog(Basic(bot))
