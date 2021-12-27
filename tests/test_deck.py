from rl_yaniv.game.deck import Deck
from rl_yaniv.exceptions import DeckException

class TestDeck:

    def test_init_deck(self):
        deck = Deck.init_54_deck()
        assert deck
        assert len(deck.cards) == 54

    def test_total_points(self):
        deck = Deck.init_54_deck()
        total_points = 0
        while True:
            try:
                card = deck.pop_from_deck()
                total_points += card.points
            except DeckException:
                break
        assert total_points == 340

    def test_index_numbers(self):
        deck = Deck.init_54_deck()
        assert list(sorted([c.index_number for c in deck.cards])) == list(range(54))
