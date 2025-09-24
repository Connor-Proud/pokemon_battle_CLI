import pandas as pd
import keyboard as kb, os
from colorama import Fore, Back, Style

options = ["Bulbasaur", "Charmander", "Squirtle"]
current_option = 0

def clear():
    os.system("cls")

def starter_menu():
    clear()
    print("Choose your starter:")
    for i, option in enumerate(options):
        if i == current_option:
            print(f"{Fore.BLACK}{Back.WHITE}[{option}]{Style.RESET_ALL}")
        else:
            print(f"[{option}]")


def test_battle(pokemon_choice,opp):
    import pandas as pd
    import ctypes
    import os
    from functions import get_pokemon_moves

    DIR= os.path.dirname(os.path.abspath(__file__)) # find whatever the directory of the current file is

    lib = ctypes.CDLL(os.path.join(DIR, "test_.dll")) # load it as our awesome sauce dll which calculates damage
    lib.dmg_calc.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    lib.dmg_calc.restype = ctypes.c_int
    opponent_death = False
    df=pd.read_csv(os.path.join(DIR, "files", "pokemon.csv"))  # Use absolute path based on script location
    name=opp.capitalize()
    charmander_row = df[df[" Name"]==name]
    opponent_hp=charmander_row[" HP"].values[0]
    
    # Get available moves for the player's Pokémon
    available_moves = get_pokemon_moves(pokemon_choice)
    print(f"\n{pokemon_choice}'s available moves: {', '.join(available_moves)}")
    
    while not opponent_death:
        print("\nit is your move, what will you use?")
        
        # Clear input buffer to prevent issues
        import sys
        if sys.platform == "win32":
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        
        move_choice = input("Enter the move you want to use: ").strip()
        
        # Check if move is empty
        if not move_choice:
            print("Please enter a move name!")
            continue
            
        # Check if the Pokémon can use this move
        if move_choice not in available_moves:
            print(f"Invalid move! {pokemon_choice} can't use {move_choice}")
            print(f"Available moves: {', '.join(available_moves)}")
            continue
            
        print(f"You used {move_choice}")
        dealt=lib.dmg_calc(pokemon_choice.encode('utf-8'), f"{opp}".encode('utf-8'), move_choice.encode('utf-8')    )
        if dealt == -1:
            print("miss")
            continue
        if dealt == -2:
            print("invalid move")
            continue
        opponent_hp -= dealt
        if opponent_hp <= 0:
            opponent_death = True
            print(f"{opp} fainted!")
        else:
            print(f"you dealt: {dealt}\n {opp} is now at {opponent_hp}")


def user():
    from time import sleep
    from users import user_create, login_user
    
    # User menu options
    user_options = ["Create user", "Login"]
    current_user_option = 0
    
    def user_menu():
        clear()
        print("please choose some option:")
        for i, option in enumerate(user_options):
            if i == current_user_option:
                print(f"{Fore.BLACK}{Back.WHITE}[{option}]{Style.RESET_ALL}")
            else:
                print(f"[{option}]")
        print("\nUse ↑/↓ arrows to navigate, Enter to select")
    
    # Display user menu and handle navigation
    user_menu()
    while True:
        event = kb.read_event()
        if event.event_type == kb.KEY_DOWN:
            if event.name == "down":
                current_user_option = (current_user_option + 1) % len(user_options)
                user_menu()
            elif event.name == "up":
                current_user_option = (current_user_option - 1) % len(user_options)
                user_menu()
            elif event.name == "enter":
                break
    
    clear()
    
    # Clear any remaining keyboard input from the buffer
    import sys
    if sys.platform == "win32":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        # For other platforms, use a simple delay
        sleep(0.2)
    
    
    if current_user_option == 0:  # Create user
        print("Creating new user...")
        username = input("Enter username: ")
        password = input("Enter password: ")
        team_input = input("Enter up to 6 Pokémon names separated by commas: ")
        pokemon_team = [p.strip().capitalize() for p in team_input.split(",") if p.strip()]
        user_create(username, password, pokemon_team)
        sleep(1)
        return username
    else:  # Login
        print("User login...")
        username = input("Enter username: ")
        password = input("Enter password: ")
        login_user(username, password)
        sleep(1)
        return username






username = user()
starter_menu()

while True:
    event = kb.read_event()
    if event.event_type == kb.KEY_DOWN:
        if event.name == "down":
            current_option = (current_option + 1) % len(options)
            starter_menu()
        elif event.name == "up":
            current_option = (current_option - 1) % len(options)
            starter_menu()
        elif event.name == "enter":
            clear()
            print(f"You selected: {options[current_option]}")
            print("Would you like to continue with " + options[current_option] + "? (" + "\u0332Y" + "es/" "\u0332N" + "o)")
            while True:
                event = kb.read_event()
                if event.event_type == kb.KEY_DOWN:
                    if event.name == "y":
                        clear()
                        pokemon = options[current_option]
                        print(f"Great! You chose {pokemon} as your starter.")
                        break
                    elif event.name == "n":
                        starter_menu()
                        break
            if event.name == "y":   
                break

pokemon = options[current_option]

#opp = "MISSINGNO" # Placeholder, will be collected from the backend later

# yeah raven, lets get the opps

from functions import get_random_pokemon

opp = get_random_pokemon()
print(f"A wild {opp} has appeared!")
test_battle(pokemon, opp)