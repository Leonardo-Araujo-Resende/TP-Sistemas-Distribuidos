from model.Collection import *
from model.Deck import *
from typing import List
from model.Card import *
from network.Client import *


class ControllerBaralhos():
    def __init__(self, collection:Collection, decks:List[Deck]):
        self.client = Client()
        self.collection = collection
        self.decks = decks


    def append_card_deck(self,id:int,  index_deck:int):
        if self.collection.get_quantity_by_id(id) > 0 and self.decks[index_deck].get_quantity_of_card(id) < 3:
            self.decks[index_deck].append_card(id)
            self.collection.decrement_quantity_by_id(id)
        else:
            return False

    def save_deck(self, deck:Deck, index_deck:int):
        #Chama network salva deck 1 no banco
        msg = {"op": "salvaDeck", "deck_index": index_deck, "deck": []}

        for card in deck.cards:
            # add id da card na msg
            msg['deck'].append(card.get_id())
        
        return self.client.send_msg(msg)

    def delete_deck(self, index_deck:int):
        self.decks[index_deck].reset_deck()

    def reset_deck(self, deck_index):
        for card in self.decks[deck_index].cards:
            for card_in_collection in self.collection.get_cards():
                if card.get_id() == card_in_collection.get_id():
                    card_in_collection.increment_quantity()
                    break
        self.decks[deck_index].clear()

