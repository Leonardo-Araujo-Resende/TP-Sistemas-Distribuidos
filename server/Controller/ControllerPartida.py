import random


class ControllerPartida():
    def __init__(self, all_cards):
        self.jogador1 = None
        self.deck1 = None
        self.jogador2 = None
        self.deck2 = None
        self.jogador3 = None
        self.deck3 = None
        self.all_cards = all_cards
    
    def game_start(self,):

        mao_player1 = self.deck1[0:2]
        mao_player2 = self.deck2[0:2]
        mao_player3 = self.deck3[0:2]
        
        self.jogador1.sendall(f"{mao_player1}".encode("utf8"))
        self.jogador2.sendall(f"{mao_player2}".encode("utf8"))
        self.jogador3.sendall(f"{mao_player3}".encode("utf8"))

    
