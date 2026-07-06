from creation_page import *


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

    "Rock Wall": {"back": "Hallway's End"},

    "Fungus Trails": {"Back": "Hallway's End",
                      "Forward": "NOT SURE YET",
                      "Stay": "Fungus Trails"},

    "Small Passage": {"Forward": "Mildred's Emporium",
                      "Stay": "Small Passage",
                      "Back": "Hallway's End"},

    "Mildred's Emporium": {"Back": "Path to Emporium",  # Hole Blocked Path
                           "Right": "Small Passage",
                           "Stay": "Mildred's Emporium"},
}


# No quotation marks around the values as they are now real objects.
treasure: dict = {
    "Secret Room": crowbar,
    "Swamp Water Center": treasure_chest,
    "Fungus Trails": diving_mask,
    "Attic Ledge": collar,
    "Mildred's Emporium": torch,
    "Hide-hole": glass_bottle,
    "Vine Room": small_pouch,
    "Swamp Water Shallows": sharpening_stone
}

# def master_key(layout, treasure):
#     print("~*~*~*~*~*~*~*~*")
#     print("~* CAVE MAP *~*")
#     print("~*~*~*~*~*~*~*~*")
#     print("\n")
#
#     # Way to handle nested dictionaries (Rooms)
#     # for location, connections in layout.items():
    #     print(f"Location: {location}")
    #     for direction, destination in connections.items():
    #         print(f"  {direction} -> {destination}")
    #     print("-" * 20)  # Separator for readability

    # print("\n")
    # print("~*~*~*~*~*~*~*~*")
    # print("~* ITEM MAP *~*")
    # print("~*~*~*~*~*~*~*~*")
    # print("\n")

    # Way to handle flat dictionaries (Items)
    # Changed variable name from 'rooms' to 'location' to avoid confusion
    # for location, tool in treasure.items():
        # print(f"{location}: {tool}")


# Call the function with your defined dictionaries
# master_key(layout, treasure)















