import discord
from discord.ext import commands

from settings import PREFIX
from utils.roles import regular
from utils.utils import embedded, create_field

# Rock Paper Scissor Game
from rps.model import RockPaperScissor as RPS
from rps.parser import RPSParser
from rps.controller import RPSGame
# Hangman Game
from hangman.controller import HangmanGame



class Games(commands.Cog):

    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    @regular()
    async def rps(self, ctx, user_choice: RPSParser):
        '''
        Play a game of Rock, Paper, Scissors
        Description:
            Choose between Rock, Paper, or Scissor to play against JabBot.
        Usage:
            [PREFIX]rps rock
            [PREFIX]rps paper
            [PREFIX]rps scissor
        '''
        game, uc = RPSGame(), None
        try: uc = user_choice.choice
        except: uc = user_choice
        won, bot_choice = game.run(uc)
        embed = embedded(
            title='Rock, Paper, Scissor',
            desc=game.rps.get_result(),
            thumbnail=ctx.author.avatar_url,
            footer_text=f'Played by {ctx.author.name}',
            footer_icon=discord.Embed.Empty)
        async with ctx.channel.typing():
            await ctx.send(embed=embed)

    @commands.command()
    @regular()
    async def hm(self, ctx, guess: str):
        '''
        Play a Hangman game
        Description:
            Guess the word with as many attempts as the word's length.
            Either guess the full word or single letters only.
        Usage:
            [PREFIX]hm a
            [PREFIX]hm b
            [PREFIX]hm word
        '''
        player_id, game = ctx.author.id, HangmanGame()
        gameover, won, retry = game.run(player_id, guess)
        if retry:
            retry_msg = (f'You already tried: [{game.get_guesses()}]\n'
                         f'Please try a different letter.')
            async with ctx.channel.typing():
                await ctx.send(retry_msg)
            return

        if gameover:
            gameover_msg = ('Wrong', 'Game Over! You did not guess correctly. You\'ve been hanged!')
            game_over_field = create_field(gameover_msg[0], gameover_msg[1])
            if won:
                gameover_msg = ('Correct', 'Congrats you Won!!! You escaped the hanging!')
                game_over_field['name'] = gameover_msg[0]
                game_over_field['value'] = gameover_msg[1]
            fields = [
                game_over_field,
                create_field('Your Guess', game.get_progword(), True),
                create_field('Guesses So Far', game.get_guesses(), True),
                create_field('The Word Was', game.get_secret())
            ]
            embed = embedded(title='Hangman Results', fields=fields,
                footer_text=discord.Embed.Empty, footer_icon=discord.Embed.Empty)
            await game.reset(player_id)
            async with ctx.channel.typing():
                await ctx.send(embed=embed)
        else:
            fields = [
                create_field('Progress', game.get_progword(), True),
                create_field('Guesses So Far', f'[{game.get_guesses()}]')
            ]
            embed = embedded(
                title='Hangman',
                desc=f'Attemps Remaining: {game.get_remaining()}',
                fields=fields,
                footer_text=discord.Embed.Empty,
                footer_icon=discord.Embed.Empty)
            async with ctx.channel.typing():
                await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Games(bot))
