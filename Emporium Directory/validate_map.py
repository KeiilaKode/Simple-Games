# VALIDATION #


# MAP DICTIONARY #

# TERMINAL GAME ROOM LAYOUT #
layout: dict = {
    "Cave Entrance": {"Left": "Upper Tunnel",
                      "Forward": "Center Room",
                      "Right": "Rock Hallway",
                      "Stay": "Cave Entrance"},

    "Upper Tunnel": {"Back": "Cave Entrance",
                     "Stay": "Upper Tunnel",
                     "Forward": "Crest Point Cavern"},  # Blocked by mysterious danger

    "Center Room": {"Left": "Attic Ledge",
                    "Right": "Vine Room",
                    "Back": "Cave Entrance",
                    "Stay": "Center Room",
                    "Forward": "Path to Emporium"},

    "Crest Point Cavern": {"Back": "Upper Tunnel",  # Knock down bolder to allow attic ledge access to Brimstone Bay
                           "Left": "The Lookout"},

    "The Lookout": {"Back": "Crest Point Cavern",
                    "Stay": "The Lookout"},

    "Attic Ledge": {"Forward": "Brimstone Bay",  # Blocked by Bolder---
                    "Back": "Center Room",
                    "Stay": "Attic Ledge",
                    "Right": "Shadow Pit"},  # Jumps down into room

    "Shadow Pit": {"Right": "Path to Emporium",
                   "Left": "Ancient Treasure Room",
                   "Stay": "Shadow Pit"},

    "Ancient Treasure Room": {"Back": "Shadow Pit",
                              "Stay": "Ancient Treasure Room"},

    "Brimstone Bay": {"Back": "Attic Ledge",
                      "Stay": "Brimstone Bay"},

    "Rock Hallway": {"Left": "Hide-hole",
                     "Right": "Swamp Water Shallows",
                     "Back": "Cave Entrance",
                     "Forward": "Rock Hallway Deep",
                     "Stay": "Rock Hallway"},

    "Path to Emporium": {"Forward": "Mildred's Emporium",  # Mildred's Emporium # hole blocked path #
                         "Back": "Center Room",
                         "Stay": "Path to Emporium",
                         "Left": "Shadow Pit"},

    "Vine Room": {"Forward": "Secret Garden Lair", # Secret Garden Lair accessible with left from Rock hallway deep Blocked by Vines---Darkness Forest
                  "Back": "Center Room",
                  "Stay": "Vine Room",
                  "Right": "Rock Hallway Deep"},

    "Secret Garden Lair": {"Back": "Vine Room",
                           "Stay": "Secret Garden Lair",
                           "Right": "Rock Hallway Deep"},

    "Hide-hole": {"Back": "Rock Hallway",
                  "Stay": "Hide-hole"},

    "Swamp Water Shallows": {"Forward": "Swamp Water Center",
                             "Back": "Rock Hallway",
                             "Stay": "Swamp Water Shallows"},

    "Swamp Water Center": {"Forward": "Secret Room",
                           "Back": "Swamp Water Shallows",
                           "Stay": "Swamp Water Center"},

    "Secret Room": {"Back": "Swamp Water Center",
                    "Stay": "Secret Room"},

    "Rock Hallway Deep": {"Right": "Animal's Cove",  # added left for secret garden room
                          "Forward": "Hallway's End",
                          "Back": "Rock Hallway",
                          "Stay": "Rock Hallway Deep",
                          "Left": "Secret Garden Lair"},

    "Animal's Cove": {"Back": "Rock Hallway Deep",
                      "Stay": "Animal's Cove"},

    "Hallway's End": {"Right": "Fungus Trails",
                      "Left": "Rock Wall",
                      "Forward": "Small Passage",
                      "Back": "Rock Hallway Deep",
                      "Stay": "Hallway's End"},

    "Rock Wall": {"Back": "Hallway's End"},

    "Fungus Trails": {"Back": "Hallway's End",
                      "Stay": "Fungus Trails"},

    "Small Passage": {"Forward": "Mildred's Emporium",
                      "Stay": "Small Passage",
                      "Back": "Hallway's End"},

    "Mildred's Emporium": {"Back": "Path to Emporium",  # Hole Blocked Path
                           "Right": "Small Passage",
                           "Stay": "Mildred's Emporium"},
}


# FUNCTION #

def validate_map(layout, starting_room):
    print("--- RUNNING MAP VALIDATION ---\n")

    # 1. Grab every room name that actually has a dictionary entry
    all_defined_rooms = set(layout.keys())

    # 2. Let's walk the map to see what we can actually reach
    reachable_rooms = set()
    stack = [starting_room]

    while stack:
        room = stack.pop()
        if room not in reachable_rooms:
            reachable_rooms.add(room)

            # Look at all doors in the current room
            for direction, next_room in layout.get(room, {}).items():
                # We want to check all rooms, even if blocked, to ensure the room exists
                if next_room != room and "NOT SURE" not in next_room:
                    stack.append(next_room)


    unreachable = all_defined_rooms - reachable_rooms


    missing = reachable_rooms - all_defined_rooms

    # --- Print the Report ---
    print(f"Total Rooms Defined: {len(all_defined_rooms)}")
    print(f"Total Rooms Reachable from Start: {len(reachable_rooms)}\n")

    if not unreachable and not missing:
        print("✅ SUCCESS: Map is perfectly connected with no missing rooms!")

    if unreachable:
        print("⚠️ WARNING: The following rooms cannot be reached by the player:")
        for room in unreachable:
            print(f"  - {room}")

    if missing:
        print("\n❌ ERROR: The following rooms are linked to, but don't exist in the layout:")
        for room in missing:
            print(f"  - {room}")

# Run the validator
validate_map(layout, "Cave Entrance")