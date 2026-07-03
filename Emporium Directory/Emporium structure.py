# file for cave layout and any dicts, list, ect.
# World Mapp  rooms:dict{}, holding dicts like Cave Entrance:dicts{} as keys,
# and the dict:rooms{} values are dicts{} of the corrosponding the directions from current room, and where they take you


layout:dict = {
        "Cave Entrance": {"Left": "Upper Tunnel",  # Still must do
                          "Straight": "Center Room",
                          "Right": "Rock Hallway",
                          "Stay": "Cave Entrance"},

        "Center Room": {"Left": "Attic Ledge",  # Still must do
                        "Right": "Vine Room",  # Still must do
                        "Back": "Cave Entrance",
                        "Stay": "Center Room"},
        "Attic Ledge": {"Forward": "Blocked by Bolder---",
                        "Back": "Center Room",
                        "Stay": "Attic Ledge"},

        "Rock Hallway": {"Left": "Hide-hole",  # Still must do
                         "Right": "Swamp Water Shallows",  # Still must do
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

        "Mildred's Emporium": {"Back": "Path to Emporium",
                               "Stay": "Mildred's Emporium"}
    }


#                items_map:{Room:Item} # add the room sentence somehow
treasure:dict = {"Secret Room": "Crowbar",
             "Swamp Water Center": "Treasure Chest",
             "Fungus Trails": "Diving Mask",
             "Attic Ledge": "Collar",
             "Mildred's Emporium": "Torch",
             "Hide-hole": "Glass Bottle",
             "Vine Room": "Small Pouch",
             "Swamp Water Shallows": "Sharpening Stone"
    }


def master_key(layout, treasure):
    print("~*~*~*~*~*~*~*~*")
    print("~* CAVE MAP *~*")
    print("~*~*~*~*~*~*~*~*")
    print("\n")

    # Way to handle nested dictionaries (Rooms)
    for location, connections in layout.items():
        print(f"Location: {location}")
        for direction, destination in connections.items():
            print(f"  {direction} -> {destination}")
        print("-" * 20)  # Separator for readability

    print("\n")
    print("~*~*~*~*~*~*~*~*")
    print("~* ITEM MAP *~*")
    print("~*~*~*~*~*~*~*~*")
    print("\n")

    # Way to handle flat dictionaries (Items)
    # Changed variable name from 'rooms' to 'location' to avoid confusion
    for location, tool in treasure.items():
        print(f"{location}: {tool}")


# Call the function with your defined dictionaries
master_key(layout, treasure)
















