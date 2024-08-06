import arcade 
from model.Card import Card
from typing import List
import Truque

DECK_SIZE = 9

class Deck():
    def __init__(self, cards:list[Card], quantity:int):
        self.quantity = quantity
        self.cards = cards

    def get_deck_size(self):
        return self.quantity
    
    def append(self, card:Card):
        if self.can_append_card():
            self.cards.append(card)

    def can_append_card(self):
        if len(self.cards) == DECK_SIZE:
            return False
        return True