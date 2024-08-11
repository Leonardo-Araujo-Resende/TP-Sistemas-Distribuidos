import arcade 
import arcade.color
import arcade.csscolor
import arcade.gui
from arcade.gui import UILabel
from controller.ControllerPartida import *


class CartaSprite(arcade.Sprite):
    def __init__(self, filename, center_x, center_y, scale, id):
        super().__init__(filename=filename, center_x=center_x, center_y=center_y, scale=scale)
        self.filename = filename
        self.init_x = center_x
        self.init_y = center_y
        self.id = id
        self.original_scale = scale


class ViewPartida(arcade.View):

    def __init__(self, window, client):
        super().__init__()
        self.window = window
        self.controller_partida = ControllerPartida(client)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.dragging_card = None
        self.used_card_x = None
        
        self.cartas_sprites:CartaSprite = arcade.SpriteList()
        
        mao_inicial = self.controller_partida.remove_colchete(self.controller_partida.listen_game_start())
        x = 525
        y = 130
        for i in range(3):
            self.cartas_sprites.append(CartaSprite(f"resources/{mao_inicial[i]}.png", x, y, 0.25, mao_inicial[i]))
            x += 175

        self.debug = UILabel(text="vai aparecer aq", x=400, y=300, width=600, height=400, font_name="Roboto", font_size=15,text_color=arcade.color.BLACK)
        self.manager.add( self.debug )


    def on_draw(self):
        self.clear()
        self.manager.draw()
        self.cartas_sprites.draw()
        #Mesa
        arcade.draw_lrtb_rectangle_outline(
            left = 20,
            right = 1380,
            top = 700,
            bottom = 300,
            color = arcade.color.WHITE
        )

        #Baralho
        arcade.draw_lrtb_rectangle_outline(
            left = 1200,
            right = 1350,
            top = 240,
            bottom = 20,
            color = arcade.color.WHITE
        )

        #Cemiterio
        arcade.draw_lrtb_rectangle_outline(
            left = 50,
            right = 200,
            top = 240,
            bottom = 20,
            color = arcade.color.WHITE
        )


        #Cartas no centro
        arcade.draw_lrtb_rectangle_outline(
            left = 625,
            right = 775,
            top = 240,
            bottom = 20,
            color = arcade.color.WHITE
        )

        #Cartas direita
        arcade.draw_lrtb_rectangle_outline(
            left = 800,
            right = 950,
            top = 240,
            bottom = 20,
            color = arcade.color.WHITE
        )

        #Cartas esquerda
        arcade.draw_lrtb_rectangle_outline(
            left = 450,
            right = 600,
            top = 240,
            bottom = 20,
            color = arcade.color.WHITE
        )

    def on_show(self):
        self.window.set_window_size(1400,750)

    def on_mouse_press(self, x, y, button, modifiers):
        for card in self.cartas_sprites:
            if card.collides_with_point((x, y)):
                self.dragging_card = card

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.dragging_card:
            self.dragging_card.center_x = x
            self.dragging_card.center_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        if self.dragging_card:
            if y > 300:
                self.dragging_card.center_x = 700
                self.dragging_card.center_y = 500
                self.used_card_x = self.dragging_card.init_x

                id = self.dragging_card.id
                self.debug.text = f"{id} {self.window.id_player}"
                
                # text = self.controller_partida.send_chosen_card(id,self.window.id_player)
                # self.debug.text = text
                # print(text)
            else:
                self.dragging_card.center_x = self.dragging_card.init_x
                self.dragging_card.center_y = self.dragging_card.init_y


            self.dragging_card = None

