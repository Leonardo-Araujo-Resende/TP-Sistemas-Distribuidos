import Truque

class Card():
    def __init__(self, velocidade:int, aceleracao:int, peso:int, capacidade:int, resistencia:int, truque:Truque, quantity:int):
        self.velocidade = velocidade
        self.aceleracao = aceleracao
        self.peso = peso
        self.capacidade = capacidade
        self.resistencia = resistencia
        self.truque = truque
        self.quantity = quantity
