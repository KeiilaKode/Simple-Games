from creation_page import *
# CAVE GAME ROOM LAYOUT #
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

# MAPS TREASURE TO ROOMS: NOT COMPLETE #
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

# DICTIONARY OF ROOM MESSAGES TO BE PRINTED WHEN ENTERING EACH ROOM #
# --- ROOM DESCRIPTIONS ---
descriptions: dict = {
    "Cave Entrance": "The gaping mouth of the cavern looms before you. Cold air whispers from the blackness within.",
    "Upper Tunnel": "The ceiling low here, forcing you to stoop. Loose gravel crunches under your boots.",
    "Center Room": "A massive subterranean chamber. Water drips slowly from stalactites high above, echoing in the dark.",
    "Crest Point Cavern": "The cavern opens wide, revealing jagged rocky ledges. A massive boulder hangs precariously over a drop.",
    "The Lookout": "A high, narrow stone ledge overlooking a vast, pitch-black abyss. The wind howls aggressively up here.",
    "Attic Ledge": "You stand on a dusty stone platform high above the Center Room. A heavy boulder completely blocks a passage forward.",
    "Shadow Pit": "A dark, sunken depression where shadows seem to twist and move on their own. The air feels heavy and unnatural.",
    "Ancient Treasure Room": "Dust settles over crumbled pedestals. Though stripped of its golden glory long ago, old energy lingers.",
    "Brimstone Bay": "The smell of sulfur and intense heat chokes your lungs. Steam rises from deep cracks in the floor.",
    "Rock Hallway": "A natural corridor made of rough, jagged stone. The path splits into darkness ahead.",
    "Path to Emporium": "A worn, old pathway carved out by feet long ago. A bizarre purple glow emanates from further down the passage.",
    "Vine Room": "Thick, thorny vines weave across the walls like frozen snakes. They block a dark thicket to the forward direction.",
    "Secret Garden Lair": "An impossible underground grove. Bioluminescent moss coats the floor, casting an eerie emerald glow.",
    "Hide-hole": "A cramped, low-ceilinged alcove. It's safe, quiet, and completely hidden from the main hallway.",
    "Swamp Water Shallows": "Brambles give way to murky, knee-deep water. Something slimy skitters across your submerged boot.",
    "Swamp Water Center": "The black water deepens. Thick mist hangs low over the surface, obscuring whatever breathes in the dark.",
    "Secret Room": "A dry, forgotten vault hidden behind the watery expanse. Stone shelves sit empty, waiting to be searched.",
    "Rock Hallway Deep": "The tunnel descends deeper into the earth. The damp stone walls feel like they are closing in.",
    "Animal's Cove": "The air here is thick and smells of wet fur. Claw marks cover the stone walls, and bones litter the dirt.",
    "Hallway's End": "The corridor terminates at a dead end, splitting into narrow side passages. A cold draft blows from the front.",
    "Rock Wall": "A massive, solid rock face blocks any further movement this way. There is nothing here but dead stone.",
    "Fungus Trails": "Massive, glowing mushrooms tower over you like umbrellas, releasing silent puffs of sparkling spores.",
    "Small Passage": "A very tight, claustrophobic crawlspace. You can hear faint chimes and murmurs coming from ahead.",
    "Mildred's Emporium": "A bizarre, cluttered underground shop filled with dusty relics, strange potions, and a very peculiar shopkeeper.",
}

# --- ENEMY ENCOUNTERS ---
# Maps room names to enemy data (Name, Role, Health)
# --- ENEMY ENCOUNTERS ---
encounters: dict = {
    "Swamp Water Shallows": {"name": "Swamp Beast", "role": "Monster", "health": 20, "damage": 5},
    "Animal's Cove": {"name": "Rabid Cave Bear", "role": "Beast", "health": 30, "damage": 8},
    "Shadow Pit": {"name": "Shadow Creeper", "role": "Demon", "health": 15, "damage": 12}
}

#print(encounters["Swamp Water Shallows"]["health"]) to get the nested value
#print(encounters.items()) to get it all

# for room, data in encounters.items():
#     print("#" * 30)
#     print(f"Room:|{room:.^30}|")
#     print(f"Enemy:|{data['name']:.^30}|")
#     print(f"Type:|{data['role']:.^30}|")
#     print(f"HP:|{data['health']:.^30}|")
#     print("#" * 30)
#     print("\n")









