import random

card_enhancement_array = ["Wild", "Bonus", "Multi", "Glass", "Steel", "Stone", "Gold", "Lucky"]
card_editions_array = ["Foil", "Holographic", "Polychrome"]
card_seals_array = ["Red", "Blue", "Purple", "Yellow"]
boss_blinds_array = ["The Plant", "The Beast", "The Machine", "The Spirit", "The Wall"]

def deckArray():
    card_deck = [[''] * 5 for _ in range(52)]

    ranks_array = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits_array = ["Clubs", "Diamonds", "Hearts", "Spades"]
    
    for i in range(len(card_deck)):
        card_deck[i][0] = ranks_array[i % 13]
        card_deck[i][1] = suits_array[i % 4]
        # now we need to add enhancements, editions, and seals to the cards
        card_deck[i][2] = "Base"
        card_deck[i][3] = "Base"
        card_deck[i][4] = "Base"
        
    return card_deck
    

def shuffle_array(card_deck):
    random_generator = random.Random()
    for i in range(len(card_deck)):
        random_int = random_generator.randint(0, len(card_deck) - 1)
        card_deck[i], card_deck[random_int] = card_deck[random_int], card_deck[i]
    return card_deck

def hand_input_valid(card_selection):
    is_valid = True

    if len(card_selection) == 0 or len(card_selection) > 5 or card_selection[0] == "":
        is_valid = False

    for i in range(len(card_selection)):
        for j in range(i + 1, len(card_selection)):
            if card_selection[i] == card_selection[j]:
                is_valid = False

        if card_selection[i] not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            is_valid = False

    return is_valid

def detect_hand(card_selection):
    """
    Detects the type of hand in a given set of cards.
    
    Args:
        card_selection (list[list[str]]): A list of lists, where each inner list represents a card with its rank and suit.
    
    Returns:
        str: The type of hand detected.
    """
    # Set up collection of ranks of played hand 
    # if Stone enhancement is present, set rank_array to NONE to indicate that the card is not part of any rank
    if "Stone" in [card[2] for card in card_selection]:
        rank_array = ["NONE" for card in card_selection]
    else:
        rank_array = [card[0] for card in card_selection]
    
    
    # Sort ranks in a new array rank_sorted
    rank_list = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    rank_sorted = []
    counter = 0
    for rank in rank_list:
        for i in range(len(rank_array)):
            if rank_array[i] == rank:
                rank_sorted.append(rank)
                counter += 1
    
    # Convert rank_sorted to int_array
    int_array = []
    for rank in rank_sorted:
        if rank == "A":
            int_array.append(1)
        elif rank == "J":
            int_array.append(11)
        elif rank == "Q":
            int_array.append(12)
        elif rank == "K":
            int_array.append(13)
        else:
            int_array.append(int(rank))
    
    # Set up collection of suits of played hand if there is no wild card enhancement present
    # If there is a wild card enhancement present, set the suit of that card be considered as every suit simultaneously
    if "Wild" in [card[2] for card in card_selection]:
        suit_array = ["Wild" for card in card_selection]
    # If there is a stone card enhancement present, set suit_array to NONE to indicate that the card is not part of any suit
    elif "Stone" in [card[2] for card in card_selection]:
        suit_array = ["NONE" for card in card_selection]
    else:
        suit_array = [card[1] for card in card_selection]
    
    # Check if the hand is a flush
    is_flush = True
    for i in range(len(suit_array) - 1):
        if suit_array[i] != suit_array[i + 1]:
            is_flush = False
            break
        # If there is a wild card enhancement present, set the suit of that card be considered as every suit simultaneously
        elif suit_array[i] != "Wild" or suit_array[i + 1] != "Wild":
            is_flush = False
            break
    if len(card_selection) < 5:
        is_flush = False
    
    # Check if the hand is a straight
    is_straight = True
    for i in range(len(rank_array)):
        for j in range(i + 1, len(rank_array)):
            if rank_array[i] == rank_array[j]:
                is_straight = False
    
    if len(card_selection) < 5:
        is_straight = False
    else:
        # Check if each number is one larger than previous
        for k in range(len(card_selection) - 1):
            if int_array[k] != int_array[k + 1] - 1:
                is_straight = False
        
        # Check for edge case 10 J Q K A
        if int_array[0] == 1 and int_array[1] == 10 and int_array[2] == 11 and int_array[3] == 12 and int_array[4] == 13:
            is_straight = True
    
    # Check if there are duplicates of ranks
    current_streak = 1
    set_info = [0, 0, 0]
    for i in range(len(rank_sorted) - 1):
        if rank_sorted[i] == rank_sorted[i + 1]:
            current_streak += 1
        else:
            current_streak = 1
        
        if current_streak == 2:
            set_info[0] += 1
        elif current_streak == 3:
            set_info[1] += 1
        elif current_streak == 4:
            set_info[2] += 1
    
    # Determine the type of hand
    if is_flush and is_straight:
        return "Straight Flush"
    elif set_info[0] == 1 and set_info[1] == 1 and set_info[2] == 1:
        return "Four of a Kind"
    elif set_info[0] == 2 and set_info[1] == 1 and set_info[2] == 0:
        return "Full House"
    elif is_flush:
        return "Flush"
    elif is_straight:
        return "Straight"
    elif set_info[0] == 1 and set_info[1] == 1 and set_info[2] == 0:
        return "Three of a Kind"
    elif set_info[0] == 2 and set_info[1] == 0 and set_info[2] == 0:
        return "Two Pair"
    elif set_info[0] == 1 and set_info[1] == 0 and set_info[2] == 0:
        return "Pair"
    else:
        return "High Card"

def score_hand_chips(hand_type, played_hand):
    chips = 0

    # Sort ranks in a new list ranks_sorted
    ranks_list = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    ranks_sorted = []
    counter = 0
    for rank in ranks_list:
        for card in played_hand:
            if card[0] == rank:
                ranks_sorted.append(rank)
                counter += 1
            # If there is a stone card enhancement present, set ranks_sorted to NONE to indicate that the card is not part of any rank
            elif card[2] == "Stone":
                ranks_sorted.append("NONE")
                counter += 1


    # Convert ranks_sorted to played_hand_int
    played_hand_int = []
    for rank in ranks_sorted:
        if rank == "A":
            played_hand_int.append(11)
        elif rank == "J":
            played_hand_int.append(10)
        elif rank == "Q":
            played_hand_int.append(10)
        elif rank == "K":
            played_hand_int.append(10)
        else:
            played_hand_int.append(int(rank))

    # Calculate the chip gain per hand
    if hand_type == "Straight Flush":
        chips += 100
        chips += sum(played_hand_int)
    elif hand_type == "Four of a Kind":
        chips += 60
        if ranks_sorted[0] == ranks_sorted[1]:
            chips += sum(played_hand_int[:4])
        else:
            chips += sum(played_hand_int[1:5])
    elif hand_type == "Full House":
        chips += 40
        chips += sum(played_hand_int)
    elif hand_type == "Flush":
        chips += 35
        chips += sum(played_hand_int)
    elif hand_type == "Straight":
        chips += 30
        chips += sum(played_hand_int)
    elif hand_type == "Three of a Kind":
        chips += 30
        if ranks_sorted[0] == ranks_sorted[1]:
            chips += sum(played_hand_int[:3])
        elif ranks_sorted[1] == ranks_sorted[2]:
            chips += sum(played_hand_int[1:4])
        else:
            chips += sum(played_hand_int[2:5])
    elif hand_type == "Two Pair":
        chips += 20
        if ranks_sorted[0] == ranks_sorted[1] and ranks_sorted[2] == ranks_sorted[3]:
            chips += sum(played_hand_int[:4])
        elif ranks_sorted[1] == ranks_sorted[2]:
            chips += sum(played_hand_int[1:5])
        else:
            chips += played_hand_int[0] + played_hand_int[1] + played_hand_int[3] + played_hand_int[4]
    elif hand_type == "Pair":
        chips += 10
        if ranks_sorted[0] == ranks_sorted[1]:
            chips += played_hand_int[0] + played_hand_int[1]
        elif ranks_sorted[1] == ranks_sorted[2]:
            chips += played_hand_int[1] + played_hand_int[2]
        elif ranks_sorted[2] == ranks_sorted[3]:
            chips += played_hand_int[2] + played_hand_int[3]
        else:
            chips += played_hand_int[3] + played_hand_int[4]
    # If there is a stone card enhancement present in played hand, +50 chips to the total chips for every stone card present
    
    elif "Stone" in [card[2] for card in played_hand]:
        chips += 50 * [card[2] for card in played_hand].count("Stone")
    else:
        chips += 5
        chips += max(played_hand_int)
        
    # If there is a Foil edition present in played hand, +30 chips to the total chips
    if "Foil" in [card[3] for card in played_hand]:
        chips += 50
    

    return chips

def score_hand_multi(hand_type, played_hand):
    Multi = 0
    
    if hand_type == "Straight Flush":
        Multi = 8
    elif hand_type == "Four of a Kind":
        Multi = 7
    elif hand_type == "Full House":
        Multi = 4
    elif hand_type == "Flush":
        Multi = 4
    elif hand_type == "Straight":
        Multi = 4
    elif hand_type == "Three of a Kind":
        Multi = 3
    elif hand_type == "Two Pair":
        Multi = 2
    elif hand_type == "Pair":
        Multi = 2
    else:
        Multi = 1
        
    # If there is a Holographic edition present in played hand, +10 mult to the total mult for every Holographic card present
    if "Holographic" in [card[3] for card in played_hand]:
        Multi += 10 * [card[3] for card in played_hand].count("Holographic")
    # if there is a Polychrome edition present in played hand, x1.5 mult to the total mult for every Polychrome card present
    elif "Polychrome" in [card[3] for card in played_hand]:
        Multi *= 1.5 * [card[3] for card in played_hand].count("Polychrome")
    
    return Multi

def toString1DArray(array):
    str1DArray = "{"
    
    for i in range(len(array)):
        str1DArray += array[i]
        
        if i != len(array) - 1:
            str1DArray += ", "
    
    str1DArray += "}"
    return str1DArray

def toString2DArray(array):
    str2DArray = "{"
    
    for i in range(len(array)):
        str2DArray += toString1DArray(array[i])
        
        if i != len(array) - 1:
            str2DArray += ", "
    
    str2DArray += "}"
    return str2DArray

def hand_input_valid(card_selection):
    is_valid = True

    if len(card_selection) == 0 or len(card_selection) > 5 or card_selection[0] == "":
        is_valid = False

    for i in range(len(card_selection)):
        for j in range(i + 1, len(card_selection)):
            if card_selection[i] == card_selection[j]:
                is_valid = False

        if card_selection[i] not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            is_valid = False

    return is_valid

def set_boss_blind_for_current_level():
    # Set the boss blind for the current level by randomly selecting a boss blind from the boss_blinds_array but not repeating until all have been used
    boss_blind = random.choice(boss_blinds_array)
    if len(boss_blinds_array) == 0:
        boss_blinds_array.extend(["The Plant", "The Beast", "The Machine", "The Spirit", "The Wall"])
    boss_blinds_array.remove(boss_blind)
    return boss_blind

def change_blind_chips_depending_on_current_ante(blind_chips,current_ante, current_blind):
    # Change the blind chips depending on the current ante and blind
    if current_ante == 1:
        if current_blind == "Small blind":
            blind_chips = 300
        elif current_blind == "Big blind":
            blind_chips = 450
        else:
            blind_chips = 600
            
    elif current_ante == 2:
        if current_blind == "Small blind":
            blind_chips = 800
        elif current_blind == "Big blind":
            blind_chips = 1050
        else:
            blind_chips = 1300
    
    return blind_chips
    
    

# Main Game Loop

    
main_deck = shuffle_array(deckArray())
main_hand = [[''] * 2 for _ in range(8)]
top_deck = 0

# Game variables to keep track of game state and player progress on the first round

hands_remaining = 4
discards_remaining = 3

total_chips = 0
blind_chips = 300
rounds_played= 0

ante_level = 1
current_money = 3

current_blind = "Small blind"
boss_blind = set_boss_blind_for_current_level()

# Draw initial hand of cards
for i in range(8):
    main_hand[i] = main_deck[top_deck]
    top_deck += 1

while ante_level <= 2:
    
    rounds_played += 1

    while total_chips < blind_chips:
        
        # if not in boss blind, show currend blind 
        
        if current_blind == "Small blind":
            print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
            print("Small Blind!")
            print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
        elif current_blind == "Big blind":
            print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
            print("Big Blind!")
            print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
        # If in boss blind, activate the current boss blind if the player has played a hand and apply the effect
        
        if current_blind == "Boss blind":
            print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
            print("Boss Blind!")
            # The plant effect sets your number of hands remaining to 1
            if boss_blind == "The Plant":
                hands_remaining = 2
                print("The Plant has activated! You have 2 hands remaining!")
            # The beast effect sets your number of discards remaining to 1
            elif boss_blind == "The Beast":
                discards_remaining = 1
                print("The Beast has activated! You have 1 discard remaining!")
            # The machine effect reduces your scored chips by exactly 50 points every hand played
            elif boss_blind == "The Machine":
                print("The Machine has activated! Your chips will be reduced by 25 each hand you play!")
            # The spirit effect sets your scored mult by exactly 5 points every hand played
            elif boss_blind == "The Spirit":
                print("The Spirit has activated! Your mult will be reduced by 5 each hand you play!")
            elif boss_blind == "The Wall":
                print("The Wall has activated! Your currend score blind required has been increase!")
                blind_chips *= 1.3
            
            
        
            
        # Tell user blind goal + current total chips scored
        print("|---------------------------------------------------------------|")
        print(f"Score at least {blind_chips} to go to the next round and earn money!")
        print(f"Current Round score: {total_chips}")
        print(f"\n{{Current Hands: {hands_remaining}}}   {{Current Discards: {discards_remaining}}}")
        print("|---------------------------------------------------------------|")

        # Display current hand
        print("\nCurrent hand: ")
        for card in main_hand:
            # Display card rank and suit, and enhancements, editions, and seals if they are not "Base"
            if card[2] != "Base":
                enhance_string = f" [{card[2]}]"
            else:
                enhance_string = ""
            
            if card[3] != "Base":
                edition_string = f" [{card[3]}]"
            else:
                edition_string = ""
                
            if card[4] != "Base":
                seal_string = f" [{card[4]}]"
            else:
                seal_string = ""
            
            print(f"[{card[0]} of {card[1]}{enhance_string}{edition_string}{seal_string}]", end=" ")
            
                

        # Ask user to pick cards from hand
        print("\n\nPick cards from hand! (Enter hand positions of cards separated by spaces, ex. \"1 2 3 4 5\")")
        card_selection = input().split()

        # Input failsafe
        while True:
            if hand_input_valid(card_selection):
                break
            print("Hand invalid, try again!")
            card_selection = input().split()

        # Build the hand array for scoring
        hand_selected = [[main_hand[int(i) - 1][0], main_hand[int(i) - 1][1], main_hand[int(i) - 1][2], main_hand[int(i) - 1][3], main_hand[int(i) - 1][4]] for i in card_selection]

        # Ask user if this hand is to be played or discarded
        while True:
            print("\nType \"Play\" to play hand, type \"Discard\" to discard hand.")
            play_or_discard = input()
            if play_or_discard == "Play":
                # Score the hand and add to total chips
                
                current_chips = score_hand_chips(detect_hand(hand_selected), hand_selected)
                current_mult = score_hand_multi(detect_hand(hand_selected), hand_selected)
                
                if boss_blind == "The Machine" and current_blind == "Boss blind":
                    print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                    print("Affected by The Machine!")
                    print("Reduced by 50 chips!")
                    print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                    if current_chips >= 50:
                        current_chips -= 50
                    else:
                        current_chips = 0
                elif boss_blind == "The Spirit" and current_blind == "Boss blind":
                    print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                    print("Affected by The Spirit!")
                    print("Reduced by 5 mult!")
                    print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                    if current_mult >= 5:
                        current_mult -= 5
                    else:
                        current_mult = 0
                
                print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                print("Played " + detect_hand(hand_selected) + "!")
                print("[" + str(current_chips) + "] X [" + str(current_mult) + "] = " + str(current_chips * current_mult) + " chips")
                print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                
                total_chips += current_chips * current_mult
                
                
                
                hands_remaining -= 1
                break
            elif play_or_discard == "Discard":
                # Skip scoring cards and decrement number of Discards remaining (check if number of discards is 0 first)
                if discards_remaining == 0:
                    print("No discards remaining!")
                else:
                    print("\n{~~~~~~~~~~~~}")
                    print("Discarded!")
                    print("{~~~~~~~~~~~~}\n")
                    
                    discards_remaining -= 1
                    break
            else:
                print("Invalid format!")
        
        # End game if hands remaining hit 0
        if hands_remaining == 0:
            print("\nYOU LOSE!")
            exit()

        # Set the used cards to "Played!" string
        for i in range(len(card_selection)):
            main_hand[int(card_selection[i]) - 1][0] = "Played!"

        # Replace "Played!" in hand with new cards
        for i in range(len(main_hand)):
            if main_hand[i][0] == "Played!":
                main_hand[i] = main_deck[top_deck]
                top_deck += 1
                
        

        
    jimbo = random.Random()
    jimbo_win = ["You Aced it!", "Too bad these chips are all virtual...", "Good thing I didn't bet against you!", "You dealt with that pretty well!"]
    jimbo_lose = ["Maybe Go Fish is more our speed...", "I'm literally a fool, what's your excuse?", "Oh no, were you bluffing too?", "You know what they say, the house always wins!"]

    if total_chips >= blind_chips:
        # Win round if total chips is greater than or equal to blind chips of the actual blind level
        
        print("\nYOU WIN!")
        print("Final Round Score:", total_chips)

        # Money earned by current blind
        if current_blind == "Small blind":
            print("You earned $3!")
            current_money += 3
        elif current_blind == "Big blind":
            print("You earned $4!")
            current_money += 4
        else:
            # Boss blind
            print("You earned $5!")
            current_money += 5
        # If player had 1 or more hands remaining, give bonus money, $1 per hand remaining
        if hands_remaining > 0:
            print(f"You earned ${hands_remaining} bonus for having {hands_remaining} hands remaining!")
            current_money += hands_remaining
        print("Total Money held: ", current_money)
        print("Rounds played: ", rounds_played)
        print("Jimbo says:", jimbo_win[jimbo.randint(0, 3)])
    else:
        # End game if total chips is less than blind chips
        
        print("\nYOU LOSE!")
        print("Final Round Score:", total_chips)
        print("Jimbo says:", jimbo_lose[jimbo.randint(0, 3)])
        break

    # Reset round variables
    total_chips = 0
    hands_remaining = 4
    discards_remaining = 3
    
    # Change the blind level, if small blind, go to big blind, if big blind, go to boss blind, if boss blind, go to small blind again and increase ante level and change boss blind effect
    
    if current_blind == "Small blind":
        current_blind = "Big blind"
    elif current_blind == "Big blind":
        current_blind = "Boss blind"
    else:
        boss_blind = set_boss_blind_for_current_level()
        current_blind = "Small blind"
        ante_level += 1
    
    blind_chips = change_blind_chips_depending_on_current_ante(blind_chips,ante_level, current_blind)
    
    # Show progress of the current ante level, blind level and boss blind effect
    print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
    print(f"Ante Level: {ante_level}")
    print(f"Next Blind: {current_blind}")
    # Print boss blind effect
    print(f"Boss Blind: {boss_blind}")
    print(f"Next Round Score: {blind_chips}")
    print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
    
    shop_choice = ""
    
    # Show Shop and ask if player wants to buy enhancements, editions, or seals, if not, skip the shop and go to the next blind level
    # Keep the shop active until the player has no money left or the player chooses to skip the shop
    while current_money > 0 and shop_choice != "No":
        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
        print("Welcome to the Shop!")
        print("Would you like to buy enhancements, editions, or seals?")
        print("Type \"Yes\" to enter the shop, type \"No\" to skip the shop.")
        shop_choice = input()
        print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
        
        # If player chooses to enter the shop, show the shop and ask player to buy enhancements, editions, or seals
        if shop_choice == "Yes":
            # Show the shop and ask the player to buy booster backs
            # These booster packs will contain enhancements, editions, and seals at random
            # When a booster pack of any type is bought, the player will draw 8 cards from the main deck at random
            # The player will then be able to choose 1 card to change the enhancement, edition, or seal from the 8 cards drawn
            # Then the player will return all the cards to the main deck and shuffle the main deck again
            # If another booster pack is bought, the player will draw 8 cards from the main deck again and repeat the process
            # If the player chooses to skip the shop, the player will go to the next blind level
            # If the player has no money left, the player will go to the next blind level
            # Enhancement booster pack costs $3
            # Edition booster pack costs $4
            # Seal booster pack costs $5
            while True:
                print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                print("Enhancement Booster Pack: $3")
                print("Edition Booster Pack: $4")
                print("Seal Booster Pack: $5")
                print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                print("Current Money: ", current_money)
                print("Enter the type of booster pack you would like to buy or type \"No\" to skip the shop! (Enter the type of booster pack, ex. \"Enhancement\"")
                
                booster_pack_choice = input()
                
                # If player chooses to buy an enhancement booster pack
                if booster_pack_choice == "Enhancement":
                    if current_money >= 3:
                        current_money -= 3
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Bought Enhancement Booster Pack!")
                        print("Current Money: ", current_money)
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                        booster_pack = [[""] * 5 for _ in range(8)]
                        for i in range(8):
                            booster_pack[i] = main_deck[top_deck]
                            top_deck += 1
                            
                        print("Cards drawn: ")
                        for card in booster_pack:
                            # Show the 8 cards drawn from the booster pack var into main hand

                            print(f"[{card[0]} of {card[1]}]", end=" ")
                            
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        # Show 3 random enhancements
                        print("Enhancements: ")
                        for i in range(3):
                            print(f"{i + 1}. {card_enhancement_array[i]}")
                        # Ask player to pick a card from the booster pack to change the enhancement
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("\n\nPick a card from the booster pack to change the enhancement! (Enter hand position of card, ex. \"1\")")
                        card_selection = input()
                        # Input failsafe
                        while True:
                            if card_selection in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                                break
                            print("Hand invalid, try again!")
                            card_selection = input()
                        # Ask the player to pick an enhancement to change the card to
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Enter the enhancement you would like to change the card to with the options shown! [Wild, Bonus, etc.]")
                        enhance_selection = input()
                        # Input failsafe
                        while True:
                            if enhance_selection in card_enhancement_array:
                                break
                            print("Enhancement invalid, try again!")
                            enhance_selection = input()
                        # Change the enhancement of the card using the function change_enhancement_single_card_by_player
                        booster_pack[int(card_selection) - 1][2] = enhance_selection
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Changed enhancement!")
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                        # Return the booster pack to the main deck and shuffle the main deck
                        for i in range(8):
                            main_deck.append(booster_pack[i])
                        main_deck = shuffle_array(main_deck)
                        break
                    else:
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Not enough money!")
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                        break
                
                # If player chooses to buy an edition booster pack
                elif booster_pack_choice == "Edition":
                    if current_money >= 4:
                        current_money -= 4
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Bought Edition Booster Pack!")
                        print("Current Money: ", current_money)
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                        booster_pack = [[""] * 5 for _ in range(8)]
                        for i in range(8):
                            booster_pack[i] = main_deck[top_deck]
                            top_deck += 1
                        print("Cards drawn: ")
                        for card in booster_pack:

                            print(f"[{card[0]} of {card[1]}]", end=" ")
                            
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        # Show 3 random editions
                        print("Editions: ")
                        for i in range(3):
                            print(f"{i + 1}. {card_editions_array[i]}")
                        # Ask player to pick a card from the booster pack to change the edition
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("\n\nPick a card from the booster pack to change the edition! (Enter hand position of card, ex. \"1\")")
                        card_selection = input()
                        # Input failsafe
                        while True:
                            if card_selection in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                                break
                            print("Hand invalid, try again!")
                            card_selection = input()
                        # Ask the player to pick an edition to change the card to
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Enter the edition you would like to change the card to!")
                        edition_selection = input()
                        # Input failsafe
                        while True:
                            if edition_selection in card_editions_array:
                                break
                            print("Edition invalid, try again!")
                            edition_selection = input()
                        # Change the edition of the card
                        booster_pack[int(card_selection) - 1][3] = edition_selection
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Changed edition!")
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                        # Return the booster pack to the main deck and shuffle the main deck
                        for i in range(8):
                            main_deck.append(booster_pack[i])
                        main_deck = shuffle_array(main_deck)
                        # Exit the loop as the edition has been changed
                        break
                    else:
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Not enough money!")
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")    
                        break    
                # If player chooses to buy a seal booster pack
                elif booster_pack_choice == "Seal":
                    if current_money >= 5:
                        current_money -= 5
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Bought Seal Booster Pack!")
                        print("Current Money: ", current_money)
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                        booster_pack = [[""] * 5 for _ in range(8)]
                        for i in range(8):
                            booster_pack[i] = main_deck[top_deck]
                            top_deck += 1
                        print("Cards drawn: ")
                        for card in booster_pack:
                            print(f"[{card[0]} of {card[1]}]", end=" ")
                            
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        # Show 3 random seals
                        print("Seals: ")
                        for i in range(3):
                            print(f"{i + 1}. {card_seals_array[i]}")
                        # Ask player to pick a card from the booster pack to change the seal
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("\n\nPick a card from the booster pack to change the seal! (Enter hand position of card, ex. \"1\")")
                        card_selection = input()
                        # Input failsafe
                        while True:
                            if card_selection in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                                break
                            print("Hand invalid, try again!")
                            card_selection = input()
                        # Ask the player to pick a seal to change the card to
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Enter the seal you would like to change the card to!")
                        seal_selection = input()
                        # Input failsafe
                        while True:
                            if seal_selection in card_seals_array:
                                break
                            print("Seal invalid, try again!")
                            seal_selection = input()
                        # Change the seal of the card
                        booster_pack[int(card_selection) - 1][4] = seal_selection
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Changed seal!")
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                        # Return the booster pack to the main deck and shuffle the main deck
                        for i in range(8):
                            main_deck.append(booster_pack[i])
                        main_deck = shuffle_array(main_deck)
                        break
                    else:
                        print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                        print("Not enough money!")
                        print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                        break
                else:
                    # If player chooses to skip the shop, break out of the shop loop
                    print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
                    print("Exiting Shop!")
                    print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
                    break
        else:
            # If player chooses to skip the shop, break out of the shop loop
            print("\n{~~~~~~~~~~~~~~~~~~~~~~~}")
            print("Exiting Shop!")
            print("{~~~~~~~~~~~~~~~~~~~~~~~}\n")
            break