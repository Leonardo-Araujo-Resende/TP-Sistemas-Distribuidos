from network.Client import *


class ControllerJogar():
    def __init__(self):
        self.client = Client()

    
    def define_deck(self, deck, index_deck):
       
        msg = {"op": "define_deck", "deck_index": index_deck, "deck": []}

        for card in deck:
            # add id da card na msg
            msg['deck'].append(card.filename)
        
        return self.client.send_msg(msg)

    def listen_game_start(self):
        return self.client.listen_for_server_msg()        
