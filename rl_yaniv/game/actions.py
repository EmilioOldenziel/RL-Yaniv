
from abc import ABC


class Action(ABC):

    def __str__(self) -> str:
        return str(self.__class__.__name__)

class CallYaniv(Action):
    pass


class PickupAction(Action):
    pass

class PickupDeckCard(PickupAction):
    pass

class PickupPileTopCard(PickupAction):
    pass

class ThrowCard(Action):
    def __init__(self, card_index: str) -> None:
        super().__init__()

        self.card_index = card_index

    def __str__(self) -> str:
        return f"{super().__str__()}_{self.card_index}"

class EndTurn(Action):
    pass
