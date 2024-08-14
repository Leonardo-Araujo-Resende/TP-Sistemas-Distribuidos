import arcade 
import arcade.color
import arcade.csscolor
import logging
import threading
import time
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
        self.fundo = arcade.Sprite(filename="resources/fundo.jpg", center_x=650, center_y=350, scale=1.1)
        self.window = window
        self.controller_partida = ControllerPartida(client)
        self.cont_rodadas = 0

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.dragging_card = None
        self.used_card_x = None

        self.can_darg_card = True
        
        self.cartas_sprites:CartaSprite = arcade.SpriteList()
        msg = self.controller_partida.listen_game_finish()

        mao_inicial, atributo = msg.split(" - ")
        
        mao_inicial = self.controller_partida.remove_colchete(mao_inicial)
        self.first_3_cards(mao_inicial)

        self.atributo = UILabel(text= f"Atributo Selecionado: {atributo}", x=700 - 250, y=625, width=500, height=60, align="center", font_name="Roboto", font_size=15,text_color=arcade.color.BLACK)
        self.manager.add( self.atributo )

        self.avisos = UILabel(text= f"", x=50, y=675, width=500, height=60, align="center", font_name="Roboto", font_size=15,text_color=arcade.color.BLACK)
        self.manager.add( self.avisos )

        self.id_jogador = UILabel(text= f"Voce é o jogador: {self.window.id_player}", x=1100, y=675, width=250, height=60, align="center", font_name="Roboto", font_size=15,text_color=arcade.color.BLACK)
        self.manager.add( self.id_jogador )

        self.pontuacao = [0,0,0]
        
        self.titulo_pontuacao = UILabel(text= "Pontuação dos Jogadores", x=20, y=200, width=250, height=60, font_name="Roboto", font_size=15,text_color=arcade.color.BLACK)
        self.manager.add( self.titulo_pontuacao )
        self.pontuacao_jogador_1 = UILabel(text= "Jogador 1: ", x=20, y=150, width=250, height=60, font_name="Roboto", font_size=15,text_color=arcade.color.BLACK)
        self.manager.add( self.pontuacao_jogador_1 )
        self.pontuacao_jogador_2 = UILabel(text= "Jogador 2: ", x=20, y=100, width=250, height=60, font_name="Roboto", font_size=15,text_color=arcade.color.BLACK)
        self.manager.add( self.pontuacao_jogador_2 )
        self.pontuacao_jogador_3 = UILabel(text= "Jogador 3: ", x=20, y=50, width=250, height=60, font_name="Roboto", font_size=15,text_color=arcade.color.BLACK)
        self.manager.add( self.pontuacao_jogador_3 )

        self.msg = None

    def first_3_cards(self, mao_inicial):
        x = 400
        y = 150
        for i in range(3):
            self.cartas_sprites.append(CartaSprite(f"resources/{mao_inicial[i]}.jpg", x, y, 0.35, mao_inicial[i]))
            x += 250

    def update_score(self, id_player):
        id_player = int(id_player) -1
        self.pontuacao[id_player] +=1 
        if id_player == 0:
            self.pontuacao_jogador_1.text += "🏆"
        elif id_player == 1:
            self.pontuacao_jogador_2.text += "🏆"
        elif id_player == 2:
            self.pontuacao_jogador_3.text += "🏆"

    def update_atributo(self, msg):
        self.atributo.text = f"Atributo selecionado: {msg}"
    
    def jogador_vencedor(self,msg):
        self.atributo.text = f"Jogador vencedor {msg}"

    def recieved_card(self, id):
        self.cartas_sprites.append(CartaSprite(f"resources/{id}.jpg", self.used_card_x, 150, 0.35, id))
    
    def desenha(self):
        self.clear()
        self.fundo.draw()
        self.manager.draw()
        self.cartas_sprites.draw()
    
    def on_draw(self):
        self.desenha()
        #Mesa
        arcade.draw_lrtb_rectangle_outline(
            left = 20,
            right = 1380,
            top = 700,
            bottom = 300,
            color = arcade.color.WHITE
        )
    def on_update(self, delta_time: float):
        if self.msg != None:
            self.update_depois_rodada()

    def on_show(self):
        self.window.set_window_size(1400,750)

    def on_mouse_press(self, x, y, button, modifiers):
        for card in self.cartas_sprites:
            if card.collides_with_point((x, y)) and self.can_darg_card == True:
                self.dragging_card = card

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        if self.dragging_card and self.can_darg_card == True:
            self.dragging_card.center_x = x
            self.dragging_card.center_y = y

    def on_mouse_release(self, x, y, button, modifiers):
        if self.dragging_card and self.can_darg_card == True:
            if y > 300:
                self.can_darg_card = False
                self.dragging_card.center_x = 700
                self.dragging_card.center_y = 500
                self.used_card_x = self.dragging_card.init_x
                id = self.dragging_card.id
                thread = threading.Thread(target=self.espera_mensagem, args=(id,))
                thread.start()

            else:
                self.dragging_card.center_x = self.dragging_card.init_x
                self.dragging_card.center_y = self.dragging_card.init_y

    def exibe_msg_aviso(self, msg):
        self.avisos.text = msg

    def espera_mensagem(self, id):
        self.msg = self.controller_partida.send_chosen_card( self.dragging_card.id, self.window.id_player)

    def update_depois_rodada(self):
        self.cont_rodadas += 1
        if self.cont_rodadas < 7:
            vencedor, nova_carta, atributo = self.msg.split(" - ")
            self.update_score(vencedor)
            self.update_atributo(atributo)
            self.cartas_sprites.remove(self.dragging_card)
            self.recieved_card(nova_carta)

        elif self.cont_rodadas == 9:
            vencedor = self.msg
            self.update_score(vencedor)
            self.cartas_sprites.remove(self.dragging_card)

            id_vencedor = self.controller_partida.listen_game_finish()

            if int(id_vencedor) == int(self.window.id_player):
                carta_premiun = self.controller_partida.send_username(self.window.username)
                self.window.switch_view_to_win(carta_premiun)
            else:
                self.jogador_vencedor(f"{id_vencedor}")

        else:
            vencedor, atributo = self.msg.split(" - ")
            self.update_score(vencedor)
            self.update_atributo(atributo)
            self.cartas_sprites.remove(self.dragging_card)
        

        self.msg = None
        self.dragging_card = None
        self.can_darg_card = True
