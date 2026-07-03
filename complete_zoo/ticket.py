# Tickets class
class Ticket:

    def __init__(self, ticket_type):
        self.price = 0
        self.ticket_type = ticket_type
        if self.ticket_type == "Adult":
            self.price = 10
        elif self.ticket_type == "Child":
            self.price = 5

    def __str__(self):
        return f"{self.ticket_type} Ticket: {self.price}."