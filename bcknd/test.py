#from functions import dmg_calc #obsolete as of now, moved to rust dll for da speed
from users import user_create, login_user
import pandas as pd
import ctypes
import os

DIR= os.path.dirname(os.path.abspath(__file__)) # find whatever the directory of the current file is

lib = ctypes.CDLL(f"{DIR}/test_.dll") # load it as our awesome sauce dll which calculates damage
lib.dmg_calc.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
lib.dmg_calc.restype = ctypes.c_int


create_user = input("Create user? (y/n): ").lower() == 'y'
if create_user:
    username = input("Enter username: ")
    password = input("Enter password: ")
    team_input = input("Enter up to 6 Pokémon names separated by commas: ")
    pokemon_team = [p.strip().capitalize() for p in team_input.split(",") if p.strip()]
    user_create(username, password, pokemon_team)
else:
    username = input("Enter username: ")
    password = input("Enter password: ")
    login_user(username, password)

print("you are facing a Charmander\nwhat pokemon will you use?")
pokemon_choice = input("Enter the name of the Pokémon you want to use: ")
print(f"You chose {pokemon_choice}")

# print("it is your move, what will you use?")
# move_choice = input("Enter the move you want to use: ")
# print(f"You used {move_choice}")

opponent_death = False
df=pd.read_csv(r"files/pokemon.csv")
charmander_row = df[df[" Name"]=="Charmander"]
opponent_hp=charmander_row[" HP"].values[0]
while not opponent_death:
    print("it is your move, what will you use?")
    move_choice = input("Enter the move you want to use: ")
    print(f"You used {move_choice}")
    dealt=lib.dmg_calc(pokemon_choice.encode('utf-8'), "Charmander".encode('utf-8'), move_choice.encode('utf-8')    )
    if dealt == -1:
        print("miss")
        continue
    if dealt == -2:
        print("invalid move")
        continue
    opponent_hp -= dealt
    if opponent_hp <= 0:
        opponent_death = True
        print("Charmander fainted!")
    else:
        print(f"you dealt: {dealt}\n charmander is now at {opponent_hp}")

