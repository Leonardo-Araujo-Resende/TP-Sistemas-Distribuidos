from network.Client import *
import ast


class ControllerPartida():
    
    def __init__(self, cliente):
        self.client = cliente

    
    def listen_game_finish(self):
        return self.client.listen_for_server_msg()    

    def remove_colchete(self, msg):
        return ast.literal_eval(msg)
    
    def send_chosen_card(self, id_carta, id_player):
        msg = {"op": "carta_escolhida", "id_carta": id_carta, "id_player": id_player}
        return self.client.send_msg(msg)