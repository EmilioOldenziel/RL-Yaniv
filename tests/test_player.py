from rl_yaniv.game.actions import PickupDeckCard, PickupPileTopCard, ThrowCard
from rl_yaniv.game.player import RandomPlayer
from rl_yaniv.game.deck import Deck

class TestPlayer:

    def test_init_Player(self):
        player = RandomPlayer(player_id=1)
        assert player

    def test_legal_actions(self):

        player = RandomPlayer(player_id=1)
        deck = Deck.init_54_deck()

        player.add_card(deck.card_from_index_number(2))  # spades 3
        player.add_card(deck.card_from_index_number(3))  # spades 4
        player.add_card(deck.card_from_index_number(4))  # spades 5
        player.add_card(deck.card_from_index_number(5))  # spades 6
        player.add_card(deck.card_from_index_number(15)) # hearts 3

        assert len(player.get_legal_actions()) == 5

        # throw spades 3
        card = player.pop_card(2)
        player.previous_actions.append(ThrowCard(card))

        assert player.get_legal_actions() == [ThrowCard(deck.card_from_index_number(15)),
                                              ThrowCard(deck.card_from_index_number(3)), 
                                              PickupDeckCard(), PickupPileTopCard()]

        # throw spades 4
        card = player.pop_card(3)
        player.previous_actions.append(ThrowCard(card))

        # throwing spades 5 should be the only legal option because there has to be 3+ in a sequence
        assert player.get_legal_actions() == [ThrowCard(deck.card_from_index_number(4))]

        # throw spades 5
        card = player.pop_card(4)
        player.previous_actions.append(ThrowCard(card))

        # throwing spades 5 should be the only legal option because there has to be at 3+ in a sequence
        assert player.get_legal_actions() == [ThrowCard(deck.card_from_index_number(5))]
                                      


        