from sys import argv
from network.Client import *

class ControllerLoginCadastrar():
    
    def __init__(self):
        self.client = Client()


    def sign_in(self, username: str, password: str):

        return self.client.sign_in(username, password)
        
    
    def sign_up(self, username: str, password: str):

        return self.client.sign_up(username, password)
