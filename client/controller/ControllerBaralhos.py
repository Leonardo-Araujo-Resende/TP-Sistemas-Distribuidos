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


    def append_card_deck(self, index_deck:int, card:Card):
        if self.collection.get_by_id(card.get_id).get_quantity() > 0 and self.decks[index_deck].get_quantity_of_card(card) < 3:
            self.decks[index_deck].append_card(card)
            self.collection.decrement_quantity_by_id(card.get_id())
                

    def save_deck(self, deck:Deck, index_deck:int):
        #Chama network salva deck 1 no banco
        msg = {"op": "salvaDeck", "deck_index": index_deck, "deck": []}

        for card in deck.cards:
            # add id da card na msg
            msg['deck'].append(card.get_id())
        
        return self.client.send_msg(msg)

    def delete_deck(self, index_deck:int):
        self.decks[index_deck].reset_deck()

