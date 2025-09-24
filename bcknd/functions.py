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


# if __name__ == "__main__":
#     print("""╭────────────────────╮
# │ Backend, can't run │
# ╰────────────────────╯""")
# else:
#     print("here is the import")

