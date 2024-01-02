import logging
from random import choice
from typing import Dict, List, Optional

from rl_yaniv.game.card import YanivCard
from rl_yaniv.game.deck import Deck
from rl_yaniv.game.player import Player
from rl_yaniv.exceptions import DeckException


class YanivRound:

    SUIT_LIST: List[str] = ["S", "H", "D", "C"]
    RANK_LIST: List[str] = [
        "A",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "T",
        "J",
        "Q",
        "K",
    ]
    SUITS_SYMBOLS_UTF_8: List[bin] = [0x1F0D1, 0x1F0C1, 0x1F0B1, 0x1F0A1]
    YANIV_TARGET_POINTS: int = 5  # below or equal can call Yaniv

    def __init__(self, players: Dict[int, Player], last_round_winner: Optional[int] = None) -> None:
        self.logger = logging.getLogger("Round logger")

        self.players = players
        self.last_round_winner = last_round_winner

        self.deck: Deck = Deck.init_54_deck()
        self.dump_pile: List[YanivCard] = []

        self.previous_thrown_cards: List[YanivCard] = []

        self._current_player_id: Optional[int] = None  # starting player is not selected yet

    def deal(self) -> None:
        self.logger.info(f"Dealing 5 cards to each of the {len(self.players)} players")
        for i in range(5):
            for player in self.players.values():
                player.add_card(self.deck.pop_from_deck())

    def start(self) -> None:

        # put first card on the dump pile
        self.dump_pile.append(self.deck.pop_from_deck())

        # select starting player
        if self.last_round_winner is not None:
            self._current_player_id = self.last_round_winner
        else:
            self._current_player_id = choice(list(self.players.values())).player_id
        self.logger.info(f"Player with id {self._current_player_id} starts")

    def draw_deck_card(self) -> None:
        self.logger.info(f"Player with id {self._current_player_id} draws a card from the deck")
        try:
            drawn_card = self.deck.pop_from_deck()
        except DeckException:
            self.logger.info("Deck is empty: reshuffling pile")
            self.deck.cards = self.dump_pile[:-1]
            self.dump_pile = [self.dump_pile[-1]]
            self.deck.shuffle()
            drawn_card = self.deck.pop_from_deck()
        self.get_current_player().add_card(drawn_card)

    def pickup_pile_top_card(self) -> None:
        self.logger.info(f"Player with id {self._current_player_id} draws the dump pile top card")
        picked_card = self.dump_pile.pop(-1 * len(self.previous_thrown_cards))

        self.get_current_player().add_card(picked_card)

    def pickup_pile_bottom_card(self) -> None:
        NotImplementedError

    def throw_card(self, card_index) -> None:
        logging.info(f"Player with id {self._current_player_id} throws {card_index}")
        card = self.get_current_player().cards.pop(card_index)
        self.dump_pile.append(card)
        self.previous_thrown_cards.append(card)

    def yaniv(self) -> Dict[int, int]:
        player_scores = {player_id: player.get_points() for player_id, player in self.players.items()}
        return sorted(player_scores.items(), key=lambda item: item[1])

    def get_pile_top_card(self):
        return self.dump_pile[-1]

    def end_player_turn(self) -> None:
        self.previous_thrown_cards = []
        self.get_current_player().end_turn()
        self._current_player_id = (self._current_player_id + 1) % self.get_num_players()

    def get_current_player_id(self) -> int:
        return self._current_player_id

    def get_current_player(self) -> Player:
        return self.players[self.get_current_player_id()]

    def get_num_players(self) -> int:
        return len(self.players)

    def is_over(self) -> bool:
        return any([player.game_score > self.max_halvation_score for player in self.players])
