import random
import Pyro5.api

class ControllerJogar():

    def __init__(self):
        self.controller_jogar = None
        self.controller_partida = None
    def define_deck(self, deck, index_deck):
        controller_jogar = Pyro5.api.Proxy("PYRONAME:server.jogar")
        self.controller_jogar = controller_jogar
        self.controller_jogar.set_user_ready()
        
        
        controller_partida = Pyro5.api.Proxy("PYRONAME:server.partida")
        self.controller_partida = controller_partida

        deck = [card.id for card in deck]
        
        if self.controller_jogar.get_qt_users_ready() == 3:
            self.controller_partida.set_deck(random.sample(deck, len(deck)), 3)
            self.controller_jogar.set_game_ready()
        elif self.controller_jogar.get_qt_users_ready() == 2:
            self.controller_partida.set_deck(random.sample(deck, len(deck)), 2)
        else:
            self.controller_partida.set_deck(random.sample(deck, len(deck)), 1)
        
        return self.controller_jogar.get_qt_users_ready()

        
    def listen_game_start(self):
        while True:
            if self.controller_jogar.get_game_is_ready():
                return "Game Ready"  