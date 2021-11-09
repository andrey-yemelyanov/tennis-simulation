import math
from typing import Dict
import point

class Tiebreak:

    def __init__(self, P: Dict[str, float], server: str) -> None:
        self.__server = server

        if not math.isclose(sum(P.values()), 1.0):
            raise Exception(f'Probabilities must add up to 1.0, but the actual sum is {sum(P.values())}')

        self.__prob = P.copy()
        player0, player1 = P.keys()
        self.__score = {player0: 0, player1: 0}

    def __returning_player(self):
        player0, player1 = self.__score.keys()
        return player0 if self.__server == player1 else player1

    def __adjust_prob_for_server_advantage(self):
        # it is a reasonable assumption that a competent server gains about 10-15% advantage during a point play
        SERVER_ADVANTAGE = 0.1
        if self.__server == 'Isner': SERVER_ADVANTAGE = 0.15
        player0, player1 = self.__prob.keys()
        if self.__server == player0: 
            return {
                player0: self.__prob[player0] + SERVER_ADVANTAGE, 
                player1: self.__prob[player1] - SERVER_ADVANTAGE
            }
        else:
            return {
                player0: self.__prob[player0] - SERVER_ADVANTAGE, 
                player1: self.__prob[player1] + SERVER_ADVANTAGE
            }

    def play_point(self):
        
        if self.tiebreak_over(): raise Exception('Unable to play point. Tie break is over.')

        winner = point.play(self.__adjust_prob_for_server_advantage())
        self.__score[winner] += 1

        # switch serving players after each odd point
        points_played = sum(self.__score.values())
        if points_played % 2 != 0:
            self.__server = self.__returning_player()

        return winner

    def print_score(self):
        player0, player1 = self.__score.keys()
        player0_pts, player1_pts = self.__score[player0], self.__score[player1]
        if self.__server == player0: player0 += ' *'
        elif self.__server == player1: player1 += ' *'
        return f'{player0:15s}{player0_pts:3d}\n{player1:15s}{player1_pts:3d}'

    def get_winner(self):
        if not self.tiebreak_over(): return None
        player0, player1 = self.__score.keys()
        player0_pts, player1_pts = self.__score[player0], self.__score[player1]
        if player0_pts > player1_pts: return player0
        return player1

    def tiebreak_over(self):
        player0, player1 = self.__score.keys()
        player0_pts, player1_pts = self.__score[player0], self.__score[player1]
        return max(player0_pts, player1_pts) >= 7 and abs(player0_pts - player1_pts) >= 2