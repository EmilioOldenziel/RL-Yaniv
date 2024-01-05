# RL-Yaniv

The game of Yaniv implemented as a Gymnasium environment to be used for Reinforcement Learning.
Ray RLLib is used for training agents using PPO. ParametricActions are used for action embeddings.

## Game

The goal is to win a round by getting to 5 points or less and call Yaniv.

| Card Rank | Points Value |
|--|--|
| Joker  | 0 |
| Ace    | 1 |
| 2-10   | same as card |
| Face Card  | 10 |

- Traditional Imperfect information game
- Non-deterministic
- 2-6 players

## Deck

- Deck type (52 card deck, 54 card deck with 2 jokers)
- Open/Closed Deck

### Card
- Suit (♠♥♦♣)
- Rank (A23456789TJQK)
- Points
- Cardinality
- Unicode

## Events/Moves
Moves that a player can take in a turn
- Call Yaniv
- Throw a card on the pile
- Pickup a card from the top of the deck
- Pickup a card from the top of the pile
- End its turn

## Implementation
The game is implemented in pure Python (no dependencies), it is wrapped to a environment encoding

## Actions
```
0: Call Yaniv (if 5 point or lower)
1 - 54: Throw card 
    Spades (A2-10JQK), 
    Hearts (..),
    Diamonds (..),
    Clubs (..),
53: Throw Red Joker
54: Throw Black Joker
55: Pickup card from deck
56: Pickup card from pile
57: End turn
```

## Observations

`Box(2, 56)` Binary masks
- The player's cards
- Card on top of the pile (1-Hot)
- 