from game import Game



if __name__ == '__main__':
    prob = {'Federer': 0.55, 'Djokovic': 0.45}
    server = 'Federer'

    N_GAMES = 10_000

    fed_wins, djo_wins = 0, 0

    for _ in range(N_GAMES):
        tennis_game = Game(prob, server)
        winner = tennis_game.play()
        if winner == 'Federer': fed_wins += 1
        elif winner == 'Djokovic': djo_wins += 1

    print(f'{N_GAMES} games played, Fed wins {fed_wins / N_GAMES:.00%}, Djoker wins {djo_wins / N_GAMES:.00%}')

    
    # print(tennis_game.get_game_state())
    # print()
    
    # while not tennis_game.game_over():
    #     point_winner = tennis_game.play_point()
    #     print(f'{point_winner} wins the point')
    #     if tennis_game.game_over(): break
    #     print(tennis_game.get_game_state())
    #     print()

    # print(f'{tennis_game.get_winner()} wins the game')
        