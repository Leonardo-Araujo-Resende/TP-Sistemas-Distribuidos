import Pyro5.api
import time

class ControllerPartida():
    
    def listen_game_start(self, username):
        controller_partida = Pyro5.api.Proxy("PYRONAME:server.partida")
        return controller_partida.send_start(username)
        
    
    def send_chosen_card(self, id_carta, username):
        controller_partida = Pyro5.api.Proxy("PYRONAME:server.partida")
        controller_partida.define_chosen_card(id_carta, username)
        time.sleep(1)
        return controller_partida.return_winner(username)

    def listen_game_finish(self):
        controller_partida = Pyro5.api.Proxy("PYRONAME:server.partida")
        return controller_partida.verificar_vencedor()
        
    def carta_recebida(self):
        controller_partida = Pyro5.api.Proxy("PYRONAME:server.partida")
        return controller_partida.define_carta_vencedor()
