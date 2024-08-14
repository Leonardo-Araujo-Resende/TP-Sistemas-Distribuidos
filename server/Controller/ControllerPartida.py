import random
import logging
import json
import sqlite3
import time
import threading

class ControllerPartida():
    def __init__(self, all_cards):
        self.username1 = None
        self.username2 = None
        self.username3 = None
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

            return f"{resultado}"

        else:
            personagens = {
                '1': personagem1[atributo],
                '2': personagem2[atributo],
                '3': personagem3[atributo]
            }
            maior_valor = max(personagens.values())
            maiores = [nome for nome, valor in personagens.items() if valor == maior_valor]
            resultado = random.choice(maiores)

            return f"{resultado}"

    def verificar_vencedor(self, cemiterio1, cemiterio2, cemiterio3):
        tamanho1 = len(cemiterio1)
        tamanho2 = len(cemiterio2)
        tamanho3 = len(cemiterio3)
        
        maior = max(tamanho1, tamanho2, tamanho3)
        
        vencedores = []
        
        if tamanho1 == maior:
            vencedores.append(1)
        if tamanho2 == maior:
            vencedores.append(2)
        if tamanho3 == maior:
            vencedores.append(3)
        
        if len(vencedores) == 1:
            return vencedores[0]
        else:
            vencedor_final = random.choice(vencedores)
            return vencedor_final

        

   
    def game_start(self,conn1, conn2, conn3):

        atributos = ["velocidade", "aceleracao", "peso", "capacidade", "resistencia", "truque"]
        atributos_ingles = ["speed", "accel", "weight", "capacity", "resistance", "gimmick"]
        index_random = random.randint(0, 5)
        self.atributo_rodada = atributos_ingles[index_random]
        mao_player1 = self.deck1[:3]
        mao_player2 = self.deck2[:3]
        mao_player3 = self.deck3[:3]
        

        cont = 0

        conn1.sendall(f"{mao_player1} - {atributos[index_random]}".encode("utf8"))
        conn2.sendall(f"{mao_player2} - {atributos[index_random]}".encode("utf8"))
        conn3.sendall(f"{mao_player3} - {atributos[index_random]}".encode("utf8"))

        cont += 1
        
        contador_deck = 3
        barrier = threading.Barrier(3)

        for x in range(9):
            def receive_and_process(conn, player_id):
                msg = conn.recv(1024)
                msg_dict = json.loads(msg.decode("utf8"))
                card = {"jogador": msg_dict['id_player'], "carta": msg_dict['id_carta']}
                self.cartas_escolhidas.append(card)
                

                barrier.wait()


            thread1 = threading.Thread(target=receive_and_process, args=(conn1, 1))
            thread2 = threading.Thread(target=receive_and_process, args=(conn2, 2))
            thread3 = threading.Thread(target=receive_and_process, args=(conn3, 3))
            
            thread1.start()
            thread2.start()
            thread3.start()
            
            thread1.join()
            thread2.join()
            thread3.join()

            personagem1 = self.get_character_by_index(int(self.cartas_escolhidas[0]['carta']))
            personagem2 = self.get_character_by_index(int(self.cartas_escolhidas[1]['carta']))
            personagem3 = self.get_character_by_index(int(self.cartas_escolhidas[2]['carta']))

            personagem_won = self.who_won(personagem1, personagem2, personagem3, self.atributo_rodada)
            
            if personagem_won == "1":
                self.cemiterio1.append(int(self.cartas_escolhidas[1]["carta"]))
                self.cemiterio1.append(int(self.cartas_escolhidas[2]["carta"]))
            elif personagem_won == "2":
                self.cemiterio2.append(int(self.cartas_escolhidas[0]["carta"]))
                self.cemiterio2.append(int(self.cartas_escolhidas[2]["carta"]))
            elif personagem_won == "3":
                self.cemiterio3.append(int(self.cartas_escolhidas[0]["carta"]))
                self.cemiterio3.append(int(self.cartas_escolhidas[1]["carta"]))
            
            atributos = ["Velocidade", "Aceleração", "Peso", "Capacidade", "Resistência", "Truque"]
            atributos_ingles = ["speed", "accel", "weight", "capacity", "resistance", "gimmick"]
            index_random = random.randint(0, 5)
            self.atributo_rodada = atributos_ingles[index_random]


            if x == 8:
                conn1.sendall(f"{personagem_won}".encode("utf8"))
                conn2.sendall(f"{personagem_won}".encode("utf8"))
                conn3.sendall(f"{personagem_won}".encode("utf8"))

            elif contador_deck < 9:
                conn1.sendall(f"{personagem_won} - {self.deck1[contador_deck]} - {atributos[index_random]}".encode("utf8"))
                conn2.sendall(f"{personagem_won} - {self.deck2[contador_deck]} - {atributos[index_random]}".encode("utf8"))
                conn3.sendall(f"{personagem_won} - {self.deck3[contador_deck]} - {atributos[index_random]}".encode("utf8"))
                contador_deck += 1
            
            else:
                conn1.sendall(f"{personagem_won} - {atributos[index_random]}".encode("utf8"))
                conn2.sendall(f"{personagem_won} - {atributos[index_random]}".encode("utf8"))
                conn3.sendall(f"{personagem_won} - {atributos[index_random]}".encode("utf8"))
            
            self.cartas_escolhidas = []

        id_jogador_vencedor = self.verificar_vencedor(self.cemiterio1, self.cemiterio2, self.cemiterio3)
        time.sleep(3)

        conn1.sendall(f"{id_jogador_vencedor}".encode("utf8"))
        conn2.sendall(f"{id_jogador_vencedor}".encode("utf8"))
        conn3.sendall(f"{id_jogador_vencedor}".encode("utf8"))

        time.sleep(3)

       

        #inserir carta recebida no banco (n funciona)
        if id_jogador_vencedor == 1:
            username = conn1.recv(1024)
            msg_dict = json.loads(username.decode("utf8"))
            index_random = random.randint(0, len(self.cemiterio1)-1)
            carta_recebida = self.cemiterio1[index_random]
        
            bd_conn = sqlite3.connect('corrida_maluca.db')
            c = bd_conn.cursor()
            c.execute("""
                INSERT INTO cards (username, filename) 
                VALUES (?, ?)
                """, (msg_dict['username'], carta_recebida))

            bd_conn.commit()
            bd_conn.close()
            conn1.sendall(f"{carta_recebida}".encode("utf8"))


        elif id_jogador_vencedor == 2:
            username = conn2.recv(1024)
            msg_dict = json.loads(username.decode("utf8"))
            index_random = random.randint(0, len(self.cemiterio2)-1)
            carta_recebida = self.cemiterio2[index_random]

            bd_conn = sqlite3.connect('corrida_maluca.db')
            c = bd_conn.cursor()
            c.execute("""
                INSERT INTO cards (username, filename) 
                VALUES (?, ?)
                """, (msg_dict['username'], carta_recebida))

            bd_conn.commit()
            bd_conn.close()
            conn2.sendall(f"{carta_recebida}".encode("utf8"))


        elif id_jogador_vencedor == 3:
            username = conn3.recv(1024)
            msg_dict = json.loads(username.decode("utf8"))
            index_random = random.randint(0, len(self.cemiterio3)-1)
            carta_recebida = self.cemiterio3[index_random]

            bd_conn = sqlite3.connect('corrida_maluca.db')
            c = bd_conn.cursor()
            c.execute("""
                INSERT INTO cards (username, filename) 
                VALUES (?, ?)
                """, (msg_dict['username'], carta_recebida))

            bd_conn.commit()
            bd_conn.close()
            conn3.sendall(f"{carta_recebida}".encode("utf8"))

        

            
        conn1.close()
        conn2.close()
        conn3.close()

        exit()
    
        


    
    
