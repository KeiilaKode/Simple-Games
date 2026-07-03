from creation_page import *

layout:dict = {
        "Cave Entrance": {"Left": "Upper Tunnel",
                          "Straight": "Center Room",
                          "Right": "Rock Hallway",
                          "Stay": "Cave Entrance"},
        "Upper Tunnel": {"Back": "Cave Entrance",
                         "Stay": "Upper Tunnel",
                         "Forward": "Blocked by mysterious danger"},

        "Center Room": {"Left": "Attic Ledge",
                        "Right": "Vine Room",
                        "Back": "Cave Entrance",
                        "Stay": "Center Room"},
        "Attic Ledge": {"Forward": "Blocked by Bolder---",
                        "Back": "Center Room",
                        "Stay": "Attic Ledge"},

        "Rock Hallway": {"Left": "Hide-hole",
                         "Right": "Swamp Water Shallows",
                         "Back": "Cave Entrance",
                         "Forward": "Rock Hallway Deep",
                         "Stay": "Rock Hallway"},

        "Path to Emporium": {"Forward": "Hole Blocked Path---Emporium Shop",
                             "Back": "Center Room",
                             "Stay": "Path to Emporium"},

        "Vine Room": {"Forward": "Blocked by Vines---Darkness Forest",
                      "Back": "Center Room",
                      "Stay": "Vine Room"},

        "Hide-hole": {"Right": "Rock Hallway",
                      "Stay": "Hide-hole"},

        "Swamp Water Shallows": {"Forward": "Swamp Water Center",
                                 "Back": "Rock Hallway",
                                 "Stay": "Swamp Water Shallows"},

        "Swamp Water Center": {"Forward": "Secret Room",
                               "Back": "Swamp Water Shallows",
                               "Stay": "Swamp Water Center"},

        "Secret Room": {"Back": "Swamp Water Center",
                        "Stay": "Secret Room"},

        "Rock Hallway Deep": {"Right": "Animal's Cove",
                              "Straight": "Hallway's End"},

        "Animal's Cove": {"Back": "Rock Hallway Deep",
                          "Stay": "Animal's Cove"},

        "Hallway's End": {"Right": "Fungus Trails",  # Still must do
                          "Left": "Rock Wall"},
        "Rock Wall": {"back": "Hallway's End"},

        "Mildred's Emporium": {"Back": "Path to Emporium",
                               "Stay": "Mildred's Emporium"},
        "Fungus Trails": {"Left": "Hallway's End",
                          "forward": "NOT SURE YET" }
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















