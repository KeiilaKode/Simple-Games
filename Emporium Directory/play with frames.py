# print("*^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^*")  # Top Boarders
# print("<" + "'"  * 52 + ">")
# print("|" + " " * 52 + "|")  # Body with Injected Stats (The :<52 keeps the right wall aligned!)
# print("|" + " " * 52 + "|")
# print("|" + " " * 52 + "|")
# print("|" + " " * 52 + "|")
# print("<" + "," * 52 + ">")
# print("*~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~*")


# One type of frame/box
class Box:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.box_data = [] #list[list[str]]
    def gen_box(self):
        self.box_data = [["." for _ in range(self.width)] for _ in range(self.height)]
    def display_box(self):
        frame = "X" + self.width * "=" + "X" + "~" * 141 + "X" + self.width * "=" + "X"
        print(frame)
        for row in self.box_data:
            print("|" + "".join(row) + "|" + " " * 141 + "|" + "".join(row) + "|")
        print(frame)

    # Second type of frame/box
    def display_boxa(self):
        frame = "X" + self.width * "=" + "X"
        center = "O" + self.width * "-" + "O"
        print(frame)
        print(center)
        for row in self.box_data:
            print("|" + "".join(row) + "|")
        print(center)
        print(frame)
box1 = Box(15, 8)
box2 = Box(173, 4)
box3 = Box(173, 4)
box4 = Box(15, 8)
box5 = Box(173, 4)
box6 = Box(173, 4)

box1.gen_box()
box2.gen_box()
box3.gen_box()
box4.gen_box()
box5.gen_box()

# Call the functions alternating, starting with display_boxa(), 9 times in total to make a continuous latter effect




#box3.display_boxa()
# box4.display_box()

#
# box1.display_box()
#box3.display_boxa()
# box4.display_box()
# box5.display_boxa()

# Third type of frame/box
def dual_menu():
    #print("\n")
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
box2.display_boxa()
box1.display_box()
#dual_menu()
box1.display_box()
box5.display_boxa()











# print(f"|{stat_name:<52}|")
# print(f"|{stat_type_hero:<52}|")
# print(f"|{stat_skill:<52}|")
# print(f"|{stat_hp:<52}|")
# print(f"|{stat_mp:<52}|")
# print(f"|{stat_gold:<52}|")
# print(f"|{stat_backpack:<52}|")

