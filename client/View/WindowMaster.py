import arcade 
import arcade.color
import arcade.csscolor
import arcade.gui
from network.Client import *
from View.ViewBaralhos import ViewBaralhos
from controller.ControllerBaralhos import *
from model.Collection import *

class WindowMaster(arcade.Window):

    def __init__(self):
        super().__init__(1400, 750, "Janela Principal", center_window=True)
        self.collection:Collection = Collection([])


        self.corEscura = arcade.color_from_hex_string("#08D8FF")
        self.corClara = arcade.color_from_hex_string("#220B60")    
    
    def switch_view(self, new_view):
        self.current_view.clear()
        self.show_view(new_view)
        new_view.on_show()
    
    def set_window_size(self, width, height):
        self.set_size(width, height)
        self.center_window()

    def switch_view_to_Baralho(self):
        self.switch_view(ViewBaralhos(Client, ControllerBaralhos(self.collection, [Deck([]), Deck([])]), self,self.collection))

    def set_collection(self, collection):
        for c in collection:
            self.collection.append_card(c)
