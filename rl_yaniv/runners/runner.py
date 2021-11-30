from rl_yaniv.game.yaniv import Yaniv
from rl_yaniv.game.player import HighCardPlayer, RandomPlayer, OptimizedHighCardPlayer, HighThrowPlayer

# player that takes random actions and only throws away one card per turn.
yaniv = Yaniv(players=[RandomPlayer(player_id=0), HighThrowPlayer(player_id=1), OptimizedHighCardPlayer(player_id=2)])
yaniv.reset()

while not yaniv.is_over():
    current_player = yaniv.get_current_player()
    current_player.step(yaniv)
    print(f"Player {current_player.player_id} has: {current_player.get_points()}  - {current_player.last_action} - Cards: {len(current_player.cards)}")

winner, *losers = (sorted(yaniv.players.values(), key=lambda p: p.game_score))
print(f"Winner: {winner.player_id} with {winner.game_score}")
for loser in losers:
    print(f"Loser: {loser.player_id} with {loser.game_score}")