import time

from rl_yaniv.game.yaniv import Yaniv
from rl_yaniv.game.player import RandomPlayer #, OptimizedHighCardPlayer, HighThrowPlayer

# player that takes random actions and only throws away one card per turn.
yaniv = Yaniv(players=[RandomPlayer(player_id=0), RandomPlayer(player_id=1)])
yaniv.reset()

counter = 0
start_time = time.time()

while not yaniv.is_over():
    current_player = yaniv.get_current_player()
    current_player.step(yaniv)
    # yaniv.render()

    counter += 1
execution_time = time.time() - start_time
print(f"rounds {counter/execution_time} per second")
winner, *losers = (sorted(yaniv.get_players(), key=lambda p: p.game_score))
print(f"Winner: {winner.player_id} with {winner.game_score} after {counter} rounds")
for loser in losers:
    print(f"Loser: {loser.player_id} with {loser.game_score}")