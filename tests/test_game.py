from rl_yaniv.game.yaniv import Yaniv

class TestGame:

    def test_init_game(self):
        yaniv = Yaniv()
        assert yaniv

        assert len(yaniv.players) == 4

        yaniv.deal()
        for player in yaniv.players:
            assert len(player.cards) == 5

    def test_start_game(self):
        yaniv = Yaniv()
        yaniv.start()
        assert isinstance(yaniv.player_turn, int)
