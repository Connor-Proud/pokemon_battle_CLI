# Pokemon-CLI
    this open source code was created to imitate the battles you would have in the Pokemon game series developed by Nintendo
    it roughly imitates the game in a CLI layout using Python and binary


## requirements
    python 3.11+
    pip requirements:
        bcrypt
        rich
        keyboard
        pandas
        colorama


### usage
    run the pokemoncli.bat file or execute: python main.py


## license
    licensed under the Apache license 2.0
    Acknowledgements:
        NumFocus, Inc - Pandas
        BoppreH - Keyboard
        Niels Provos, David Mazières - bcrypt
        Will McGugan - rich
        Jonathan Hartley - colorama
        Python - Guido van Rossum


# Troubleshooting
    if anything in the program stops working, create a new account/user in the program to see if the issue is resolved
    if the issue is still not resolved after that step contact: contact.connor.proudlock@gmail.com


## created by:
    connor kennedy proudlock - SCRUM:
        worked on:
            all functions in functions.py
            main_menu.py
            majority of main.py
            creating the codebase structure
            finding all of the sounds to use
            creating the backend
            creating the damage function as a ctypes function to increase speed + UX
            linking all of the files together
            creating the shop
            improving the rewards system
            integrating the rewards system with the battles
    Raven Kirkham:
        worked on:
            adding to sql calls in main
            preparing the file to handle battles
    James Smith:
        worked on:
            creating the UI
            creating a basic rewards system
    Kian Watt:
        worked on:
            creating the shop // Kian took too long so Connor made it himself


### file structure:
```
    pokemon_battle_CLI-main/
    │
    ├── main.py                   # Main game engine with battle system
    ├── main_menu.py              # Animated main menu system
    ├── reward_module.py          # Reward system for battles
    ├── shop.py                   # Shop system (standalone)
    ├── shop_anim.py              # Shop building animation frames
    ├── test_items.py             # Item functionality test script
    ├── testfile.txt              # Test/debug file
    ├── documentation.md          # Project documentation
    ├── pokemoncli.bat            # Windows batch file to run the game
    ├── License                   # Apache 2.0 license file
    │
    ├── bcknd/                    # Backend systems
    │   ├── functions.py          # Core game functions (battle, shop, items, catching)
    │   ├── users.py              # User management and authentication system
    │   ├── pokemon_users.db      # SQLite database for user accounts and inventory
    │   ├── test_.dll             # Compiled Rust damage calculation library
    │   ├── test_.d               # Rust library definition file
    │   ├── libtest_.dll.a        # Static library file
    │   ├── files/                # Backend data files
    │   │   ├── instigator_lv.csv
    │   │   └── moves.csv
    │   └── __pycache__/          # Python bytecode cache
    │
    ├── files/                    # Main data files
    │   ├── capable_moves.csv     # Pokemon move compatibility data
    │   ├── instigator_lv.csv     # Level progression data
    │   ├── moves.csv             # Complete move database with stats
    │   ├── pokemon.csv           # Complete Pokemon database with stats
    │   └── sounds/               # Sound effects directory (38 files)
    │       ├── Title Theme.wav   # Main menu background music
    │       ├── button click.wav  # UI interaction sounds
    │       ├── button Hover.wav
    │       ├── IMHIT_Damage.wav  # Battle feedback sounds
    │       ├── IMHITSUPER_Super_Effective.wav
    │       ├── IMHITWEAK_Not_Very_Effective.wav
    │       └── [32 move sound files]
    │           ├── Tackle.wav
    │           ├── Scratch.wav
    │           ├── Quick Attack.wav
    │           ├── Water Gun.wav
    │           ├── Flame Burst.wav
    │           ├── Vine Whip.wav
    │           ├── Hydro Pump.wav
    │           ├── Psycho Cut.wav
    │           ├── Shadow Punch.wav
    │           ├── Dragon Claw.wav
    │           └── ... (etc.)
    │
    ├── __pycache__/              # Python bytecode cache (root level)
    ├── .idea/                    # IDE configuration files
    └── [System files]
```

