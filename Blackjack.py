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
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10
]

def reshuffle_deck():
    deck.clear()
    deck.extend([
        1,2,3,4,5,6,7,8,9,10,10,10,10,
        1,2,3,4,5,6,7,8,9,10,10,10,10,
        1,2,3,4,5,6,7,8,9,10,10,10,10,
        1,2,3,4,5,6,7,8,9,10,10,10,10
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

def blackjack():

    global playermoney

    playervalue = 0
    dealervalue = 0

    novalidint = True

    while novalidint is True:
        try:
            clear_screen()
            playerbet = (input(f"{Style.RESET_ALL}How much would you like to bet for this round?: $"))

            if playerbet == "ENABLE_CHEATS":
                print(f"{Fore.BLUE}CHEATS ENABLED. TYPE 'OVERRIDE_[OUTCOME]' TO SET THE OUTCOME OF THE ROUND.")
                action = input(f"ACTION: ")
                if action == "OVERRIDE_WIN":
                    dealervalue = 400
                    print("DO NOT DRAW ANY CARDS THIS ROUND AND YOU WILL WIN.")
                if action == "OVERRIDE_LOSE":
                    playervalue = 400
                    print("YOU WILL LOSE THIS ROUND.")
                if action == "OVERRIDE_PUSH":
                    playervalue = 400
                    dealervalue = 400
                    print("THE OUTCOME WILL BE A PUSH.")
                else:
                    print("INVALID COMMAND. PROCEDING WITH STANDARD GAME LOOP.")
                time.sleep(3)

                clear_screen()
                playerbet = (input(f"{Style.RESET_ALL}How much would you like to bet for this round? (Type your actual bet this time.): $"))

            playerbet = int(playerbet)

            if playerbet > playermoney:
                clear_screen()
                print(f"{Fore.RED}You tryna cheat me? You don't have that much money!{Style.RESET_ALL}")
                time.sleep(3)
            elif playerbet < 50:
                clear_screen()
                print(f"{Fore.RED}You think this is a cheapskate casino? You need to bet at least $50.{Style.RESET_ALL}")
                time.sleep(3)
            else:
                novalidint = False
        except ValueError:
            clear_screen()
            print(f"{Fore.RED}That isn't a number. I need a valid number.{Style.RESET_ALL}")
            time.sleep(3)


    playerhand1 = draw_card()
    playerhand2 = draw_card()
    playerhand3 = 0
    playerhand4 = 0
    playervalue = playerhand1 + playerhand2 + playervalue

    dealerhandshown = draw_card()
    dealerhandhidden = draw_card()
    dealervalue = dealerhandshown + dealerhandhidden + dealervalue


    clear_screen()
    print(f"Your hand: {Fore.BLUE}{playerhand1}, {playerhand2}{Style.RESET_ALL}. Total value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\n\nDealer's hand: {Fore.BLUE}{dealerhandshown}, ???{Style.RESET_ALL}. Total known value: {Fore.BLUE}{dealerhandshown}{Style.RESET_ALL}\n")

    time.sleep(1)

    novalidchoice = True
    playerchoice = "NOT GIVEN"
    
    while novalidchoice is True:
        
        playerchoice = str(input("'Hit', 'Stand', or 'Double down'?: "))

        if playerchoice.lower() != "hit" and playerchoice.lower() != "stand" and playerchoice.lower() != "double down":
            clear_screen()
            print(f"{Fore.RED}\nThat isn't a valid choice kid. It's either hit, stand, or double down.\n\n{Style.RESET_ALL}")
            time.sleep(1)
        else:
            novalidchoice = False

        if playerchoice.lower() == "hit" or playerchoice.lower() == "double down":
            if playerchoice.lower() == "double down":
                if playerbet * 2 > playermoney:
                    clear_screen()
                    print(f"{Fore.RED}You tryna cheat me? You don't have that much money!{Style.RESET_ALL}")
                    time.sleep(3)
                    novalidchoice = True
                else:
                    playerbet = playerbet * 2
                    novalidchoice = False
            playerhand3 = draw_card()
            playervalue = playervalue + playerhand3
            clear_screen()
            print(f"Your hand: {Fore.BLUE}{playerhand1}, {playerhand2}, {playerhand3}{Style.RESET_ALL}. Total value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\n\nDealer's hand: {Fore.BLUE}{dealerhandshown}, ???{Style.RESET_ALL}. Total known value: {Fore.BLUE}{dealerhandshown}{Style.RESET_ALL}\n\n")

        while novalidchoice is True:

            if playerchoice.lower() != "double down" and playerchoice.lower() != "stand" and playervalue <= 21:
            
                playerchoice = str(input(f"'Hit', 'Stand', or 'Double down'?: "))

                if playerchoice.lower() != "hit" and playerchoice.lower() != "stand" and playerchoice.lower() != "double down":
                    clear_screen()
                    print(f"\n{Fore.RED}That isn't a valid choice kid. It's either hit, stand, or double down.{Style.RESET_ALL}\n\n")
                    time.sleep(1)
                else:
                    novalidchoice = False
            

                if playerchoice.lower() == "hit" or playerchoice.lower() == "double down":
                    if playerchoice.lower() == "double down":
                        if playerbet * 2 > playermoney:
                            clear_screen()
                            print(f"{Fore.RED}You tryna cheat me? You don't have that much money!{Style.RESET_ALL}")
                            time.sleep(3)
                        else:
                            playerbet = playerbet * 2
                            novalidchoice = False
                    playerhand4 = draw_card()
                    playervalue = playervalue + playerhand4
                    clear_screen()
                    print(f"Your hand: {Fore.BLUE}{playerhand1}, {playerhand2}, {playerhand3}, {playerhand4}{Style.RESET_ALL}. Total value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\n\nDealer's hand: {Fore.BLUE}{dealerhandshown}, ???{Style.RESET_ALL}. Total known value: {Fore.BLUE}{dealerhandshown}{Style.RESET_ALL}\n\n")
    

                
            else:
                novalidchoice = False

            


    time.sleep(2)
    dealer_card_loop(reveal)
    clear_screen()
    print(f"It's a {Fore.BLUE}{dealerhandhidden}{Style.RESET_ALL}! Their total value is {Fore.BLUE}{dealervalue}{Style.RESET_ALL}.")
    time.sleep(3)

    if dealervalue <= 16:
        dealerhand3 = draw_card()
        dealervalue = dealervalue + dealerhand3

        dealer_card_loop(draw)
        clear_screen()
        print(f"It's a {Fore.BLUE}{dealerhand3}{Style.RESET_ALL}! Their total value is {Fore.BLUE}{dealervalue}{Style.RESET_ALL}.")
        time.sleep(3)

    if dealervalue <= 16:
        dealerhand4 = draw_card()
        dealervalue = dealervalue + dealerhand4

        dealer_card_loop(draw)
        clear_screen()
        print(f"It's a {Fore.BLUE}{dealerhand4}{Style.RESET_ALL}! Their total value is {Fore.BLUE}{dealervalue}{Style.RESET_ALL}.")
        time.sleep(3)


    time.sleep(1)

    clear_screen()

    if dealervalue >= playervalue and dealervalue <= 21:
        playermoney -= playerbet
        print(f"{Fore.RED}Dealer has a higher value! You lose ${playerbet}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
    
    elif playervalue >= dealervalue and playervalue <= 21:
        playermoney += playerbet
        print(f"{Fore.GREEN}You have a higher value! You win ${playerbet}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
    
    elif dealervalue > 21 and playervalue <= 21:
        playermoney += playerbet
        print(f"{Fore.GREEN}Dealer busts! You win ${playerbet}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
    
    elif playervalue > 21 and dealervalue <= 21:
        playermoney -= playerbet
        print(f"{Fore.RED}You bust! You lose ${playerbet}. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
    
    elif playervalue == dealervalue or playervalue > 21 and dealervalue > 21:
        print(f"{Fore.YELLOW}It's a push! You get your bet of ${playerbet} back. Your balance: ${playermoney}{Style.RESET_ALL}\n\n")
    
    else:
        print(f"I uh... I don't know what this is. If you could do me a favor and take a screenshot of this and file a bug report, I'd appreciate it.\n\nPlayer value: {Fore.BLUE}{playervalue}{Style.RESET_ALL}\nDealer value: {Fore.BLUE}{dealervalue}{Style.RESET_ALL}")

    set_window_title(f"Blackjack Casino - Balance: ${playermoney}")

    time.sleep(5)



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
