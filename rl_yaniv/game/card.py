from typing import Dict, Optional

from rlcard.games.base import Card


class YanivCard(Card):
    CARD_POINTS: Dict[int, str] = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "T": 10,
        "J": 10,
        "Q": 10,
        "K": 10,
    }

    def __init__(self, suit, rank, index_number: int = None):
        super().__init__(suit, rank)

        if suit in ["BJ", "RJ"]:
            self.points = 0
        else:
            self.points = self.CARD_POINTS[rank]

        self.rank_number = self._get_rank_number()
        self.index_number = index_number  # unique integer

    def _get_rank_number(self) -> Optional[int]:
        """Returns the index number of a card in the card ranking based on points."""
        if self.rank:
            return list(self.CARD_POINTS.keys()).index(self.rank)
        else:
            return None

    def render(self):

        if self.suit in ["BJ", "RJ"]:
            return "🃏"

        card_dict = {
            "SA": "🂡",
            "S2": "🂢",
            "S3": "🂣",
            "S4": "🂤",
            "S5": "🂥",
            "S6": "🂦",
            "S7": "🂧",
            "S8": "🂨",
            "S9": "🂩",
            "ST": "🂪",
            "SJ": "🂫",
            "SQ": "🂭",
            "SK": "🂮",
            "HA": "🂱",
            "H2": "🂲",
            "H3": "🂳",
            "H4": "🂴",
            "H5": "🂵",
            "H6": "🂶",
            "H7": "🂷",
            "H8": "🂸",
            "H9": "🂹",
            "HT": "🂺",
            "HJ": "🂻",
            "HQ": "🂽",
            "HK": "🂾",
            "DA": "🃁",
            "D2": "🃂",
            "D3": "🃃",
            "D4": "🃄",
            "D5": "🃅",
            "D6": "🃆",
            "D7": "🃇",
            "D8": "🃈",
            "D9": "🃉",
            "DT": "🃊",
            "DJ": "🃋",
            "DQ": "🃍",
            "DK": "🃎",
            "CA": "🃑",
            "C2": "🃒",
            "C3": "🃓",
            "C4": "🃔",
            "C5": "🃕",
            "C6": "🃖",
            "C7": "🃗",
            "C8": "🃘",
            "C9": "🃙",
            "CT": "🃚",
            "CJ": "🃛",
            "CQ": "🃝",
            "CK": "🃞",
        }

        return card_dict[self.get_index()]
