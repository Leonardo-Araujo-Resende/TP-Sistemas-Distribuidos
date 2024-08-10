import arcade 
from model.Card import Card
from typing import List
from model.Truque import *

DECK_SIZE = 9

class Deck():
    def __init__(self, cards:list[Card]):
        self.quantity = len(cards)
        self.cards = cards

    def get_deck_size(self):
        return self.quantity
    
    def append_card(self, id:int):
        if len(self.cards) <= DECK_SIZE:
            for c in self.cards:
                if c.get_id == id:
                    c.increment_quantity
                    return
            self.cards.append(Card(id,1))
        else:
            return False

    def reset_deck(self):
        self.cards.clear()

    def get_quantity_of_card(self, id):
        count = 0
        for c in self.cards:
            if c.id == id:
                count += 1
        return count
            