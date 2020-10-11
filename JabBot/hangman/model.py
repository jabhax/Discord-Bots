class Hangman:
    guess_word, prog_word, guesses, max_guesses = '', '', [], 11
    def __init__(self, guess_word):
        self.guess_word, self.guesses = guess_word, []

    def guess(self, c):
        c = c.lower()
        self.prog_word = ''
        for gc in self.guess_word.lower():
            self.prog_word += gc if c == gc or gc in self.guesses else '\_.'
        self.guesses.append(c)

    def check_guess(self, word):
        return (self.prog_word == self.guess_word)

    def is_gameover(self, guess):
        gameover = True if self.get_remaining_guesses() <= 0 else False
        won = self.check_guess(guess)
        if won: gameover = won
        return gameover, won

    def get_num_guesses(self):
        return len(self.guesses)

    def get_max_guesses(self):
        return len(self.guess_word)+1 if len(self.guess_word) > self.max_guesses else self.max_guesses

    def get_remaining_guesses(self):
        return (0 if self.get_num_guesses() >= self.get_max_guesses() else
                self.get_max_guesses() - self.get_num_guesses())
