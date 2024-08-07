import arcade 
import arcade.csscolor
import arcade.gui
from arcade.gui import UILabel
from arcade.gui.widgets import UIInputText
from client.network.Client import Client
from typing import List

class CartaSprite(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale, id):
        super().__init__(filename=filename, center_x=center_x, center_y=center_y, scale=scale)
        self.filename = filename
        self.init_x = center_x
        self.init_y = center_y
        self.id = id
        self.original_scale = scale
        self.is_hover = False


    
class BaralhoCompleto():
    def __init__(self, x: int, y: int, distance_x_between_cards: int, distance_y_between_cards:int, cartas_sprites:CartaSprite):
        self.x = x
        self.y = y
        self.scale = None
        self.cards_list = cartas_sprites
        self.distance_x_between_cards = distance_x_between_cards
        self.distance_y_between_cards = distance_y_between_cards

    def print_cards(self):
        for i in range(3):
            for j in range(10):
                add_card = CartaSprite(f"client/resources/{i*10+j+1}.png", self.x + j * self.distance_x_between_cards, self.y - i * self.distance_y_between_cards, 0.5, i*10+j)
                self.cards_list.append(add_card)
                self.cards_list.draw()
    

class Deck():
    def __init__(self, top: int, bottom: int, distance_x_between_cards: int, ui_manager: arcade.gui.UIManager):
        self.top = top
        self.bottom = bottom
        self.scale = None
        self.cards_list = arcade.SpriteList()
        self.distance_x_between_cards = distance_x_between_cards
        self.ui_manager = ui_manager
        self.ui_tittle = None
        self.tittle()

    def append_card(self, card: CartaSprite):
        if len(self.cards_list) >= 9:
            self.alert("Baralho cheio!")
            return


        self.scale = (self.top-self.bottom)/card.height
        add_card = CartaSprite(card.filename, (card.width * self.scale * card.scale)* 2 * len(self.cards_list) + self.distance_x_between_cards * len(self.cards_list) + 100, (self.top + self.bottom)//2, self.scale * card.scale, card.id)
        self.cards_list.append(add_card)
        self.cards_list.draw()
        self.update_tittle()


    def verify_if_in(self, y: int):
        if self.top > y > self.bottom:
            return True
        return False
    
    def rectangle(self):
        arcade.draw_lrtb_rectangle_outline(
            left = 20,
            right = 850,
            top = self.top,
            bottom = self.bottom,
            color = arcade.color_from_hex_string("#220B60") 
        )
    
    def alert(self, msg):
        self.ui_tittle.text = msg
        arcade.schedule( self.stop_alert , 3)
    
    def stop_alert(self, delta_time):
        self.update_tittle()
        arcade.unschedule(self.stop_alert)

    def tittle(self):
        self.ui_tittle = UILabel( text="Baralho", x=20, y=self.top, width=300, height=15, font_name="Roboto", font_size=10,text_color=arcade.color_from_hex_string("#220B60") )
        self.ui_manager.add( self.ui_tittle)
    
    def update_tittle(self):
        self.ui_tittle.text = f"Baralho {len(self.cards_list)}"
    

class ViewBaralhos(arcade.Window):

    def __init__(self, width, height, title, client: Client):
        super().__init__(width, height, title, center_window=True)

                
        self.corEscura = arcade.color_from_hex_string("#08D8FF")
        self.corClara = arcade.color_from_hex_string("#220B60")       

        arcade.set_background_color(self.corEscura)

        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        #sprites e colisao
        self.cartas_sprites:CartaSprite = arcade.SpriteList()
        self.all_cards = BaralhoCompleto(60, 670, 110, 145,self.cartas_sprites)
        self.all_cards.print_cards()

        #auxiliares
        self.dragging_card:CartaSprite = None

        #baralho
        self.deck_list: List[Deck] = []

        self.deck_list.append(Deck(105, 5, 10, self.ui_manager))
        self.deck_list.append(Deck(220, 120, 10, self.ui_manager))

        #Carta destacada
        self.spotted_card:CartaSprite = arcade.SpriteList()


        

    def on_draw(self):
        self.clear()
        self.cartas_sprites.draw()
        self.all_cards.cards_list.draw()
        self.spotted_card.draw()
        for baralho in self.deck_list:
            baralho.cards_list.draw()
            baralho.rectangle()
        self.ui_manager.draw()


    def on_mouse_press(self, x, y, button, modifiers):
        for card in self.cartas_sprites:
            if card.collides_with_point((x, y)):

                self.dragging_card = card

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.dragging_card:
            self.dragging_card.center_x = x
            self.dragging_card.center_y = y


    def on_mouse_motion(self, x, y, dx, dy):
        for card in self.cartas_sprites:
            if card.collides_with_point((x, y)):
                self.create_highlight_card(card)
                break


    def create_highlight_card(self, card :CartaSprite):
        self.spotted_card.clear()
        self.spotted_card.append(CartaSprite(card.filename, 1250, 554, 1.3, card.id))
            
                


    def on_mouse_release(self, x, y, button, modifiers):
        if self.dragging_card:
            for baralho in self.deck_list:
                if baralho.verify_if_in(y):
                    baralho.append_card(self.dragging_card)
            self.dragging_card.center_x = self.dragging_card.init_x
            self.dragging_card.center_y = self.dragging_card.init_y

            self.dragging_card = None


def main(): 
    window  = ViewBaralhos(1400, 750, "Montar Deck", Client())
    arcade.run()



if __name__ == "__main__":
    main()