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
        self.cemiterio1 = []
        self.cemiterio2 = []
        self.cemiterio3 = []
        self.all_cards = all_cards
    
    def get_character_by_index(self, index):
        characters_data = list(self.all_cards.keys())
        if 1 <= index <= len(characters_data):
            character_name = characters_data[index - 1]
            return self.all_cards[character_name]


    def who_won(self, personagem1, personagem2, personagem3, atributo):
        if atributo == "gimmick":
            vantagens = {
                'GUARDA': 'DANO',
                'DANO': 'VOO',
                'VOO': 'TURBO',
                'TURBO': 'GUARDA'
            }
            personagens = [personagem1[atributo], personagem2[atributo], personagem3[atributo]]
            personagens_pontos = [0,0,0]

            for i in range(3):
                for j in range(3):
                    if vantagens[personagens[i]] == personagens[j]:
                        personagens_pontos[j] += 1

            menor_valor = min(personagens_pontos)
            indices_menor_valor = [i for i, valor in enumerate(personagens_pontos) if valor == menor_valor]
            resultado = random.choice(indices_menor_valor) + 1

            return f"personagem{resultado}"

        else:
            personagens = {
                'personagem1': personagem1[atributo],
                'personagem2': personagem2[atributo],
                'personagem3': personagem3[atributo]
            }
            maior_valor = max(personagens.values())
            maiores = [nome for nome, valor in personagens.items() if valor == maior_valor]
            resultado = random.choice(maiores)

            return f"{resultado}"

    def verificar_vencedor(self, cemiterio1, cemiterio2, cemiterio3):
        tamanho1 = len(cemiterio1)
        tamanho2 = len(cemiterio2)
        tamanho3 = len(cemiterio3)
        
        menor_tamanho = max(tamanho1, tamanho2, tamanho3)
        
        vencedores = []
        
        if tamanho1 == menor_tamanho:
            vencedores.append(1)
        if tamanho2 == menor_tamanho:
            vencedores.append(2)
        if tamanho3 == menor_tamanho:
            vencedores.append(3)
        

        return f"O jogador {vencedores[0]} ganhou!"
        if len(vencedores) == 1:
            return f"O jogador {vencedores[0]} ganhou!"
        else:
            return f"Empate entre os jogadores: {', '.join(map(str, vencedores))}"

   
    def game_start(self,conn1, conn2, conn3):

        atributos = ["velocidade", "aceleracao", "peso", "capacidade", "resistencia", "truque"]
        atributos_ingles = ["speed", "accel", "weight", "capacity", "resistance", "gimmick"]
        index_random = random.randint(0, 5)
        self.atributo_rodada = atributos_ingles[index_random]
        mao_player1 = self.deck1[:3]
        mao_player2 = self.deck2[:3]
        mao_player3 = self.deck3[:3]
        
        conn1.sendall(f"{mao_player1} - {atributos[index_random]}".encode("utf8"))
        conn2.sendall(f"{mao_player2} - {atributos[index_random]}".encode("utf8"))
        conn3.sendall(f"{mao_player3} - {atributos[index_random]}".encode("utf8"))

        contador_deck = 3
        for x in range(9):
            msg1 = conn1.recv(1024)
            msg2 = conn2.recv(1024)
            msg3 = conn3.recv(1024)
            
            msg1_dict = json.loads(msg1.decode("utf8"))
            msg2_dict = json.loads(msg2.decode("utf8"))
            msg3_dict = json.loads(msg3.decode("utf8"))

            
            card1 = {"jogador": msg1_dict['id_player'], "carta": msg1_dict['id_carta']}
            self.cartas_escolhidas.append(card1)
            card2 = {"jogador": msg2_dict['id_player'], "carta": msg2_dict['id_carta']}
            self.cartas_escolhidas.append(card2)
            card3 = {"jogador": msg3_dict['id_player'], "carta": msg3_dict['id_carta']}
            self.cartas_escolhidas.append(card3)
            
            personagem1 = self.get_character_by_index(int(self.cartas_escolhidas[0]['carta']))
            personagem2 = self.get_character_by_index(int(self.cartas_escolhidas[1]['carta']))
            personagem3 = self.get_character_by_index(int(self.cartas_escolhidas[2]['carta']))
      
            
            personagem_won = self.who_won(personagem1, personagem2, personagem3, self.atributo_rodada)

            
            #atualizar cemiterio
            if personagem_won  == "personagem1":
                self.cemiterio1.append(card2["carta"])
                self.cemiterio1.append(card3["carta"])
            if personagem_won  == "personagem2":
                self.cemiterio2.append(card1["carta"])
                self.cemiterio2.append(card3["carta"])
            if personagem_won  == "personagem3":
                self.cemiterio3.append(card2["carta"])
                self.cemiterio3.append(card3["carta"])
            
            atributos = ["velocidade", "aceleracao", "peso", "capacidade", "resistencia", "truque"]
            atributos_ingles = ["speed", "accel", "weight", "capacity", "resistance", "gimmick"]
            index_random = random.randint(0, 5)
            self.atributo_rodada = atributos_ingles[index_random]


            if contador_deck < 9:
                conn1.sendall(f"{personagem_won} - {self.deck1[contador_deck]} - {atributos[index_random]}".encode("utf8"))
                conn2.sendall(f"{personagem_won} - {self.deck2[contador_deck]} - {atributos[index_random]}".encode("utf8"))
                conn3.sendall(f"{personagem_won} - {self.deck3[contador_deck]} - {atributos[index_random]}".encode("utf8"))
                contador_deck += 1
            
            else:
                conn1.sendall(f"{personagem_won} - {atributos[index_random]}".encode("utf8"))
                conn2.sendall(f"{personagem_won} - {atributos[index_random]}".encode("utf8"))
                conn3.sendall(f"{personagem_won} - {atributos[index_random]}".encode("utf8"))
            
            self.cartas_escolhidas = []

        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.debug(self.verificar_vencedor(self.cemiterio1, self.cemiterio2, self.cemiterio3))
    
        


    
    
