import random
import logging
import json

class ControllerPartida():
    def __init__(self, all_cards):
        self.jogador1 = None
        self.deck1 = None
        self.jogador2 = None
        self.deck2 = None
        self.jogador3 = None
        self.deck3 = None
        self.cartas_escolhidas = []
        self.atributo_rodada = ""
        self.rodada_atual = 1
        self.cemiterio = []
        self.all_cards = all_cards
    
    def get_character_by_index(self, index):
        characters_data = list(self.all_cards.keys())
        if 1 <= index <= len(characters_data):
            character_name = characters_data[index - 1]
            return self.all_cards[character_name]

                    
    def who_won():
        pass
    
    def send_graveyard():
        pass

   
    def game_start(self,conn1, conn2, conn3):

        atributos = ["velocidade", "aceleracao", "peso", "capacidade", "resistencia", "truque"]
        index_random = random.randint(0, 5)
        self.atributo_rodada = atributos[index_random]
        mao_player1 = self.deck1[:3]
        mao_player2 = self.deck2[:3]
        mao_player3 = self.deck3[:3]
        
        conn1.sendall(f"{mao_player1} - {self.atributo_rodada}".encode("utf8"))
        conn2.sendall(f"{mao_player2} - {self.atributo_rodada}".encode("utf8"))
        conn3.sendall(f"{mao_player3} - {self.atributo_rodada}".encode("utf8"))
        
        for x in range(9):
            msg1 = conn1.recv(1024)
            msg2 = conn2.recv(1024)
            msg3 = conn3.recv(1024)
            
            msg1_dict = json.loads(msg1.decode("utf8"))
            msg2_dict = json.loads(msg2.decode("utf8"))
            msg3_dict = json.loads(msg3.decode("utf8"))

            
            card = {"jogador": msg1_dict['id_player'], "carta": msg1_dict['id_carta']}
            self.cartas_escolhidas.append(card)
            card = {"jogador": msg2_dict['id_player'], "carta": msg2_dict['id_carta']}
            self.cartas_escolhidas.append(card)
            card = {"jogador": msg3_dict['id_player'], "carta": msg3_dict['id_carta']}
            self.cartas_escolhidas.append(card)
            
            personagem1 = self.get_character_by_index(int(self.cartas_escolhidas[0]['carta']))
            personagem2 = self.get_character_by_index(int(self.cartas_escolhidas[1]['carta']))
            personagem3 = self.get_character_by_index(int(self.cartas_escolhidas[2]['carta']))
      
        
            

            
            
    # logging.basicConfig(level=logging.DEBUG)
    # logger = logging.getLogger(__name__)
    # logger.debug(f"{self.get_character_by_index(int(self.cartas_escolhidas[0]['carta']), logger)}")



        


    
    
