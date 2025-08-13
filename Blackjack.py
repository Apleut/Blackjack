import subprocess
import sys
import pkg_resources
import os
import random
import time
import colorama
from colorama import Fore, Style, Back

colorama.init()

def set_window_title(title):
    if os.name == "nt":  # Windows
        os.system(f"title {title}")
    else:  # macOS/Linux
        sys.stdout.write(f"\33]0;{title}\a")
        sys.stdout.flush()

set_window_title("Blackjack Casino - Balance: $1000")

REQUIREMENTS_FILE = "Requirements.txt"

def install_missing_requirements():
    # Read requirements from file
    if not os.path.exists(REQUIREMENTS_FILE):
        print(f"Requirements file '{REQUIREMENTS_FILE}' not found.")
        return
    
    with open(REQUIREMENTS_FILE) as f:
        required = f.read().splitlines()

    installed = {pkg.key for pkg in pkg_resources.working_set}
    missing = [pkg for pkg in required if pkg.lower() not in installed]

    if missing:
        print("Installing missing requirements...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *missing],
            stdout=subprocess.DEVNULL,  # Suppress output
            stderr=subprocess.DEVNULL   # Suppress errors in console (pip still fails if it can't install)
        )
    else:
        print("All requirements are satisfied.")

install_missing_requirements()



playermoney = 1000
player_has_money = True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def game_over_banner():
    print(f"""{Fore.RED}
   ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
  ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
  ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████═╝
  ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██║   ██║██╔══╝  ██╔██║  
  ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝╚██████╔╝███████╗██║║██║ 
   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚══╝ 
    {Style.DIM}You ran out of money!{Style.RESET_ALL}                       """)


# Deck logic

deck = [
    "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", 
    "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", 
    "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", 
    "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"
]

def reshuffle_deck():
    deck.clear()
    deck.extend([
    "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", 
    "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", 
    "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", 
    "A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"
    ])

def draw_card():

    if not deck:
        reshuffle_deck()

    index = random.randrange(len(deck))
    card = deck.pop(index)

    return card

def rules():

    clear_screen()
    print(f"The goal of Blackjack is to get as close to a total value of {Fore.BLUE}21{Style.RESET_ALL} as possible without going over. For example, a value of {Fore.BLUE}20{Style.RESET_ALL} is good, a value of {Fore.BLUE}25{Style.RESET_ALL} is bad.")
    input("\n\nPress ENTER to continue.")
    clear_screen()
    print(f"There are {Fore.BLUE}3{Style.RESET_ALL} different things you can do each turn. You can {Fore.YELLOW}Hit{Style.RESET_ALL}, {Fore.YELLOW}Stand{Style.RESET_ALL}, or {Fore.YELLOW}Double Down{Style.RESET_ALL}.")
    input("\n\nPress ENTER to continue.")
    clear_screen()
    print(f"If you choose to {Fore.YELLOW}Hit{Style.RESET_ALL}, you draw {Fore.BLUE}1{Style.RESET_ALL} card and end your turn.\n\n\nIf you choose to {Fore.YELLOW}Stand{Style.RESET_ALL}, you end your turn and draw no cards.\n\n\nIf you choose to {Fore.YELLOW}Double Down{Style.RESET_ALL}, you draw {Fore.BLUE}1{Style.RESET_ALL} card, double your bet, and {Style.BRIGHT}take no more actions for the rest of the game.{Style.RESET_ALL}")
    input("\n\nPress ENTER to continue.")
    clear_screen()
    print(f"The dealer will attempt to beat you by reaching a higher value (while still not going over {Fore.BLUE}21{Style.RESET_ALL}.)\nIf the dealer has a value closer to 21 at the end of the game, you lose.")
    input("\n\nPress ENTER to continue.")



def blackjack():

    global playermoney

    playervalue = 0
    dealervalue = 0

    novalidint = True

    while novalidint is True:
        try:
            clear_screen()
            playerbet = int(input(f"{Style.RESET_ALL}How much would you like to bet for this round?: $"))

            if playerbet > playermoney:
                clear_screen()
                print(f"{Fore.RED}You tryna cheat me? You don't have that much money!{Style.RESET_ALL}")
                input("\n\nPress ENTER to continue.")
            elif playerbet < 50:
                clear_screen()
                print(f"{Fore.RED}You think this is a cheapskate casino? You need to bet at least $50.{Style.RESET_ALL}")
                input("\n\nPress ENTER to continue.")
            else:
                novalidint = False
        except ValueError:
            clear_screen()
            print(f"{Fore.RED}That isn't a number. I need a valid number.{Style.RESET_ALL}")
            input("\n\nPress ENTER to continue.")

    def validate_choice(choice):

        if choice.lower() not in ["hit", "stand", "double down"]:
            clear_screen()
            print(f"{Fore.RED}That's not a valid choice.{Style.RESET_ALL}")
            input("\n\nPress ENTER to continue.")
            return False
        else:
            if choice.lower() == "double down" and playerbet * 2 > playermoney:
                print(f"{Fore.RED}You don't have enough money for that. Try hitting instead.{Style.RESET_ALL}")
                return False
            else:
                return True

    def calculate_hand_value(hand1, hand2, hand3, hand4):
        hand_value = 0
        aces = 0

        def special_check(card, hand_value):
            nonlocal aces
            
            if card is None:
                return hand_value
            else:
                if card == "A":
                    new_hand_value = hand_value + 11
                    aces += 1
                elif card in ["J", "Q", "K"]:
                    new_hand_value = hand_value + 10
                else:
                    new_hand_value = hand_value + card

                return new_hand_value

        hand_value = special_check(hand1, hand_value)
        hand_value = special_check(hand2, hand_value)
        hand_value = special_check(hand3, hand_value)
        hand_value = special_check(hand4, hand_value)

        while hand_value > 21 and aces > 0:
            hand_value -= 10
            aces -= 1

        return hand_value
        

    





    playerhand1 = draw_card()
    playerhand2 = draw_card()
    playerhand3 = None
    playerhand4 = None
    playervalue = calculate_hand_value(playerhand1, playerhand2, playerhand3, playerhand4)

    dealerhandshown = draw_card()
    dealerhandhidden = draw_card()
    dealerhand3 = None
    dealerhand4 = None
    dealervalue = calculate_hand_value(dealerhandshown, dealerhandhidden, dealerhand3, dealerhand4)

    draw = "draw"
    reveal = "reveal"
    reshuffle = "reshuffle"

    def dealer_card_loop(type):
        if type == "draw":
            text = "draws a card"
            duration = 5
        elif type == "reveal":
            text = "reveals their card"
            duration = 5
        elif type == "reshuffle":
            text = "is reshuffling the cards"
            duration = 10
        for i in range(1, duration):

            clear_screen()
            print(f"{Style.DIM}The dealer {text}.{Style.RESET_ALL}")
            time.sleep(0.3)
            clear_screen()
            print(f"{Style.DIM}The dealer {text}..{Style.RESET_ALL}")
            time.sleep(0.3)
            clear_screen()
            print(f"{Style.DIM}The dealer {text}...{Style.RESET_ALL}")
            time.sleep(0.3)


    clear_screen()
    if dealerhandshown == "A":
        dealerknownvalue = 11
    elif dealerhandshown in ["J", "Q", "K"]:
        dealerknownvalue = 10
    else:
        dealerknownvalue = dealerhandshown
    print(f"Your hand: {Fore.BLUE}{playerhand1}, {playerhand2}{Style.RESET_ALL}. Total value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\n\nDealer's hand: {Fore.BLUE}{dealerhandshown}, ???{Style.RESET_ALL}. Total known value: {Fore.BLUE}{dealerknownvalue}{Style.RESET_ALL}")

    input("\n\nPress ENTER to continue.")

    # Choice logic
    def choice():

        nonlocal playerbet

        validchoice = False

        while validchoice is False:

            clear_screen()
            playerchoice = input(f"{Fore.YELLOW}Hit{Style.RESET_ALL}, {Fore.YELLOW}stand{Style.RESET_ALL}, or {Fore.YELLOW}double down{Style.RESET_ALL}?: ")
            validchoice = validate_choice(playerchoice)

        if playerchoice.lower() == "hit":
            card = draw_card()
            # The boolean variable here is our continue flag. It tells the game to allow another choice afterwards.
            return True, card
        elif playerchoice.lower() == "double down":
            card = draw_card()
            playerbet = playerbet * 2
            return False, card
        else: # Standing
            return False, None

    # Choice round 1

    if playervalue <= 20:

        continue_flag, playerhand3 = choice()
        if playerhand3:
            playervalue = calculate_hand_value(playerhand1, playerhand2, playerhand3, playerhand4)
            clear_screen()
            print(f"Your hand: {Fore.BLUE}{playerhand1}, {playerhand2}, {playerhand3}{Style.RESET_ALL}. Total value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\n\nDealer's hand: {Fore.BLUE}{dealerhandshown}, ???{Style.RESET_ALL}. Total known value: {Fore.BLUE}{dealerknownvalue}{Style.RESET_ALL}")
            input("\n\nPress ENTER to continue.")

        # Choice round 2, but only if the continue flag is True and playervalue is still under 21

        if continue_flag is True and playervalue <= 20:
            continue_flag, playerhand4 = choice()
            if playerhand4:
                playervalue = calculate_hand_value(playerhand1, playerhand2, playerhand3, playerhand4)
                clear_screen()
                print(f"Your hand: {Fore.BLUE}{playerhand1}, {playerhand2}, {playerhand3}, {playerhand4}{Style.RESET_ALL}. Total value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\n\nDealer's hand: {Fore.BLUE}{dealerhandshown}, ???{Style.RESET_ALL}. Total known value: {Fore.BLUE}{dealerknownvalue}{Style.RESET_ALL}")
                input("\n\nPress ENTER to continue.")
    


    dealer_card_loop(reveal)
    clear_screen()
    print(f"It's a {Fore.BLUE}{dealerhandhidden}{Style.RESET_ALL}! Their total value is {Fore.BLUE}{dealervalue}{Style.RESET_ALL}.")
    input("\n\nPress ENTER to continue.")

    if dealervalue <= 16:
        dealerhand3 = draw_card()
        dealervalue = calculate_hand_value(dealerhandshown, dealerhandhidden, dealerhand3, dealerhand4)

        dealer_card_loop(draw)
        clear_screen()
        print(f"It's a {Fore.BLUE}{dealerhand3}{Style.RESET_ALL}! Their total value is {Fore.BLUE}{dealervalue}{Style.RESET_ALL}.")
        input("\n\nPress ENTER to continue.")

    if dealervalue <= 16:
        dealerhand4 = draw_card()
        dealervalue = calculate_hand_value(dealerhandshown, dealerhandhidden, dealerhand3, dealerhand4)

        dealer_card_loop(draw)
        clear_screen()
        print(f"It's a {Fore.BLUE}{dealerhand4}{Style.RESET_ALL}! Their total value is {Fore.BLUE}{dealervalue}{Style.RESET_ALL}.")
        input("\n\nPress ENTER to continue.")



    clear_screen()

    if dealervalue >= playervalue and dealervalue <= 21:
        playermoney -= playerbet
        print(f"{Fore.RED}Dealer has a higher value! You lose ${playerbet}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
        input("\n\nPress ENTER to continue.")

    elif playervalue >= dealervalue and playervalue <= 21:
        playerwinnings = playerbet * 2
        playermoney += playerwinnings
        print(f"{Fore.GREEN}You have a higher value! You win ${playerwinnings}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
        input("\n\nPress ENTER to continue.")

    elif dealervalue > 21 and playervalue <= 21:
        playerwinnings = playerbet * 2
        playermoney += playerwinnings
        print(f"{Fore.GREEN}Dealer busts! You win ${playerwinnings}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
        input("\n\nPress ENTER to continue.")

    elif playervalue > 21 and dealervalue <= 21:
        playermoney -= playerbet
        print(f"{Fore.RED}You bust! You lose ${playerbet}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
        input("\n\nPress ENTER to continue.")

    elif playervalue == dealervalue or playervalue > 21 and dealervalue > 21:
        print(f"{Fore.YELLOW}It's a push! You get your bet of ${playerbet} back. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
        input("\n\nPress ENTER to continue.")

    else:
        print(f"I uh... I don't know what this is. If you could do me a favor and take a screenshot of this and file a bug report, I'd appreciate it.\n\nPlayer value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\nDealer value: {Fore.BLUE}{dealervalue}{Style.RESET_ALL}")
        input("\n\nPress ENTER to continue.")

    set_window_title(f"Blackjack Casino - Balance: ${playermoney}")




    if playermoney < 50:
        clear_screen()
        game_over_banner()
        time.sleep(5)
        global player_has_money
        player_has_money = False
    else:
        dealer_card_loop(reshuffle)

    reshuffle_deck()

clear_screen()
rules_decision = input(f"Hey kid, welcome to Blackjack. Do you know how things work around here or do you need me to tell you the rules?\n\nType 'RULES' if you need the run-down: ")

if rules_decision.upper() == "RULES":
    rules()

clear_screen()
print(f"Alright then, let's get started with your first round. You've got ${playermoney} to start with, so don't sweat finding cash to bet with.\nIf you reach $0, the game will end, so don't make super risky bets!\n\nAlso, I recommend putting this window in fullscreen. It prevents the text from looking wacky.")
input("\n\nPress ENTER to begin.")

while player_has_money is True:

    blackjack()
