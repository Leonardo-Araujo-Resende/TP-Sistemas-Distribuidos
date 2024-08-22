from sys import argv
from network.Client import *
import json
import Pyro5.api

class ControllerLoginCadastrar():
    
    def __init__(self):
        self.client = Client()


    def sign_in(self, username: str, password: str):

        controller_server = Pyro5.api.Proxy("PYRONAME:server.log_cad")
        
        
        resultado = controller_server.sign_in_bd(username, password)
        if resultado == 0:
            return controller_server.return_colection(username) 
        else:
            return 1
    
    def sign_up(self, username: str, password: str):
        controller_server = Pyro5.api.Proxy("PYRONAME:server.log_cad")
        
        
        resultado = controller_server.sign_up_bd(username, password)
        if resultado == 0:
            return 0 
        else:
            return 1
        

        
        
