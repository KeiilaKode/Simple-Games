import time
from visitor import Visitor
from ticket import Ticket
from employee import Employee, GateKeeper
from mammal import Lion, Tiger, Leopard, Gorilla, Chimpanzee, Black_Bear, Kodiak_Bear
from animal import Terrestrial, Aquatic, Aerial
from enclosure import Building, Terrestrial_Enclosure, Aerial_Enclosure, Aquatic_Enclosure
from aerial import Eagle, Turkey, Parrot, Ostrich, Falcon, Peacock
from aquatic import Fish, Octopus, Dolphin, Squid, Star_fish, Shark, Sea_Urchin


### RUN THE FIRST CHAPTER  * ### * CREATING VISITORS ###
if __name__ == "__main__":
    # --- 1. BUILD THE ZOO BUILDINGS--- # NEED TO CREATE MORE BUILDINGS AND ENCLOSURES
    enter_center = Building("Enter Center")
    lions_den = Terrestrial_Enclosure(name="Lions Den", wing="Carnivore Wing")
    top_watch = Aerial_Enclosure(name="The Point", wing="Aviary")

    # --- 2. HIRE EMPLOYEES & ASSIGN THEM --- # # NEED TO CREATE MORE EMPLOYEES
    katie = GateKeeper(name="Katie", job_title="Gate Cashier")
    richard = Employee(name="Richard", job_title="Lion Tender")

    enter_center.assign_employee(katie)
    lions_den.assign_employee(richard)

    # --- 3. BREED ANIMALS --- # # NEED TO CREATE MORE ANIMALS OF ALL CLASSES AVAILABLE
    billy = Lion("Billy", age=4)
    eli = Eagle("Eli", age=2)

    # --- 4. ASSIGN THE ANIMALS TO BUILDINGS --- # # NEED TO CREATE MORE BUILDINGS
    lions_den.add_creature(billy)
    top_watch.add_creature(eli)

    # --- 5. STARTS THE TERMINAL OUTPUT --- # ### NEED TO ADD MORE HOTKEY OPTIONS, TO CHECK ENCLOSURES AND BUILDINGS FOR ANIMALS AND EMPLOYEES ###
         ### GAME LOGIC AND LOOP ###

    print("--- ZOO SIMULATION STARTED ---")
    print("Type 'q' at the name prompt to quit.")
    print("Type 'r' to see amount of tickets sold so far.\n")
    sale_number = 0
    # 2. The Continuous Loop (Simulating a line of people)
    while True:
            # Generate a visitor dynamically via console input
        print("-" * 33)
        visitor_name = input("Enter the next visitor's name: ").title()
        if visitor_name.lower() == 'r':
            katie.report()
            continue
        elif visitor_name.lower() == 'q':
            print("Closing the zoo gates!")
            break
        visitor_money = int(input(f"How much money does {visitor_name} have? $"))
        print("-" * 33 + "\n")

        # Instantiate the Visitor
        current_visitor = Visitor(name=visitor_name, money=visitor_money)

        print("\n--- Interaction Begins ---")
        # 3. The Interaction
        katie.greet(current_visitor)


        # Ask for ticket counts
        adults = int(input("How many ADULT tickets are needed? "))
        time.sleep(.5)
        kids = int(input("And how many CHILD tickets are needed? "))
        print("\n")
        time.sleep(.5)

        # Process the sale
        transaction_successful = katie.sell_tickets(visitor=current_visitor, num_adults=adults, num_kids=kids)

        # This below, is the same thing as: if transaction_successful == False:
        if not transaction_successful:
            print("-" * 33 + "\n")
            continue

        sale_number += 1

        # 4. Check the aftermath to ensure logic worked
        time.sleep(1)
        print("\n*---* Events Happening *---*")
        print(f"*{current_visitor.name} hands {katie.name} the money and then {katie.name} hands them their tickets.*")
        print(f"*They eagerly smile and wave goodbye, making their way into the zoo.*")
        print("-" * 33 + "\n")
        time.sleep(2)
        print("\n--- Transaction Results ---")
        print(f"Completed Sales: {sale_number}")
        print(current_visitor)
        print(f"Tickets purchased: {len(current_visitor.tickets)}")
        print(f"Money in Katie's Register: ${katie.register}")
        print("-" * 33 + "\n")





# 3. Test it out!
# print(katie)
# print(katie.building)
# print(richard)
# print(richard.building)
# print(lions_den.assigned_employees)
# print(enter_center.assigned_employees)