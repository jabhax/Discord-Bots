import emoji


class RockPaperScissor:
    ROCK = {'ROCK': ':rock:'}
    PAPER = {'PAPER': ':roll_of_paper:'}
    SCISSOR = {'SCISSOR': ':scissors:'}
    winner_check = {
        (ROCK['ROCK'], PAPER['PAPER']): False,
        (ROCK['ROCK'], SCISSOR['SCISSOR']): True,
        (PAPER['PAPER'], ROCK['ROCK']): True,
        (PAPER['PAPER'], SCISSOR['SCISSOR']): False,
        (SCISSOR['SCISSOR'], ROCK['ROCK']): False,
        (SCISSOR['SCISSOR'], PAPER['PAPER']): True
    }
    won, p1_choice, p2_choice = None, None, None

    def check_win(self, p1_choice, p2_choice):
        self.won = (None if p1_choice == p2_choice else
                    RockPaperScissor.winner_check[(p1_choice, p2_choice)])
        self.p1_choice, self.p2_choice = p1_choice, p2_choice
        return self.won

    def get_result(self):
        if self.won is None:
            return f'It\'s a Draw {self.p1_choice} vs {self.p2_choice}'
        elif self.won is True:
            return f'You Won! {self.p1_choice} vs {self.p2_choice}'
        elif self.won is False:
            return f'You Lost! {self.p1_choice} vs {self.p2_choice}'

    @staticmethod
    def get_choices():
        return (RockPaperScissor.ROCK, RockPaperScissor.PAPER,
                RockPaperScissor.SCISSOR)

    @staticmethod
    def get_choice(key):
        for c in RockPaperScissor.get_choices():
            (rps_type, rps_emoji) = next(iter(c.items()))
            if key.upper() in c: return c[key.upper()]
            elif emoji.demojize(key) == rps_emoji: return emoji.demojize(key)
        return None
