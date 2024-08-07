from view.ViewBaralhos import ViewBaralhos
from model.Collection import Collection
from model.Deck import Deck
from typing import List
from model.Card import Card


class ControllerBaralhos():
    def __init__(self, view:ViewBaralhos, collection:Collection, decks:List[Deck]):
        self.collection = collection
        self.decks = decks


    def append_card_deck(self, index_deck:int, card:Card):
        if self.collection.get_by_id(card.get_id).get_quantity() > 0 and self.decks[index_deck].get_quantity_of_card(card) < 3:
            self.decks[index_deck].append_card(card)
            self.collection.decrement_quantity_by_id(card.get_id())
                

    def save_deck_(self, deck:Deck, index_deck:int):
        #Chama network salva deck 1 no banco
        print()

    def delete_deck(self, index_deck:int):
        self.decks[index_deck].reset_deck()

