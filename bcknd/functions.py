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




import os
import pandas as pd
from random import randint,choice


### this function has been moved to a rust dll cause this was slow as shit

# def dmg_calc(instigator:str,
#             victim:str,move:str)->int:
#     df=pd.read_csv(r"files/pokemon.csv")
#     instigator=instigator.capitalize()
#     instigator_row=df[df[" Name"]==instigator]
#     #change

#     instigator_level=1

#     #
#     instigator_crit_p1=(randint(0,1000)/10)
#     if instigator_crit_p1 < 4.7:
#         instigator_crit=2
#     else:
#         instigator_crit=1
    
#     move_df=pd.read_csv(r"files/moves.csv")
#     instigator_pwr=move_df[move_df["name"]==move]["power"].iloc[0]
#     effective_attack=instigator_row[" Attack"].iloc[0]
#     instigator_type_2=instigator_row[" Type2"].iloc[0]
#     if pd.isna(instigator_type_2):
#         instigator_type_2=None
#     move_type = move_df[move_df["name"]==move]["type"].iloc[0].lower()
#     victim_row = df[df[" Name"]==victim.capitalize()]
#     victim_def = victim_row[" Defense"].iloc[0]
#     type_columns = {
#         'normal': ' Normal_Dmg',
#         'fire': ' Fire_Dmg', 
#         'water': ' Water_Dmg',
#         'electric': ' Eletric_Dmg',  # note: CSV has typo "Eletric"
#         'grass': ' Grass_Dmg',
#         'ice': ' Ice_Dmg',
#         'fighting': ' Fight_Dmg',
#         'poison': ' Poison_Dmg',
#         'ground': ' Ground_Dmg',
#         'flying': ' Flying_Dmg',
#         'psychic': ' Psychic_Dmg',
#         'bug': ' Bug_Dmg',
#         'rock': ' Rock_Dmg',
#         'ghost': ' Ghost_Dmg',
#         'dragon': ' Dragon_Dmg'
#     }
#     if move_type in type_columns:
#         type_effectiveness = victim_row[type_columns[move_type]].iloc[0]
#     else:
#         type_effectiveness = 1
#     instigator_type_1 = instigator_row[" Type1"].iloc[0].lower()
#     instigator_type_2_val = instigator_row[" Type2"].iloc[0] if not pd.isna(instigator_row[" Type2"].iloc[0]) else None
#     same_type_attack_bonus = 1.0
#     if move_type == instigator_type_1:
#         same_type_attack_bonus = 1.5
#     elif instigator_type_2_val and move_type == instigator_type_2_val.lower():
#         same_type_attack_bonus = 1.5
#     base_damage = (2 * instigator_level * instigator_crit / 5 + 2) * instigator_pwr * effective_attack / victim_def / 50 + 2
#     dmg_dealt = base_damage * same_type_attack_bonus * type_effectiveness
#     dmg_dealt = int(dmg_dealt * randint(217, 255) / 255)
#     if dmg_dealt == 0:
#         return "miss"
#     return int(dmg_dealt)

def playsound(move_name: str):
    """Play the sound effect for a Pokémon move.

    Args:
        move_name (str): holy shit it works, just put the move name in bruh
    """
    import os
    import subprocess
    try:
        # Go up one level from bcknd/ to the root directory, then into files/sounds/
        DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = os.path.join(DIR, "files", "sounds", f"{move_name}.wav")
        
        # Use Windows' built-in sound player in a non-blocking way
        if os.path.exists(file):
            subprocess.Popen(['powershell', '-c', f'(New-Object Media.SoundPlayer "{file}").PlaySync()'], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"Sound file not found for move: {move_name}")
    except Exception as e:
        print(f"Error playing sound: {e}")


def play_hit_sound(damage: int):
    """Play hit sound based on damage dealt to player.
    
    Args:
        damage (int): Amount of damage dealt
    """
    import os
    import subprocess
    try:
        # Go up one level from bcknd/ to the root directory, then into files/sounds/
        DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        if damage <= 5:
            sound_file = "IMHITWEAK_Not_Very_Effective.wav"
        elif damage <= 11:
            sound_file = "IMHIT_Damage.wav"
        else:  # 12+
            sound_file = "IMHITSUPER_Super_Effective.wav"
        
        file_path = os.path.join(DIR, "files", "sounds", sound_file)
        
        # Use Windows' built-in sound player in a non-blocking way
        if os.path.exists(file_path):
            subprocess.Popen(['powershell', '-c', f'(New-Object Media.SoundPlayer "{file_path}").PlaySync()'], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            print(f"Hit sound file not found: {sound_file}")
    except Exception as e:
        print(f"Error playing hit sound: {e}")




def get_pokemon_moves(pokemon_name: str) -> list:
    import os
    # Go up one level from bcknd/ to the root directory, then into files/
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        # Read the capable_moves CSV file
        df = pd.read_csv(os.path.join(DIR, "files", "capable_moves.csv"))
        # Normalize the pokemon name (capitalize first letter)
        pokemon_name = pokemon_name.capitalize()
        # Find the row for the specified Pokémon
        pokemon_row = df[df["pokemon"] == pokemon_name]
        if pokemon_row.empty:
            print(f"Warning: Pokémon '{pokemon_name}' not found in capable_moves.csv")
            return []
        moves_string = pokemon_row["moves"].iloc[0]
        moves_list = [move.strip() for move in moves_string.split(",")]
        
        return moves_list
        
    except FileNotFoundError:
        print("Error: capable_moves.csv file not found in files/ directory")
        return []
    except Exception as e:
        print(f"Error reading capable_moves.csv: {e}")
        return []


def get_random_pokemon() -> str:
    import os
    # Go up one level from bcknd/ to the root directory, then into files/
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        df = pd.read_csv(os.path.join(DIR, "files", "pokemon.csv"))
        pokemon_list = df[" Name"].tolist()
        return choice(pokemon_list).strip()
    except FileNotFoundError:
        print("Error: pokemon.csv file not found in files/ directory")
        return "MissingNo"
    except Exception as e:
        print(f"Error reading pokemon.csv: {e}")
        return "MissingNo"


def get_scaled_pokemon(player_pokemon_name: str) -> str:
    """
    Get a scaled Pokemon opponent based on player's Pokemon strength
    
    Scaling probabilities:
    - 50% chance: Similar strength (±50 base total points)
    - 30% chance: Weaker opponent (-51 to -100 base total points)  
    - 20% chance: Stronger opponent (+51 to +120 base total points)
    
    Args:
        player_pokemon_name (str): Name of the player's current Pokemon
        
    Returns:
        str: Name of the selected opponent Pokemon
    """
    import os
    from random import randint
    
    # Go up one level from bcknd/ to the root directory, then into files/
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        df = pd.read_csv(os.path.join(DIR, "files", "pokemon.csv"))
        
        # Get player Pokemon's base total
        player_row = df[df[" Name"] == player_pokemon_name]
        if player_row.empty:
            print(f"Warning: Player Pokemon '{player_pokemon_name}' not found, using random selection")
            return get_random_pokemon()
        
        player_base_total = int(player_row[" Base_Total"].iloc[0])
        
        # Determine scaling tier based on probability
        roll = randint(1, 100)
        
        if roll <= 50:  # 50% chance - Similar strength
            min_total = max(0, player_base_total - 50)
            max_total = player_base_total + 50
            tier_name = "similar"
        elif roll <= 80:  # 30% chance - Weaker opponent  
            min_total = max(0, player_base_total - 100)
            max_total = max(0, player_base_total - 51)
            tier_name = "weaker"
        else:  # 20% chance - Stronger opponent
            min_total = player_base_total + 51
            max_total = player_base_total + 120
            tier_name = "stronger"
        
        # Filter Pokemon within the target range
        suitable_pokemon = df[
            (df[" Base_Total"] >= min_total) & 
            (df[" Base_Total"] <= max_total)
        ]
        
        # If no suitable Pokemon found, expand the search
        if suitable_pokemon.empty:
            print(f"No Pokemon found in {tier_name} tier ({min_total}-{max_total}), expanding search...")
            # Fallback to a wider range
            if tier_name == "weaker":
                suitable_pokemon = df[df[" Base_Total"] < player_base_total]
            elif tier_name == "stronger":
                suitable_pokemon = df[df[" Base_Total"] > player_base_total]
            else:  # similar
                min_total = max(0, player_base_total - 100)
                max_total = player_base_total + 100
                suitable_pokemon = df[
                    (df[" Base_Total"] >= min_total) & 
                    (df[" Base_Total"] <= max_total)
                ]
        
        # If still no suitable Pokemon, use random selection
        if suitable_pokemon.empty:
            print("No suitable scaled Pokemon found, using random selection")
            return get_random_pokemon()
        
        # Select random Pokemon from suitable candidates
        selected_pokemon = choice(suitable_pokemon[" Name"].tolist()).strip()
        selected_base_total = int(suitable_pokemon[suitable_pokemon[" Name"] == selected_pokemon][" Base_Total"].iloc[0])
        
        return selected_pokemon
        
    except FileNotFoundError:
        print("Error: pokemon.csv file not found in files/ directory")
        return "MissingNo"
    except Exception as e:
        print(f"Error in scaled Pokemon selection: {e}")
        return get_random_pokemon()



def get_move_data(move_name: str) -> dict:
    """Get move data including PP from moves.csv"""
    import os
    # Go up one level from bcknd/ to the root directory, then into files/
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        df = pd.read_csv(os.path.join(DIR, "files", "moves.csv"))
        move_row = df[df["name"] == move_name]
        if move_row.empty:
            print(f"Warning: Move '{move_name}' not found in moves.csv")
            return {"name": move_name, "pp": 10}  # Default PP if not found
        
        return {
            "name": move_name,
            "pp": int(move_row["pp"].iloc[0]),
            "power": move_row["power"].iloc[0],
            "accuracy": move_row["accuracy"].iloc[0],
            "type": move_row["type"].iloc[0]
        }
    except FileNotFoundError:
        print("Error: moves.csv file not found in files/ directory")
        return {"name": move_name, "pp": 10}
    except Exception as e:
        print(f"Error reading moves.csv: {e}")
        return {"name": move_name, "pp": 10}


def initialize_pokemon_moves_with_pp(pokemon_name: str) -> dict:
    """Initialize a Pokemon's moves with their maximum PP"""
    moves_list = get_pokemon_moves(pokemon_name)
    moves_with_pp = {}
    
    for move in moves_list:
        move_data = get_move_data(move)
        moves_with_pp[move] = {
            "current_pp": move_data["pp"],
            "max_pp": move_data["pp"],
            "power": move_data.get("power", 0),
            "accuracy": move_data.get("accuracy", 100),
            "type": move_data.get("type", "Normal")
        }
    
    return moves_with_pp


def shop_system(pokecoins=0, current_bag=None):
    """
    Shop system with keyboard navigation and smooth animations
    Returns updated pokecoin count and bag
    """
    import keyboard as kb
    from colorama import Fore, Back, Style
    import os
    from time import sleep
    
    def clear():
        os.system("cls")
    
    def clear_lines(num_lines):
        """Clear a specific number of lines by moving cursor up and clearing each line"""
        for _ in range(num_lines):
            print('\033[1A', end='')  # Move cursor up one line
            print('\033[2K', end='')  # Clear the entire line
    
    # Shop items with prices
    shop_items = [
        {"name": "Pokeball", "price": 3, "description": "Catch wild Pokemon"},
        {"name": "Super Potion", "price": 5, "description": "Restores 50 HP"},
        {"name": "Max Potion", "price": 10, "description": "Fully restores HP"},
        {"name": "Revive", "price": 10, "description": "Revives fainted Pokemon"},
        {"name": "Max Revive", "price": 20, "description": "Fully revives Pokemon"},
        {"name": "Exit Shop", "price": 0, "description": "Leave the shop"}
    ]
    
    # Use current bag or create default
    if current_bag is None:
        bag = {
            "pokeballs": 0,
            "super_potion": 0,
            "max_potion": 0,
            "revive": 0,
            "max_revive": 0
        }
    else:
        bag = current_bag.copy()  # Create a copy to avoid modifying original
    
    current_option = 0
    last_menu_lines = 0  # Track lines for smooth clearing
    
    def shop_menu():
        nonlocal last_menu_lines
        
        # Clear previous menu if this isn't the first display
        if last_menu_lines > 0:
            clear_lines(last_menu_lines)
        
        menu_content = []
        menu_content.append("═" * 60)
        menu_content.append("                    POKEMON SHOP")
        menu_content.append("═" * 60)
        menu_content.append(f"Pokecoins: {pokecoins}")
        menu_content.append("═" * 60)
        menu_content.append("")
        
        for i, item in enumerate(shop_items):
            price_display = f"{item['price']}¢" if item['price'] > 0 else "FREE"
            
            if i == current_option:
                if pokecoins >= item['price'] or item['price'] == 0:
                    menu_content.append(f"{Fore.BLACK}{Back.WHITE}► {item['name']:<15} | {price_display:<6} | {item['description']}{Style.RESET_ALL}")
                else:
                    menu_content.append(f"{Fore.BLACK}{Back.RED}► {item['name']:<15} | {price_display:<6} | {item['description']} (Can't afford!){Style.RESET_ALL}")
            else:
                if pokecoins >= item['price'] or item['price'] == 0:
                    menu_content.append(f"  {item['name']:<15} | {price_display:<6} | {item['description']}")
                else:
                    menu_content.append(f"{Fore.RED}  {item['name']:<15} | {price_display:<6} | {item['description']} (Can't afford!){Style.RESET_ALL}")
        
        menu_content.append("")
        menu_content.append("═" * 60)
        menu_content.append("Current Bag:")
        menu_content.append(f"  Pokeballs: {bag['pokeballs']} | Super Potions: {bag['super_potion']} | Max Potions: {bag['max_potion']}")
        menu_content.append(f"  Revives: {bag['revive']} | Max Revives: {bag['max_revive']}")
        menu_content.append("═" * 60)
        menu_content.append("Use ↑/↓ arrows to navigate, Enter to purchase/select")
        
        # Print all content
        for line in menu_content:
            print(line)
        
        # Update line count for next clear
        last_menu_lines = len(menu_content)
    
    # Shop building animation with frames from shop_anim.py
    clear()
    
    # Define all animation frames from shop_anim.py
    anim_frames = [
        r""" """,
        
        r"""
 
/
█         
█    
█         
█
""",
        
        r"""
 ,
//
█         
█    
█         
█_
""",
        
        r"""
 ,,
//=
█         
█    
█         
█__
""",
        
        r"""
 ,,=
//==
█         
█    
█         
█___
""",
        
        r"""
 ,,==
//===
█         
█  ⊞   
█         
█____
""",
        
        r"""
 ,,===
//====
█         
█  ⊞   
█         
█____█
""",
        
        r"""
 ,,====
//=====
█         
█  ⊞   
█         
█____█_
""",
        
        r"""
 ,,=====
//======
█         
█  ⊞   
█         
█____█__
""",
        
        r"""
 ,,=====,
//=======
█         
█  ⊞   
█         
█____█___
""",
        
        r"""
 ,,=====,,
//=======\
█         
█  ⊞   ⊞  
█         
█____█____
""",
        
        r"""
 ,,=====,,
//=======\\
█         █
█  ⊞   ⊞  █
█         █
█____█____█
""",
        
        r"""
 ,,=====,,    █
//=======\\   █
█         █   █
█  ⊞   ⊞  █       
█         █   █
█____█____█
""",
        
        r"""
 ,,=====,,    ██
//=======\\   ██
█         █   ██
█  ⊞   ⊞  █       
█         █   ██
█____█____█
""",
        
        r"""
 ,,=====,,    ███
//=======\\   ██
█         █   ███
█  ⊞   ⊞  █       
█         █   ███
█____█____█
""",
        
        r"""
 ,,=====,,    ████
//=======\\   ██
█         █   ████
█  ⊞   ⊞  █       
█         █   ████
█____█____█
""",
        
        r"""
 ,,=====,,    █████
//=======\\   ██
█         █   █████
█  ⊞   ⊞  █       █
█         █   █████
█____█____█
""",
        
        r"""
 ,,=====,,    ██████
//=======\\   ██
█         █   ██████
█  ⊞   ⊞  █       ██
█         █   ██████
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  █
//=======\\   ██      █
█         █   ██████  █
█  ⊞   ⊞  █       ██  █
█         █   ██████  █
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██
//=======\\   ██      ██
█         █   ██████  ██
█  ⊞   ⊞  █       ██  ██
█         █   ██████  ██
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██
//=======\\   ██      ██
█         █   ██████  ███
█  ⊞   ⊞  █       ██  ██
█         █   ██████  ██
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██
//=======\\   ██      ██
█         █   ██████  ████
█  ⊞   ⊞  █       ██  ██
█         █   ██████  ██
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  █
//=======\\   ██      ██  █
█         █   ██████  █████
█  ⊞   ⊞  █       ██  ██  █
█         █   ██████  ██  █
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██
//=======\\   ██      ██  ██
█         █   ██████  ██████
█  ⊞   ⊞  █       ██  ██  ██
█         █   ██████  ██  ██
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  █
//=======\\   ██      ██  ██  █
█         █   ██████  ██████  █
█  ⊞   ⊞  █       ██  ██  ██  █
█         █   ██████  ██  ██  █
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  ██
//=======\\   ██      ██  ██  ██  
█         █   ██████  ██████  ██  
█  ⊞   ⊞  █       ██  ██  ██  ██  
█         █   ██████  ██  ██  ██
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  ███
//=======\\   ██      ██  ██  ██  
█         █   ██████  ██████  ██  
█  ⊞   ⊞  █       ██  ██  ██  ██  
█         █   ██████  ██  ██  ███
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  ████
//=======\\   ██      ██  ██  ██  
█         █   ██████  ██████  ██  
█  ⊞   ⊞  █       ██  ██  ██  ██  
█         █   ██████  ██  ██  ████
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  █████
//=======\\   ██      ██  ██  ██  █
█         █   ██████  ██████  ██  █
█  ⊞   ⊞  █       ██  ██  ██  ██  █
█         █   ██████  ██  ██  █████
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  ██████
//=======\\   ██      ██  ██  ██  ██
█         █   ██████  ██████  ██  ██
█  ⊞   ⊞  █       ██  ██  ██  ██  ██
█         █   ██████  ██  ██  ██████
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  ██████  █
//=======\\   ██      ██  ██  ██  ██  █
█         █   ██████  ██████  ██  ██  █
█  ⊞   ⊞  █       ██  ██  ██  ██  ██  █
█         █   ██████  ██  ██  ██████  █
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  ██████  ██
//=======\\   ██      ██  ██  ██  ██  ██  
█         █   ██████  ██████  ██  ██  ██
█  ⊞   ⊞  █       ██  ██  ██  ██  ██  ██
█         █   ██████  ██  ██  ██████  ██
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  ██████  ███
//=======\\   ██      ██  ██  ██  ██  ██  
█         █   ██████  ██████  ██  ██  ███
█  ⊞   ⊞  █       ██  ██  ██  ██  ██  ██
█         █   ██████  ██  ██  ██████  ██
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  ██████  ████
//=======\\   ██      ██  ██  ██  ██  ██  
█         █   ██████  ██████  ██  ██  ████
█  ⊞   ⊞  █       ██  ██  ██  ██  ██  ██
█         █   ██████  ██  ██  ██████  ██
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  ██████  █████
//=======\\   ██      ██  ██  ██  ██  ██  █
█         █   ██████  ██████  ██  ██  █████
█  ⊞   ⊞  █       ██  ██  ██  ██  ██  ██
█         █   ██████  ██  ██  ██████  ██
█____█____█
""",
        
        r"""
 ,,=====,,    ██████  ██  ██  ██████  ██████
//=======\\   ██      ██  ██  ██  ██  ██  ██
█         █   ██████  ██████  ██  ██  ██████
█  ⊞   ⊞  █       ██  ██  ██  ██  ██  ██
█         █   ██████  ██  ██  ██████  ██
█____█____█
"""
    ]
    
    # Animate through frames with timing similar to shop_anim.py
    for i, frame in enumerate(anim_frames):
        if i == 0:
            # Print first frame normally
            print(frame, end='')
        else:
            # For subsequent frames, clear previous content and print new frame
            current_lines = len(anim_frames[i-1].split('\n'))
            clear_lines(current_lines)
            print(frame, end='')
        
        # Apply timing logic from shop_anim.py
        if i <= 10:  # Early frames (building foundation)
            sleep(0.04)
        elif i == 11:  # Pause at shop structure completion
            sleep(0.5)
        else:  # Later frames (adding details)
            sleep(0.02)
    
    # Final message after animation
    sleep(0.5)
    print("\n\nShop is ready! Press any key to enter...")
    try:
        kb.read_event()
    except:
        input()  # Fallback for systems where keyboard doesn't work
    
    clear()
    shop_menu()
    
    while True:
        try:
            event = kb.read_event()
            if event.event_type == kb.KEY_DOWN:
                if event.name == "down":
                    try:
                        playsound("button Hover")
                    except:
                        pass  # Sound not critical
                    current_option = (current_option + 1) % len(shop_items)
                    shop_menu()
                elif event.name == "up":
                    try:
                        playsound("button Hover")
                    except:
                        pass  # Sound not critical
                    current_option = (current_option - 1) % len(shop_items)
                    shop_menu()
                elif event.name == "enter":
                    selected_item = shop_items[current_option]
                    
                    # Exit shop
                    if selected_item["name"] == "Exit Shop":
                        try:
                            playsound("button click")
                        except:
                            pass
                        
                        # Animated exit
                        clear_lines(last_menu_lines)
                        exit_frames = [
                            "Thanks for visiting the Pokemon Shop!",
                            "Thanks for visiting the Pokemon Shop! .",
                            "Thanks for visiting the Pokemon Shop! ..",
                            "Thanks for visiting the Pokemon Shop! ..."
                        ]
                        
                        for frame in exit_frames:
                            clear_lines(5)  # Clear previous exit message
                            print(frame)
                            print(f"Final Pokecoins: {pokecoins}")
                            if sum(bag.values()) > 0:
                                print("Items purchased:")
                                for item, count in bag.items():
                                    if count > 0:
                                        print(f"  {item.replace('_', ' ').title()}: {count}")
                            sleep(0.5)
                        
                        print("\nPress any key to continue...")
                        try:
                            kb.read_event()
                        except:
                            input()
                        return pokecoins, bag
                    
                    # Check if player can afford the item
                    if pokecoins >= selected_item["price"]:
                        try:
                            playsound("button click")
                        except:
                            pass
                        pokecoins -= selected_item["price"]
                        
                        # Add item to bag
                        if selected_item["name"] == "Pokeball":
                            bag["pokeballs"] += 1
                        elif selected_item["name"] == "Super Potion":
                            bag["super_potion"] += 1
                        elif selected_item["name"] == "Max Potion":
                            bag["max_potion"] += 1
                        elif selected_item["name"] == "Revive":
                            bag["revive"] += 1
                        elif selected_item["name"] == "Max Revive":
                            bag["max_revive"] += 1
                        
                        # Animated purchase confirmation
                        clear_lines(last_menu_lines)
                        purchase_frames = [
                            f"Purchasing {selected_item['name']}...",
                            f"Purchasing {selected_item['name']}... .",
                            f"Purchasing {selected_item['name']}... ..",
                            f"Purchased {selected_item['name']} for {selected_item['price']} Pokecoins!"
                        ]
                        
                        for frame in purchase_frames:
                            clear_lines(3)
                            print(frame)
                            print(f"Remaining Pokecoins: {pokecoins}")
                            sleep(0.4)
                        
                        print("\nPress any key to continue shopping...")
                        try:
                            kb.read_event()
                        except:
                            input()
                        
                        clear()
                        last_menu_lines = 0  # Reset for fresh menu
                        shop_menu()
                    else:
                        # Can't afford - animated error
                        try:
                            playsound("button Hover")  # Different sound for error
                        except:
                            pass
                        
                        clear_lines(last_menu_lines)
                        error_frames = [
                            "Checking funds...",
                            "Not enough Pokecoins!",
                            f"You have: {pokecoins} | Need: {selected_item['price']}"
                        ]
                        
                        for frame in error_frames:
                            clear_lines(4)
                            print(frame)
                            if "Need:" in frame:
                                print("Defeat more Pokemon to earn Pokecoins!")
                            sleep(0.6)
                        
                        print("\nPress any key to continue...")
                        try:
                            kb.read_event()
                        except:
                            input()
                        
                        clear()
                        last_menu_lines = 0  # Reset for fresh menu
                        shop_menu()
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            clear()
            print("Exiting shop...")
            return pokecoins, bag
        except Exception as e:
            # Fallback for any keyboard issues
            print(f"Keyboard error: {e}")
            print("Using fallback input method...")
            clear()
            print("Shop items:")
            for i, item in enumerate(shop_items):
                print(f"{i+1}. {item['name']} - {item['price']}¢")
            
            try:
                choice = int(input("Enter item number (0 to exit): "))
                if choice == 0:
                    return pokecoins, bag
                elif 1 <= choice <= len(shop_items):
                    selected_item = shop_items[choice-1]
                    if selected_item["name"] != "Exit Shop" and pokecoins >= selected_item["price"]:
                        pokecoins -= selected_item["price"]
                        # Add to bag logic here...
                        print(f"Purchased {selected_item['name']}!")
            except:
                print("Invalid input. Exiting shop.")
                return pokecoins, bag


def calculate_battle_reward(opponent_name: str, won_battle: bool) -> int:
    """
    Calculate pokecoin reward based on opponent's stats and battle outcome
    Improved version of reward_module system
    
    Args:
        opponent_name (str): Name of the defeated Pokemon
        won_battle (bool): True if player won, False if lost
    
    Returns:
        int: Amount of pokecoins earned (positive) or lost (negative)
    """
    import os
    
    # Go up one level from bcknd/ to the root directory, then into files/
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        df = pd.read_csv(os.path.join(DIR, "files", "pokemon.csv"))
        opp_row = df[df[" Name"] == opponent_name]
        
        if opp_row.empty:
            print(f"Warning: Pokemon '{opponent_name}' not found for reward calculation")
            return 5 if won_battle else -5  # Default reward
        
        # Get opponent's base stats for reward calculation
        opp_hp = int(opp_row[" HP"].values[0])
        opp_base_total = int(opp_row[" Base_Total"].values[0])
        
        # Calculate base reward based on opponent strength
        # Base reward: HP/10 + Base_Total/100
        base_reward = int(round(opp_hp / 10, 0)) + int(round(opp_base_total / 100, 0))
        
        # Ensure minimum reward of 5 coins
        base_reward = max(base_reward, 5)
        
        if won_battle:
            print(f"Victory! You earned {base_reward} Pokecoins for defeating {opponent_name}!")
            return base_reward
        else:
            # When losing, pay for Pokemon Center healing (reduced cost)
            healing_cost = max(int(base_reward * 0.6), 3)  # 60% of base reward, minimum 3
            print(f"You pay {healing_cost} Pokecoins for Pokemon Center healing after losing.")
            return -healing_cost
            
    except Exception as e:
        print(f"Error calculating battle reward: {e}")
        return 5 if won_battle else -3


def attempt_pokemon_catch(opponent_name: str, pokeballs_count: int) -> tuple[bool, str]:
    """
    Attempt to catch a wild Pokemon if player has Pokeballs
    
    Args:
        opponent_name (str): Name of the Pokemon to catch
        pokeballs_count (int): Number of Pokeballs the player has
    
    Returns:
        tuple[bool, str]: (success, message)
    """
    import random
    
    if pokeballs_count <= 0:
        return False, "No Pokeballs available to catch Pokemon!"
    
    # 50% chance to successfully catch
    catch_success = random.randint(1, 100) <= 50
    
    if catch_success:
        message = f"Success! You caught {opponent_name}!\nUsed 1 Pokeball"
        return True, message
    else:
        message = f"{opponent_name} broke free from the Pokeball!\nUsed 1 Pokeball"
        return False, message


def pokemon_catch_system(opponent_name: str, bag: dict) -> tuple[bool, dict, str]:
    """
    Handle the Pokemon catching interface and logic
    
    Args:
        opponent_name (str): Name of the Pokemon to potentially catch
        bag (dict): Player's current bag with items
    
    Returns:
        tuple[bool, dict, str]: (caught, updated_bag, caught_pokemon_name)
    """
    import keyboard as kb
    from colorama import Fore, Back, Style
    import os
    
    def clear():
        os.system("cls")
    
    # Check if player has Pokeballs
    if bag.get("pokeballs", 0) <= 0:
        return False, bag, ""
    
    # Catching menu
    catch_options = ["Throw Pokeball", "Don't Catch"]
    current_catch_option = 0
    
    def catch_menu():
        clear()
        print("═" * 60)
        print(f"          WILD {opponent_name.upper()} DEFEATED!")
        print("═" * 60)
        print(f"Pokeballs Available: {bag['pokeballs']}")
        print()
        print("What would you like to do?")
        print()
        for i, option in enumerate(catch_options):
            if i == current_catch_option:
                print(f"{Fore.BLACK}{Back.WHITE}► {option}{Style.RESET_ALL}")
            else:
                print(f"  {option}")
        print()
        print("Use ↑/↓ arrows to navigate, Enter to select")
        print("═" * 60)
    
    catch_menu()
    
    while True:
        try:
            event = kb.read_event()
            if event.event_type == kb.KEY_DOWN:
                if event.name == "down":
                    try:
                        playsound("button Hover")
                    except:
                        pass
                    current_catch_option = (current_catch_option + 1) % len(catch_options)
                    catch_menu()
                elif event.name == "up":
                    try:
                        playsound("button Hover")
                    except:
                        pass
                    current_catch_option = (current_catch_option - 1) % len(catch_options)
                    catch_menu()
                elif event.name == "enter":
                    try:
                        playsound("button click")
                    except:
                        pass
                    
                    if current_catch_option == 0:  # Throw Pokeball
                        clear()
                        print(f"Throwing Pokeball at {opponent_name}...")
                        print("...")
                        
                        # Use a Pokeball
                        bag["pokeballs"] -= 1
                        
                        # Attempt to catch
                        success, message = attempt_pokemon_catch(opponent_name, 1)  # We know we have at least 1
                        
                        print(message)
                        print(f"Pokeballs remaining: {bag['pokeballs']}")
                        
                        if success:
                            print(f"\n{opponent_name} was added to your team!")
                            print("\nPress any key to continue...")
                            try:
                                kb.read_event()
                            except:
                                input()
                            return True, bag, opponent_name
                        else:
                            print(f"\n{opponent_name} escaped! Better luck next time.")
                            print("\nPress any key to continue...")
                            try:
                                kb.read_event()
                            except:
                                input()
                            return False, bag, ""
                    
                    else:  # Don't Catch
                        clear()
                        print(f"You decided not to catch {opponent_name}.")
                        print("The wild Pokemon runs away...")
                        print("\nPress any key to continue...")
                        try:
                            kb.read_event()
                        except:
                            input()
                        return False, bag, ""
                        
        except KeyboardInterrupt:
            return False, bag, ""
        except Exception as e:
            # Fallback for keyboard issues
            print(f"Keyboard error: {e}")
            choice = input("Throw Pokeball? (y/n): ").lower().strip()
            if choice == 'y':
                bag["pokeballs"] -= 1
                success, message = attempt_pokemon_catch(opponent_name, 1)
                print(message)
                return success, bag, opponent_name if success else ""
            else:
                return False, bag, ""


def use_item_on_pokemon(item_name: str, target_pokemon: dict, bag: dict, team_status: dict = None) -> tuple[bool, str, dict]:
    """
    Use an item on a Pokemon
    
    Args:
        item_name (str): Name of the item to use
        target_pokemon (dict): Pokemon to use the item on
        bag (dict): Player's bag with item counts
        team_status (dict): Status of all team Pokemon (for revives)
    
    Returns:
        tuple[bool, str, dict]: (success, message, updated_bag)
    """
    import copy
    
    updated_bag = copy.deepcopy(bag)
    
    # Check if player has the item
    item_key = item_name.lower().replace(" ", "_")
    if updated_bag.get(item_key, 0) <= 0:
        return False, f"You don't have any {item_name}s!", updated_bag
    
    # Apply item effects
    if item_name == "Super Potion":
        if target_pokemon["hp"] >= target_pokemon["max_hp"]:
            return False, f"{target_pokemon['name']} is already at full health!", updated_bag
        
        heal_amount = min(50, target_pokemon["max_hp"] - target_pokemon["hp"])
        target_pokemon["hp"] += heal_amount
        updated_bag[item_key] -= 1
        
        return True, f"{target_pokemon['name']} recovered {heal_amount} HP!", updated_bag
    
    elif item_name == "Max Potion":
        if target_pokemon["hp"] >= target_pokemon["max_hp"]:
            return False, f"{target_pokemon['name']} is already at full health!", updated_bag
        
        heal_amount = target_pokemon["max_hp"] - target_pokemon["hp"]
        target_pokemon["hp"] = target_pokemon["max_hp"]
        updated_bag[item_key] -= 1
        
        return True, f"{target_pokemon['name']} was fully healed! Recovered {heal_amount} HP!", updated_bag
    
    elif item_name == "Revive":
        if target_pokemon["hp"] > 0:
            return False, f"{target_pokemon['name']} is not fainted!", updated_bag
        
        target_pokemon["hp"] = target_pokemon["max_hp"] // 2
        updated_bag[item_key] -= 1
        
        # Update team status if provided
        if team_status and target_pokemon["name"] in team_status:
            team_status[target_pokemon["name"]]["fainted"] = False
        
        return True, f"{target_pokemon['name']} was revived with half HP!", updated_bag
    
    elif item_name == "Max Revive":
        if target_pokemon["hp"] > 0:
            return False, f"{target_pokemon['name']} is not fainted!", updated_bag
        
        target_pokemon["hp"] = target_pokemon["max_hp"]
        updated_bag[item_key] -= 1
        
        # Update team status if provided
        if team_status and target_pokemon["name"] in team_status:
            team_status[target_pokemon["name"]]["fainted"] = False
        
        return True, f"{target_pokemon['name']} was revived with full HP!", updated_bag
    
    else:
        return False, f"Unknown item: {item_name}", updated_bag


def get_available_items(bag: dict, in_battle: bool = False) -> list:
    """
    Get list of available items that can be used
    
    Args:
        bag (dict): Player's bag
        in_battle (bool): Whether we're in battle (affects which items are shown)
    
    Returns:
        list: List of available items with counts
    """
    available_items = []
    
    item_mapping = {
        "super_potion": "Super Potion",
        "max_potion": "Max Potion",
        "revive": "Revive",
        "max_revive": "Max Revive"
    }
    
    for key, display_name in item_mapping.items():
        count = bag.get(key, 0)
        if count > 0:
            available_items.append({
                "name": display_name,
                "key": key,
                "count": count,
                "usable_in_battle": True  # All healing/revival items can be used in battle
            })
    
    return available_items


if __name__ == "__main__":
    print("""    ╭────────────────────╮
    │ Backend, can't run │
    ╰────────────────────╯""")
else:
   print("here is the import")

