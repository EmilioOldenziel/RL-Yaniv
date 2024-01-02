from rl_yaniv.game.player import RandomPlayer


class TestDeck:
    def test_init_Player(self):
        player = RandomPlayer(player_id=1)
        assert player
