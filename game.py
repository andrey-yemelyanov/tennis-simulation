import random
from typing import Dict

class Game:

    ADV, GAME_OVER = 45, 50
    pts = [0, 15, 30, 40, ADV, GAME_OVER]

    def __init__(self, prob: Dict[str, float], server: str) -> None:
        self.game_state: Dict[str, int] = {}
        for player in prob:
            self.game_state[player] = 0
        self.prob = prob
        self.server = server

    def get_game_state(self):
        state = []

        player0, player1 = self.game_state.keys()
        player0_score, player1_score = self.points(player0), self.points(player1)

        if player0 == self.server: player0 += ' *'
        elif player1 == self.server: player1 += ' *'

        if player0_score == Game.ADV and player1_score == 40:
            state.append(f'{player0:15s}ADV')
            state.append(f'{player1:15s}')
        elif player1_score == Game.ADV and player0_score == 40:
            state.append(f'{player0:15s}')
            state.append(f'{player1:15s}ADV')
        else:
            state.append(f'{player0:15s}{player0_score:3d}')
            state.append(f'{player1:15s}{player1_score:3d}')

        return '\n'.join(state)

    def points(self, player: str):
        return Game.pts[self.game_state[player]]

    def get_winner(self) -> str:
        '''
            Returns the winner of this game if it is over. Otherwise, returns None.
        '''

        player_0, player_1 = self.game_state.keys()

        player_0_won = (
                (self.points(player_0) == Game.ADV and self.game_state[player_1] <= 2) or
                (self.points(player_0) == Game.GAME_OVER))
        if player_0_won: return player_0

        player_1_won = (
                (self.points(player_1) == Game.ADV and self.game_state[player_0] <= 2) or
                (self.points(player_1) == Game.GAME_OVER))
        if player_1_won: return player_1

        return None

    def game_over(self) -> bool:
        return self.get_winner() is not None

    def play_point(self) -> str:

        def play_single_point() -> str:
            '''
                Simulates a play of a single point, given probability of winning a single point for each player.
                Returns player name that wins the point.
                Probability distribution is not always uniform, as some players are better than others.
                E.g. if probability distribution is prob={'Federer': 0.7, 'Rublev': 0.3}, 
                then on average Federer will win 7 out of 10 points.
            '''
            #   Rublev           Federer
            # |--------+--------------------------|
            # 0       0.3                         1
            player0, player1 = self.prob.keys()
            if random.random() < self.prob[player0]: return player0
            else: return player1

        if self.game_over(): raise Exception('Unable to play point. Game over.')
        winner = play_single_point()
        self.game_state[winner] += 1

        player0, player1 = self.prob.keys()

        if self.points(player0) == self.points(player1) and self.points(player0) == Game.ADV:
            self.game_state[player0] -= 1
            self.game_state[player1] -= 1

        return winner

    def play(self):
        while not self.game_over():
            self.play_point()
        return self.get_winner()

