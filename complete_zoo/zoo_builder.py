from zoo import Zoo
from employee import Employee, GateKeeper
from enclosure import Building, Terrestrial_Enclosure, Aerial_Enclosure, Aquatic_Enclosure
from mammal import Lion, Tiger, Leopard, Gorilla, Chimpanzee, Black_Bear, Kodiak_Bear
from aerial import Eagle, Turkey, Parrot, Ostrich, Falcon, Peacock, Chicken
from aquatic import Fish, Octopus, Dolphin, Squid, Star_fish, Shark, Sea_Urchin


def setup_zoo():
    print("Building the Zoo... Please wait.")

    # 1. Create the master container!
    my_zoo = Zoo(name="Complete Zoo Interactive")

    # --- 1. BUILD THE ZOO BUILDINGS ---
    enter_center = Building("Enter Center")
    safari_shop = Building("Safari Souvenirs Gift Shop")
    grazing_station = Building("The Grazing Station Cafeteria")
    main_restrooms = Building("Main Plaza Restrooms")
    east_restrooms = Building("East Wing Restrooms")
    first_aid = Building("First Aid & Medical Station")
    info_kiosk = Building("Information Kiosk")

    my_zoo.add_building(enter_center)
    my_zoo.add_building(safari_shop)
    my_zoo.add_building(grazing_station)
    my_zoo.add_building(main_restrooms)
    my_zoo.add_building(east_restrooms)
    my_zoo.add_building(first_aid)
    my_zoo.add_building(info_kiosk)

    # --- 2. TERRESTRIAL ENCLOSURES ---
    lions_den = Terrestrial_Enclosure(name="Lions Den", wing="Carnivore Wing")
    tiger_trek = Terrestrial_Enclosure(name="Tiger Trek", wing="Carnivore Wing")
    leopard_lounge = Terrestrial_Enclosure(name="Spotted Sanctuary", wing="Carnivore Wing")
    primate_house = Terrestrial_Enclosure(name="Ape Alley", wing="Primate Wing")
    chimp_reserve = Terrestrial_Enclosure(name="Chimp Canopy", wing="Primate Wing")
    bear_habitat = Terrestrial_Enclosure(name="Grizzly Gulch", wing="Bear Country")
    kodiak_cave = Terrestrial_Enclosure(name="The Great Cave", wing="Bear Country")

    my_zoo.add_enclosure(lions_den)
    my_zoo.add_enclosure(tiger_trek)
    my_zoo.add_enclosure(leopard_lounge)
    my_zoo.add_enclosure(primate_house)
    my_zoo.add_enclosure(chimp_reserve)
    my_zoo.add_enclosure(bear_habitat)
    my_zoo.add_enclosure(kodiak_cave)

    # --- 3. AQUATIC ENCLOSURES ---
    shark_tank = Aquatic_Enclosure(name="Predator Reef", wing="Deep Sea")
    dolphin_cove = Aquatic_Enclosure(name="Dolphin Cove", wing="Marine Mammals")
    kelp_forest = Aquatic_Enclosure(name="Kelp Forest", wing="Coastal Waters")
    touch_pool = Aquatic_Enclosure(name="Interactive Touch Pool", wing="Shallows")
    octopus_cave = Aquatic_Enclosure(name="Cephalopod Cavern", wing="Deep Sea")
    coral_reef = Aquatic_Enclosure(name="Great Coral Reef", wing="Tropical Waters")

    my_zoo.add_enclosure(shark_tank)
    my_zoo.add_enclosure(dolphin_cove)
    my_zoo.add_enclosure(kelp_forest)
    my_zoo.add_enclosure(touch_pool)
    my_zoo.add_enclosure(octopus_cave)
    my_zoo.add_enclosure(coral_reef)

    # --- 4. AERIAL ENCLOSURES ---
    top_watch = Aerial_Enclosure(name="The Point", wing="Aviary")
    eagle_aerie = Aerial_Enclosure(name="Raptor Ridge", wing="Birds of Prey")
    falcon_roost = Aerial_Enclosure(name="Falconer's Peak", wing="Birds of Prey")
    parrot_paradise = Aerial_Enclosure(name="Tropical Tropics", wing="Exotic Birds")
    ostrich_paddock = Aerial_Enclosure(name="Flightless Field", wing="Plains Birds")
    poultry_pen = Aerial_Enclosure(name="Domestic Fowl Barn", wing="Farm Birds")
    peacock_garden = Aerial_Enclosure(name="Peacock Promenade", wing="Free Flight")

    my_zoo.add_enclosure(top_watch)
    my_zoo.add_enclosure(eagle_aerie)
    my_zoo.add_enclosure(falcon_roost)
    my_zoo.add_enclosure(parrot_paradise)
    my_zoo.add_enclosure(ostrich_paddock)
    my_zoo.add_enclosure(poultry_pen)
    my_zoo.add_enclosure(peacock_garden)

    # --- 5. HIRE EMPLOYEES & MANAGEMENT ---
    katie = GateKeeper(name="Katie", job_title="Gate Cashier")
    sarah = GateKeeper(name="Sarah", job_title="Turnstile Operator")
    marcus = GateKeeper(name="Marcus", job_title="VIP Entrance Guard")
    chloe = GateKeeper(name="Chloe", job_title="Group Sales Kiosk")

    richard = Employee(name="Richard", job_title="Lion Tender")
    mr_sterling = Employee(name="Mr. Sterling", job_title="Zoo Director")
    dr_vance = Employee(name="Dr. Vance", job_title="Head Veterinarian")
    jessica = Employee(name="Jessica", job_title="Operations Manager")

    gordon = Employee(name="Gordon", job_title="Head Chef")
    bob = Employee(name="Bob", job_title="Plaza Janitor")
    alice = Employee(name="Alice", job_title="East Wing Janitor")

    joe = Employee(name="Joe", job_title="Exotic Cat Specialist")
    amanda = Employee(name="Amanda", job_title="Feline Expert")
    jane = Employee(name="Jane", job_title="Primatologist")
    carl = Employee(name="Carl", job_title="Primate Keeper")
    ben = Employee(name="Ben", job_title="Bear Handler")
    ken = Employee(name="Ken", job_title="Large Mammal Expert")

    finn = Employee(name="Finn", job_title="Marine Biologist")
    marina = Employee(name="Marina", job_title="Marine Trainer")
    shelly = Employee(name="Shelly", job_title="Aquarist")
    toby = Employee(name="Toby", job_title="Shallow Water Guide")
    ollie = Employee(name="Ollie", job_title="Cephalopod Specialist")
    coral = Employee(name="Coral", job_title="Reef Conservationist")

    avi = Employee(name="Avi", job_title="Master Falconer")
    sam = Employee(name="Sam", job_title="Raptor Handler")
    fiona = Employee(name="Fiona", job_title="Falconry Expert")
    pete = Employee(name="Pete", job_title="Exotic Bird Keeper")
    ozzie = Employee(name="Ozzie", job_title="Large Bird Handler")
    pam = Employee(name="Pam", job_title="Farm Specialist")
    penny = Employee(name="Penny", job_title="Ground Bird Caretaker")

    # Pack them all into the zoo roster!
    employees_to_hire = [
        katie, sarah, marcus, chloe, richard, mr_sterling, dr_vance, jessica,
        gordon, bob, alice, joe, amanda, jane, carl, ben, ken, finn, marina,
        shelly, toby, ollie, coral, avi, sam, fiona, pete, ozzie, pam, penny
    ]
    for emp in employees_to_hire:
        my_zoo.hire_employee(emp)

    # --- 6. ASSIGN EMPLOYEES TO BUILDINGS ---
    enter_center.assign_employee(katie)
    enter_center.assign_employee(sarah)
    enter_center.assign_employee(mr_sterling)

    safari_shop.assign_employee(chloe)
    info_kiosk.assign_employee(marcus)
    info_kiosk.assign_employee(jessica)
    first_aid.assign_employee(dr_vance)

    grazing_station.assign_employee(gordon)
    main_restrooms.assign_employee(bob)
    east_restrooms.assign_employee(alice)

    lions_den.assign_employee(richard)
    tiger_trek.assign_employee(joe)
    leopard_lounge.assign_employee(amanda)
    primate_house.assign_employee(jane)
    chimp_reserve.assign_employee(carl)
    bear_habitat.assign_employee(ben)
    kodiak_cave.assign_employee(ken)

    shark_tank.assign_employee(finn)
    dolphin_cove.assign_employee(marina)
    kelp_forest.assign_employee(shelly)
    touch_pool.assign_employee(toby)
    octopus_cave.assign_employee(ollie)
    coral_reef.assign_employee(coral)

    top_watch.assign_employee(avi)
    eagle_aerie.assign_employee(sam)
    falcon_roost.assign_employee(fiona)
    parrot_paradise.assign_employee(pete)
    ostrich_paddock.assign_employee(ozzie)
    poultry_pen.assign_employee(pam)
    peacock_garden.assign_employee(penny)

    # --- 7. BREED ANIMALS ---
    # Aquatic
    Fish("Bubbles", age=1)
    Fish("Fin", age=2)
    Fish("Gills", age=1)
    Octopus("Inkwell", age=3)
    Octopus("Squishy", age=4)
    Octopus("Kraken", age=2)
    Squid("Dart", age=1)
    Squid("Calamari", age=2)
    Squid("Slippy", age=1)
    Sea_Urchin("Spike", age=5)
    Sea_Urchin("Pincushion", age=3)
    Sea_Urchin("Prickle", age=4)
    Shark("Bruce", age=8)
    Shark("Mako", age=5)
    Shark("Jaws", age=12)
    Dolphin("Flipper", age=6)
    Dolphin("Echo", age=4)
    Dolphin("Splash", age=7)
    Star_fish("Patrick", age=2)
    Star_fish("Stella", age=3)
    Star_fish("Nova", age=1)

    # Aerial
    Parrot("Polly", age=15)
    Parrot("Rio", age=5)
    Parrot("Captain", age=22)
    Eagle("Eli", age=4)
    Eagle("Liberty", age=7)
    Eagle("Justice", age=5)
    Turkey("Gobbles", age=2)
    Turkey("Tom", age=3)
    Turkey("Cranberry", age=1)
    Ostrich("Stretch", age=5)
    Ostrich("Bolt", age=4)
    Ostrich("Legs", age=6)
    Peacock("Strut", age=3)
    Peacock("Jewel", age=4)
    Peacock("Feathers", age=2)
    Chicken("Cluck", age=1)
    Chicken("Nugget", age=2)
    Chicken("Eggbert", age=1)
    Falcon("Apollo", age=3)
    Falcon("Swoop", age=2)
    Falcon("Jet", age=4)

    # Terrestrial
    Lion("Simba", age=5)
    Lion("Mufasa", age=8)
    Lion("Nala", age=4)
    Tiger("Rajah", age=6)
    Tiger("Tony", age=9)
    Tiger("Shere Khan", age=11)
    Leopard("Spot", age=3)
    Leopard("Shadow", age=5)
    Leopard("Ghost", age=4)
    Gorilla("Kong", age=15)
    Gorilla("Silver", age=12)
    Gorilla("Caesar", age=10)
    Chimpanzee("Bubbles", age=7)
    Chimpanzee("Caesar", age=9)
    Chimpanzee("Koba", age=8)
    Black_Bear("Baloo", age=6)
    Black_Bear("Smokey", age=8)
    Black_Bear("Midnight", age=4)
    Kodiak_Bear("Titan", age=10)
    Kodiak_Bear("Goliath", age=12)
    Kodiak_Bear("Tank", age=9)

    # RETURN THE ENTIRE ZOO!
    return my_zoo