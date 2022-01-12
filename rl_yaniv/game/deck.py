from typing import List
from random import shuffle
from itertools import product

from rl_yaniv.game.card import YanivCard
from rl_yaniv.exceptions import DeckException

class Deck:
    def __init__(self) -> None:
        self.cards: List[YanivCard] = []
        self.cards_map = {}

    def shuffle(self) -> None:
        shuffle(self.cards)

    def pop_from_deck(self) -> YanivCard:
        if len(self.cards) == 0:
            raise DeckException('The card deck was already empty')
        return self.cards.pop()

    def is_empty(self) -> bool:
        return self.cards == []

    def card_from_index_number(self, index_number: int) -> YanivCard:
        return self.cards_map[index_number]

    @classmethod
    def init_54_deck(cls):
        deck = cls()

        suit_list = ['S', 'H', 'D', 'C']
        rank_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']

        for i, (suit, rank) in enumerate(product(suit_list, rank_list)):
            deck.cards_map[i] = YanivCard(suit, rank, index_number=i)

        deck.cards_map[52] = YanivCard('BJ', '', index_number=52)
        deck.cards_map[53] = YanivCard('RJ', '', index_number=53)

        deck.cards = list(deck.cards_map.values())

        deck.shuffle()

        return deck
