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


from random import randint, choice

# earn or lose pokecoins equal opponent hp divided by 10 for winning or losing a battle
def get_reward():
    global pokecoins
    with open('testfile.txt', 'r') as f:
        pokecoins = int(f.readline())
    if win == True:
        reward = int(round(opp_hp/10,0))
        pokecoins += reward
        print(f'you earn {reward} pokecoins for winning')
    else:
        reward = int(round(opp_hp/10,0))
        pokecoins -= reward
        if pokecoins < 0:
            print(f'you couldn\'t afford the {reward} pokecoins to heal your pokemon, but the pokemon center took what you had and healed them anyway')
            pokecoins = 0
        else:
            print(f'you pay {reward} pokecoins to heal your pokemon after losing')
    print(f'total pokecoins: {pokecoins}')
    with open('testfile.txt', 'w') as f:
        f.write(str(pokecoins))
        
# testing the code innit (simulates winning/losing 10 battles)
for i in range(10):
    win = choice([True,False])
    opp_hp = randint(10,100)
    get_reward()