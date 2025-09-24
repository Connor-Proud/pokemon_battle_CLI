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
    from bcknd.functions import get_pokemon_moves, initialize_pokemon_moves_with_pp
    from random import choice

    DIR= os.path.dirname(os.path.abspath(__file__)) # find whatever the directory of the current file is

    lib = ctypes.CDLL(os.path.join(DIR, "bcknd", "test_.dll")) # load it as our awesome sauce dll which calculates damage
    lib.dmg_calc.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    lib.dmg_calc.restype = ctypes.c_int
    
    # Read Pokemon data
    df=pd.read_csv(r"files/pokemon.csv")
    
    # Get player Pokemon stats
    player_row = df[df[" Name"]==pokemon_choice]
    player_hp = player_row[" HP"].values[0]
    player_max_hp = player_hp
    
    # Get opponent Pokemon stats
    opp_row = df[df[" Name"]==opp]
    opponent_hp = opp_row[" HP"].values[0]
    opponent_max_hp = opponent_hp
    
    # Initialize moves with PP for both Pokemon
    player_moves = initialize_pokemon_moves_with_pp(pokemon_choice)
    opponent_moves = initialize_pokemon_moves_with_pp(opp)
    
    # Display initial move info
    print(f"\n{pokemon_choice}'s moves:")
    for move_name, move_data in player_moves.items():
        print(f"  {move_name}: {move_data['current_pp']}/{move_data['max_pp']} PP")
    
    print(f"{pokemon_choice} HP: {player_hp}/{player_max_hp}")
    print(f"{opp} HP: {opponent_hp}/{opponent_max_hp}")
    
    battle_over = False
    
    while not battle_over:
        # Check if player has any moves with PP left
        available_moves = [move for move, data in player_moves.items() if data['current_pp'] > 0]
        
        if not available_moves:
            print(f"\n{pokemon_choice} has no moves left! {pokemon_choice} struggles but can't attack!")
            print(f"{pokemon_choice} fainted from exhaustion!")
            print(f"{opp} wins the battle!")
            battle_over = True
            break
        
        # Player turn
        print(f"\n--- {pokemon_choice}'s turn ---")
        print("What will you use?")
        
        # Display available moves with PP
        print("Available moves:")
        for move_name, move_data in player_moves.items():
            if move_data['current_pp'] > 0:
                print(f"  {Fore.GREEN}{move_name}: {move_data['current_pp']}/{move_data['max_pp']} PP{Style.RESET_ALL}")
            else:
                print(f"  {Fore.RED}{move_name}: 0/{move_data['max_pp']} PP (No PP left!){Style.RESET_ALL}")
        
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
            
        # Check if the Pokémon knows this move
        if move_choice not in player_moves:
            print(f"Invalid move! {pokemon_choice} doesn't know {move_choice}")
            print(f"Available moves: {', '.join(available_moves)}")
            continue
        
        # Check if the move has PP left
        if player_moves[move_choice]['current_pp'] <= 0:
            print(f"{move_choice} has no PP left! Choose another move.")
            continue
            
        # Use the move - deduct PP
        player_moves[move_choice]['current_pp'] -= 1
        print(f"{pokemon_choice} used {move_choice}! (PP: {player_moves[move_choice]['current_pp']}/{player_moves[move_choice]['max_pp']})")
        
        # Calculate player damage
        player_damage = lib.dmg_calc(pokemon_choice.encode('utf-8'), opp.encode('utf-8'), move_choice.encode('utf-8'))
        
        if player_damage == -1:
            print(f"{pokemon_choice}'s attack missed!")
        elif player_damage == -2:
            print("Error calculating damage!")
            continue
        else:
            opponent_hp -= player_damage
            print(f"You dealt {player_damage} damage!")
            
            if opponent_hp <= 0:
                opponent_hp = 0
                print(f"\n{opp} fainted!")
                print(f"🎉 {pokemon_choice} wins the battle! 🎉")
                battle_over = True
                break
            else:
                print(f"{opp} HP: {opponent_hp}/{opponent_max_hp}")
        
        # Opponent turn (if still alive)
        if not battle_over:
            print(f"\n--- {opp}'s turn ---")
            
            # AI chooses a random move from available moves (with PP > 0)
            available_opp_moves = [move for move, data in opponent_moves.items() if data['current_pp'] > 0]
            
            if not available_opp_moves:
                print(f"{opp} has no moves left! {opp} struggles but can't attack!")
                print(f"{opp} fainted from exhaustion!")
                print(f"🎉 {pokemon_choice} wins by default! 🎉")
                battle_over = True
                break
            
            opponent_move = choice(available_opp_moves)
            opponent_moves[opponent_move]['current_pp'] -= 1
            print(f"{opp} used {opponent_move}! (PP: {opponent_moves[opponent_move]['current_pp']}/{opponent_moves[opponent_move]['max_pp']})")
            
            # Calculate opponent damage
            opponent_damage = lib.dmg_calc(opp.encode('utf-8'), pokemon_choice.encode('utf-8'), opponent_move.encode('utf-8'))
            
            if opponent_damage == -1:
                print(f"{opp}'s attack missed!")
            elif opponent_damage == -2:
                print("Error calculating opponent damage!")
            else:
                player_hp -= opponent_damage
                print(f"{opp} dealt {opponent_damage} damage!")
                
                if player_hp <= 0:
                    player_hp = 0
                    print(f"\n{pokemon_choice} fainted!")
                    print(f"{opp} wins the battle!")
                    battle_over = True
                else:
                    print(f"{pokemon_choice} HP: {player_hp}/{player_max_hp}")
        
        # Show current HP status if battle continues
        if not battle_over:
            print(f"\n--- Battle Status ---")
            print(f"{pokemon_choice}: {player_hp}/{player_max_hp} HP")
            print(f"{opp}: {opponent_hp}/{opponent_max_hp} HP")
            
            # Show remaining PP for player's moves
            print(f"\n{pokemon_choice}'s PP Status:")
            for move_name, move_data in player_moves.items():
                if move_data['current_pp'] > 0:
                    print(f"  {move_name}: {move_data['current_pp']}/{move_data['max_pp']} PP")
                else:
                    print(f"  {Fore.RED}{move_name}: 0/{move_data['max_pp']} PP{Style.RESET_ALL}")


def rich_battle(pokemon_choice, opp):
    """Enhanced battle system using rich library for better UI"""
    import pandas as pd
    import ctypes
    import os
    import random
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    from rich.panel import Panel
    from time import sleep
    from bcknd.functions import initialize_pokemon_moves_with_pp, playsound, play_hit_sound

    console = Console()
    
    DIR = os.path.dirname(os.path.abspath(__file__))
    lib = ctypes.CDLL(os.path.join(DIR, "bcknd", "test_.dll"))
    lib.dmg_calc.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    lib.dmg_calc.restype = ctypes.c_int
    
    # Read Pokemon data
    df = pd.read_csv(r"files/pokemon.csv")
    
    # Get player Pokemon stats
    player_row = df[df[" Name"] == pokemon_choice]
    player_pokemon = {
        "name": pokemon_choice,
        "hp": int(player_row[" HP"].values[0]),
        "max_hp": int(player_row[" HP"].values[0]),
        "moves": initialize_pokemon_moves_with_pp(pokemon_choice)
    }
    
    # Get opponent Pokemon stats
    opp_row = df[df[" Name"] == opp]
    opponent_pokemon = {
        "name": opp,
        "hp": int(opp_row[" HP"].values[0]),
        "max_hp": int(opp_row[" HP"].values[0]),
        "moves": initialize_pokemon_moves_with_pp(opp)
    }
    
    def get_hp_bar(pokemon, width=30):
        """Create a visual HP bar"""
        hp_ratio = pokemon["hp"] / pokemon["max_hp"]
        filled_length = int(width * hp_ratio)
        empty_length = width - filled_length

        bar = Text()
        if hp_ratio > 0.5:
            bar.append("█" * filled_length, style="bold green")
        elif hp_ratio > 0.2:
            bar.append("█" * filled_length, style="bold yellow")
        else:
            bar.append("█" * filled_length, style="bold red")
        bar.append("░" * empty_length, style="dim")

        return bar
    
    def show_battle_status():
        """Display current battle status"""
        table = Table(title="🔥 Battle Arena 🔥", show_lines=True, expand=True)
        table.add_column("Your Pokémon", justify="center", style="bold blue")
        table.add_column("Wild Pokémon", justify="center", style="bold red")

        player_hp_bar = get_hp_bar(player_pokemon)
        opponent_hp_bar = get_hp_bar(opponent_pokemon)

        player_text = Text(f"{player_pokemon['name']}\n", style="bold blue") + player_hp_bar + Text(f"\n{player_pokemon['hp']}/{player_pokemon['max_hp']} HP")
        opponent_text = Text(f"{opponent_pokemon['name']}\n", style="bold red") + opponent_hp_bar + Text(f"\n{opponent_pokemon['hp']}/{opponent_pokemon['max_hp']} HP")

        table.add_row(player_text, opponent_text)
        console.print(table)
    
    def choose_move(pokemon, is_ai=False):
        """Let player choose a move or AI pick randomly"""
        moves = pokemon["moves"]
        available_moves = [name for name, stats in moves.items() if stats["current_pp"] > 0]
        
        if not available_moves:
            return None
        
        if is_ai:
            return random.choice(available_moves)
        else:
            while True:
                # Create moves table
                moves_table = Table(title=f"{pokemon['name']}'s Moves", show_header=True)
                moves_table.add_column("No.", justify="right", style="cyan")
                moves_table.add_column("Move", style="bold")
                moves_table.add_column("PP", justify="center")
                moves_table.add_column("Status", justify="center")
                
                move_list = list(moves.items())
                for i, (move_name, stats) in enumerate(move_list, 1):
                    pp_text = f"{stats['current_pp']}/{stats['max_pp']}"
                    if stats['current_pp'] > 0:
                        status = Text("Available", style="bold green")
                        moves_table.add_row(str(i), move_name, pp_text, status)
                    else:
                        status = Text("No PP", style="bold red")
                        moves_table.add_row(str(i), move_name, pp_text, status, style="dim")
                
                console.print(moves_table)
                
                user_input = console.input("Choose a move [1-{}]: ".format(len(move_list))).strip()
                if user_input.isdigit():
                    choice = int(user_input)
                    if 1 <= choice <= len(move_list):
                        move_name = move_list[choice - 1][0]
                        if moves[move_name]['current_pp'] > 0:
                            return move_name
                        else:
                            console.print("[red]That move has no PP left! Choose another.[/red]")
                            continue
                console.print("[red]Invalid input. Please enter a valid move number.[/red]")
    
    def apply_move(attacker, defender, move_name, is_player_attacking=True):
        """Apply move effects using the DLL for damage calculation"""
        if move_name is None:
            console.print(Panel(f"[red]{attacker['name']} has no moves left and struggles![/red]", 
                              title="No Moves!", border_style="red"))
            return 0
        
        move = attacker["moves"][move_name]
        if move["current_pp"] <= 0:
            console.print(Panel(f"[red]{move_name} has no PP left![/red]", 
                              title="Out of PP!", border_style="red"))
            return 0
        
        # Deduct PP
        move["current_pp"] -= 1
        
        # Play move sound effect
        try:
            playsound(move_name)
        except Exception as e:
            console.print(f"[dim]Sound error: {e}[/dim]")  # Debug output
        
        # Calculate damage using DLL
        damage = lib.dmg_calc(attacker["name"].encode('utf-8'), 
                             defender["name"].encode('utf-8'), 
                             move_name.encode('utf-8'))
        
        if damage == -1:
            console.print(Panel(f"[yellow]{attacker['name']} used {move_name}![/yellow]\n[dim]The attack missed![/dim]", 
                              title="Move Used", border_style="yellow"))
            return 0
        elif damage == -2:
            console.print(Panel(f"[red]Error calculating damage for {move_name}![/red]", 
                              title="Error", border_style="red"))
            return 0
        else:
            defender["hp"] = max(defender["hp"] - damage, 0)
            
            # Play hit sound if damage is dealt to the player
            if not is_player_attacking and damage > 0:
                try:
                    play_hit_sound(damage)
                except Exception as e:
                    console.print(f"[dim]Hit sound error: {e}[/dim]")  # Debug output
            
            console.print(Panel(f"[bold]{attacker['name']} used {move_name}![/bold]\n[green]It dealt {damage} damage![/green]\nPP: {move['current_pp']}/{move['max_pp']}", 
                              title="Move Used", border_style="green"))
            return damage
    
    # Start the battle
    console.clear()
    console.print(Panel(f"[bold cyan]A wild {opp} appeared![/bold cyan]", title="Wild Encounter!", border_style="cyan"))
    console.print(f"[bold blue]{pokemon_choice}, I choose you![/bold blue]\n")
    
    battle_over = False
    turn_count = 0
    
    while not battle_over:
        turn_count += 1
        console.clear()
        
        # Check win conditions
        if player_pokemon["hp"] <= 0:
            console.print(Panel(f"[red]{player_pokemon['name']} fainted![/red]\n[bold red]{opponent_pokemon['name']} wins![/bold red]", 
                              title="Battle Over!", border_style="red"))
            battle_over = True
            break
        
        if opponent_pokemon["hp"] <= 0:
            console.print(Panel(f"[green]{opponent_pokemon['name']} fainted![/green]\n[bold green]🎉 {player_pokemon['name']} wins! 🎉[/bold green]", 
                              title="Victory!", border_style="green"))
            battle_over = True
            break
        
        # Show battle status
        console.rule(f"[bold]Turn {turn_count}[/bold]")
        show_battle_status()
        
        # Player turn
        console.rule("[bold blue]Your Turn[/bold blue]")
        player_move = choose_move(player_pokemon)
        
        if player_move is None:
            console.print(Panel(f"[red]{player_pokemon['name']} has no moves left![/red]\n[red]{player_pokemon['name']} fainted from exhaustion![/red]", 
                              title="Out of Moves!", border_style="red"))
            console.print(Panel(f"[bold red]{opponent_pokemon['name']} wins![/bold red]", 
                              title="Battle Over!", border_style="red"))
            battle_over = True
            break
        
        apply_move(player_pokemon, opponent_pokemon, player_move, is_player_attacking=True)
        
        # Check if opponent fainted
        if opponent_pokemon["hp"] <= 0:
            console.clear()
            show_battle_status()
            console.print(Panel(f"[green]{opponent_pokemon['name']} fainted![/green]\n[bold green]🎉 {player_pokemon['name']} wins! 🎉[/bold green]", 
                              title="Victory!", border_style="green"))
            battle_over = True
            break
        
        # Opponent turn
        console.rule("[bold red]Opponent's Turn[/bold red]")
        show_battle_status()
        
        opponent_move = choose_move(opponent_pokemon, is_ai=True)
        
        if opponent_move is None:
            console.print(Panel(f"[green]{opponent_pokemon['name']} has no moves left![/green]\n[green]{opponent_pokemon['name']} fainted from exhaustion![/green]", 
                              title="Opponent Out of Moves!", border_style="green"))
            console.print(Panel(f"[bold green]🎉 {player_pokemon['name']} wins by default! 🎉[/bold green]", 
                              title="Victory!", border_style="green"))
            battle_over = True
            break
        
        apply_move(opponent_pokemon, player_pokemon, opponent_move, is_player_attacking=False)
        
        # Check if player fainted
        if player_pokemon["hp"] <= 0:
            console.clear()
            show_battle_status()
            console.print(Panel(f"[red]{player_pokemon['name']} fainted![/red]\n[bold red]{opponent_pokemon['name']} wins![/bold red]", 
                              title="Defeat!", border_style="red"))
            battle_over = True
            break
    
    # Final message
    console.print("\n[dim]Press any key to continue...[/dim]")
    console.input("")


def user():
    from time import sleep
    from bcknd.users import user_create, login_user
    
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

from bcknd.functions import get_random_pokemon

opp = get_random_pokemon()
print(f"A wild {opp} has appeared!")

# Choose battle UI
# print("\nChoose battle system:")
# print("1. Standard UI (for testing)")
# print("2. Enhanced Rich UI")

# while True:
#     try:
#         ui_choice = input("Enter your choice (1 or 2): ").strip()
#         if ui_choice == "1":
#             print("Starting battle with standard UI...")
#             test_battle(pokemon, opp)
#             break
#         elif ui_choice == "2":
#             print("Starting battle with enhanced UI...")
#             rich_battle(pokemon, opp)
#             break
#         else:
#             print("Please enter 1 or 2.")
#     except KeyboardInterrupt:
#         print("\nExiting...")
#         break


rich_battle(pokemon, opp)