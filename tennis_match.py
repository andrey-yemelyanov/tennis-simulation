from game import Game
from tiebreak import Tiebreak

if __name__ == '__main__':
    prob = {'Federer': 0.55, 'Isner': 0.45}
    server = 'Isner'

    player0, player1 = prob.keys()
    stats = {player0: 0, player1: 0}

    for _ in range(10_000):
        tiebreak = Tiebreak(prob, server)
        #print(tiebreak.print_score())
        #print()
        while True:
            point_winner = tiebreak.play_point()
            #print(f'{point_winner} wins the point')
            #print(tiebreak.print_score())
            #print()
            if tiebreak.tiebreak_over(): break
        stats[tiebreak.get_winner()] += 1
        #print(f'{tiebreak.get_winner()} wins the tie break')

    print(stats)
    print(f'{player0} wins {stats[player0] / sum(stats.values()):.3%} tie breaks')

    # tennis_game = Game(prob, server)
    # print(f'{server} serving')
    # print(tennis_game.print_score())
    # print()

    # while True:
    #     point_winner = tennis_game.play_point()
    #     print(f'{point_winner} wins the point')
    #     if tennis_game.game_over(): break
    #     print(tennis_game.print_score())
    #     print()

    # print(f'{tennis_game.get_winner()} wins the game')
        