
from rl_yaniv.game.actions import (CallYaniv, EndTurn, PickupDeckCard,
                                   PickupPileTopCard, ThrowCard)
from rl_yaniv.game.yaniv import Yaniv

yaniv = Yaniv(num_players=2)
yaniv.reset()
while not yaniv.is_over():
    current_player = yaniv.get_current_player()
    print(f"Current player: {yaniv.get_current_player().player_id}")
    print(f"Pile top card: {yaniv.yaniv_round.get_pile_top_card().get_index()}")
    print("Your cards:")

    for card_index, card in current_player.cards.items():
        print(card_index)

    # Yaniv
    if input("Call YANIV!? YES (1), NO (0)") == '1':
        yaniv.step(CallYaniv())

    # Pickup
    pickup_choice = int(input("Pickup Deck (1) or Pickup Pile Top (2)"))
    if pickup_choice == 1:
        yaniv.step(PickupDeckCard())
    if pickup_choice == 2:
        yaniv.step(PickupPileTopCard())

    # Throw
    end_throw = False
    while not end_throw:
        for card_index, card in current_player.cards.items():
            print(card_index)
        trow_card_index = input("Which card to throw:")
        yaniv.step(ThrowCard(trow_card_index))

        end_throw = (input("End Turn? YES (1), NO (0)") == '1')
    
    yaniv.step(EndTurn())

    for card_index, card in current_player.cards.items():
        print(card_index)

    
    
    