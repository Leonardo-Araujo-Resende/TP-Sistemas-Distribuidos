from model.Card import Card

class Collection():
    def __init__(self, cards:list[Card]):
        self.cards = cards

    def get_cards(self) -> list[Card]:
        return self.cards
    
    def get_by_id(self, id:int) -> Card:
        for card in self.cards:
            if id == card.get_id():
                return card
            
    def decrement_quantity_by_id(self, id:int):
        for card in self.cards:
            if(card.get_id == id):
                card.decrement_quantity()