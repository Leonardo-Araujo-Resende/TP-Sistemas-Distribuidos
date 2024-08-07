import arcade 
from View.ViewLoginCadastrar import *
from controller.ControllerLoginCadastrar import *

def main(): 
    window  = ViewLoginCadastrar(1300, 700, "Login/Cadastrar", ControllerLoginCadastrar())
    arcade.run()


if __name__ == "__main__":
    main()