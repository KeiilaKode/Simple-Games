import sys
import time
import os

# --- IMPORTING YOUR CUSTOM MODULES ---
from players import Character, Hero
from emporium_structure import layout, treasure
from creation_page import *  # Brings in any pre-made weapons/items


# ==========================================
# --- SYSTEM FUNCTIONS ---
# ==========================================

def clear_screen():
    """Clears the terminal screen for a fresh slate."""
    os.system('cls' if os.name == 'nt' else 'clear')


def typewriter_whole(text, delay=0.03):
    """Prints text one character at a time."""
    for char in text:
        print(char, end="")
        sys.stdout.flush()
        time.sleep(delay)


def typewriter_input(text, delay=0.03):
    """Types out a question, waits for input, and intercepts global commands."""
    while True:
        typewriter_whole(text, delay)
        action = input().strip().lower()

        # INTERCEPT GLOBAL COMMANDS
        if action.endswith(".show_stats()"):
            requested_name = action.split(".")[0]
            player_found = False

            # Notice it now searches your Character class list!
            for p in Character.all_characters:
                if p.name.lower() == requested_name:
                    print("\n")
                    p.show_stats()
                    print("\n")
                    player_found = True
                    break

            if not player_found:
                print(f"\nSystem Error: No ID Card found for '{requested_name}'.\n")
            continue

        elif action == "quit":
            print("\nCowards...")
            quit()

        return action


def create_new_player():
    """Gathers user input to dynamically create a new Hero instance."""
    p_name = input("What is your name? \n").title()
    p_role = input("What type of adventurer are you? \n").title()

    while True:
        try:
            p_skill = int(input("What is your skill level? \n"))
            break
        except ValueError:
            print("Invalid input! Please enter a number.")

    # Create the hero using your class from players.py!
    new_hero = Hero(name=p_name, role=p_role)
    new_hero.health = p_skill
    new_hero.health_max = p_skill

    return new_hero


# ==========================================
# --- GAME EXECUTION ---
# ==========================================

if __name__ == "__main__":
    clear_screen()
    welcoming_words = ("   --- CHARACTER CREATION ---\n"
                       "Welcome to the Dungeon, you must have 2 people to enter. ")

    typewriter_whole(welcoming_words, 0.03)

    # --- PHASE 1: INTRO SEQUENCE ---
    while True:
        has_two = typewriter_input("\nDo you have two players in mind? yes/no \n", 0.03).lower()

        if has_two == "yes":
            print("Tell me who Player 1 is...")
            hero1 = create_new_player()
            time.sleep(1)
            print("And now for Player 2...")
            hero2 = create_new_player()
            time.sleep(1)
            break
        elif has_two == "no":
            print("Goodbye!")
            quit()
        else:
            print("That response is INVALID. Please type 'yes' or 'no'.")

    clear_screen()
    time.sleep(1)

    intro_message = """Aww, two brave little weaklings ready to die, HAHAHA! Suit yourself.
Now, I wont tell you very much but one thing you should know is that
every person that gains entry to this cave is given an ID CARD.
Here are both of your ID cards. \n"""

    typewriter_whole(intro_message, 0.04)
    print("\n")
    time.sleep(2)
    clear_screen()

    # These will now use the show_stats() you pasted into players.py
    hero1.show_stats()
    print("\n")
    time.sleep(2)
    hero2.show_stats()
    print("\n")

    enter_offer = ("Okay, now that you have your cards and you're already at the gates of the unknown,"
                   " I think its about time you two got lost inside the darkness. \n")
    typewriter_whole(enter_offer, 0.03)

    while True:
        enter = typewriter_input(" Are you ready to see what awaits you..? yes/no \n", 0.03).lower()

        if enter == "yes":
            clear_screen()
            typewriter_whole(" You and your friend are suddenly alone, no voice addressing you,"
                             " no weight hanging above. Just the empty darkness waiting for you "
                             "to fill its mouth.\n", 0.05)
            time.sleep(1)
            break
        elif enter == "no":
            print("Cowards...")
            quit()
        else:
            print("Answer the question! 'yes' or 'no'!")

    # ==========================================
    # --- PHASE 2: CAVE EXPLORATION ---
    # ==========================================

    current_room = "Cave Entrance"

    while True:
        print("\n" + "=" * 40)
        print(f" LOCATION: {current_room}")

        # Look up the paths available in the current room from emporium_structure.py
        available_paths = list(layout[current_room].keys())
        print(f" PATHS: {', '.join(available_paths)}")
        print("=" * 40)

        action = typewriter_input("\nWhat would you like to do? \n", 0.02).strip().lower()

        # Convert action to Title Case to match your dictionary keys (e.g., "Left")
        direction = action.title()

        if direction in layout[current_room]:
            current_room = layout[current_room][direction]
            clear_screen()
            typewriter_whole(f"You cautiously move {direction}...\n", 0.03)
            time.sleep(1)
        else:
            print("\nYou can't go that way, or that is an invalid command.")





























# ********* KEEP FOR MOVEMENT LOGIC **************#
# current_room = "Cave Entrance"
#
# # Let's say the player types 'Right'
# choice = "Right"
#
# if choice in rooms[current_room]:
#     current_room = rooms[current_room][choice]
#     print(f"You moved to the {current_room}!")
# else:
#     print("You can't go that way.")



