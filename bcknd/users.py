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
DIR= os.path.dirname(os.path.abspath(__file__))


def user_create(username:str,password:str,pokemon_team: list) -> str:
    import bcrypt
    import sqlite3
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    conn = sqlite3.connect(f"{DIR}/pokemon_users.db")
    cur = conn.cursor()
    pokemon_team += [None] * (6 - len(pokemon_team))  #pad with None if fewer than 6
    
    try:
        cur.execute("""
            INSERT INTO users (username, password_hash, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (username, hashed, *pokemon_team))
        conn.commit()
        print(f"User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        print("Username already exists!")


def login_user(username, password):
    import bcrypt
    import sqlite3
    conn = sqlite3.connect(f"{DIR}/pokemon_users.db")
    cur = conn.cursor()
    cur.execute("SELECT password_hash, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6 FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    
    if row and bcrypt.checkpw(password.encode("utf-8"), row[0]):
        print("Login successful!")
        pokemons = [p for p in row[1:] if p is not None]
        print("Current Pokémon:", pokemons)
        return pokemons
    else:
        print("Invalid username or password")
        return False


def add_pokemon_to_team(username: str, pokemon_name: str) -> bool:
    """
    Add a caught Pokemon to a user's team if there's space
    
    Args:
        username (str): Username of the player
        pokemon_name (str): Name of the Pokemon to add
    
    Returns:
        bool: True if Pokemon was added, False if team is full
    """
    import sqlite3
    
    conn = sqlite3.connect(f"{DIR}/pokemon_users.db")
    cur = conn.cursor()
    
    try:
        # Get current Pokemon team
        cur.execute("SELECT pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6 FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        
        if not row:
            print(f"User {username} not found!")
            return False
        
        # Find first empty slot
        pokemon_slots = list(row)
        for i, slot in enumerate(pokemon_slots):
            if slot is None:
                # Found empty slot, add Pokemon
                column_name = f"pokemon{i+1}"
                cur.execute(f"UPDATE users SET {column_name} = ? WHERE username = ?", (pokemon_name, username))
                conn.commit()
                print(f"{pokemon_name} added to team slot {i+1}!")
                return True
        
        # No empty slots
        print("Your team is full! (6/6 Pokemon)")
        print("Consider releasing a Pokemon to make space.")
        return False
        
    except Exception as e:
        print(f"Error adding Pokemon to team: {e}")
        return False
    finally:
        conn.close()


def get_user_team(username: str) -> list:
    """
    Get current Pokemon team for a user
    
    Args:
        username (str): Username to look up
    
    Returns:
        list: List of Pokemon names (excluding None values)
    """
    import sqlite3
    
    conn = sqlite3.connect(f"{DIR}/pokemon_users.db")
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6 FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        
        if row:
            pokemons = [p for p in row if p is not None]
            return pokemons
        else:
            return []
    except Exception as e:
        print(f"Error getting user team: {e}")
        return []
    finally:
        conn.close()


def save_user_inventory(username: str, bag: dict, coins: int = 0) -> bool:
    """
    Save user's inventory (bag items and coins) to database
    
    Args:
        username (str): Username of the player
        bag (dict): Dictionary with item counts
        coins (int): Current pokecoin count
    
    Returns:
        bool: True if saved successfully, False otherwise
    """
    import sqlite3
    
    # First, ensure the inventory columns exist
    conn = sqlite3.connect(f"{DIR}/pokemon_users.db")
    cur = conn.cursor()
    
    try:
        # Add inventory columns if they don't exist
        try:
            cur.execute("ALTER TABLE users ADD COLUMN pokeballs INTEGER DEFAULT 0")
            cur.execute("ALTER TABLE users ADD COLUMN super_potions INTEGER DEFAULT 0")
            cur.execute("ALTER TABLE users ADD COLUMN max_potions INTEGER DEFAULT 0")
            cur.execute("ALTER TABLE users ADD COLUMN revives INTEGER DEFAULT 0")
            cur.execute("ALTER TABLE users ADD COLUMN max_revives INTEGER DEFAULT 0")
            cur.execute("ALTER TABLE users ADD COLUMN pokecoins INTEGER DEFAULT 0")
            conn.commit()
        except sqlite3.OperationalError:
            # Columns already exist
            pass
        
        # Update user's inventory
        cur.execute("""
            UPDATE users SET 
                pokeballs = ?, 
                super_potions = ?, 
                max_potions = ?, 
                revives = ?, 
                max_revives = ?, 
                pokecoins = ?
            WHERE username = ?
        """, (
            bag.get("pokeballs", 0),
            bag.get("super_potion", 0),
            bag.get("max_potion", 0),
            bag.get("revive", 0),
            bag.get("max_revive", 0),
            coins,
            username
        ))
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error saving inventory: {e}")
        return False
    finally:
        conn.close()


def load_user_inventory(username: str) -> tuple[dict, int]:
    """
    Load user's inventory (bag items and coins) from database
    
    Args:
        username (str): Username of the player
    
    Returns:
        tuple[dict, int]: (bag dictionary, coins)
    """
    import sqlite3
    
    # Default inventory for new users
    default_bag = {
        "pokeballs": 3,  # Start with 3 pokeballs
        "super_potion": 0,
        "max_potion": 0,
        "revive": 0,
        "max_revive": 0
    }
    default_coins = 10
    
    conn = sqlite3.connect(f"{DIR}/pokemon_users.db")
    cur = conn.cursor()
    
    try:
        # Check if inventory columns exist
        cur.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cur.fetchall()]
        
        if "pokeballs" not in columns:
            # Inventory system not set up yet, return defaults
            return default_bag, default_coins
        
        # Load user's inventory
        cur.execute("""
            SELECT pokeballs, super_potions, max_potions, revives, max_revives, pokecoins 
            FROM users WHERE username = ?
        """, (username,))
        
        row = cur.fetchone()
        
        if row:
            bag = {
                "pokeballs": row[0] if row[0] is not None else 3,
                "super_potion": row[1] if row[1] is not None else 0,
                "max_potion": row[2] if row[2] is not None else 0,
                "revive": row[3] if row[3] is not None else 0,
                "max_revive": row[4] if row[4] is not None else 0
            }
            coins = row[5] if row[5] is not None else 10
            return bag, coins
        else:
            return default_bag, default_coins
            
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return default_bag, default_coins
    finally:
        conn.close()


#user_create("test_user", "test", ["Pikachu", "Bulbasaur", "Charmander"])
#login_user("test_user", "test")





