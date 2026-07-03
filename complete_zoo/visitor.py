
# Visitors
class Visitor:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.max_money = 100

        self.impression = 0
        self.impression_max = 10
        self.tickets = []        # The visitor starts with no tickets
        self.amount_spent = 0


    def __str__(self):
        return f"{self.name} spent {self.amount_spent} and has {self.money} dollars left."

    @property
    def has_ticket(self):
        # Returns True if the visitor has at least one ticket in their list
        return len(self.tickets) > 0

    def pay(self, amount):
        # Checks if the visitor has enough money, deducts it, and hands it over
        if self.money >= amount:
            self.money -= amount
            self.amount_spent += amount
            return amount
        else:
            return 0  # Not enough money

##########################