from rl_yaniv.game.yaniv import Yaniv, YanivRound
from rl_yaniv.game.player import RandomPlayer
from rl_yaniv.game.actions import PickupDeckCard, PickupPileTopCard, ThrowCard


class TestGame:
    def test_init_yaniv_round(self):
        yaniv_round = YanivRound([])
        assert yaniv_round

        assert len(yaniv_round.players) == 0

    def test_init_yaniv(self):
        yaniv = Yaniv(players=[RandomPlayer(player_id=0), RandomPlayer(player_id=1)])
        assert yaniv

        yaniv.reset()

    def test_draw_deck_card(self):
        yaniv = Yaniv(players=[RandomPlayer(player_id=0), RandomPlayer(player_id=1)])
        assert yaniv

        yaniv.reset()
        yaniv.step(PickupDeckCard())
        assert len(yaniv.get_current_player().cards) == 5

    def test_draw_pile_card(self):
        yaniv = Yaniv(players=[RandomPlayer(player_id=0), RandomPlayer(player_id=1)])
        assert yaniv

        yaniv.reset()
        yaniv.step(PickupPileTopCard())
        assert len(yaniv.get_current_player().cards) == 5

    def test_throw_card(self):
        yaniv = Yaniv(players=[RandomPlayer(player_id=0), RandomPlayer(player_id=1)])
        assert yaniv

        yaniv.reset()
        first_card_index, *_ = yaniv.get_current_player().cards.keys()
        yaniv.step(ThrowCard(first_card_index))
        assert len(yaniv.get_current_player().cards) == 4
