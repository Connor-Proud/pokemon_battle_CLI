#    Copyright 2025 Connor Proudlock, Raven Kirkham, James Smith, Kian Watt

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.



#import pandas as pd
import keyboard as kb, os
from colorama import Fore, Back, Style
import getpass
from time import sleep
from bcknd.functions import playsound

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
                print(f"{pokemon_choice} wins the battle!")
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
                print(f"{pokemon_choice} wins by default!")
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


def main_battle(pokemon_choice, opp, team, position, username):
    """Enhanced battle system using rich library for better UI with multi-Pokemon support"""
    import pandas as pd
    import ctypes
    import os
    import random
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    from rich.panel import Panel
    #from time import sleep
    from bcknd.functions import initialize_pokemon_moves_with_pp, playsound, play_hit_sound
    import sys
    if sys.platform == "win32":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    console = Console()
    
    DIR = os.path.dirname(os.path.abspath(__file__))
    lib = ctypes.CDLL(os.path.join(DIR, "bcknd", "test_.dll"))
    lib.dmg_calc.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    lib.dmg_calc.restype = ctypes.c_int
    
    # Read Pokemon data
    df = pd.read_csv(r"files/pokemon.csv")
    
    # Initialize team status - track which Pokemon are still available
    team_status = {}
    for i, pokemon_name in enumerate(team):
        pokemon_row = df[df[" Name"] == pokemon_name]
        team_status[pokemon_name] = {
            "position": i,
            "fainted": False,
            "max_hp": int(pokemon_row[" HP"].values[0])
        }
    
    # Initialize current player Pokemon
    def initialize_pokemon(pokemon_name):
        pokemon_row = df[df[" Name"] == pokemon_name]
        return {
            "name": pokemon_name,
            "hp": int(pokemon_row[" HP"].values[0]),
            "max_hp": int(pokemon_row[" HP"].values[0]),
            "moves": initialize_pokemon_moves_with_pp(pokemon_name)
        }
    
    player_pokemon = initialize_pokemon(pokemon_choice)
    
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
        table = Table(title="Battle Arena", show_lines=True, expand=True)
        table.add_column("Your Pokémon", justify="center", style="bold blue")
        table.add_column("Wild Pokémon", justify="center", style="bold red")

        player_hp_bar = get_hp_bar(player_pokemon)
        opponent_hp_bar = get_hp_bar(opponent_pokemon)

        player_text = Text(f"{player_pokemon['name']}\n", style="bold blue") + player_hp_bar + Text(f"\n{player_pokemon['hp']}/{player_pokemon['max_hp']} HP")
        opponent_text = Text(f"{opponent_pokemon['name']}\n", style="bold red") + opponent_hp_bar + Text(f"\n{opponent_pokemon['hp']}/{opponent_pokemon['max_hp']} HP")

        table.add_row(player_text, opponent_text)
        console.print(table)
    
    def choose_battle_action(pokemon, bag, team_status):
        """Let player choose between using a move or an item"""
        from bcknd.functions import get_available_items, use_item_on_pokemon
        
        while True:
            # Create action menu
            console.print("\n" + "─" * 60)
            console.print(f"What will {pokemon['name']} do?")
            console.print("─" * 60)
            console.print("1. Use Move")
            console.print("2. Use Item")
            console.print("─" * 60)
            
            action_choice = console.input("Choose an action [1-2]: ").strip()
            
            if action_choice == "1":
                # Use move
                move = choose_move(pokemon, is_ai=False)
                return {"type": "move", "move": move}
            
            elif action_choice == "2":
                # Use item
                available_items = get_available_items(bag, in_battle=True)
                
                if not available_items:
                    console.print("[red]You don't have any usable items![/red]")
                    continue
                
                # Show available items
                console.print("\nAvailable Items:")
                for i, item in enumerate(available_items, 1):
                    if item["usable_in_battle"]:
                        console.print(f"{i}. {item['name']} x{item['count']}")
                
                console.print(f"{len(available_items) + 1}. Go Back")
                
                item_choice = console.input(f"Choose an item [1-{len(available_items) + 1}]: ").strip()
                
                if item_choice.isdigit():
                    choice_num = int(item_choice)
                    if choice_num == len(available_items) + 1:
                        continue  # Go back to action menu
                    elif 1 <= choice_num <= len(available_items):
                        selected_item = available_items[choice_num - 1]
                        if selected_item["usable_in_battle"]:
                            # Use item on current Pokemon
                            success, message, updated_bag = use_item_on_pokemon(
                                selected_item["name"], pokemon, bag, team_status
                            )
                            console.print(f"[green]{message}[/green]" if success else f"[red]{message}[/red]")
                            if success:
                                return {"type": "item", "item": selected_item["name"], "bag": updated_bag}
                            # If item use failed, continue to let player choose again
                        else:
                            console.print("[red]This item cannot be used in battle![/red]")
            else:
                console.print("[red]Invalid choice. Please enter 1 or 2.[/red]")

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
    
    def get_available_pokemon():
        """Get list of Pokemon that haven't fainted"""
        return [name for name, status in team_status.items() if not status["fainted"]]
    
    def choose_next_pokemon():
        """Let player choose their next Pokemon after one faints"""
        available = get_available_pokemon()
        if len(available) <= 0:  # Only current Pokemon or no Pokemon left
            return None
            
        console.print(Panel("[yellow]Choose your next Pokémon![/yellow]", title="Switch Pokémon", border_style="yellow"))
        
        # Create selection table
        switch_table = Table(title="Available Pokémon", show_header=True)
        switch_table.add_column("No.", justify="right", style="cyan")
        switch_table.add_column("Pokémon", style="bold")
        switch_table.add_column("Status", justify="center")
        
        selectable_pokemon = [name for name in available if name != player_pokemon["name"]]
        
        if not selectable_pokemon:
            return None
            
        for i, pokemon_name in enumerate(selectable_pokemon, 1):
            status = Text("Ready", style="bold green")
            switch_table.add_row(str(i), pokemon_name, status)
        
        console.print(switch_table)
        
        while True:
            user_input = console.input(f"Choose a Pokémon [1-{len(selectable_pokemon)}]: ").strip()
            if user_input.isdigit():
                choice = int(user_input)
                if 1 <= choice <= len(selectable_pokemon):
                    return selectable_pokemon[choice - 1]
            console.print("[red]Invalid choice. Please try again.[/red]")
    
    def switch_pokemon(new_pokemon_name):
        """Switch to a new Pokemon"""
        nonlocal player_pokemon
        
        # Mark current Pokemon as fainted
        team_status[player_pokemon["name"]]["fainted"] = True
        
        # Initialize new Pokemon
        player_pokemon = initialize_pokemon(new_pokemon_name)
        
        console.print(Panel(f"[bold blue]Go, {new_pokemon_name}![/bold blue]", 
                          title="Pokémon Switch", border_style="blue"))
        return True
    
    # Start the battle
    console.clear()
    console.print(Panel(f"[bold cyan]A wild {opp} appeared![/bold cyan]", title="Wild Encounter!", border_style="cyan"))
    console.print(f"[bold blue]{pokemon_choice}, I choose you![/bold blue]\n")
    
    # Load player's inventory for battle use
    from bcknd.users import load_user_inventory
    bag, current_coins = load_user_inventory(username)
    
    battle_over = False
    turn_count = 0
    
    while not battle_over:
        turn_count += 1
        console.clear()
        
        # Check win conditions
        if player_pokemon["hp"] <= 0:
            # Player Pokemon fainted - check if they have other Pokemon
            console.print(Panel(f"[red]{player_pokemon['name']} fainted![/red]", 
                              title="Pokémon Fainted!", border_style="red"))
            
            # Mark current Pokemon as fainted
            team_status[player_pokemon["name"]]["fainted"] = True
            
            # Check if player has any Pokemon left
            available_pokemon = get_available_pokemon()
            
            if not available_pokemon:
                # No Pokemon left - player loses
                console.print(Panel(f"[bold red]All your Pokémon have fainted!\n{opponent_pokemon['name']} wins the battle![/bold red]", 
                              title="Battle Over!", border_style="red"))
                battle_over = True
                break
            else:
                # Player can switch Pokemon
                next_pokemon = choose_next_pokemon()
                if next_pokemon:
                    switch_pokemon(next_pokemon)
                    continue  # Skip opponent turn, give player a free switch
                else:
                    # Somehow no Pokemon to switch to
                    console.print(Panel(f"[bold red]No Pokémon available to switch!\n{opponent_pokemon['name']} wins![/bold red]", 
                                  title="Battle Over!", border_style="red"))
                    battle_over = True
                    break
        
        if opponent_pokemon["hp"] <= 0:
            console.print(Panel(f"[green]{opponent_pokemon['name']} fainted![/green]\n[bold green]{player_pokemon['name']} wins![/bold green]", 
                              title="Victory!", border_style="green"))
            battle_over = True
            break
        
        # Show battle status
        console.rule(f"[bold]Turn {turn_count}[/bold]")
        show_battle_status()
        
        # Player turn
        console.rule("[bold blue]Your Turn[/bold blue]")
        
        # Get player's action choice (move or item)
        action_result = choose_battle_action(player_pokemon, bag, team_status)
        
        if action_result["type"] == "item":
            # Update bag after item use
            bag = action_result["bag"]
            # Save inventory immediately after item use
            from bcknd.users import save_user_inventory
            save_user_inventory(username, bag, current_coins)
            # Item turn ends here, player used an item
            player_move = None  # No move to execute
        elif action_result["type"] == "move":
            player_move = action_result["move"]
        
        if player_move is None:
            # Player Pokemon has no moves left
            console.print(Panel(f"[red]{player_pokemon['name']} has no moves left![/red]", 
                              title="Out of Moves!", border_style="red"))
            
            # Mark current Pokemon as fainted from exhaustion
            team_status[player_pokemon["name"]]["fainted"] = True
            
            # Check if player has any Pokemon left
            available_pokemon = get_available_pokemon()
            
            if not available_pokemon:
                # No Pokemon left - player loses
                console.print(Panel(f"[bold red]All your Pokémon are unable to battle!\n{opponent_pokemon['name']} wins![/bold red]", 
                              title="Battle Over!", border_style="red"))
                battle_over = True
                break
            else:
                # Player can switch Pokemon
                next_pokemon = choose_next_pokemon()
                if next_pokemon:
                    switch_pokemon(next_pokemon)
                    continue  # Skip this turn, give player a free switch
                else:
                    # No Pokemon to switch to
                    console.print(Panel(f"[bold red]No Pokémon available to switch!\n{opponent_pokemon['name']} wins![/bold red]", 
                                  title="Battle Over!", border_style="red"))
                    battle_over = True
                    break
        
        # Apply player's move if they used one (not an item)
        if player_move is not None:
            apply_move(player_pokemon, opponent_pokemon, player_move, is_player_attacking=True)
        
        # Check if opponent fainted
        if opponent_pokemon["hp"] <= 0:
            console.clear()
            show_battle_status()
            console.print(Panel(f"[green]{opponent_pokemon['name']} fainted![/green]\n[bold green]{player_pokemon['name']} wins![/bold green]", 
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
            console.print(Panel(f"[bold green]{player_pokemon['name']} wins by default![/bold green]", 
                              title="Victory!", border_style="green"))
            battle_over = True
            break
        
        apply_move(opponent_pokemon, player_pokemon, opponent_move, is_player_attacking=False)
        
        # Check if player fainted after opponent's attack
        if player_pokemon["hp"] <= 0:
            console.clear()
            show_battle_status()
            console.print(Panel(f"[red]{player_pokemon['name']} fainted![/red]", 
                              title="Pokémon Fainted!", border_style="red"))
            
            # Mark current Pokemon as fainted
            team_status[player_pokemon["name"]]["fainted"] = True
            
            # Check if player has any Pokemon left
            available_pokemon = get_available_pokemon()
            
            if not available_pokemon:
                # No Pokemon left - player loses
                console.print(Panel(f"[bold red]All your Pokémon have fainted!\n{opponent_pokemon['name']} wins the battle![/bold red]", 
                              title="Battle Over!", border_style="red"))
                battle_over = True
                break
            else:
                # Player can switch Pokemon
                next_pokemon = choose_next_pokemon()
                if next_pokemon:
                    switch_pokemon(next_pokemon)
                    # Continue to next turn
                else:
                    # No Pokemon to switch to
                    console.print(Panel(f"[bold red]No Pokémon available to switch!\n{opponent_pokemon['name']} wins![/bold red]", 
                                  title="Battle Over!", border_style="red"))
                    battle_over = True
                    break
    
    # Final message
    console.print("\n[dim]Press any key to continue...[/dim]")
    console.input("")

    # Battle conclusion - determine if player won
    player_won = opponent_pokemon["hp"] <= 0
    
    # Calculate and award battle rewards
    from bcknd.functions import calculate_battle_reward, pokemon_catch_system
    
    # Calculate pokecoin reward
    coins_earned = calculate_battle_reward(opponent_pokemon["name"], player_won)
    current_coins += coins_earned  # Add battle reward to existing coins
    
    # Pokemon catching system (only if player won and has pokeballs)
    caught_pokemon = ""
    if player_won:
        # Give player some pokeballs if they don't have any for first-time players
        if bag.get("pokeballs", 0) == 0:
            bag["pokeballs"] = 3  # Start with 3 pokeballs
            console.print(Panel("[yellow] You found 3 Pokeballs in your bag![/yellow]", 
                              title="Items Found", border_style="yellow"))
        
        # Attempt to catch the defeated Pokemon
        caught, updated_bag, caught_name = pokemon_catch_system(opponent_pokemon["name"], bag)
        bag = updated_bag
        if caught:
            caught_pokemon = caught_name
            # Add the Pokemon to the player's team in the database
            from bcknd.users import add_pokemon_to_team
            if add_pokemon_to_team(username, caught_pokemon):
                console.print(Panel(f"[green]{caught_pokemon} added to your team![/green]", 
                                  title="Pokemon Caught!", border_style="green"))
            else:
                console.print(Panel(f"[yellow]{caught_pokemon} was caught but your team is full!\nConsider releasing a Pokemon to make space.[/yellow]", 
                                  title="Team Full!", border_style="yellow"))

    # Save updated inventory to database
    from bcknd.users import save_user_inventory
    save_user_inventory(username, bag, current_coins)
    
    # Post-battle menu system
    return post_battle_menu(current_coins, bag, username, team)


def post_battle_menu(current_coins, bag, username, team):
    """
    Handle post-battle choices: continue battling, shop (if available), or exit
    Returns True if player wants to continue, False to exit
    """
    import random
    import keyboard as kb
    from bcknd.functions import shop_system, get_scaled_pokemon
    
    # Check if shop event is triggered
    shop_available = random.randint(1, 10) >= 7  # 40% chance to find a shop
    
    if shop_available:
        # Shop event - 3 options
        menu_options = ["Enter Shop", "Battle Again", "Exit Game"]
        menu_title = "You found a shop on your journey!"
    else:
        # No shop - 2 options
        menu_options = ["Battle Again", "Exit Game"]
        menu_title = "What would you like to do next?"
    
    current_option = 0
    
    def post_battle_display():
        clear()
        print("═" * 60)
        print(f"                {menu_title}")
        print("═" * 60)
        print(f"Current Pokecoins: {current_coins}")
        print(f"Pokeballs: {bag.get('pokeballs', 0)} | Items: {sum(bag.values()) - bag.get('pokeballs', 0)}")
        print("═" * 60)
        print()
        print("What would you like to do?")
        print()
        for i, option in enumerate(menu_options):
            if i == current_option:
                print(f"{Fore.BLACK}{Back.WHITE}► {option}{Style.RESET_ALL}")
            else:
                print(f"  {option}")
        print()
        print("Use ↑/↓ arrows to navigate, Enter to select")
        print("═" * 60)
    
    post_battle_display()
    
    while True:
        event = kb.read_event()
        if event.event_type == kb.KEY_DOWN:
            if event.name == "down":
                playsound("button Hover")
                current_option = (current_option + 1) % len(menu_options)
                post_battle_display()
            elif event.name == "up":
                playsound("button Hover")
                current_option = (current_option - 1) % len(menu_options)
                post_battle_display()
            elif event.name == "enter":
                playsound("button click")
                selected_option = menu_options[current_option]
                
                if selected_option == "Enter Shop":
                    # Enter shop
                    clear()
                    print("Welcome to the Pokemon Shop!")
                    sleep(1)
                    final_coins, bag = shop_system(current_coins, bag)
                    
                    # Update coins after shopping
                    current_coins = final_coins
                    
                    # Save updated inventory to database
                    from bcknd.users import save_user_inventory
                    save_user_inventory(username, bag, current_coins)
                    
                    print("\nPress any key to continue...")
                    kb.read_event()
                    
                    # Return to post-battle menu (recursive call with updated values)
                    return post_battle_menu(current_coins, bag, username, team)
                
                elif selected_option == "Battle Again":
                    # Start another battle
                    clear()
                    print("Searching for another opponent...")
                    sleep(1)
                    
                    # Get updated team from database in case Pokemon were caught
                    from bcknd.users import get_user_team
                    updated_team = get_user_team(username)
                    if updated_team:
                        team = updated_team
                    
                    # Choose Pokemon for next battle
                    temp_pokemon = team[0]  # Use first Pokemon to determine opponent scaling
                    next_opponent = get_scaled_pokemon(temp_pokemon)
                    chosen_pokemon, chosen_position = choose_battle_pokemon(team, 0, next_opponent)
                    
                    # Start new battle
                    main_battle(chosen_pokemon, next_opponent, team, chosen_position, username)
                    return True  # Continue the game loop
                
                elif selected_option == "Exit Game":
                    # Exit the game
                    clear()
                    print("═" * 50)
                    print("         Thank you for playing!")
                    print("         Pokemon Battle CLI")
                    print("═" * 50)
                    print("See you next time, trainer!")
                    print()
                    sleep(2)
                    return False  # Exit the game
    
    return False  # Fallback


def choose_battle_pokemon(pokemon_team, current_position, opponent_name=None):
    """
    Let the user choose which Pokemon to use for battle
    If only one Pokemon, return that Pokemon automatically
    """
    if len(pokemon_team) == 1:
        return pokemon_team[0], 0
    
    # Multiple Pokemon available - let user choose
    current_choice = current_position
    
    def get_pokemon_stats(pokemon_name):
        """Get basic stats for a Pokemon to display in selection"""
        try:
            import pandas as pd
            df = pd.read_csv(r"files/pokemon.csv")
            pokemon_row = df[df[" Name"] == pokemon_name]
            if not pokemon_row.empty:
                hp = int(pokemon_row[" HP"].iloc[0])
                attack = int(pokemon_row[" Attack"].iloc[0])
                defense = int(pokemon_row[" Defense"].iloc[0])
                base_total = int(pokemon_row[" Base_Total"].iloc[0])
                return f"HP: {hp} | ATK: {attack} | DEF: {defense} | Total: {base_total}"
            else:
                return "Stats not found"
        except Exception as e:
            return "Stats unavailable"
    
    def pokemon_selection_menu():
        clear()
        print("═" * 60)
        if opponent_name:
            print(f"          WILD {opponent_name.upper()} APPEARED!")
            print("═" * 60)
            print("            CHOOSE YOUR POKEMON FOR BATTLE")
        else:
            print("            CHOOSE YOUR POKEMON FOR BATTLE")
        print("═" * 60)
        print(f"Available Pokemon ({len(pokemon_team)}):")
        print()
        for i, pkmn in enumerate(pokemon_team):
            stats = get_pokemon_stats(pkmn)
            if i == current_choice:
                print(f"{Fore.BLACK}{Back.WHITE}► {pkmn:<12} | {stats}{Style.RESET_ALL}")
            else:
                print(f"  {pkmn:<12} | {stats}")
        print()
        print("Use ↑/↓ arrows to navigate, Enter to select")
        print("═" * 60)
    
    pokemon_selection_menu()
    
    while True:
        event = kb.read_event()
        if event.event_type == kb.KEY_DOWN:
            if event.name == "down":
                playsound("button Hover")
                current_choice = (current_choice + 1) % len(pokemon_team)
                pokemon_selection_menu()
            elif event.name == "up":
                playsound("button Hover")
                current_choice = (current_choice - 1) % len(pokemon_team)
                pokemon_selection_menu()
            elif event.name == "enter":
                playsound("button click")
                clear()
                print(f"You chose {pokemon_team[current_choice]} for battle!")
                sleep(1)
                return pokemon_team[current_choice], current_choice


def user():
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
                playsound("button Hover")
                current_user_option = (current_user_option + 1) % len(user_options)
                user_menu()
            elif event.name == "up":
                playsound("button Hover")
                current_user_option = (current_user_option - 1) % len(user_options)
                user_menu()
            elif event.name == "enter":
                playsound("button click")
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
        password = getpass.getpass("Enter password: ")
        global current_option
        global pokemon
        starter_menu()

        while True:
            event = kb.read_event()
            if event.event_type == kb.KEY_DOWN:
                if event.name == "down":
                    playsound("button Hover")
                    current_option = (current_option + 1) % len(options)
                    starter_menu()
                elif event.name == "up":
                    playsound("button Hover")
                    current_option = (current_option - 1) % len(options)
                    starter_menu()
                elif event.name == "enter":
                    playsound("button click")
                    clear()
                    print(f"You selected: {options[current_option]}")
                    print("Would you like to continue with " + options[current_option] + "? (" + "\u0332Y" + "es/" "\u0332N" + "o)")
                    while True:
                        event = kb.read_event()
                        if event.event_type == kb.KEY_DOWN:
                            if event.name == "y":
                                playsound("button click")
                                clear()
                                pokemon = options[current_option]
                                print(f"Great! You chose {pokemon} as your starter.")
                                break
                            elif event.name == "n":
                                playsound("button click")
                                starter_menu()
                                break
                    if event.name == "y":   
                        break

        pokemon = options[current_option]
        pokemon_team = [p.strip().capitalize() for p in pokemon.split(",") if p.strip()]
        user_create(username, password, pokemon_team)
        sleep(1)
        return pokemon_team, username  # Return both team and username
    else:  # Login
        while True:
            print("User login...")
            username = input("Enter username: ")
            password = getpass.getpass("Enter password: ")
            user = login_user(username, password)
            sleep(1)
            if user == False:
                continue
            else:
                return user, username  # Return both team and username






pokemon_team, current_username = user()
current_position = 0
pokemon = pokemon_team[current_position]

# starter_menu()

# while True:
#     event = kb.read_event()
#     if event.event_type == kb.KEY_DOWN:
#         if event.name == "down":
#             current_option = (current_option + 1) % len(options)
#             starter_menu()
#         elif event.name == "up":
#             current_option = (current_option - 1) % len(options)
#             starter_menu()
#         elif event.name == "enter":
#             clear()
#             print(f"You selected: {options[current_option]}")
#             print("Would you like to continue with " + options[current_option] + "? (" + "\u0332Y" + "es/" "\u0332N" + "o)")
#             while True:
#                 event = kb.read_event()
#                 if event.event_type == kb.KEY_DOWN:
#                     if event.name == "y":
#                         clear()
#                         pokemon = options[current_option]
#                         print(f"Great! You chose {pokemon} as your starter.")
#                         break
#                     elif event.name == "n":
#                         starter_menu()
#                         break
#             if event.name == "y":   
#                 break

# pokemon = options[current_option]

#opp = "MISSINGNO" # Placeholder, will be collected from the backend later

# yeah raven, lets get the opps

from bcknd.functions import get_scaled_pokemon

# Main game loop - allows for continuous battles
def main_game_loop():
    """Main game loop that handles continuous battles"""
    global pokemon_team, current_username
    
    clear()
    print("Welcome to Pokemon Battle CLI!")
    print("Prepare for your first battle!")
    sleep(2)
    
    # Start the battle loop
    continue_playing = True
    while continue_playing:
        try:
            # Refresh team data in case Pokemon were caught
            from bcknd.users import get_user_team
            current_team = get_user_team(current_username)
            if current_team:
                pokemon_team = current_team
            
            # Get the opponent first
            temp_pokemon = pokemon_team[0]  # Use first Pokemon to determine opponent
            opp = get_scaled_pokemon(temp_pokemon)
            
            # Let user choose which Pokemon to use for battle (now showing the opponent)
            chosen_pokemon, chosen_position = choose_battle_pokemon(pokemon_team, 0, opp)
            
            clear()
            print(f"A wild {opp} has appeared!")
            print("Battle starting...")
            sleep(2)
            
            # Start battle - this will return True to continue or False to exit
            continue_playing = main_battle(chosen_pokemon, opp, pokemon_team, chosen_position, current_username)
            
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            clear()
            print("\nThanks for playing Pokemon Battle CLI!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Restarting battle system...")
            sleep(2)
            continue
    
    # Game ended
    clear()
    print("═" * 50)
    print("         Game Over")
    print("   Thanks for playing!")
    print("═" * 50)

# Start the main game
main_game_loop()