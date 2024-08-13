from network.Client import *
import ast


class ControllerPartida():
    
    def __init__(self, cliente):
        self.client = cliente

    
    def listen_game_finish(self):
        msg = self.client.listen_for_server_msg()  
        return msg

    def remove_colchete(self, msg):
        return ast.literal_eval(msg)
    
    def send_chosen_card(self, id_carta, id_player):
        msg = {"op": "carta_escolhida", "id_carta": id_carta, "id_player": id_player}
        response = self.client.send_msg(msg)
        return response

    def send_username(self, username):
        msg = {"op": "send_username", "username": username, }
        response = self.client.send_msg(msg)
        return response