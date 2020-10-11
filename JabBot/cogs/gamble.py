import random
from discord.ext import commands

from settings import PREFIX
from utils.utils import mention


class Gamble(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    async def roll(self, ctx):
        '''
        Roll a number
        Description:
            Roll a random number
        Usage:
            [PREFIX]roll
        '''
        r = f'{mention(ctx.message.author)} rolled a ({random.randint(1, 101)})'
        async with ctx.channel.typing():
            await ctx.send(r)

    @commands.command()
    async def dice(self, ctx, *args):
        '''
        Roll some dice
        Description:
            Roll any number of any faced dice. Default is 1 die with 6 faces.
            First parameter is the number of dice, the second parameter
            is the number of faces for each die.
        Usage:
            [PREFIX]dice         -->     (1-die, 6-faces)
            [PREFIX]dice 2 6     -->     (2-dice, 6-faces)
            [PREFIX]dice 9 9     -->     (9-dice, 9-faces)
            [PREFIX]dice 10 10   -->     (10-dice, 10-faces)
        '''
        # Check if user inputed custom number of dice or faces.
        dice, faces = (
            (1, 6) if len(args) == 0 else  # default dice=1, face=6
            (int(args[0]), 6) if len(args) == 1 else  # if only args[0], then dice=args[0], face=6
            (int(args[0]), int(args[1]))  # if both args[0] and args[1], then dice=args[0], face=args[1]
        )
        # Compute rolls and total rolls
        total_roll, rolls_msg = 0, mention(ctx.message.author)+ '\n'
        for i in range(dice):
            curr_roll = random.randint(1, faces)
            total_roll += curr_roll
            rolls_msg += f'Rolled a die [{str(curr_roll)}]\n'

        bot_reply_9 = (f'JabBot says "{dice} dice...what kind of gamble are '
                       f'you doing, Human?"\n')
        # Format bot reply based on number of dice.
        r = (f'{bot_reply_9}Total Roll [{total_roll}]' if dice > 9 else
             f'{rolls_msg}Total Roll [{total_roll}]' if dice > 3 else
             f'{rolls_msg}')
        async with ctx.channel.typing():
            await ctx.send(r)

    @commands.command()
    async def coin(self, ctx):
        '''
        Flip a coin
        Description:
            Flip a coin; land Head or Tails.
        Usage:
            [PREFIX]coin
        '''
        coin_result = (':head_bandage: Heads' if random.randint(0, 1) else
                        ':t_rex: Tails')
        r = f'{mention(ctx.message.author)} flipped {coin_result}!'
        async with ctx.channel.typing():
            await ctx.send(r)


def setup(bot):
    bot.add_cog(Gamble(bot))
