
from abc import ABC


class Action(ABC):
    pass

class CallYaniv(Action):
    pass

class PickupDeckCard(Action):
    pass

class PickupPileTopCard(Action):
    pass

class ThrowCard(Action):
    def __init__(self, card_index: int) -> None:
        super().__init__()
        
        self.card_index = card_index

class EndTurn(Action):
    pass
