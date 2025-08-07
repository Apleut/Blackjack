import subprocess
import sys
import pkg_resources
import os


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



import random
import time
from colorama import Fore, Style, Back

playermoney = 1000
player_has_money = True

def game_over_banner():
    print(f"""{Fore.RED}{Back.YELLOW}
   ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
  ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
  ██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████═╝
  ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██║   ██║██╔══╝  ██╔██║  
  ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝╚██████╔╝███████╗██║║██║ 
   ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚══╝ 
    {Style.DIM}You ran out of money!{Style.RESET_ALL}                       """)


# Deck logic

deck = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10
]

def draw_card():

    if not deck:
        raise ValueError(f"{Back.RED}{Fore.BLACK}No more cards in the deck!{Style.RESET_ALL}")

    index = random.randrange(len(deck))
    card = deck.pop(index)

    return card

def reshuffle_deck():
    deck.clear()
    deck.extend([
        1,2,3,4,5,6,7,8,9,10,10,10,10,
        1,2,3,4,5,6,7,8,9,10,10,10,10,
        1,2,3,4,5,6,7,8,9,10,10,10,10,
        1,2,3,4,5,6,7,8,9,10,10,10,10
    ])



def blackjack():

    global playermoney

    cleartext = "\033[2J\033[H"

    playervalue = 0
    dealervalue = 0

    novalidint = True

    while novalidint is True:
        try:
            playerbet = int(input(f"{Style.RESET_ALL}{cleartext}How much would you like to bet for this round?: $"))

            if playerbet > playermoney:
                print(f"{cleartext}{Fore.RED}{Back.WHITE}You tryna cheat me? You don't have that much money!{Style.RESET_ALL}")
                time.sleep(3)
            elif playerbet < 50:
                print(f"{cleartext}{Fore.RED}{Back.WHITE}You think this is a cheapskate casino? You need to bet at least $50.{Style.RESET_ALL}")
                time.sleep(3)
            else:
                novalidint = False
        except ValueError:
            print(f"{cleartext}{Fore.RED}{Back.WHITE}That isn't a number. I need a valid number.{Style.RESET_ALL}")
            time.sleep(3)


    playerhand1 = draw_card()
    playerhand2 = draw_card()
    playerhand3 = 0
    playerhand4 = 0
    playervalue = playerhand1 + playerhand2

    dealerhandshown = draw_card()
    dealerhandhidden = draw_card()
    dealervalue = dealerhandshown + dealerhandhidden



    print(f"{cleartext}Your hand: {Fore.BLUE}{playerhand1}, {playerhand2}{Style.RESET_ALL}. Total value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\n\nDealer's hand: {Fore.BLUE}{dealerhandshown}, ???{Style.RESET_ALL}. Total known value: {Fore.BLUE}{dealerhandshown}{Style.RESET_ALL}\n")

    time.sleep(1)

    novalidchoice = True
    playerchoice = "NOT GIVEN"
    
    while novalidchoice is True:
        playerchoice = str(input("'Hit', 'Stand', or 'Double down'?: "))

        if playerchoice.lower() != "hit" and playerchoice.lower() != "stand" and playerchoice.lower() != "double down":
            print(f"{Fore.RED}{Back.WHITE}\nThat isn't a valid choice kid. It's either hit, stand, or double down.\n\n{Style.RESET_ALL}")
            time.sleep(1)
        else:
            novalidchoice = False
    novalidchoice = True

    if playerchoice.lower() == "hit" or playerchoice.lower() == "double down":
        playerhand3 = draw_card()
        playervalue = playervalue + playerhand3
        print(f"{cleartext}Your hand: {Fore.BLUE}{playerhand1}, {playerhand2}, {playerhand3}{Style.RESET_ALL}. Total value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\n\nDealer's hand: {Fore.BLUE}{dealerhandshown}, ???{Style.RESET_ALL}. Total known value: {Fore.BLUE}{dealerhandshown}{Style.RESET_ALL}\n\n")

        if playerchoice.lower() == "double down":
            if playerbet * 2 > playermoney:
                print(f"{cleartext}{Fore.RED}{Back.WHITE}You tryna cheat me? You don't have that much money!{Style.RESET_ALL}")
                time.sleep(3)
            else:
                playerbet = playerbet * 2

        while novalidchoice is True:

            if playerchoice.lower() != "double down" and playervalue <= 21:
            
                playerchoice = str(input(f"'Hit', 'Stand', or 'Double down'?: "))

                if playerchoice.lower() != "hit" and playerchoice.lower() != "stand" and playerchoice.lower() != "double down":
                    print(f"\n{Fore.RED}{Back.WHITE}That isn't a valid choice kid. It's either hit, stand, or double down.{Style.RESET_ALL}\n\n")
                    time.sleep(1)
                else:
                    novalidchoice = False
            

                if playerchoice.lower() == "hit" or playerchoice.lower() == "double down":
                    playerhand4 = draw_card()
                    playervalue = playervalue + playerhand4
                    print(f"{cleartext}Your hand: {Fore.BLUE}{playerhand1}, {playerhand2}, {playerhand3}, {playerhand4}{Style.RESET_ALL}. Total value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\n\nDealer's hand: {Fore.BLUE}{dealerhandshown}, ???{Style.RESET_ALL}. Total known value: {Fore.BLUE}{dealerhandshown}{Style.RESET_ALL}\n\n")
    
                    if playerchoice.lower() == "double down":
                        if playerbet * 2 > playermoney:
                            print(f"{cleartext}{Fore.RED}{Back.WHITE}You tryna cheat me? You don't have that much money!{Style.RESET_ALL}")
                            time.sleep(3)
                        else:
                            playerbet = playerbet * 2
                
            else:
                novalidchoice = False

            


    time.sleep(2)
    print(f"{cleartext}{Style.DIM}Dealer is revealing their card...{Style.RESET_ALL}")
    time.sleep(3)
    print(f"{cleartext}It's a {Fore.BLUE}{dealerhandhidden}{Style.RESET_ALL}! Their total value is {Fore.BLUE}{dealervalue}{Style.RESET_ALL}.")
    time.sleep(3)

    if dealervalue <= 16:
        dealerhand3 = draw_card()
        dealervalue = dealervalue + dealerhand3

        print(f"{cleartext}{Style.DIM}The dealer draws a card...{Style.RESET_ALL}")
        time.sleep(3)
        print(f"{cleartext}It's a {Fore.BLUE}{dealerhand3}{Style.RESET_ALL}! Their total value is {Fore.BLUE}{dealervalue}{Style.RESET_ALL}.")
        time.sleep(3)

    if dealervalue <= 16:
        dealerhand4 = draw_card()
        dealervalue = dealervalue + dealerhand4

        print(f"{cleartext}{Style.DIM}The dealer draws another card...{Style.RESET_ALL}")
        time.sleep(3)
        print(f"{cleartext}It's a {Fore.BLUE}{dealerhand4}{Style.RESET_ALL}! Their total value is {Fore.BLUE}{dealervalue}{Style.RESET_ALL}.")
        time.sleep(3)

    playerwinnings = playerbet * 2

    time.sleep(1)

    print(cleartext)

    if dealervalue >= playervalue and dealervalue <= 21:
        playermoney -= playerbet
        print(f"\n\n{Fore.RED}{Back.WHITE}Dealer has a higher value! You lose ${playerbet}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
    elif playervalue >= dealervalue and playervalue <= 21:
        playermoney += playerbet
        print(f"\n\n{Fore.GREEN}You have a higher value! You win ${playerwinnings}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
    elif dealervalue > 21 and playervalue <= 21:
        playermoney += playerbet
        print(f"\n\n{Fore.GREEN}Dealer busts! You win ${playerwinnings}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
    elif playervalue > 21 and dealervalue <= 21:
        playermoney -= playerbet
        print(f"\n\n{Fore.RED}{Back.WHITE}You bust! You lose ${playerbet}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
    else:
        print(f"\n\n{Fore.YELLOW}It's a push! You get your bet of ${playerbet} back. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")

    set_window_title(f"Blackjack Casino - Balance: ${playermoney}")

    time.sleep(5)



    if playermoney < 50:
        print(cleartext)
        game_over_banner()
        time.sleep(5)
        global player_has_money
        player_has_money = False
    else:
        for i in range(1, 10):

            print(f"{cleartext}{Style.DIM}The dealer is reshuffling the cards.{Style.RESET_ALL}")
            time.sleep(0.3)
            print(f"{cleartext}{Style.DIM}The dealer is reshuffling the cards..{Style.RESET_ALL}")
            time.sleep(0.3)
            print(f"{cleartext}{Style.DIM}The dealer is reshuffling the cards...{Style.RESET_ALL}")
            time.sleep(0.3)

    reshuffle_deck()

while player_has_money is True:

    blackjack()
