import Truque

class Card():
    def __init__(self, id:int, velocidade:int, aceleracao:int, peso:int, capacidade:int, resistencia:int, truque:Truque, quantity:int):
        self.id = id
        self.velocidade = velocidade
        self.aceleracao = aceleracao
        self.peso = peso
        self.capacidade = capacidade
        self.resistencia = resistencia
        self.truque = truque
        self.quantity = quantity

    def get_id(self) -> int:
        return self.id

    def get_velocidade(self) -> int:
        return self.velocidade

    def get_aceleracao(self) -> int:
        return self.aceleracao

    def get_peso(self) -> int:
        return self.peso

    def get_capacidade(self) -> int:
        return self.capacidade

    def get_resistencia(self) -> int:
        return self.resistencia

    def get_truque(self) -> Truque:
        return self.truque

    def get_quantity(self) -> int:
        return self.quantity
    
    def increment_quantity(self):
        self.quantity += self.quantity

    def decrement_quantity(self):
        self.quantity -= self.quantity