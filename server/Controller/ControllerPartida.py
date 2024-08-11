import random


class ControllerPartida():
    def __init__(self, all_cards):
        self.jogador1 = None
        self.deck1 = None
        self.jogador2 = None
        self.deck2 = None
        self.jogador3 = None
        self.deck3 = None
        self.cartas_escolhidas = []
        self.all_cards = all_cards
    
    def game_start(self,conn1, conn2, conn3):

        mao_player1 = self.deck1[:3]
        mao_player2 = self.deck2[:3]
        mao_player3 = self.deck3[:3]
        
        conn1.sendall(f"{mao_player1}".encode("utf8"))
        conn2.sendall(f"{mao_player2}".encode("utf8"))
        conn3.sendall(f"{mao_player3}".encode("utf8"))

    
