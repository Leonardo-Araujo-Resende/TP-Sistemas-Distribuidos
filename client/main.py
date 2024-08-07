import arcade 
from View.ViewLoginCadastrar import *
from controller.ControllerLoginCadastrar import *

def main(): 
    window  = ViewLoginCadastrar(1300, 700, "Login/Cadastrar", ControllerLoginCadastrar())
    arcade.run()
    # window = arcade.Window(800, 600, f"Client - {client_name}", resizable=True)
    # main_view = MainView(client_name)
    # window.show_view(main_view)
    # arcade.run()


if __name__ == "__main__":
    main()