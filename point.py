import random
from typing import Dict

def play(P: Dict[str, float]) -> str:
    '''
        Simulates a play of a single point, given probability of winning a single point for each player.
        Returns player name that wins the point.
        Probability distribution is not uniform, as some players are better than others.
        E.g. if probability distribution is P={'Federer': 0.7, 'Rublev': 0.3}, 
        then Federer will win on average 7 out of 10 points.
    '''
    #   Rublev           Federer
    # |--------+--------------------------|
    # 0       0.3                         1
    player0, player1 = P.keys()
    if random.random() < P[player0]: return player0
    else: return player1

def adjust_prob_for_server_advantage(P: Dict[str, float], server: str):
    pass