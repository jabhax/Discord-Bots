import emoji
from .model import RockPaperScissor as RPS


class RPSParser():
    def __init__(self, choice):
        if RPS.get_choice(choice):
            self.choice = RPS.get_choice(choice)
        elif RPS.get_choice(emoji.demojize(choice)):
            self.choice = RPS.get_choice(emoji.demojize(choice))
        # else:
            # raise ValueError(f'Invalid choice from RPSParser init: {choice}')
