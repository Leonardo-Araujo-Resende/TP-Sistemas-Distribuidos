from sys import argv
import Pyro5.api

class ControllerLoginCadastrar():

    def sign_in(self, username: str, password: str):

        controller_login_cad = Pyro5.api.Proxy("PYRONAME:server.log_cad")
        controller_deck = Pyro5.api.Proxy("PYRONAME:server.deck")             
        resultado = controller_login_cad.sign_in_bd(username, password)
        deck1 = controller_deck.search_deck_on_db(username, 0)
        deck2 = controller_deck.search_deck_on_db(username, 1)
        print("seu deck 1: ", deck1, flush= True)
        print("seu deck 2: ", deck2, flush= True)
        if resultado == 0:
            return controller_login_cad.return_colection(username) 
        else:
            return 1
    
    def sign_up(self, username: str, password: str):
        controller_login_cad = Pyro5.api.Proxy("PYRONAME:server.log_cad")
        
        
        resultado = controller_login_cad.sign_up_bd(username, password)
        if resultado == 0:
            return 0 
        else:
            return 1
        

        
        
