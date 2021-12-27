from abc import ABC, abstractmethod
from collections import OrderedDict
from itertools import groupby
from random import choice, randint
from typing import List, Optional

from rl_yaniv.game.actions import (Action, CallYaniv, PickupAction,
                                   PickupDeckCard, PickupPileTopCard,
                                   ThrowCard)
from rl_yaniv.game.card import Card


class Player(ABC):
    
    def __init__(self, player_id) -> None:
        self.player_id = player_id
        self.cards: OrderedDict[str, Card] = OrderedDict()
        self.game_score: int = 0

        self.previous_actions: List[Action] = []

    def add_card(self, card: Card) -> None:
        self.cards[card.index_number] = card

    def get_points(self) -> int:
        return sum([card.points for card in self.cards.values()])

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

class YanivPlayer(Player):

    def __init__(self, player_id) -> None:
        super().__init__(player_id)
        self.last_valid_actions: Optional[List[bool]] = None

    def get_legal_actions(self) -> List[bool]:

        action_mask = [False] * 58

        if self.last_action is None:
            # yaniv
            action_mask[0] = True

            # must throw a card from hand
            for card in self.cards.values():
                action_mask[card.index_number + 1] = True

        elif isinstance(self.last_action, ThrowCard):
            # other of the same rank
            for card in self.cards.values():
                if self.last_action.card_index == card.index_number:
                    action_mask[card.index_number + 1] = True

            # pickup deck or pile card
            action_mask[55:56] = True
        
        return action_mask


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
                action = ThrowCard(choice(list(self.cards.keys())))
        # Pickup
        elif isinstance(self.last_action, ThrowCard):
            pickup_choice = randint(1,2)
            if pickup_choice == 1:
                action = PickupDeckCard()
            if pickup_choice == 2:
                action = PickupPileTopCard()
        
        yaniv.step(action)
        self.previous_actions.append(action)

        if isinstance(action, PickupAction) or isinstance(action, CallYaniv):
            self.end_turn()

# class HighCardPlayer(YanivPlayer):
#     """
#         Player that always maximizes chance by:
#         - Calling yaniv when possible.
#         - Picking up from pile if card is below 4 points otherwise from deck.
#         - throwing the card with the most points.
#     """
#     def step(self, yaniv) -> None:

#         # Call Yaniv
#         if self.last_action is None:
#             if self.get_points() < 6:
#                 print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")
#                 action = CallYaniv()
#                 yaniv.step(action)
#                 return

#         # Pickup
#         if self.last_action is None:
#             pickup_choice = randint(1,2)
#             if pickup_choice == 1:
#                 action = PickupDeckCard()
#             if pickup_choice == 2:
#                 action = PickupPileTopCard()
#             yaniv.step(action)
#             self.last_action = action
#             return
        
#         # Throw
#         if isinstance(self.last_action, PickupDeckCard) or isinstance(self.last_action, PickupPileTopCard):
#             action = ThrowCard(max(list(self.cards.values()), key=lambda c: c.points).index_number)
#             yaniv.step(action)
#             self.last_action = action
#             return

#         if isinstance(self.last_action, ThrowCard):
#             # Done
#             yaniv.step(EndTurn())
#             self.last_action = None
#             return


# class OptimizedHighCardPlayer(YanivPlayer):
#     """
#         Player that always maximizes chance by:
#         - Calling yaniv when possible
#         - Picking up from pile if card is below 4 points otherwise from deck.
#         - throwing the set of cards with the most points.
#     """
#     def step(self, yaniv) -> None:

#         # Call Yaniv
#         if self.last_action is None and self.get_points() < 6:
#             print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")
#             action = CallYaniv()
#             yaniv.step(action)
#             return

#         # Pickup
#         if self.last_action is None:
#             if yaniv.yaniv_round.get_pile_top_card().points < 5:
#                 action = PickupPileTopCard()
#             else:
#                 action = PickupDeckCard()

#             yaniv.step(action)
#             self.last_action = action
#             return
        
#         # Throw
#         if isinstance(self.last_action, PickupDeckCard) or isinstance(self.last_action, PickupPileTopCard):
#             action = ThrowCard(max(list(self.cards.values()), key=lambda c: c.points).index_number)
#             yaniv.step(action)
#             self.last_action = action
#             return

#         if isinstance(self.last_action, ThrowCard):
#             # Done
#             yaniv.step(EndTurn())
#             self.last_action = None
#             return

# class HighThrowPlayer(YanivPlayer):
#     """
#         Player that always maximizes chance by:
#         - Calling yaniv when possible
#         - Picking up from pile if card is below 4 points otherwise from deck
#         - throwing the set of cards with the most points.
#     """
#     def step(self, yaniv) -> None:

#         # Call Yaniv
#         if self.last_action is None and self.get_points() < 6:
#             print(f"Player {self.player_id} calls Yaniv: {self.get_points()}")
#             action = CallYaniv()
#             yaniv.step(action)
#             return

#         # Pickup
#         if self.last_action is None:
#             if yaniv.yaniv_round.get_pile_top_card().points < 5:
#                 action = PickupPileTopCard()
#             else:
#                 action = PickupDeckCard()

#             yaniv.step(action)
#             self.last_action = action
#             return
        
#         # Throw
#         if isinstance(self.last_action, PickupDeckCard) or isinstance(self.last_action, PickupPileTopCard):
#             rank_group_points = [(rank, sum([c.points for c in cards])) for rank, cards in groupby(self.cards.values(), lambda x: x.rank)]
#             (rank, points), *_ = sorted(rank_group_points, key=lambda x: x[1], reverse=True)

#             card, *_ = [c for c in self.cards.values() if c.rank == rank]
#             action = ThrowCard(card.index_number)
#             yaniv.step(action)
#             self.last_action = action
#             return

#         # Optional: Throw again
#         if isinstance(self.last_action, ThrowCard):
#             last_thrown_card = yaniv.yaniv_round.get_pile_top_card()
#             assert last_thrown_card.index_number == self.last_action.card_index

#             # check if possible to throw another card
#             if throw_options := [card for card in self.cards.values() if last_thrown_card.rank == card.rank]:
#                 action = ThrowCard(throw_options[0].index_number)  # throw first found card
#                 yaniv.step(action)
#                 self.last_action = action
#                 return

#         if isinstance(self.last_action, ThrowCard):
#             # Done
#             yaniv.step(EndTurn())
#             self.last_action = None
#             return


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
            57: Do nothing because its an other agents' turn        
        """

        self.action_space = {
             0: CallYaniv,
             55: PickupDeckCard,
             56: PickupPileTopCard,
        }

    def step(self, yaniv, action_index: int) -> None:

        if action_index == 57:
            return

        if action_index > 0 and action_index < 55:
            card_index = yaniv.yaniv_round.deck.card_index_num2str(action_index - 1)
            action = ThrowCard(card_index=card_index)
        else:
            action_class = self.action_space[action_index]
            action = action_class()

        yaniv.step(action)
        self.previous_actions.append(action)
