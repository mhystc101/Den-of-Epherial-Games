import random
import time
import os
import csv
import numpy as np
import sys
import threading


#def clear_console():
    #if platform.system() == 'Windows':
        #os.system('cls')  # For Windows
    #else:
        #os.system('clear')  # For Unix/Linux/MacOS



RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

# for crash game

max_value = 100
exponent = 3 


# counter for loans
loan_counter = 0

# loan multiplier
# all source code of games

def make_loan_multi():
    # This variable will hold the current value
    value = 0
    
    def incrementer(amount):
        nonlocal value
        # Add 5% to the current value
        value += value * 0.05
        # Add the amount to the updated value
        value += amount
        return value
    
    return incrementer

# Create an instance of the incrementer function
loan_multi = make_loan_multi()

def save_variables(name):
    global total_credit
    global names_and_credits
    total_credit = round(total_credit)
    banked_credits = 0
    if name in names_and_credits:
        banked_credits = names_and_credits[name]['credits']
    else:
        names_and_credits[name] = {'credits': 0, 'net_profit_loss': 0}
    loan_amount = total_credit * 2
    loaned = False
    
    # Prompt user for input
    print("")
    user_input_var = input("Would you like to deposit, withdraw, or take out a loan(d/w/l): ")
    print("")
        # deposit
    if user_input_var == "d" or user_input_var == "deposit":
        while True:
            time.sleep(0.5)
            print(f"You currently have {GREEN}{total_credit}{RESET} total credits.")
            print("") 
            time.sleep(0.5)
            print(f"You currently have {YELLOW}{banked_credits}{RESET} in the bank") 
            print("")
            banked_amount = int(input("How much would you like to deposit: "))
           
            if banked_amount > total_credit:
                print("Insufficient credits.")
            else:
                total_credit -= banked_amount
                banked_credits += banked_amount
                names_and_credits[name]['credits'] = banked_credits
                update_bank("bank.csv", names_and_credits)
                print(f"You have deposited {YELLOW}{banked_amount}{RESET}")
                time.sleep(1) 
                home() # returns
                # withdraw
    elif user_input_var.lower() == "w" or user_input_var == "withdraw":
        while True:
            time.sleep(0.5)
            print(f"You currently have {GREEN}{total_credit}{RESET} total credits.")
            print("")
            time.sleep(0.5)
            print(f"You currently have {YELLOW}{banked_credits}{RESET} in the bank")
            print("")
            withdraw_var = int(input("How much would you like to withdraw: "))
            # checks if user has enough to withdraw
            if withdraw_var > banked_credits:
                print("Insufficient credits.")
            else:
                banked_credits -= withdraw_var
                total_credit += withdraw_var
                names_and_credits[name]['credits'] = banked_credits
                update_bank("bank.csv", names_and_credits)
                print("")
                print(f"You have withdrew {YELLOW}{withdraw_var}{RESET}")
                time.sleep(1)
                home() #returns
    elif user_input_var.lower() == "l" or user_input_var == "loan":
        if loaned == False:
            while True:
                time.sleep(0.5)
                print(f"You qualify to take out a loan of {YELLOW}{loan_amount}{RESET}.")
                time.sleep(0.5)
                print(f"The interest rate is {RED}5%{RESET} each bet.")
                loan_var = int(input("How much you like to acquire: "))
                print("")
                if loan_var > loan_amount:
                    print("Insufficient credits.")
                else:
                    loaned = True
                    total_credit += loan_var
                    time.sleep(0.5)
                    print(f"You have taken out a loan of {YELLOW}{loan_var}{RESET}")
                    time.sleep(0.5)
                    print(f"You will have to pay back the loan within {RED}10 bets{RESET}")
                    time.sleep(0.5)
                    print(f"The interest rate each bet is {RED}5%{RESET}")
                    time.sleep(1.5)
                    print("Good luck.")
                    time.sleep(1.5)
                    home()
        #elif loaned == True:



        
    #int_var3 = int(input("Enter one more integer value for variable3: "))

    # Store variables in a dictionary
    update_bank("bank.csv", names_and_credits, names_and_profit_loss)

# Example usage
#save_variables()

def update_bank(file_path, data):
    # Assume 'data' is a dictionary where each value is another dictionary including 'credits' and 'net_profit_loss'
    new_data = [{'name': name, 'credits': info['credits'], 'net profit/loss': info['net_profit_loss']} for name, info in data.items()]

    # Write the data to the CSV file
    with open(file_path, mode='w', newline='') as file:
        fieldnames = ['name', 'credits', 'net profit/loss']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        # Write the header
        writer.writeheader()
        
        # Write the data
        writer.writerows(new_data)


def extract_name_and_credits(csv_file_path, name_to_check):
    name_details_dict = {}
    name_found = False

    # Open and read the CSV file
    with open(csv_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        
        # Iterate over each row in the CSV
        for row in reader:
            name = row['name'].strip()  # Strip whitespace from name
            credits = int(row['credits'].strip())
            net_profit_loss = int(row['net profit/loss'].strip())

            # Add the name, credits, and net profit/loss to the dictionary
            name_details_dict[name] = {'credits': credits, 'net_profit_loss': net_profit_loss}

            # Check if the current row's name matches the name_to_check
            if name == name_to_check.strip():  # Strip whitespace from name_to_check
                name_found = True
    
    # Return True if the name was found, otherwise return the dictionary
    if name_found:
        return True
    else:
        return name_details_dict

def skewed_random(max_value, exponent):
    # Generate a random number between 0 and 1
    rand_value = random.random()
    
    # Apply the exponent to skew the distribution
    skewed_value = rand_value ** exponent
    
    # Scale to the desired maximum value
    result = skewed_value * max_value
    if result > 90:
        result = random.uniform(19,43)
    elif result > 75:
        result =  random.uniform(9,18.99)
    elif result > 65:
        result = random.uniform(3.5,8.99)
    elif result > 35:
        result = random.uniform(1.4,3.4)
    else:
        result = random.uniform(1,1.4)
    
    if isinstance(result, (int, float)):
        result = round(result, 2)
    return result
    



#test thing

#thingy = skewed_random(max_value, exponent)
#print(thingy)
#thingy = skewed_random(max_value, exponent)
#print(thingy)
#for i in range(100):
    #print(skewed_random(max_value, exponent))


def exponential_rise(max_value, num_points):
    log_space = np.logspace(0, np.log10(max_value), num=num_points)
    scaled_values = np.interp(log_space, (log_space.min(), log_space.max()), (1, max_value))
    return scaled_values

def display_exponential_change(explode_value, stop_flag):
    global value
    
    max_value = explode_value
    num_points = random.randint(15, 30)
    sequence = exponential_rise(max_value, num_points)
    
    for value in sequence:
        if stop_flag.is_set():
            break
        
        sys.stdout.write("\r" + f"RISING... {value:.2f}" + "x")
        sys.stdout.flush()
        time.sleep(0.6)  # Sleep for 0.6 seconds to simulate time passing
        if value >= max_value:
            print("")
            print(f"{RED}BOOM{RESET}")
            return True
    return False

def user_input_thread(stop_flag):
    input("Press Enter to stop the rocketship...\n")
    stop_flag.set()


def bank():
    global total_credit
    global user_name
    print("")
    print(f"{YELLOW}Welcome to the bank!{RESET}")
    print("")
    save_variables(user_name)

    

def dice_game():
    global total_credit
    global user_name
    
    
    # Display welcome message and instructions
    print("")
    print(f"{GREEN}Welcome to the dice game!{RESET}")
    print("")
    print("In this game all you do is try to guess the number the dice will roll on.")
    print("")
    print(f"There are two versions, one the {BLUE}dice will have 3 sides{RESET} and the other, the {MAGENTA}dice will have 6.{RESET}")
    print("")
    
    # Prompt user to select the dice game version
    while True:
        time.sleep(1)
        sub_game_dice = int(input(f"Type {BLUE}0{RESET} for the first game; Type {MAGENTA}1{RESET} for the second game; Type {RED}2{RESET} to go back: "))
        if sub_game_dice not in [0, 1, 2]:
            print("Please select a valid input (0/1/2)")
        else:
            break
    if sub_game_dice == 2:
        home()
        
    # Game loop for the dice with 3 sides
    if sub_game_dice == 0:
        while True:
            total_credit = round(total_credit)
            # Roll the dice and display credits
            dice_side_3 = random.randint(1, 3)
            print("")
            print(f"You currently have {GREEN}{total_credit}{RESET} credits")
            print("")
            time.sleep(0.5)

            # Get and validate the bet amount
            while True:
                bet_amount_dice_3 = float((input("How much would you like to bet: ")))
                if bet_amount_dice_3 <= 0 or bet_amount_dice_3 > total_credit:
                    print("Invalid input. Please enter a valid bet amount.")
                    dice_game()
                    return
                else:
                    break
            time.sleep(0.5)
            print("")
            print(f"You have selected {GREEN}{bet_amount_dice_3}{RESET} to bet")
            total_credit -= bet_amount_dice_3
            print("")
            time.sleep(0.5)

            # Get and validate the user's guess
            while True:
                guess_dice_3 = int(input(f"Guess which side the dice rolled {GREEN}(1-3){RESET}: "))
                if guess_dice_3 not in [1, 2, 3]:
                    print("Please select a valid input (1-3)")
                else:
                    break
            time.sleep(0.5)
            print("Rolling....")
            time.sleep(0.5)
            print("Rolling....")
            time.sleep(0.5)
            print("Rolling....")
            time.sleep(1)

            # Check if the user guessed correctly
            if guess_dice_3 == dice_side_3:
                print("")
                print(f"The dice rolled a {GREEN}{dice_side_3}{RESET}")
                print(f"{GREEN}You have guessed correctly{RESET}")
                bet_amount_dice_3 *= 2
                total_credit += bet_amount_dice_3
                total_credit = round(total_credit)
                print(f"You now have {GREEN}{total_credit}{RESET} total credits!")
            else:
                # User guessed incorrectly
                print(f"The dice rolled a {RED}{dice_side_3}{RESET}")
                print(f"{RED}You have guessed incorrectly.{RESET}")
                print(f"You now have {RED}{total_credit}{RESET} total credit.")

            # Ask user if they want to play again
            while True:
                restart_dice_3 = input("Would you like to play again, go to bank, or new game? (p/b/n): ")
                if restart_dice_3.lower() not in ["p", "b", "n"]:
                    print("Please select a valid input (p/b/n)")
                elif restart_dice_3 == "n":
                    home()
                elif restart_dice_3 == "b":
                    save_variables(user_name)
                elif restart_dice_3 == "p":
                    break
                else:
                    break
            if total_credit == 0.0:
                print("You thought you could play again?")
                print(f"You have {RED}lost everything,{RESET} Sad man Sad.")
                break
            if restart_dice_3 == "n":
                home()

    # Game loop for the dice with 6 sides
    if sub_game_dice == 1:
        while True:
            # Roll the dice and display credits
            total_credit = round(total_credit)
            dice_side_6 = random.randint(1, 6)
            print("")
            print(f"You currently have {GREEN}{total_credit}{RESET} credits")
            print("")
            time.sleep(0.5)

            # Get and validate the bet amount
            while True:
                bet_amount_dice_6 = float((input("How much would you like to bet: ")))
                if bet_amount_dice_6 <= 0 or bet_amount_dice_6 > total_credit:
                    print("Invalid input. Please enter a valid bet amount.")
                else:
                    break
            time.sleep(0.5)
            print("")
            print(f"You have selected {GREEN}{bet_amount_dice_6}{RESET} to bet")
            total_credit -= bet_amount_dice_6
            print("")
            time.sleep(0.5)

            # Get and validate the user's guess
            while True:
                guess_dice_6 = int(input(f"Guess which side the dice rolled {GREEN}(1-6){RESET}: "))
                if guess_dice_6 not in [1, 2, 3, 4, 5, 6]:
                    print("Please select a valid input (1-6)")
                else:
                    break
            time.sleep(0.5)
            print("Rolling....")
            time.sleep(0.5)
            print("Rolling....")
            time.sleep(0.5)
            print("Rolling....")
            time.sleep(1)

            # Check if the user guessed correctly
            if guess_dice_6 == dice_side_6:
                print("")
                print(f"The dice rolled a {GREEN}{dice_side_6}{RESET}")
                print(f"{GREEN}You have guessed correctly{RESET}")
                bet_amount_dice_6 *= 4
                total_credit += bet_amount_dice_6
                total_credit = round(total_credit)
                print(f"You now have {GREEN}{total_credit}{RESET} total credits!")
            else:
                # User guessed incorrectly
                print(f"The dice rolled a {RED}{dice_side_6}{RESET}")
                print(f"{RED}You have guessed incorrectly.{RESET}")
                print(f"You now have {RED}{total_credit}{RESET} total credit.")

            # Ask user if they want to play again
            while True:
                restart_dice_6 = input("Would you like to play again, go to bank, or new game? (p/b/n): ")
                if restart_dice_6.lower() not in ["p", "b", "n"]:
                    print("Please select a valid input (p/b/n)")
                elif restart_dice_6 == "n":
                    home()
                elif restart_dice_6 == "b":
                    save_variables(user_name)
                elif restart_dice_6 == "p":
                    break
            if total_credit == 0.0:
                print("You thought you could play again?")
                print(f"You have {RED}lost everything,{RESET} Sad man Sad.")
                break
            if restart_dice_6 == "n":
                home()


def black_jack():
    global total_credit
    global restart_blackjack
    global user_name
    
    # Display welcome message for the Black Jack game
    print("")
    print(f"{GREEN}Welcome to Black Jack!{RESET}")
    print("")
    
    while True:
        win = 21  # Define the winning score for Black Jack
        # Deal initial cards to the user and dealer
        card_dealt_user = random.randint(2, 11)
        card_dealt_dealer = random.randint(2, 11)
        total_credit = round(total_credit)
        # Show the current credit of the user
        print("")
        print(f"You currently have {GREEN}{total_credit}{RESET} credits")
        print("")
        time.sleep(0.5)
        
        # Get and validate the bet amount from the user
        while True:
            if total_credit == 0.0:
                print("You thought you could play again?")
                print(f"You have {RED}lost everything,{RESET} sad man sad. ")
                return
            bet_amount_blackjack = float((input("How much would you like to bet: ")))
            if bet_amount_blackjack <= 0:
                print("Invalid input. Please enter a valid bet amount.")
            elif bet_amount_blackjack > total_credit:
                print("Invalid input. Please enter a valid bet amount.")
            else:
                break
        time.sleep(0.5)
        print("")
        print(f"You have selected {GREEN}{bet_amount_blackjack}{RESET} to bet")
        total_credit -= bet_amount_blackjack
        print("")
        time.sleep(0.5)

        # Show the initial cards and scores
        user_score = card_dealt_user
        dealer_score = card_dealt_dealer
        print(f"You have been dealt a {CYAN}{user_score}{RESET}.")
        print("")
        time.sleep(0.5)
        print(f"The dealer has been dealt a {RED}{dealer_score}{RESET}")
        
        # Deal additional cards to the user and dealer
        card_dealt_user = random.randint(2, 11)
        card_dealt_dealer = random.randint(2, 11)
        user_score += card_dealt_user
        print("")
        time.sleep(0.5)
        print(f"You have been dealt a {CYAN}{card_dealt_user}{RESET}")
        print("")
        
        # Check if the user has hit blackjack
        if user_score == win:
            print(f"{GREEN}You have hit blackjack, you win!{RESET}")
            bet_amount_blackjack *= 2
            total_credit += bet_amount_blackjack
            total_credit = round(total_credit)
            while True:
                restart_blackjack = input("Would you like to play again, go to bank, or new game? (p/b/n): ")
                if restart_blackjack.lower() not in ["p", "b", "n"]:
                    print("Please select a valid input (p/b/n)")
                elif restart_blackjack == "n":
                    home()
                elif restart_blackjack == "b":
                    save_variables(user_name)
                elif restart_blackjack.lower() == "p":
                    black_jack()
                    return
        
        # User's turn to hit or stand
        while True:
            
            if user_score == win:
                print(f"You have dealt a {CYAN}{card_dealt_user}{RESET}")
                print(f"{GREEN}You have won!{RESET}")
                
                bet_amount_blackjack *= 2
                total_credit += bet_amount_blackjack
                print(f"You won {GREEN}{bet_amount_blackjack}{RESET}")
                total_credit = round(total_credit)
                while True:
                    restart_blackjack = input("Would you like to play again, go to bank, or new game? (p/b/n): ")
                    if restart_blackjack.lower() not in ["p", "b", "n"]:
                        print("Please select a valid input (p/b/n)")
                    elif restart_blackjack == "n":
                        home()
                    elif restart_blackjack == "b":
                        save_variables(user_name)
                    elif restart_blackjack.lower() == "p":
                        black_jack()
                        return
                if restart_blackjack.lower() == "y":
                    black_jack() # Restart the game
                    return
                else:
                    return
            #needs checker
            while True:
                user_input = input(f"You currently have {CYAN}{user_score}{RESET}. Would you like to hit or stand? (h/s): ")
                if user_input not in ["h","s"]:
                    print("Invalid input. Please enter a valid input (h/s)")
                else:
                    break
            if user_input == "h":
                card_dealt_user = random.randint(2, 11)
                user_score += card_dealt_user
                # check if user bust
                if user_score > win:
                    print(f"You have been dealt a {RED}{card_dealt_user}{RESET}")
                    print(f"{RED}You have busted.{RESET}")
                    while True:
                        restart_blackjack = input("Would you like to play again, go to bank, or new game? (p/b/n): ")
                        if restart_blackjack.lower() not in ["p", "b", "n"]:
                            print("Please select a valid input (p/b/n)")
                        elif restart_blackjack == "n":
                            home()
                        elif restart_blackjack == "b":
                            save_variables(user_name)
                        elif restart_blackjack.lower() == "p":
                            black_jack()
                            return
                elif user_score < win:
                    print("")
                    time.sleep(0.5)
                    print(f"You have been dealt a {CYAN}{card_dealt_user}{RESET}")
                    print("")
                    continue
            if user_input == "s":
                while True:

                    card_dealt_dealer = random.randint(2,11)
                    dealer_score += card_dealt_dealer
                    print("")
                    time.sleep(1)
                    print(f"The dealer dealt a {RED}{card_dealt_dealer}{RESET}")
                    print("")
                    time.sleep(1)
                    print(f"The dealer currently has {RED}{dealer_score}{RESET}")
                    print("")
                    # check if dealer score  = 21
                    if dealer_score == win:
                        print("")
                        print(f"{RED}The dealer has reached 21{RESET}")
                        while True:
                            restart_blackjack = input("Would you like to play again, go to bank, or new game? (p/b/n): ")
                            if restart_blackjack.lower() not in ["p", "b", "n"]:
                                print("Please select a valid input (p/b/n)")
                            elif restart_blackjack == "n":
                                home()
                            elif restart_blackjack == "b":
                                save_variables(user_name)
                            elif restart_blackjack.lower() == "p":
                                black_jack()
                                return
                    # check if dealer bust
                    elif dealer_score > win:
                        bet_amount_blackjack *= 2
                        total_credit += bet_amount_blackjack
                        total_credit = round(total_credit)

                        print(f"The dealer has {RED}busted{RESET}")
                        print(f"{GREEN}You have won{RESET}")
                        print(f"You won {GREEN}{bet_amount_blackjack}{RESET}")
                        while True:
                            restart_blackjack = input("Would you like to play again, go to bank, or new game? (p/b/n): ")
                            if restart_blackjack.lower() not in ["p", "b", "n"]:
                                print("Please select a valid input (p/b/n)")
                            elif restart_blackjack == "n":
                                home()
                            elif restart_blackjack == "b":
                                save_variables(user_name)
                            elif restart_blackjack.lower() == "p":
                                black_jack()
                                return
                    # check if dealer score more than user score
                    elif dealer_score > user_score:
                        print(f"{RED}You have lost.(LOSER){RESET}")
                        while True:
                            restart_blackjack = input("Would you like to play again, go to bank, or new game? (p/b/n): ")
                            if restart_blackjack.lower() not in ["p", "b", "n"]:
                                print("Please select a valid input (p/b/n)")
                            elif restart_blackjack == "n":
                                home()
                            elif restart_blackjack == "b":
                                save_variables(user_name)
                            elif restart_blackjack.lower() == "p":
                                black_jack()
                                return
                    # push
                    elif dealer_score ==  user_score:
                        total_credit += bet_amount_blackjack
                        print("You and the dealer have the same score.")
                        print(f"{YELLOW}PUSH{RESET}.")
                        while True:
                            restart_blackjack = input("Would you like to play again, go to bank, or new game? (p/b/n): ")
                            if restart_blackjack.lower() not in ["p", "b", "n"]:
                                print("Please select a valid input (p/b/n)")
                            elif restart_blackjack == "n":
                                home()
                            elif restart_blackjack == "b":
                                save_variables(user_name)
                            elif restart_blackjack.lower() == "p":
                                black_jack()
                                return

def texas_hold_em():
    print("Welcome to Texas Hold'em")

def slots():
    print("Welcome to the Slots")

def mines():
    print("Welcome to Mines")


def crash():
    global total_credit
    global user_name
    global restart_crash
    
    total_credit = round(total_credit)
    
    print(f"\nWelcome to {RED}Crash{RESET}\n")
    print(f"To play this game you have to press enter before the rocketship {RED}CRASHES!!{RESET}\n")
    time.sleep(0.5)
    print(f"You currently have {GREEN}{total_credit}{RESET} credits\n")
    
    while True:
        bet_amount_crash = float(input("How much would you like to bet: "))
        if bet_amount_crash <= 0 or bet_amount_crash > total_credit:
            print("Invalid bet amount.")
        else:
            break
        total_credit -= bet_amount_crash
        

    
    time.sleep(0.5)
    stop_flag = threading.Event()
    explode_value = skewed_random(max_value, exponent)  # Example max_value and exponent

    input_thread = threading.Thread(target=user_input_thread, args=(stop_flag,))
    input_thread.start()

    loss = display_exponential_change(explode_value, stop_flag)

    input_thread.join()

    if not loss:
        bet_amount_crash *= explode_value
        total_credit += bet_amount_crash
        temp_shown_value = round(bet_amount_crash)
        print(f"You have won {GREEN}{temp_shown_value}{RESET}")
    else:
        total_credit -= bet_amount_crash
        print(f"{RED}You have lost...{RESET}")
        print(f"The rocket has crashed at {value}.")

    while True:
        restart_crash = input("Would you like to play again, go to bank, or start a new game? (p/b/n): ")
        if restart_crash.lower() == "p":
            crash()
            return
        elif restart_crash.lower() == "b":
            save_variables(user_name)
        elif restart_crash.lower() == "n":
            home()
        else:
            print("Please select a valid input (p/b/n)")
def roulette():
    print("Welcome to Roulette")

def tower():
    print("Welcome to Tower")

# distionary of games
game_functions = {
    0: bank,
    1: dice_game,
    2: black_jack,
    3: texas_hold_em,
    4: slots,
    5: mines,
    6: crash,
    7: roulette,
    8: tower
}
class Leaderboard:
    def __init__(self):
        # Initialize an empty leaderboard
        self.leaderboard = []

    def add_entry(self, name, credits):
        # Add the new entry to the leaderboard
        self.leaderboard.append((name, credits))
        # Sort the leaderboard by credits in descending order
        self.leaderboard.sort(key=lambda x: x[1], reverse=True)

    def print_leaderboard(self):
        # Color codes for terminal output
        MAGENTA = '\033[35m'
        YELLOW = '\033[33m'
        CYAN = '\033[36m'
        RED = '\033[31m'
        RESET = '\033[0m'
        
        # Define color mapping based on rank
        color_map = {
            1: MAGENTA,
            2: YELLOW,
            3: CYAN
        }

        # Print the leaderboard
        for rank, (name, credits) in enumerate(self.leaderboard, start=1):
            color = color_map.get(rank, RED)  # Default to RED for ranks beyond 3
            print(f"{rank}.{color}{name}{RESET} {credits} CREDITS")


# Example usage
leaderboard = Leaderboard()

# Add entries
entries = [
    ("LIAM (Mr.Shootemdown)", 150),
    ("ETHAN (Owner/SwagMaster)", 121),
    ("JACK POWELL (Mothercreamer)", 102),
    ("REECE BARCLAY (Shitter/Noob Proprietor)", -25),
    ("ZACH C (Everyone HATE Zach)", -25),
    ("THEO (DingletheShoota)", -25),
    ("ISSAC (Big Money Guy)", -25),
    ("REMY (The Gamer)", -55),
    ("NICK K. (NOOB SHITTER)", -75),
    ("HARRIS JAMES (Lvl 100 Mafia NOOB)", -75),
    ("NICK F. (StreetRunnerFentQueen)", -3950),
    ("George Erdozain (FireMasterController)", -9500)
]

for name, credits in entries:
    leaderboard.add_entry(name, credits)

# Add some more entries
#additional_entries = [
    #("ALICE (Champion)", 200),
    #("BOB (Rookie)", 50)
#]





##NEED
#TO
#DO
# add blackjack sidebet if blackjack deals ace 
# automatic bank which flucations according to the positive or negative gambling trends
# automatic name to credit total
# bug fix when user prompted to pick a dice side 1-3 and 1-6
# bug fix when user goes all in and loses and doesnt hit y for play again.
# how can i fix this probably just add a check if they hit n and if total credit = 0
# blackjack ace situation bc double 11 == 22
#  blackjack needs to hit on 16 and stand 17+
def game_finished():
    print("GG")
    return
def home():
    global user_name
    global names_and_credits
    global name_given
    global total_credit
    #if name_given == True:
        #while True:
            #leaderboard_user_input = input("Would you like to stop playing.(y/n)")
            #if leaderboard_user_input.lower() not in ["y","n"]:
                #print("Invalid input")
            #elif leaderboard_user_input == "y":
                #leaderboard.add_entry(user_name,total_credit)
                #game_finished()
                #leaderboard.print_leaderboard()
                #break
            #elif leaderboard_user_input == "n":
                #game_finished()

    # Display the menu
    print("")
    print(f"Welcome to the {RED}Den of Ephemeral games{RESET}")
    print("Here is the selection of games")
    if name_given == True:
            print(f"You currently have {GREEN}{total_credit}{RESET} total CREDITS.")        
    print("")
    print(f"Bank:{GREEN}'0'{RESET}")
    print(f"Dice guesser: {GREEN}'1'{RESET}")
    print(f"Black jack: {GREEN}'2'{RESET}")
    print(f"Texas hold-em: {RED}'3'{RESET}")
    print(f"Slots: {RED}'4'{RESET}")
    print(f"Mines: {RED}'5'{RESET}")
    print(f"Crash: {GREEN}'6'{RESET}")
    print(f"Roulette: {RED}'7'{RESET}")
    print(f"Tower: {RED}'8'{RESET}")

    if name_given == False:
        total_credit = 0
        names_and_credits = extract_name_and_credits("bank.csv","")
        user_name = input("Enter your name: ")
        result = extract_name_and_credits("bank.csv", user_name)
        if result is True:
            total_credit = 0
            checker123 = True
        else:
            checker123 = False
            total_credit = 25
        name_given = True
        print(checker123)
    
    while True:
            game_selection = int(input("Which game would you like to play (type in the number next to the word): "))

            # Check if the selected game is valid

            if game_selection in game_functions:

                # Call the appropriate game function
                if total_credit == 0:
                    print("You have zero credits You are not allowed to play, you are going to the bank")
                    time.sleep(1)
                    save_variables(user_name)
                    
                game_functions[game_selection]()
                return
            else:
                print("Invalid selection. Please enter a number between 0 and 8.")
user_name = ""   
names_and_credits = {}
names_and_profit_loss = {}
name_given = False

home()
# Now make the leaderboard function with the last cloumn of bank.csv 
# prob just chatgpt
# for the leaderboard function make the orginal value - the new value(after they're done playing) to get the profit
# maybe make it so if its negative only show it