import arcade 
import arcade.color
import arcade.csscolor
import arcade.gui
from arcade.gui import UILabel
from arcade.gui.widgets import UIInputText


class ViewVitoria(arcade.View):

    def __init__(self, window, id_carta):
        super().__init__()

        self.carta = arcade.Sprite(filename=f"resources/{id_carta}.png", center_x=700, center_y=375, scale = 0.7)
        self.fundo = arcade.Sprite(filename="resources/fundo.png", center_x=650, center_y=350, scale=1.1)




        self.window = window

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.atributo = UILabel(text= f"Parabéns você ganhou a carta:", x=700 - 250, y=650, width=500, height=60, align="center", font_name="Roboto", font_size=15,text_color=arcade.color.BLACK)
        self.manager.add( self.atributo )



    def on_draw(self):
        self.fundo.draw()
        self.carta.draw()
        self.manager.draw()
    
    def on_show(self):
        self.clear()
        #self.window.set_window_size(1400,750)
        self.manager.draw()


