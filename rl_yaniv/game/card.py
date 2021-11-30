
from typing import Dict, Optional
from rlcard.games.base import Card

class YanivCard(Card):
    CARD_POINTS: Dict[int, str] = {
    'A': 1 , '2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9,'T': 10,
    'J': 10,'Q': 10,'K': 10
    }

    def __init__(self, suit, rank):
        super().__init__(suit, rank)

        if suit in ['BJ', 'RJ']:
            self.points = 0
        else:
            self.points = self.CARD_POINTS[rank]

        self.rank_number = self.get_rank_number()

    def get_rank_number(self) -> Optional[int]:
        """Returns the index number of a card in the card ranking."""
        if self.rank:
            return list(self.CARD_POINTS.keys()).index(self.rank)
        else: 
            return None
