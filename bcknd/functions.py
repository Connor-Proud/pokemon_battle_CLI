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
















# if __name__ == "__main__":
#     print("""╭────────────────────╮
# │ Backend, can't run │
# ╰────────────────────╯""")
# else:
#     print("here is the import")