import arcade 
from model.Card import Card
from typing import List
from model.Truque import *

DECK_SIZE = 9

class Deck():
    def __init__(self, cards:list[Card], quantity:int):
        self.quantity = quantity
        self.cards = cards

    def get_deck_size(self):
        return self.quantity
    
    def append_card(self, card:Card):
        if len(self.cards) == DECK_SIZE:
            self.cards.append(card)
        else:
            return False

    def reset_deck(self):
        self.cards.clear()

    def get_quantity_of_card(self, card:Card):
        count = 0
        for c in self.cards:
            if c.id == card.id:
                count += 1
        return count
            