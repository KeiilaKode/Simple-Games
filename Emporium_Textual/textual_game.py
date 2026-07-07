from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.containers import Vertical, Horizontal, Center
from textual.widgets import Header, Footer, Static, Input, Button, Label
from textual import on

# Import your game logic
from emporium_structure import layout, descriptions, treasure, encounters
from players import Hero
from creation_page import *  # Ensures items/weapons exist


# ==========================================
# --- SCREEN 1: CHARACTER CREATION ---
# ==========================================
class CharacterCreationScreen(Screen):
    """The intro screen where players build their hero."""

    def compose(self) -> ComposeResult:
        with Center():
            with Vertical(id="creation-box"):
                yield Label("--- WELCOME TO CAVE ELSEWHERE ---", id="intro-title")
                yield Label("This is where you come to die, brave soul.", id="intro-subtitle")

                yield Label("\nWhat is your name?")
                yield Input(placeholder="e.g., Arthur", id="hero-name")

                yield Label("What type of adventurer are you?")
                yield Input(placeholder="e.g., Knight", id="hero-class")

                yield Button("Enter the Darkness", id="start-button", variant="error")

    @on(Button.Pressed, "#start-button")
    def start_game(self, event: Button.Pressed) -> None:
        """When the button is clicked, build the hero and start the game."""
        name = self.query_one("#hero-name", Input).value.strip().title()
        role = self.query_one("#hero-class", Input).value.strip().title()

        if name and role:
            # 1. Create the Hero object (saving it to the main App so all screens can access it)
            self.app.player_hero = Hero(name=name, role=role)

            # 2. Switch to the main game screen
            self.app.push_screen("main_game")


# ==========================================
# --- SCREEN 2: MAIN GAME LOOP ---
# ==========================================
class MainGameScreen(Screen):
    """The main exploration UI."""

    current_room = "Cave Entrance"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-container"):
            # Left side: Room info and typing command
            with Vertical(id="left-panel"):
                yield Static("ROOM TITLE", id="room-title")
                yield Static("Room description...", id="room-desc")
                yield Input(placeholder="What would you like to do?", id="command-input")

            # Right side: Stats and Paths
            with Vertical(id="right-panel"):
                yield Static("Stats will load here...", id="player-stats")
                # I ADDED INSPECT TO THE MENU BELOW!
                yield Static(
                    "\n--- COMMAND MENU ---\n> move [direction]\n> pick up\n> inventory\n> inspect [item]\n> equip [weapon]\n> attack",
                    id="commands")
                yield Static("\n--- AVAILABLE PATHS ---\n", id="paths")
        yield Footer()

    def on_mount(self) -> None:
        """Fires right when the game screen loads."""
        self.update_ui(self.current_room)
        self.query_one("#command-input", Input).focus()

    def update_ui(self, room_name: str) -> None:
        """Paints the text based on the room and player stats."""
        self.query_one("#room-title", Static).update(f"*** {room_name.upper()} ***")

        desc_text = descriptions.get(room_name, "There is nothing here.")

        if room_name in treasure:
            desc_text += f"\n\n*** YOU SEE A: {treasure[room_name].name.upper()} ***"

        if room_name in encounters:
            enemy = encounters[room_name]
            desc_text += f"\n\n!!! WARNING: A {enemy['name'].upper()} ({enemy['role']}) is here! !!!\nHP: {enemy['health']} | DMG: {enemy['damage']}"

        self.query_one("#room-desc", Static).update(desc_text)
        self.query_one("#player-stats", Static).update(self.app.player_hero.get_stats_string())

        path_text = "--- AVAILABLE PATHS ---\n"
        for direction, destination in layout[room_name].items():
            path_text += f"> {direction}: {destination}\n"
        self.query_one("#paths", Static).update(path_text)

    @on(Input.Submitted, "#command-input")
    def handle_command(self, event: Input.Submitted) -> None:
        """Handles player commands."""
        command_text = event.value.strip().lower()
        words = command_text.split()
        self.query_one("#command-input", Input).value = ""  # Clear the box

        if not words: return
        command = words[0]

        # Grab the base description so we can append messages to it
        base_desc = descriptions.get(self.current_room, "")

        # --- MOVEMENT ---
        if command == "move" and len(words) > 1:
            direction = words[1].title()
            if direction in layout[self.current_room]:
                self.current_room = layout[self.current_room][direction]
                self.update_ui(self.current_room)
            else:
                self.query_one("#room-desc", Static).update(
                    f"{base_desc}\n\n*** You cannot move '{direction}' from here. ***")

        # --- PICK UP ---
        elif command == "pick" and len(words) > 1 and words[1] == "up":
            if self.current_room in treasure:
                found_item = treasure[self.current_room]
                result_message = self.app.player_hero.pick_up(found_item)

                # Check if the item actually made it into the bag before deleting from room
                if found_item in self.app.player_hero.bag.purse:
                    del treasure[self.current_room]

                # FORCE update the stats panel no matter what
                self.query_one("#player-stats", Static).update(self.app.player_hero.get_stats_string())
                self.query_one("#room-desc", Static).update(f"{base_desc}\n\n{result_message}")
            else:
                self.query_one("#room-desc", Static).update(f"{base_desc}\n\n*** There is nothing to pick up here. ***")

        # --- EQUIP ---
        elif command == "equip" and len(words) > 1:
            weapon_name = " ".join(words[1:])
            result_message = self.app.player_hero.equip(weapon_name)

            # FORCE update stats so the new weapon and DMG values show up
            self.query_one("#player-stats", Static).update(self.app.player_hero.get_stats_string())
            self.query_one("#room-desc", Static).update(f"{base_desc}\n\n{result_message}")

        # --- INSPECT ---
        elif command == "inspect" and len(words) > 1:
            target_name = " ".join(words[1:]).lower()
            found_desc = None

            # Check inventory first
            for item in self.app.player_hero.bag.purse:
                if item.name.lower() == target_name:
                    found_desc = item.description
                    break

            # Check room if not in inventory
            if not found_desc and self.current_room in treasure:
                if treasure[self.current_room].name.lower() == target_name:
                    found_desc = treasure[self.current_room].description

            # Display results
            if found_desc:
                self.query_one("#room-desc", Static).update(
                    f"{base_desc}\n\n*** INSPECTING {target_name.upper()} ***\n{found_desc}")
            else:
                self.query_one("#room-desc", Static).update(
                    f"{base_desc}\n\n*** You don't see any '{target_name}' to inspect. ***")

        # --- INVENTORY ---
        elif command in ["inventory", "bag"]:
            inv_string = self.app.player_hero.get_inventory_string()
            self.query_one("#room-desc", Static).update(f"{base_desc}\n\n{inv_string}")

# ==========================================
# --- APP LAUNCHER ---
# ==========================================
class CaveElsewhereApp(App):
    """The core application that manages screens and data."""

    CSS = """
    Screen { background: #111111; }

    /* Character Creation CSS */
    #creation-box { width: 50; height: auto; border: solid green; padding: 2; align: center middle; }
    #intro-title { text-style: bold; color: lime; text-align: center; }
    #intro-subtitle { color: grey; margin-bottom: 2; text-align: center; }
    Input { margin-bottom: 1; }
    Button { width: 100%; margin-top: 1; }

    /* Main Game CSS */
    #main-container { height: 100%; }
    #left-panel { width: 2fr; border: solid green; padding: 1; }
    #right-panel { width: 1fr; border: solid purple; padding: 1; }
    #room-title { content-align: center middle; text-style: bold; color: lime; height: 3; border-bottom: solid green; }
    #room-desc { height: 1fr; margin-top: 1; }
    #player-stats { border-bottom: solid purple; padding-bottom: 1; }
    #command-input { dock: bottom; border: solid white; }
    """

    def on_mount(self) -> None:
        # Register the screens
        self.install_screen(CharacterCreationScreen(), name="creation")
        self.install_screen(MainGameScreen(), name="main_game")
        # Push the first screen to start
        self.push_screen("creation")


if __name__ == "__main__":
    app = CaveElsewhereApp()
    app.run()