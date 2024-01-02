from abc import ABC, abstractmethod
from collections import OrderedDict
from itertools import groupby
from random import choice, randint
from typing import Iterable, List, Optional

from rl_yaniv.game.actions import (
    Action,
    CallYaniv,
    PickupAction,
    PickupDeckCard,
    PickupPileTopCard,
    ThrowCard,
)
from rl_yaniv.game.card import Card


class Player(ABC):
    def __init__(self, player_id) -> None:
        self.player_id = player_id
        self.cards: OrderedDict[str, Card] = OrderedDict()
        self.game_score: int = 0

        self.previous_actions: List[Action] = []

    def add_card(self, card: Card) -> None:
        self.cards[card.index_number] = card

    def pop_card(self, card_index: int) -> Card:
        return self.cards.pop(card_index)

    def get_points(self) -> int:
        return sum([card.points for card in self.get_cards()])

    def reset(self):
        self.reset_cards()
        self.game_score = 0
        self.previous_actions = []

    def reset_cards(self):
        self.cards = OrderedDict()

    @property
    def last_action(self) -> Optional[Action]:
        if self.previous_actions == []:
            return None
        return self.previous_actions[-1]

    @abstractmethod
    def get_legal_actions(self) -> List[bool]:
        ...

    @abstractmethod
    def step(self, yaniv) -> None:
        ...

    def end_turn(self):
        self.previous_actions = []

    def get_cards(self) -> Iterable[Card]:
        """
        Returns the players list of cards
        """
        return self.cards.values()


class YanivPlayer(Player, ABC):
    def get_legal_actions(self) -> List[Action]:

        legal_actions: List[Action] = []

        if self.last_action is None:
            if self.get_points() < 6:
                # yaniv
                legal_actions.append(CallYaniv())

            # must throw a card from hand
            for card in self.get_cards():
                legal_actions.append(ThrowCard(card))

        elif isinstance(self.last_action, ThrowCard):

            previous_thrown_cards = [a.card for a in self.previous_actions if isinstance(a, ThrowCard)]

            # other of the same rank
            for card in self.get_cards():
                if all([thrown_card.rank == card.rank for thrown_card in previous_thrown_cards]):
                    legal_actions.append(ThrowCard(card))

            for card in self.get_cards():
                if (
                    card.suit == self.last_action.card.suit
                    and card.rank_number == self.last_action.card.rank_number + 1
                ):
                    if (
                        len(previous_thrown_cards) > 1
                        and card.suit == previous_thrown_cards[-2].suit
                        and card.rank_number == previous_thrown_cards[-2].rank_number + 2
                    ):
                        return [ThrowCard(card)]

                    if len(previous_thrown_cards) == 1 and any(
                        [
                            card.suit == other_card.suit and card.rank_number + 1 == other_card.rank_number
                            for other_card in self.get_cards()
                        ]
                    ):
                        legal_actions.append(ThrowCard(card))

            # pickup deck or pile card
            legal_actions += [PickupDeckCard(), PickupPileTopCard()]

        return legal_actions


class RandomPlayer(YanivPlayer):
    """

    Player that
    - Calls Yaniv when possible.
    - Picks up from deck or pile randomly.
    - Trows a random single card.
    """

    def step(self, yaniv) -> None:

        # Call Yaniv
        if self.last_action is None:
            if self.get_points() < 6:
                print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")
                action = CallYaniv()
            else:
                # Throw
                action = ThrowCard(card=choice(list(self.get_cards())))
        # Pickup
        elif isinstance(self.last_action, ThrowCard):
            if randint(0, 1):  # random pickup Deck card or Pile top card
                action = PickupDeckCard()
            else:
                action = PickupPileTopCard()

        yaniv.step(action)
        self.previous_actions.append(action)

        if isinstance(action, PickupAction) or isinstance(action, CallYaniv):
            self.end_turn()


class HighCardPlayer(YanivPlayer):
    """
    Player that always maximizes chance by:
    - Calling yaniv when possible.
    - Picking up from pile if card is below 4 points otherwise from deck.
    - throwing the card with the most points.
    """

    def step(self, yaniv) -> None:

        # Call Yaniv
        if self.last_action is None:
            if self.get_points() < 6:
                # print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")
                action = CallYaniv()
            else:
                # Throw
                action = ThrowCard(card=max(list(self.get_cards()), key=lambda c: c.points))
        # Pickup
        elif isinstance(self.last_action, ThrowCard):
            if yaniv.yaniv_round.get_pile_top_card().points > 4:
                action = PickupDeckCard()
            else:
                action = PickupPileTopCard()

        yaniv.step(action)
        self.previous_actions.append(action)

        if isinstance(action, PickupAction) or isinstance(action, CallYaniv):
            self.end_turn()


class HighThrowPlayer(YanivPlayer):
    """
    Player that always maximizes chance by:
    - Calling yaniv when possible
    - Picking up from pile if card is below 4 points otherwise from deck
    - throwing the set of cards with the most points.
    """

    def step(self, yaniv) -> None:

        # Call Yaniv
        if self.last_action is None:
            if self.get_points() < 6:
                # print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")
                action = CallYaniv()
            else:
                # Throw a card from the equal rank set with the highest total score
                rank_group_points = [
                    (rank, sum([c.points for c in cards]))
                    for rank, cards in groupby(self.get_cards(), lambda x: x.rank)
                ]
                (rank, points), *_ = sorted(rank_group_points, key=lambda x: x[1], reverse=True)

                card, *_ = [c for c in self.get_cards() if c.rank == rank]
                action = ThrowCard(card)

        # Pickup or throw additional card
        elif isinstance(self.last_action, ThrowCard):
            last_thrown_card = self.last_action.card
            if throw_options := [card for card in self.get_cards() if last_thrown_card.rank == card.rank]:
                action = ThrowCard(throw_options[0])  # throw first found card
            elif yaniv.yaniv_round.get_pile_top_card().points > 4:
                action = PickupDeckCard()
            else:
                action = PickupPileTopCard()

        yaniv.step(action)
        self.previous_actions.append(action)

        if isinstance(action, PickupAction) or isinstance(action, CallYaniv):
            self.end_turn()


class RLPLayer(YanivPlayer):
    """
    Player where actions are taken by an RL Agent.
    """

    def __init__(self, player_id) -> None:
        super().__init__(player_id)

        """
        Action indices:
            0: Call Yaniv
            1 - 54: Throw card (Spades (A2-10JQK), Hearts (..), Diamonds (..), Clubs (..), Red Joker, Black Joker) 
            55: Pickup card from deck
            56: Pickup card from pile   
            57: Do nothing because its another agents' turn        
        """

        self.action_space = {
            0: CallYaniv,
            55: PickupDeckCard,
            56: PickupPileTopCard,
        }

    def step(self, yaniv, action_index: int) -> None:

        if action_index > 0 and action_index < 55:
            card = yaniv.yaniv_round.deck.card_from_index_number(action_index - 1)
            action = ThrowCard(card=card)
        else:
            action_class = self.action_space[action_index]
            action = action_class()

        # if action_index == 0:
        #     print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")

        yaniv.step(action)
        self.previous_actions.append(action)

        if isinstance(action, PickupAction) or isinstance(action, CallYaniv):
            self.end_turn()
