from model.Card import Card

class Collection():
    def __init__(self, cards:list[Card]):
        self.cards:list[Card] = cards

    def get_cards(self) -> list[Card]:
        return self.cards
    
    def get_quantity_by_id(self, id:int) -> int:
        for card in self.cards:
            if id == card.get_id():
                return card.get_quantity()

    def increment_quantity_by_id(self, id:int):
        for card in self.cards:
            if card.get_id() == id:
                card.increment_quantity()
            
    def decrement_quantity_by_id(self, id:int):
        for card in self.cards:
            if card.get_id() == id:
                card.decrement_quantity()

    def append_card(self, id):
        for c in self.cards:
            if int(c.get_id()) == int(id):
                c.increment_quantity()
                return
        self.cards.append(Card(int(id), 1))

