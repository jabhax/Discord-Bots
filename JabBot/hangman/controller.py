import random

from .model import Hangman
from utils.utils import get_words_dict


games = {}
WORDS_DICT = [key for key in get_words_dict().keys()]


class HangmanGame:
    curr_game = None

    def get_secret(self):
        return self.curr_game.guess_word

    def get_guesses(self):
        return ', '.join(self.curr_game.guesses)

    def is_already_used(self, guess):
        return (guess in self.curr_game.guesses)

    def get_progword(self):
        return self.curr_game.prog_word

    def get_remaining(self):
        return self.curr_game.get_remaining_guesses()

    def get_random_word(self):
        return random.choice(WORDS_DICT)

    def run(self, player_id, guess):
        self.get_game(player_id)
        retry = self.is_already_used(guess)
        if retry: return None, None, retry
        gameover, won = self.play_round(guess)
        self.save(player_id)
        return gameover, won, retry

    def play_round(self, guess):
        is_word = False
        if len(guess) == 1: pass
        elif len(guess) > 1: is_word = True
        else: return None, None
        if not is_word: self.curr_game.guess(guess)
        gameover, won = self.curr_game.is_gameover(guess)
        return gameover, won

    def get_game(self, player_id):
        if player_id in games:
            self.curr_game = games[player_id]
            if self.curr_game is None:
                self.create_game(player_id)
        else:
            self.create_game(player_id)

    def create_game(self, player_id):
        self.curr_game = Hangman(self.get_random_word())
        self.save(player_id)

    def save(self, player_id):
        games[player_id] = self.curr_game

    async def reset(self, player_id):
        games.pop(player_id)
