class Inventory():
    def __init__(self, name:str, capacity:int):
        self.name = name
        self.capacity = capacity
        self.capacity_max = capacity
        self.purse = []

    def is_full(self):
        return len(self.purse) >= self.capacity

    def add_item(self, item):
        if self.is_full():
            #print(f"The {self.name} is full!")
            return False  # Tell the game it failed
        self.purse.append(item)
        print(f"You have {len(self.purse)} items in your {self.name}")
        #print(f"Put {item} in {self.name}.")
        return True  # Tell the game it worked



class Store(Inventory):
    def __init__(self, name, capacity):
        super().__init__(name=name, capacity=capacity)


class Bag(Inventory):
    def __init__(self, name, capacity, size="Small"):
        super().__init__(name=name, capacity=capacity)
        self.size = size

lil_bag = Bag("Regular Backpack", 10)

