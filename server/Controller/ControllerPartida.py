import random
import logging
import json
import sqlite3
import time
import threading
import Pyro5.api

@Pyro5.api.expose
class ControllerPartida():

    def __init__(self, all_cards):
        self.username1 = None
        self.username2 = None
        self.username3 = None
        self.deck1 = None
        self.deck2 = None
        self.deck3 = None
        self.cartas_escolhidas = {"carta1": -1, "carta2": -2, "carta3": -3}
        self.qt_cartas_escolhidas = 0
        self.qt_jogadores_prontos = 0
        self.qt_jogadores_respondidos = 0
        self.atributo_rodada = ""
        
        self.rodada_atual = 0
        self.cemiterio1 = []
        self.cemiterio2 = []
        self.cemiterio3 = []
        self.all_cards = all_cards
        self.vencedor_rodada = ""
        self.atributo_retorno = ""
        self.vencedor_final = -1
    
    
    

    def get_qt_usuarios_prontos(self,):
        return self.qt_jogadores_prontos
    

    def set_deck(self, deck, id):
        
        self.qt_jogadores_prontos += 1
        if id == 1:
            self.deck1 = deck
        elif id == 2:
            self.deck2 = deck
        else:
            self.deck3 = deck
                
        while True:
            if self.qt_jogadores_prontos == 3:
                self.qt_jogadores_respondidos += 1       
                if self.qt_jogadores_respondidos == 3:
                    self.set_first_attribute()
                    self.qt_jogadores_respondidos = 0
                break 
    
    def set_first_attribute(self):
        atributos = ["Velocidade", "Aceleração", "Peso", "Capacidade", "Resistência", "Truque"]
        atributos_ingles = ["speed", "accel", "weight", "capacity", "resistance", "gimmick"]
        index_random = random.randint(0, 5)
        self.atributo_rodada = atributos_ingles[index_random]
        self.atributo_retorno = atributos[index_random]

    def set_username(self, username, id):

        if id == 1:
            self.username1 = username
        elif id == 2:
            self.username2 = username
        else:
            self.username3 = username
            

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


    def verificar_vencedor(self):
        if self.vencedor_final != -1:
            return self.vencedor_final

        tamanho1 = len(self.cemiterio1)
        tamanho2 = len(self.cemiterio2)
        tamanho3 = len(self.cemiterio3)
        
        maior = max(tamanho1, tamanho2, tamanho3)
        
        vencedores = []
        
        if tamanho1 == maior:
            vencedores.append(1)
        if tamanho2 == maior:
            vencedores.append(2)
        if tamanho3 == maior:
            vencedores.append(3)
        
        if len(vencedores) == 1:
            self.vencedor_final = vencedores[0]
            return self.vencedor_final
        else:
            self.vencedor_final = random.choice(vencedores)
            return self.vencedor_final


    def send_start(self, username):

        if username == self.username1:
            return self.deck1[:3], self.atributo_retorno
        elif username == self.username2:
            return self.deck2[:3], self.atributo_retorno
        else:
            return self.deck3[:3], self.atributo_retorno
        

    def define_chosen_card(self, id_carta, username):

        if username == self.username1:
            self.cartas_escolhidas['carta1'] = id_carta
        elif username == self.username2:
            self.cartas_escolhidas['carta2'] = id_carta
        else:
            self.cartas_escolhidas['carta3'] = id_carta
        
        self.qt_cartas_escolhidas += 1
        
        
        while True:
            if self.qt_cartas_escolhidas == 3:
                self.qt_jogadores_respondidos += 1       
                if self.qt_jogadores_respondidos == 3:
                    self.define_winner()
                    self.qt_jogadores_respondidos = 0
                break
    

    def define_winner(self):
        
        personagem1 = self.get_character_by_index(self.cartas_escolhidas["carta1"])
        personagem2 = self.get_character_by_index(self.cartas_escolhidas["carta2"])
        personagem3 = self.get_character_by_index(self.cartas_escolhidas["carta3"])
        self.vencedor_rodada = self.who_won(personagem1, personagem2, personagem3, self.atributo_rodada)


        if self.vencedor_rodada == "1":
            self.append_carta_cemiterio(1,self.cartas_escolhidas["carta2"])
            self.append_carta_cemiterio(1,self.cartas_escolhidas["carta3"])
        elif self.vencedor_rodada == "2":
            self.append_carta_cemiterio(2,self.cartas_escolhidas["carta1"])
            self.append_carta_cemiterio(2,self.cartas_escolhidas["carta3"])
        elif self.vencedor_rodada == "3":
            self.append_carta_cemiterio(3,self.cartas_escolhidas["carta1"])
            self.append_carta_cemiterio(3,self.cartas_escolhidas["carta2"])

        atributos = ["Velocidade", "Aceleração", "Peso", "Capacidade", "Resistência", "Truque"]
        atributos_ingles = ["speed", "accel", "weight", "capacity", "resistance", "gimmick"]
        index_random = random.randint(0, 5)
        self.atributo_rodada = atributos_ingles[index_random]
        self.atributo_retorno = atributos[index_random]
        self.rodada_atual += 1
        self.qt_cartas_escolhidas = 0
        
        

    def append_carta_cemiterio(self, id_cemiterio, id_carta):
        if id_cemiterio == 1:
            self.cemiterio1.append(id_carta)
        if id_cemiterio == 2:
            self.cemiterio2.append(id_carta)
        if id_cemiterio == 3:
            self.cemiterio3.append(id_carta)
            


    def return_winner(self, username):
        
        
        if self.rodada_atual < 7:
            if username == self.username1:
                return self.vencedor_rodada, self.deck1[self.rodada_atual+2], self.atributo_retorno, self.cartas_escolhidas["carta1"], self.cartas_escolhidas["carta2"], self.cartas_escolhidas["carta3"]
            elif username == self.username2:
                return self.vencedor_rodada, self.deck2[self.rodada_atual+2], self.atributo_retorno, self.cartas_escolhidas["carta1"], self.cartas_escolhidas["carta2"], self.cartas_escolhidas["carta3"]
            else:
                return self.vencedor_rodada, self.deck3[self.rodada_atual+2], self.atributo_retorno, self.cartas_escolhidas["carta1"], self.cartas_escolhidas["carta2"], self.cartas_escolhidas["carta3"]
        elif self.rodada_atual < 9:
            return self.vencedor_rodada, self.atributo_retorno,self.cartas_escolhidas["carta1"], self.cartas_escolhidas["carta2"], self.cartas_escolhidas["carta3"]
        else:
            return self.vencedor_rodada

    def define_carta_vencedor(self):
        carta_escolhida = 0

        if self.vencedor_final == 1:
            carta_escolhida = random.choice(self.cemiterio1)
        if self.vencedor_final == 2:
            carta_escolhida = random.choice(self.cemiterio2)
        if self.vencedor_final == 3:
            carta_escolhida = random.choice(self.cemiterio3)

        return self.salva_carta_banco( carta_escolhida)

    def salva_carta_banco(self, carta_escolhida):

        username_vencedor = ""

        if self.vencedor_final == 1:
            username_vencedor = self.username1
        if self.vencedor_final == 2:
            username_vencedor = self.username2
        if self.vencedor_final == 3:
            username_vencedor = self.username3

        bd_conn = sqlite3.connect('corrida_maluca.db')
        c = bd_conn.cursor()
        c.execute("""
            INSERT INTO cards (username, filename) 
            VALUES (?, ?)
            """, (username_vencedor, carta_escolhida))


        bd_conn.commit()
        bd_conn.close()

        return carta_escolhida
        


    
    
