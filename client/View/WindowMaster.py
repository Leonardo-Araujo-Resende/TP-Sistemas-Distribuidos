import arcade 
import arcade.color
import arcade.csscolor
import arcade.gui
from controller.ControllerJogar import *
from View.ViewBaralhos import ViewBaralhos
from controller.ControllerBaralhos import *
from model.Collection import *
from View.ViewPartida import *

class WindowMaster(arcade.Window):

    def __init__(self):
        super().__init__(1400, 750, "Janela Principal", center_window=True, resizable=True)
        self.collection:Collection = Collection([])
        self.cliente = Client()
        self.id_player = 0

        self.cor_escura = arcade.color_from_hex_string("#08D8FF")
        self.cor_clara = arcade.color_from_hex_string("#220B60")    

        self.botao_style = {
            "font_name": "Roboto",
            "font_size": 15,
            "font_color": self.cor_clara,
            "border_width": 2,
            "border_color": self.cor_clara,
            "bg_color": (0, 0, 0, 0),

            "bg_color_pressed": (0, 0, 0, 0),
            "border_color_pressed": self.cor_escura,  
            "font_color_pressed": self.cor_escura,
        }
    
    def switch_view(self, new_view):
        self.current_view.clear()
        self.show_view(new_view)
        new_view.on_show()
    
    def set_window_size(self, width, height):
        self.set_size(width, height)
        self.center_window()

    def switch_view_to_Baralho(self):
        self.switch_view( ViewBaralhos( ControllerJogar(self.cliente), ControllerBaralhos( self.collection, [Deck([]), Deck([])] ), self, self.collection) )
    
    def switch_view_to_Partida(self):
        self.switch_view( ViewPartida(self, self.cliente) )

    def set_collection(self, collection):
        for c in collection:
            self.collection.append_card(c)
