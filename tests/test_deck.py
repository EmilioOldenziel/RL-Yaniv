from rl_yaniv.game.deck import Deck

class TestDeck:

    def test_init_deck(self):
        deck = Deck.init_54_deck()
        assert deck
        assert len(deck.cards) == 54