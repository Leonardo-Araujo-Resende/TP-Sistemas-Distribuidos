from network.Client import *


class ControllerJogar():

    def __init__(self, cliente):
        self.client = cliente
   
    def define_deck(self, deck, index_deck):
       
        msg = {"op": "define_deck", "deck_index": index_deck, "deck": []}
        for card in deck:
            # add id da card na msg
            msg['deck'].append(card.id)
        
        return self.client.send_msg(msg)

    def listen_game_start(self):
        return self.client.listen_for_server_msg()    