from rl_yaniv.game.deck import Deck
from rl_yaniv.game.player import Player
from rl_yaniv.exceptions import DeckException

class TestDeck:

    def test_init_Player(self):
        player = Player(player_id=1)