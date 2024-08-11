import arcade 
import arcade.color
import arcade.csscolor
import arcade.gui


class ViewPartida(arcade.View):

    def __init__(self, window):
        super().__init__()
        self.window = window

    def on_draw(self):
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

