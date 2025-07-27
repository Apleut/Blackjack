import random
import time


def blackjack():

    cleartext = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"

    playervalue = 0
    dealervalue = 0

    novalidint = True

    while novalidint is True:
        try:
            playerbet = int(input(f"{cleartext}How much would you like to bet for this round?: $"))

            if playerbet < 50:
                print("You think this is a cheapskate casino? You need to bet at least $50.")
                time.sleep(3)
            else:
                novalidint = False
        except ValueError:
            print("That isn't a number. I need a valid number.")
            time.sleep(3)

    deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


    playerhand1 = random.choice(deck)
    playerhand2 = random.choice(deck)
    playerhand3 = 0
    playerhand4 = 0
    playervalue = playerhand1 + playerhand2

    dealerhandshown = random.choice(deck)
    dealerhandhidden = random.choice(deck)
    dealervalue = dealerhandshown + dealerhandhidden



    print(f"{cleartext}Your hand: {playerhand1}, {playerhand2}. Total value: {playervalue}\n\nDealer's hand: {dealerhandshown}, ???. Total known value: {dealerhandshown}\n")

    time.sleep(1)

    novalidchoice = True
    playerchoice = "NOT GIVEN"
    
    while novalidchoice is True:
        playerchoice = str(input("'Hit', 'Stand', or 'Double down'?: "))

        if playerchoice.lower() != "hit" and playerchoice.lower() != "stand" and playerchoice.lower() != "double down":
            print("\nThat isn't a valid choice kid. It's either hit or stand.\n\n")
            time.sleep(1)
        else:
            novalidchoice = False
    novalidchoice = True

    if playerchoice.lower() == "hit" or playerchoice.lower() == "double down":
        playerhand3 = random.choice(deck)
        playervalue = playervalue + playerhand3
        print(f"{cleartext}Your hand: {playerhand1}, {playerhand2}, {playerhand3}. Total value: {playervalue}\n\nDealer's hand: {dealerhandshown}, ???. Total known value: {dealerhandshown}\n\n")

        if playerchoice.lower() == "double down":
            playerbet = playerbet * 2

        while novalidchoice is True:

            if playerchoice.lower() != "double down":
            
                playerchoice = str(input("'Hit', 'Stand', or 'Double down'?: "))

                if playerchoice.lower() != "hit" and playerchoice.lower() != "stand" and playerchoice.lower() != "double down":
                    print("\nThat isn't a valid choice kid. It's either hit or stand.\n\n")
                    time.sleep(1)
                else:
                    novalidchoice = False
            

                if playerchoice.lower() == "hit" or playerchoice.lower() == "double down":
                    playerhand4 = random.choice(deck)
                    playervalue = playervalue + playerhand4
                    print(f"{cleartext}Your hand: {playerhand1}, {playerhand2}, {playerhand3}, {playerhand4}. Total value: {playervalue}\n\nDealer's hand: {dealerhandshown}, ???. Total known value: {dealerhandshown}\n\n")
    
                    if playerchoice.lower() == "double down":
                         playerbet = playerbet * 2
                
            else:
                novalidchoice = False

            


    time.sleep(1)
    print("\nDealer is revealing their card...\n")
    time.sleep(1)
    print(f"\n\nIt's a {dealerhandhidden}! Their total value is {dealervalue}.\n\n")

    if dealervalue <= 16:
        dealerhand3 = random.choice(deck)
        dealervalue = dealervalue + dealerhand3

        print(f"The dealer draws a card...")
        time.sleep(1)
        print(f"It's a {dealerhand3}! Their total value is {dealervalue}.\n\n")
        time.sleep(1)

    if dealervalue <= 16:
        dealerhand4 = random.choice(deck)
        dealervalue = dealervalue + dealerhand4

        print(f"The dealer draws a card...")
        time.sleep(1)
        print(f"It's a {dealerhand4}! Their total value is {dealervalue}.\n\n")
        time.sleep(1)

    playerwinnings = playerbet * 2

    time.sleep(1)

    if dealervalue >= playervalue and dealervalue <= 21:
        print(f"\n\nDealer has a higher value! You lose ${playerbet}.\n\n")
    elif playervalue >= dealervalue and playervalue <= 21:
        print(f"\n\nYou have a higher value! You win ${playerwinnings}.\n\n")
    elif dealervalue > 21 and playervalue <= 21:
        print(f"\n\nDealer busts! You win ${playerwinnings}.\n\n")
    elif playervalue > 21 and dealervalue <= 21:
        print(f"\n\nYou bust! You lose ${playerbet}.\n\n")
    else:
        print(f"\n\nIt's a push! You get your bet of ${playerbet} back.\n\n")

    time.sleep(5)

    for i in range(1, 10):

        print(f"{cleartext}The dealer is reshuffling the cards.\n\n\n\n\n\n")
        time.sleep(0.3)
        print(f"{cleartext}The dealer is reshuffling the cards..\n\n\n\n\n\n")
        time.sleep(0.3)
        print(f"{cleartext}The dealer is reshuffling the cards...\n\n\n\n\n\n")
        time.sleep(0.3)


while True:
    blackjack()
