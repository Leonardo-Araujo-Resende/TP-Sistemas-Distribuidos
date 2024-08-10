from model.Truque import *

class Card():
    def __init__(self, id:int, quantity:int):
        self.id = id
        self.quantity = quantity

    def get_id(self) -> int:
        return self.id

    def get_quantity(self) -> int:
        return self.quantity
    
    def increment_quantity(self):
        self.quantity += 1

    def decrement_quantity(self):
        self.quantity -= 1
