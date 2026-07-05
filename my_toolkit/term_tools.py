# For tools (methods/functions) dealing with the terminal specifically #
import os
import sys
import time


# Decorator Function #
def cage_prompt(func):
    def wrapper(*args, **kwargs):
        print("|" + "*" * 120 + "|")
        print("|" + " " * 120 + "|")
        # 1. Grab the raw multi-line string from the function
        raw_text = func(*args, **kwargs)
        # 2. Split it by the newline character, and format each line individually!
        for line in raw_text.split("\n"):
            print(f"|{line:~^120}|")
        print("|" + " " * 120 + "|")
        print("|" + "*" * 120 + "|")

    return wrapper

# pass variables into function
@cage_prompt
def hold_narrative(*lines):
    # This automatically glues every string inside the 'lines' bucket
    # together, placing a newline '\n' between each one.
    return "\n".join(lines)



def clear_screen():                                                  # clear_screen()
    """Clears the terminal screen for a fresh slate."""
    os.system('cls' if os.name == 'nt' else 'clear')

# OUTPUTS MESSAGE TO CONSOLE LIKE A TYPEWRITER INSTEAD OF ALL AT ONCE # PUT THE STRING IN A TEXT VARIABLE
def typewriter_whole(text, delay=0.03):                              # typewriter_whole(text, delay=0.03)
    """Prints text one character at a time."""
    for char in text:
        print(char, end="")
        sys.stdout.flush()
        time.sleep(delay)

# OUTPUTS A DICT ORGANIZED INTO A PRETTY FRAME OR BOX IN TERMINAL #
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

# OUTPUTS A COMMAND MENU WITH ACTION OPTIONS IN TERMINAL #
def display_action_ui():                                              # display_action_ui()
    """Draws the command menu directly below the room UI."""
    print(f"|{'--- COMMAND MENU ---':^52}|")
    print("|" + " " * 52 + "|")
    print(f"|{'  > move [direction]    > pick up':<52}|")
    print(f"|{'  > equip [weapon]      > inventory':<52}|")
    print(f"|{'  > inspect [item]      > attack':<52}|")  # Added inspect here
    print(f"|{'  > barter              > .show_stats()':<52}|")
    print("<" + "," * 52 + ">")
    print("*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*")

# Global Interceptor, ALSO ALLOWS IMPUT STATMENTS TO BE TYPEWRITTER PRINTED T TERMINAL IF STATEMENT IS VAR = Typewriter_input(text, delay=0.03)
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

# SIMPLE CHARACTOR CREATOR #
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






















# NOTES on terminal display formating # alignment specifiers #
#messa = "I have always been a wild person but it lead to my success."
# {mess: <80} -> aligns the variable text on left side of spaces
# {mess: >80} -> aligns the variable text on left side of spaces
# {mess: ^80} -> aligns the variable text in the center of spaces
#print(f"| {messa: <80}  |") # {variable:"fill char" alignment direction symbol,num of spaces} {message:*^80}



























# For creating different structures in the terminal, for text based purposes #
class Box:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.box_data = [] #list[list[str]]

    # Generates the Box
    def gen_box(self):
        self.box_data = [["." for _ in range(self.width)] for _ in range(self.height)]

    # Prints Box style 1, Method of Box
    def display_box(self):
        frame = "X" + self.width * "=" + "X" + "~" * 141 + "X" + self.width * "=" + "X"
        print(frame)
        for row in self.box_data:
            print("|" + "".join(row) + "|" + " " * 141 + "|" + "".join(row) + "|")
        print(frame)

    # Prints Box style 2, Method of Box
    def display_boxa(self):
        frame = "X" + self.width * "=" + "X"
        center = "O" + self.width * "-" + "O"
        print(frame)
        print(center)
        for row in self.box_data:
            print("|" + "".join(row) + "|")
        print(center)
        print(frame)

# Prints Box style 3, lone function
def dual_menu():
    # print("\n")
    print(
        "*^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^*" + "*^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^*")  # Top Boarders
    print("<" + "'" * 52 + ">" + "<" + "'" * 52 + ">")
    print(f"|" + "I:" + " " * 48 + ":I" + "|" + "|" + "I:" + " " * 48 + ":I" + "|")
    print(f"|" + "I:" + " " * 48 + ":I" + "|" + "|" + "I:" + " " * 48 + ":I" + "|")
    print(f"|" + "I:" + " " * 48 + ":I" + "|" + "|" + "I:" + " " * 48 + ":I" + "|")
    print(f"|" + "I:" + " " * 48 + ":I" + "|" + "|" + "I:" + " " * 48 + ":I" + "|")
    print("<" + "," * 52 + ">" + "<" + "," * 52 + ">")  # Bottom Borders
    print(
        "*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*" + "*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*")
# Prints Box style 4, lone function
def action_menu():
    print("*____________________________________________________*")
    print("*" + "-" * 52 + "*")
    print(f"----SIMULATION STARTED -----*")
    print("*   Option 1: Type 'q' to quit.                      *")
    print("*   Option 2: Type 'r' to see the report.            *")
    print("*   Option 3: Type 'show' to see list of all animals *")
    print("*   Option 4: Enter your name.                       *")
    print("-" * 52 + "                                          *")
    print("*____________________________________________________*\n")


# Prints Box style 3, lone function


if __name__ == "__main__":
    # Creation of objects and calling methods/functions #
    # Instantiate the boxes
    box1 = Box(15, 8)
    box2 = Box(173, 4)
    box3 = Box(173, 4)
    box4 = Box(15, 8)
    box5 = Box(173, 4)
    box6 = Box(173, 4)
    # Generate the boxes
    box1.gen_box()
    box2.gen_box()
    box3.gen_box()
    box4.gen_box()
    box5.gen_box()
    # Display the boxes
    box2.display_boxa() # solid strip
    box1.display_box() # Box on both left and right
    dual_menu() # small duel window box
    action_menu()