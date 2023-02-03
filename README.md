# RL-Yaniv

The game of Yaniv implemented as a Gymnasium environment to be used for Reinforcement Learning.
Ray RLLib is used for training agents using PPO. ParametricActions are used for action embeddings.

## Deck

- Deck type (52 card deck, 54 card deck)
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

## Actions
```
0: Call Yaniv
1 - 54: Throw card 
    Spades (A2-10JQK), 
    Hearts (..),
    Diamonds (..),
    Clubs (..),
    Red Joker, 
    Black Joker
55: Pickup card from deck
56: Pickup card from pile
57: End turn
```

## Observations

