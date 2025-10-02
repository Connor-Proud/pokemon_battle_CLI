import pandas
# import keyboard as kb, os
# from colorama import Fore, Back, Style




pokecoins = max(0, 0)
pokeballs = 0
potion_super = 0
potion_max = 0
revive = 0
max_revive = 0
enter = 0
order_item = 0

bag = (pokeballs,
       potion_super,
       potion_max,
       revive,
       max_revive,)

if pokecoins <= 0:
    print(" -----You do not have any pokecoins----- ")
    print(" -----Defeat pokemon to earn more----- ")
else:
    print("-----What do you wish to purchase-----")
    print("--------------------------------------")
    print("-----pokeballs     3c")
    print("-----super.potion  5c")
    print("-----max.potion    10c")
    print("-----revive        10c")
    print("-----max.revive    20c")

cpu_magikarp = 0
if cpu_magikarp <= 0:
    pokecoins = pokecoins + 10
print("Your pokecoin balance is:", pokecoins ,)

if cpu_magikarp <= 0:
    print("1.YES")
while enter <= 0 or enter > 1:
    try:
        enter =(int(input("Do you wish to view the shop?   ")))
    except:
        print("enter a valid choice")
        print("1.YES")
    
    if enter == 1:
        print("-----What do you wish to purchase-----")
        print("--------------------------------------")
        print("--1--pokeballs     3c")
        print("--2--super.potion  5c")
        print("--3--max.potion    10c")
        print("--4--revive        10c")
        print("--5--max.revive    20c")

        print("Your current balance is ",pokecoins,)

while order_item <= 0 or order_item > 5:
    try:
        order_item = int(input("What do you wish to purchase? "))
    except:
        print("enter a valid choice")

flag:bool=True
while flag==True:

    if order_item == 1:
        pokeballs = pokeballs + 1
        pokecoins = pokecoins - 3
        flag=False
        print(bag)
    if order_item == 2:
        potion_super = potion_super + 1
        pokecoins = pokecoins - 5
        flag=False
        print(bag)
    if order_item == 3:
        potion_max = potion_max + 1
        pokecoins = pokecoins - 10
        flag=False
        print(bag)
    if order_item == 4:
        revive = revive + 1
        pokecoins = pokecoins - 10
        flag=False
        print("bag")
    if order_item == 5:
        max_revive = max_revive + 1
        pokecoins = pokecoins - 20
        flag=False
        print(bag)

    if pokecoins < 0:
        print("-----you need more pokecoins")
        print("-----battle more pokemons to earn more")
        flag=True