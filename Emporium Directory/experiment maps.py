import sys
import time
import os

class Player:
    all_players = []
    def __init__(self, name, type_hero, skill_lvl):
        # These are instance attributes now!
        self.name = name
        self.type_hero = type_hero
        self.skill_lvl = skill_lvl

        # Default starting stats
        self.hp = 10
        self.mp = 5
        self.gold = 0
        self.backpack = []
        Player.all_players.append(self)
    # Method
    def show_stats(self):
        # Unpack the dictionary values into your display strings
        stat_title = f"---CHARACTER ATTRIBUTES---"
        stat_name = f" NAME:  {self.name}"
        stat_type_hero = f" CLASS: {self.type_hero}"
        stat_skill = f" SKILL: {self.skill_lvl}"
        stat_hp = f" HP:    {self.hp}/10"
        stat_mp = f" MP:    {self.mp}/5"
        stat_gold = f" GOLD:  {self.gold}"
        stat_backpack = f" ITEMS: {self.backpack}"

        # Prints it all out in a frame to the terminal.
        print("*^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^*")  # Top Boarders
        print("<" + "'"  * 52 + ">")
        print(f"|{stat_title:^52}|")  # Body with Injected Stats (The :<52 keeps the right wall aligned!)
        print(f"|{stat_name:<52}|")
        print(f"|{stat_type_hero:<52}|")
        print(f"|{stat_skill:<52}|")
        print(f"|{stat_hp:<52}|")
        print(f"|{stat_mp:<52}|")
        print(f"|{stat_gold:<52}|")
        print(f"|{stat_backpack:<52}|")
        print("<" + "," * 52 + ">")  # Bottom Borders
        print("*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*")


# Function that Creates Players
def create_new_player():
    """Gathers user input to dynamically create a new Player instance."""
    p_name = input("What is your name? \n")
    p_hero = input("What type of adventurer are you? \n")

    while True:
        try:
            p_skill = int(input("What is your skill level? \n"))
            break
        except ValueError:
            print("Invalid input! Please enter a number.")

    # Instantiate and return the player object directly!
    return Player(name=p_name, type_hero=p_hero, skill_lvl=p_skill)

if __name__ == "__main__":

    def typewriter_whole(text, delay):
        for char in text:
            print(char, end="")
            sys.stdout.flush()
            time.sleep(delay)


    def typewriter_input(text, delay=0.03):
        """Types out a question, waits for input, and intercepts global commands."""

        while True:
            # 1. Type the question and get the answer
            typewriter_whole(text, delay)
            action = input().strip().lower()

            # 2. INTERCEPT GLOBAL COMMANDS
            # Is the player asking for stats?
            if action.endswith(".show_stats()"):
                requested_name = action.split(".")[0]
                player_found = False

                for p in Player.all_players:
                    if p.name.lower() == requested_name:
                        print("\n")
                        p.show_stats()
                        print("\n")
                        player_found = True
                        break

                if not player_found:
                    print(f"\nSystem Error: No ID Card found for '{requested_name}'.\n")

                # Use 'continue' to restart this while loop and ask the question again!
                continue

                # Is the player trying to quit the whole game?
            elif action == "quit":
                print("\nCowards...")
                quit()

            # 3. NORMAL INPUT
            # If it wasn't a global command, hand the text back to the main game
            return action


    def clear_screen():
        """Clears the terminal screen for a fresh slate."""
        os.system('cls' if os.name == 'nt' else 'clear')

    welcoming_words = ("   --- CHARACTER CREATION ---"
    "Welcome to the Dungeon, you must have 2 people to enter. ")

    typewriter_whole(welcoming_words, 0.03)
    while True:
        has_two = typewriter_input("\nDo you have two players in mind? yes/no \n", 0.03).lower()

        if has_two == "yes":
            print("Tell me who Player 1 is...")
            hero1 = create_new_player()
            time.sleep(1)
            print("And now for Player 2...")
            hero2 = create_new_player()
            time.sleep(1)
            break  # Exit the loop since we got valid input and created the players!

        elif has_two == "no":
            print("Goodbye!")
            quit()

        else:
            # If they typed anything other than 'yes' or 'no'
            print("That response is INVALID. Please type 'yes' or 'no'.")
    clear_screen()
    time.sleep(1)
    intro_message = """Aww, two brave little weaklings ready to die, HAHAHA! Suit yourself.
    Now, I wont tell you very much but one thing you should know is that
    every person that gains entry to this cave is given an ID CARD.
    Here are both of your ID cards. \n"""

    # Next sentence then shows both cards.
    typewriter_whole(intro_message, 0.04)
    print("\n")
    time.sleep(2)
    clear_screen()
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
            # Added a typewriter effect here for dramatic flair!
            clear_screen()
            typewriter_whole(
                " You and your friend are suddenly alone, no voice addressing you,"
                " no weight hanging above. Just the empty darkness waiting for you "
                "to fill its mouth.\n",
                0.05)
            break
        elif enter == "no":
            print("Cowards...")
            quit()
        else:
            print("Answer the question! 'yes' or 'no'!")
        # ==========================================
        # --- PHASE 2: THE MAIN GAME LOOP ---
        # ==========================================

    while True:
        # 1. Ask the question. The function automatically handles '.show_stats()' and 'quit'!
        action = typewriter_input("\nWhat would you like to do? (explore) \n", 0.03)

        # 2. You only need to code the story choices here!
        if action == "explore":
            print("\nYou two take one last glance at the outside world, and begin the descent into the shadows.")
            break  # Moves you to the next room/phase
        elif action == "quit":
            print("\nCowards...")
            quit()

        else:
            print("\nInvalid command. Try typing 'explore'.")




