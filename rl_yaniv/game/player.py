from abc import ABC, abstractmethod
from collections import OrderedDict
from random import choice, randint
from typing import Optional
from itertools import groupby

from rl_yaniv.game.actions import (Action, CallYaniv, EndTurn, PickupDeckCard,
                                   PickupPileTopCard, ThrowCard)
from rl_yaniv.game.card import Card


class Player(ABC):
    
    def __init__(self, player_id) -> None:
        self.player_id = player_id
        self.cards: OrderedDict[str, Card] = OrderedDict()
        self.game_score: int = 0

        self.last_action: Optional[Action] = None

    def add_card(self, card: Card) -> None:
        self.cards[card.get_index()] = card

    def get_points(self) -> int:
        return sum([card.points for card in self.cards.values()])

    def reset(self):
        self.reset_cards()
        self.game_score = 0
        self.last_action = None

    def reset_cards(self):
        self.cards = OrderedDict()

    @abstractmethod
    def step(self, yaniv_round) -> None:
        ...


class RandomPlayer(Player):
    """

        Player that 
        - Calls Yaniv when possible.
        - Picks up from deck or pile randomly.
        - Trows a random single card. 
    """
    def step(self, yaniv) -> None:

        # Call Yaniv
        if self.last_action is None and self.get_points() < 6:
            print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")
            action = CallYaniv()
            yaniv.step(action)
            self.last_action = None
            return

        # Pickup
        if self.last_action is None:
            pickup_choice = randint(1,2)
            if pickup_choice == 1:
                action = PickupDeckCard()
            if pickup_choice == 2:
                action = PickupPileTopCard()
            yaniv.step(action)
            self.last_action = action
            return
        
        # Throw
        if isinstance(self.last_action, PickupDeckCard) or isinstance(self.last_action, PickupPileTopCard):
            action = ThrowCard(choice(list(self.cards.keys())))
            yaniv.step(action)
            self.last_action = action
            return

        if isinstance(self.last_action, ThrowCard):
            # Done
            yaniv.step(EndTurn())
            self.last_action = None
            return


class HighCardPlayer(Player):
    """
        Player that always maximizes chance by:
        - Calling yaniv when possible.
        - Picking up from pile if card is below 4 points otherwise from deck.
        - throwing the card with the most points.
    """
    def step(self, yaniv) -> None:

        # Call Yaniv
        if self.last_action is None and self.get_points() < 6:
            print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")
            action = CallYaniv()
            yaniv.step(action)
            return

        # Pickup
        if self.last_action is None:
            pickup_choice = randint(1,2)
            if pickup_choice == 1:
                action = PickupDeckCard()
            if pickup_choice == 2:
                action = PickupPileTopCard()
            yaniv.step(action)
            self.last_action = action
            return
        
        # Throw
        if isinstance(self.last_action, PickupDeckCard) or isinstance(self.last_action, PickupPileTopCard):
            action = ThrowCard(max(list(self.cards.values()), key=lambda c: c.points).get_index())
            yaniv.step(action)
            self.last_action = action
            return

        if isinstance(self.last_action, ThrowCard):
            # Done
            yaniv.step(EndTurn())
            self.last_action = None
            return


class OptimizedHighCardPlayer(Player):
    """
        Player that always maximizes chance by:
        - Calling yaniv when possible
        - Picking up from pile if card is below 4 points otherwise from deck
        - throwing the set of cards with the most points.
    """
    def step(self, yaniv) -> None:

        # Call Yaniv
        if self.last_action is None and self.get_points() < 6:
            print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")
            action = CallYaniv()
            yaniv.step(action)
            return

        # Pickup
        if self.last_action is None:
            if yaniv.yaniv_round.get_pile_top_card().points < 5:
                action = PickupPileTopCard()
            else:
                action = PickupDeckCard()

            yaniv.step(action)
            self.last_action = action
            return
        
        # Throw
        if isinstance(self.last_action, PickupDeckCard) or isinstance(self.last_action, PickupPileTopCard):
            action = ThrowCard(max(list(self.cards.values()), key=lambda c: c.points).get_index())
            yaniv.step(action)
            self.last_action = action
            return

        if isinstance(self.last_action, ThrowCard):
            # Done
            yaniv.step(EndTurn())
            self.last_action = None
            return

class HighThrowPlayer(Player):
    """
        Player that always maximizes chance by:
        - Calling yaniv when possible
        - Picking up from pile if card is below 4 points otherwise from deck
        - throwing the set of cards with the most points.
    """
    def step(self, yaniv) -> None:

        # Call Yaniv
        if self.last_action is None and self.get_points() < 6:
            print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")
            action = CallYaniv()
            yaniv.step(action)
            return

        # Pickup
        if self.last_action is None:
            if yaniv.yaniv_round.get_pile_top_card().points < 5:
                action = PickupPileTopCard()
            else:
                action = PickupDeckCard()

            yaniv.step(action)
            self.last_action = action
            return
        
        # Throw
        if isinstance(self.last_action, PickupDeckCard) or isinstance(self.last_action, PickupPileTopCard):
            rank_group_points = [(rank, sum([c.points for c in cards])) for rank, cards in groupby(self.cards.values(), lambda x: x.rank)]
            (rank, points), *_ = sorted(rank_group_points, key=lambda x: x[1], reverse=True)

            card, *_ = [c for c in self.cards.values() if c.rank == rank]
            action = ThrowCard(card.get_index())
            yaniv.step(action)
            self.last_action = action
            return

        # Optional: Throw again
        if isinstance(self.last_action, ThrowCard):
            last_thrown_card = yaniv.yaniv_round.get_pile_top_card()
            assert last_thrown_card.get_index() == self.last_action.card_index

            # check if possible to throw another card
            if throw_options := [card for card in self.cards.values() if last_thrown_card.rank == card.rank]:
                action = ThrowCard(throw_options[0].get_index())  # throw first found card
                yaniv.step(action)
                self.last_action = action
                return

        if isinstance(self.last_action, ThrowCard):
            # Done
            yaniv.step(EndTurn())
            self.last_action = None
            return


class RLPLayer(Player):
    """
        Player where actions are taken by an RL Agent.
    """
    pass
