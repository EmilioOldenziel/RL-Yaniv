from typing import List
from random import shuffle

from rl_yaniv.game.card import YanivCard
from rl_yaniv.exceptions import DeckException

class Deck:
    def __init__(self) -> None:
        self.cards: List[YanivCard] = []

    def shuffle(self) -> None:
        shuffle(self.cards)

    def pop_from_deck(self) -> YanivCard:
        if len(self.cards) == 0:
            raise DeckException('The card deck was already empty')
        return self.cards.pop()

    def is_empty(self) -> bool:
        return self.cards == []

    @classmethod
    def init_54_deck(cls):
        deck = cls()
        
        suit_list = ['S', 'H', 'D', 'C']
        rank_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        deck.cards = [YanivCard(suit, rank) for suit in suit_list for rank in rank_list]
        deck.cards.append(YanivCard('BJ', ''))
        deck.cards.append(YanivCard('RJ', ''))
        deck.shuffle()

        return deck
