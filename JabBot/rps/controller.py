import random

from .model import RockPaperScissor as RPS


class RPSGame:
    rps = None

    def __init__(self):
        self.rps = RPS()

    def run(self, user_choice):
        if not self.rps.get_choice(user_choice):
            raise Exception('Need either rock, paper, or scissor')
        bot_choice = random.choice(self.rps.get_choices()).values()
        bot_choice = next(iter(bot_choice))
        won = self.rps.check_win(user_choice, bot_choice)
        return won, bot_choice
