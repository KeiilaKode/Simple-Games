from my_toolkit.term_tools import Box, dual_menu
import sys
import time
import os
# --- IMPORTING YOUR CUSTOM MODULES ---
from players import Character, Hero
from emporium_structure import layout, treasure, descriptions
from creation_page import *  # Brings in any pre-made weapons/items

# ==========================================
# --- SYSTEM FUNCTIONS ---                                                # --- SYSTEM FUNCTIONS --- #
# ==========================================

def clear_screen():                                                  # clear_screen()
    """Clears the terminal screen for a fresh slate."""
    os.system('cls' if os.name == 'nt' else 'clear')


def typewriter_whole(text, delay=0.03):                              # typewriter_whole(text, delay=0.03)
    """Prints text one character at a time."""
    for char in text:
        print(char, end="")
        sys.stdout.flush()
        time.sleep(delay)


def display_room_ui(room_name):                                      # display_room_ui(room_name)
    """Dynamically draws the room UI frame, paths, and items."""
    # 1. Format the title
    title = f"{room_name.upper()}"

    # 2. Draw Top Borders
    print("\n*^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^*")
    print("<" + "'" * 52 + ">")

    # 3. Print Title Centered
    print(f"|{title:^52}|")
    print("|" + " " * 52 + "|")  # Blank spacing line

    # new addition starts here
    if room_name in descriptions:
        desc_text = descriptions[room_name]

        # This breaks long sentences into pieces that are maximum 46 characters long
        words = desc_text.split()
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= 46:
                current_line += (word + " ")
            else:
                print(f"|  {current_line:<48}  |")
                current_line = word + " "
        if current_line:
            print(f"|  {current_line:<48}  |")

        print("|" + " " * 52 + "|")  # Blank spacing line
    # new addition ends here
    # 4. Check for Items on the floor!
    if room_name in treasure:
        item_text = f" YOU SEE A: {treasure[room_name].name}"
        print(f"|{item_text:<52}|")
        print("|" + " " * 52 + "|")  # Blank spacing line

    # 5. Print Available Paths
    print(f"|{' AVAILABLE PATHS:':<52}|")
    for direction, destination in layout[room_name].items():
        path_string = f"   > {direction}: {destination}"
        print(f"|{path_string:<52}|")

    # 6. Draw Bottom Borders # Possibly remove #
    print("<" + "," * 52 + ">")
    print("*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*")


def display_action_ui():                                              # display_action_ui()
    """Draws the command menu directly below the room UI."""
    print(f"|{'--- COMMAND MENU ---':^52}|")
    print("|" + " " * 52 + "|")
    print(f"|{'  > move [direction]    > pick up':<52}|")
    print(f"|{'  > equip [weapon]      > inventory':<52}|")
    print(f"|{'  > inspect [item]      > attack':<52}|")  # Added inspect here
    print(f"|{'  > barter              > .show_stats()':<52}|")

    # Cap off the bottom of the UI
    print("<" + "," * 52 + ">")
    print("*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*")


# Global Interceptor
def typewriter_input(text, delay=0.03):                                # typewriter_input(text, delay=0.03)
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


def create_new_player():                                             # create_new_player()
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
# --- GAME EXECUTION ---                                                  # ---PHASE 1: GAME EXECUTION --- #
# ==========================================


if __name__ == "__main__":
    clear_screen()
    box1 = Box(15, 8)
    box2 = Box(173, 4)
    box2.gen_box()
    box2.display_boxa()

    print("\n")
    welcoming_words = ("   --- WELCOME TO CAVE ELSEWHERE ---\n"
                       "This is where you come to die, brave soul. ")

    typewriter_whole(welcoming_words, 0.03)

    # --- PHASE 1: INTRO SEQUENCE ---
    print("\nTell me...")
    hero1 = create_new_player()
    time.sleep(1)

    clear_screen()
    time.sleep(1)



    box2.display_boxa()


    intro_message = """Aww, a brave little weakling ready to die, HAHAHA! Suit yourself.
Now, I wont tell you very much but one thing you should know is that
every person that gains entry to this cave is given an ID CARD.
Here is your ID card. \n"""

    typewriter_whole(intro_message, 0.04)
    print("\n")
    time.sleep(2)
    clear_screen()

    # These will now use the show_stats() you pasted into players.py
    box2.display_boxa()
    print("\n")
    hero1.show_stats()
    print("\n")
    time.sleep(2)


    enter_offer = ("Okay, now that you have your cards and you're already at the gates of the unknown,"
                   " I think its about time you got lost inside the darkness. \n")
    typewriter_whole(enter_offer, 0.03)

    while True:
        enter = typewriter_input(" Are you ready to see what awaits you..? yes/no \n", 0.03).lower()
        dual_menu()

        if enter == "yes":
            clear_screen()

            box2.display_boxa()
            typewriter_whole(" You are suddenly alone, no voice addressing you,"
                             " no weight hanging above. Just the empty darkness waiting for you "
                             "to fill its mouth.", 0.05)
            time.sleep(1)
            break
        elif enter == "no":
            print("Cowards...")
            quit()
        else:
            print("Answer the question! 'yes' or 'no'!")

    # ==========================================
    # --- PHASE 2: CAVE EXPLORATION ---                                    # --- PHASE 2: CAVE EXPLORATION --- #
    # ==========================================
    #print("---------------------------------")
    current_room = "Cave Entrance"
    print("---------------------------------")

    #  GAME LOOP #
    while True:
        # 1. Paint the UI (Room first, then Actions)
        display_room_ui(current_room)
        display_action_ui()

        # 2. Get the player's command
        action = typewriter_input("\nWhat would you like to do? \n", 0.02).strip().lower()

        # 3. Split the command into separate words (e.g., ["move", "left"])
        words = action.split()

        # If they just hit enter without typing anything, ignore it
        if not words:
            clear_screen()
            continue

        # The first word they typed is the primary command
        command = words[0]

        # --- THE COMMAND PARSER ---                                  #  --- THE COMMAND PARSER --- #

        if command == "move":                                                       # Move
            # Check if they actually typed a direction after "move"
            if len(words) > 1:
                direction = words[1].title()
                if direction in layout[current_room]:
                    current_room = layout[current_room][direction]
                    clear_screen()
                    box1.display_box()
                    typewriter_whole(f"You cautiously move {direction} into a different room...\n", 0.03)
                    time.sleep(1)
                else:
                    clear_screen()
                    box1.display_box()
                    print(f"\n*** You can't move '{direction}' from here. ***\n")
            else:
                clear_screen()
                box1.display_box()
                print("\n*** Move where? (Try 'move left' or 'move straight') ***\n")

        elif command == "inspect":                                                  # Inspect
            if len(words) > 1:
                target_name = " ".join(words[1:]).lower()
                found = False

                # Check items in the bag first
                for item in hero1.bag.purse:
                    if item.name.lower() == target_name:
                        clear_screen()
                        print(f"\n--- INSPECTING: {item.name.upper()} ---")
                        print(f"\n{item.description}\n")
                        typewriter_input("Press Enter to continue...", 0.01)
                        found = True
                        break

                # If not in bag, check the room
                if not found and current_room in treasure:
                    item_in_room = treasure[current_room]
                    if item_in_room.name.lower() == target_name:
                        clear_screen()
                        print(f"\n--- INSPECTING: {item_in_room.name.upper()} ---")
                        print(f"\n{item_in_room.description}\n")
                        typewriter_input("Press Enter to continue...", 0.01)
                        found = True

                if not found:
                    clear_screen()
                    box1.display_box()
                    print(f"\n*** You don't see any '{target_name}' to inspect. ***\n")
            else:
                clear_screen()
                box1.display_box()
                print("\n*** Inspect what? (Try 'inspect crowbar') ***\n")
            clear_screen()

        # Controls picking up items #
        elif command == "pick" and len(words) > 1 and words[1] == "up":                # Pick up
            # Does this room actually have treasure?
            if current_room in treasure:
                found_item = treasure[current_room]
                clear_screen()
                print("\n")
                # hero1 automatically gets the item!
                hero1.pick_up(found_item)
                # Remove the item from the room
                del treasure[current_room]
                print("\n")
                time.sleep(2)
                clear_screen()
            else:
                clear_screen()
                box1.display_box()
                print("\n*** There is nothing to pick up here. ***\n")

        # NEED TO DO: INPUT VALIDATION needs to be here, cause if u attempt to equip a non weapon, the game crashes #
        elif command == "equip":                                                       # Equip
            if len(words) > 1:
                # Join the words together (e.g., "Iron Sword")
                weapon_name = " ".join(words[1:]).title()
                clear_screen()
                print("\n")
                # hero1 automatically equips it
                hero1.equip(weapon_name)
                print("\n")
                time.sleep(2)
                clear_screen()
            else:
                clear_screen()
                box1.display_box()
                print("\n*** Equip what? (Try 'equip knife') ***\n")

        elif command == "attack":                                                       # Attack
            clear_screen()
            box1.display_box()
            print("\n*** There is nothing to attack yet! ***\n")

        elif command == "barter":                                                        # Barter
            clear_screen()
            box1.display_box()
            print("\n*** There is no one to trade with right now. ***\n")
        elif command == "inventory" or command == "bag":
            clear_screen()
            print("-------------------------------")
            print(f"\n--- {hero1.name}'s Inventory ---")

            if len(hero1.bag.purse) == 0:
                print("Your bag is empty.")
            else:
                for item in hero1.bag.purse:
                    print(f" - {item.name}")

            print(f"Capacity: {len(hero1.bag.purse)}/{hero1.bag.capacity}")
            print("-------------------------------\n")

            typewriter_input("Press Enter to continue...", 0.01)
            clear_screen()

        else:
            # If the command wasn't move, pick up, equip, attack, or barter (and wasn't intercepted as a global command)
            clear_screen()
            print(f"\n*** '{command}' is not a valid action. ***\n")



























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



