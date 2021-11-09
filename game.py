import point
from typing import Dict
import math

class Game:
    '''
        Encapsulates a tennis game with its internal score tracking. A game continues until a player
        passes 40 points where the other player had max 30 points. If a deuce occurred, then the 
        game continues until a single player wins two points in a row.
    '''

    ADV, GAME_OVER = 45, 50
    point_scale = [0, 15, 30, 40, ADV, GAME_OVER]

    def __points(self, player: str):
        return Game.point_scale[self.__score[player]]

    def __init__(self, P: Dict[str, float], server: str) -> None:
        '''
            Creates a new instance of Game with given probability distribution of each player winning a single point in a typical rally.
            The probability distribution is in the form e.g. P={'Federer': 0.7, 'Rublev': 0.3} and indicates that
            Federer will win on average 7 out of 10 points played. The sum of probabilities must be 1.0.
        '''

        if not math.isclose(sum(P.values()), 1.0):
            raise Exception(f'Probabilities must add up to 1.0, but the actual sum is {sum(P.values())}')
        
        player0, player1 = P.keys()
        self.__score: Dict[str, int] = {player0: 0, player1: 0}
        self.__prob = P.copy()
        self.__server = server

    def print_score(self):
        state = []

        player0, player1 = self.__score.keys()
        player0_pts, player1_pts = self.__points(player0), self.__points(player1)

        # mark serving player
        if player0 == self.__server: player0 += ' *'
        elif player1 == self.__server: player1 += ' *'

        if player0_pts == Game.ADV and player1_pts == 40:
            state.append(f'{player0:15s}ADV')
            state.append(f'{player1:15s}')
        elif player1_pts == Game.ADV and player0_pts == 40:
            state.append(f'{player0:15s}')
            state.append(f'{player1:15s}ADV')
        else:
            state.append(f'{player0:15s}{player0_pts:3d}')
            state.append(f'{player1:15s}{player1_pts:3d}')

        return '\n'.join(state)

    def get_winner(self) -> str:
        '''
            Returns the winner of this game if it is over. Otherwise, returns None.
        '''

        player_0, player_1 = self.__score.keys()

        player_0_won = (
                (self.__points(player_0) == Game.ADV and self.__points(player_1) <= 30) or
                (self.__points(player_0) == Game.GAME_OVER))
        if player_0_won: return player_0

        player_1_won = (
                (self.__points(player_1) == Game.ADV and self.__points(player_0) <= 30) or
                (self.__points(player_1) == Game.GAME_OVER))
        if player_1_won: return player_1

        return None

    def game_over(self) -> bool:
        return self.get_winner() is not None

    def play_point(self) -> str:
        '''
            Simulates a point play in this game by advancing the winning player's current score.
            Throws exception if the game is already over.
            Returns the name of the winning player.
        '''
        if self.game_over(): raise Exception('Unable to play point. Game over.')
        
        winner = point.play(self.__prob)
        self.__score[winner] += 1

        player0, player1 = self.__prob.keys()

        # corner case: when e.g. player0 had ADVANTAGE but player1 wins the point,
        # then the overall score must go back to 40 all
        if self.__points(player0) == self.__points(player1) and self.__points(player0) == Game.ADV:
            self.__score[player0] -= 1
            self.__score[player1] -= 1

        return winner

