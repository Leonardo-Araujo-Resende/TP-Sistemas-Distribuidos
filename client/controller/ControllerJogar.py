import random
import Pyro5.api

class ControllerJogar():

    def __init__(self):
        self.controller_jogar = None
        self.controller_partida = None

    def define_deck(self, deck, index_deck, username):

               
        controller_partida = Pyro5.api.Proxy("PYRONAME:server.partida")
        self.controller_partida = controller_partida

        deck = [card.id for card in deck]

        id_jogador = self.controller_partida.get_qt_usuarios_prontos() + 1
        
        self.controller_partida.set_deck(random.sample(deck, len(deck)),id_jogador)
        self.controller_partida.set_username(username, id_jogador)

        return id_jogador
