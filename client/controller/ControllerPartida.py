import ast
import Pyro5.api


class ControllerPartida():
    
    def listen_game_start(self, username):
        controller_partida = Pyro5.api.Proxy("PYRONAME:server.partida")
        return controller_partida.send_start(username)
        
        # msg = self.client.listen_for_server_msg()  
        # return msg

    def remove_colchete(self, msg):
        return ast.literal_eval(msg)
    
    def send_chosen_card(self, id_carta, id_player):
        pass
        # msg = {"op": "carta_escolhida", "id_carta": id_carta, "id_player": id_player}
        # response = self.client.send_msg(msg)
        # return response

    def send_username(self, username):
        pass
        # msg = {"op": "send_username", "username": username, }
        # response = self.client.send_msg(msg)
        # return response