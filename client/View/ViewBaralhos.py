import arcade 
import arcade.csscolor
import arcade.gui
from arcade.gui import UILabel
from arcade.gui.widgets import UIInputText
from controller.ControllerBaralhos import *
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
    def __init__(self, x: int, y: int, distance_x_between_cards: int, distance_y_between_cards:int, cartas_sprites:CartaSprite, collection):
        self.x = x
        self.y = y
        self.scale = None
        self.cards_list = cartas_sprites
        self.distance_x_between_cards = distance_x_between_cards
        self.distance_y_between_cards = distance_y_between_cards
        self.collection = collection

    def print_cards(self):
        tamanho = len(self.collection.get_cards())
        cont = 0
        for i in range(3):
            for j in range(10):
                add_card = CartaSprite(f"resources/{self.collection.get_cards()[i*10+j].get_id()}.png", self.x + j * self.distance_x_between_cards, self.y - i * self.distance_y_between_cards, 0.5, int(self.collection.get_cards()[i*10+j].get_id()))
                self.cards_list.append(add_card)
                self.cards_list.draw()
                cont += 1
                if cont == tamanho:
                    break
            if cont == tamanho:
                break
    

class DeckView():
    def __init__(self, deck_id:int, top: int, bottom: int, distance_x_between_cards: int, ui_manager: arcade.gui.UIManager, controller: ControllerBaralhos):
        self.deck_id = deck_id
        self.top = top
        self.bottom = bottom
        self.scale = None
        self.cards_list = arcade.SpriteList()
        self.distance_x_between_cards = distance_x_between_cards
        self.ui_manager = ui_manager
        self.ui_title = None
        self.controller = controller
        self.title()

    def append_card(self, card: CartaSprite):
        if len(self.cards_list) >= 9:
            self.alert("Baralho cheio!")
            return
        
        if self.controller.append_card_deck(card.id, self.deck_id) == False:
            self.alert("Não possui carta ou mais de 3 cópias")
            return



        self.scale = (self.top-self.bottom)/card.height
        add_card = CartaSprite(card.filename, (card.width * self.scale * card.scale)* 2 * len(self.cards_list) + self.distance_x_between_cards * len(self.cards_list) + 100, (self.top + self.bottom)//2, self.scale * card.scale, card.id)
        self.cards_list.append(add_card)
        self.cards_list.draw()
        self.update_title()

    def reset(self):
        self.controller.reset_deck(self.deck_id)
        self.cards_list.clear()
        self.update_title()



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
        self.ui_title.text = msg
        arcade.schedule( self.stop_alert , 3)
    
    def stop_alert(self, delta_time):
        self.update_title()
        arcade.unschedule(self.stop_alert)

    def title(self):
        self.ui_title = UILabel( text="Baralho", x=20, y=self.top, width=300, height=15, font_name="Roboto", font_size=10,text_color=arcade.color_from_hex_string("#220B60") )
        self.ui_manager.add( self.ui_title)
    
    def update_title(self):
        self.ui_title.text = f"Baralho {len(self.cards_list)}"
    

class ViewBaralhos(arcade.View):

    def __init__(self, controller_client: Client, controller_view:ControllerBaralhos, window, collection):
        super().__init__()
        self.collection = collection
        self.window = window
        self.controller_client = controller_client
        self.controller_view = controller_view
        
                
        self.corEscura = arcade.color_from_hex_string("#08D8FF")
        self.corClara = arcade.color_from_hex_string("#220B60")       


        self.ui_manager = arcade.gui.UIManager()
        self.ui_manager.enable()

        #sprites e colisao
        self.cartas_sprites:CartaSprite = arcade.SpriteList()
        self.all_cards = BaralhoCompleto(60, 670, 110, 145, self.cartas_sprites, self.collection)
        self.all_cards.print_cards()

        #auxiliares
        self.dragging_card:CartaSprite = None

        #baralhos
        self.deck_list: List[DeckView] = []

        self.deck_list.append(DeckView(0, 220, 120, 10, self.ui_manager, self.controller_view ))
        self.deck_list.append(DeckView(1, 105, 5, 10, self.ui_manager, self.controller_view ))

        #Carta destacada e quantidade
        self.spotted_card:CartaSprite = arcade.SpriteList()

        self.text_quantity = UILabel(text="Quantidade nao usada: ", x=1125, y=300, width=300, height=40, font_name="Roboto", font_size=15,text_color=arcade.color_from_hex_string("#220B60") )
        self.ui_manager.add( self.text_quantity)

        #Botoes
        botao_style = {
            "font_name": "Roboto",
            "font_size": 15,
            "font_color": self.corClara,
            "border_width": 2,
            "border_color": self.corClara,
            "bg_color": self.corEscura,

            "bg_color_pressed": arcade.color.BLACK,
            "border_color_pressed": self.corEscura,  
            "font_color_pressed": self.corClara,
        }

        #Botoes deck01
        button_save_deck_01 = arcade.gui.UIFlatButton(x=855,y=220-50+2,text="Salvar1",height=50,width=100,style=botao_style)
        self.ui_manager.add(button_save_deck_01)

        @button_save_deck_01.event
        def on_click(event):
            #Chama controller e salva no banco deck 01
            if self.controller_client.save_deck(self.deck_list[0], 0) == 1:
                self.deck_list[0].alert("Deck Salvo")
            else:
                self.deck_list[0].alert("Erro ao salvar")


        button_delete_deck_01 = arcade.gui.UIFlatButton(x=855,y=120-1,text="Excluir1",height=50,width=100,style=botao_style)
        self.ui_manager.add(button_delete_deck_01)
        @button_delete_deck_01.event
        def on_click(event):
            self.deck_list[0].reset()

        #Botoes deck02
        button_save_deck_02 = arcade.gui.UIFlatButton(x=855,y=105-50+2,text="Salvar2",height=50,width=100,style=botao_style)
        self.ui_manager.add(button_save_deck_02)
        @button_save_deck_02.event
        def on_click(event):
            #Chama controller e salva no banco deck 02
            if self.controller_client.save_deck(self.deck_list[1], 1) == 1:
                self.deck_list[1].alert("Deck Salvo")
            else:
                self.deck_list[1].alert("Erro ao salvar")

        button_delete_deck_02 = arcade.gui.UIFlatButton(x=855,y=5-1,text="Excluir2",height=50,width=100,style=botao_style)
        self.ui_manager.add(button_delete_deck_02)
        @button_delete_deck_02.event
        def on_click(event):
            self.deck_list[1].reset()






        #Botoes jogar partida
        button_play_with_deck_01 = arcade.gui.UIFlatButton(x=1000,y=120,text="Jogar 01",height=110,width=300,style=botao_style)
        self.ui_manager.add(button_play_with_deck_01)

        @button_play_with_deck_01.event
        def on_click(event):
            #Inicia partida com deck 01
            print()

        #Botoes jogar
        button_play_with_deck_2 = arcade.gui.UIFlatButton(x=1000,y=5,text="Jogar02",height=110,width=300,style=botao_style)
        self.ui_manager.add(button_play_with_deck_2)

        @button_play_with_deck_2.event
        def on_click(event):
            #Inicia partida com deck 02
            print()




    def on_show(self):
        self.window.set_window_size(1400,750)


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
        self.text_quantity.text = f"Quantidade nao usada: {self.controller_view.collection.get_quantity_by_id(card.id)}"
            
                


    def on_mouse_release(self, x, y, button, modifiers):
        if self.dragging_card:
            for baralho in self.deck_list:
                if baralho.verify_if_in(y):
                    baralho.append_card(self.dragging_card)
            self.dragging_card.center_x = self.dragging_card.init_x
            self.dragging_card.center_y = self.dragging_card.init_y

            self.dragging_card = None


# def main(): 
#     window  = ViewBaralhos(1400, 750, "Montar Deck", Client())
#     arcade.run()



# if __name__ == "__main__":
#     main()