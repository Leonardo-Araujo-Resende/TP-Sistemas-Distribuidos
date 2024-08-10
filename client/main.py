import arcade 
from View.ViewLoginCadastrar import *
from controller.ControllerLoginCadastrar import *
from View.WindowMaster import WindowMaster

def main(): 

    window = WindowMaster()
    window.show_view(ViewLoginCadastrar(window, ControllerLoginCadastrar()))
    arcade.run()



if __name__ == "__main__":
    main()