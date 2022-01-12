from abc import ABC

from rl_yaniv.game.card import Card

class Action(ABC):

    def __str__(self) -> str:
        return str(self.__class__.__name__)

    def __eq__(self, other):
        if (isinstance(other, self.__class__)):
            return True

class CallYaniv(Action):
    pass


class PickupAction(Action):
    pass

class PickupDeckCard(PickupAction):
    pass

class PickupPileTopCard(PickupAction):
    pass

class ThrowCard(Action):
    def __init__(self, card: Card) -> None:
        super().__init__()

        self.card = card

    def __eq__(self, other):
        if isinstance(other, ThrowCard):
            return self.card.card_index == other.card.card_index
        else:
            # don't attempt to compare against unrelated types
            return NotImplemented

    def __str__(self) -> str:
        return f"{super().__str__()}_{self.card.card_index}"

class DoNothing(Action):
    pass

class EndTurn(Action):
    pass
