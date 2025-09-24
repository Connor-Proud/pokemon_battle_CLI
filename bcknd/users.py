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
        return True
    else:
        print("Invalid username or password")
        return False

#user_create("test_user", "test", ["Pikachu", "Bulbasaur", "Charmander"])
#login_user("test_user", "test")





