from sys import argv
from network.Client import *

class ControllerLoginCadastrar():
    
    def __init__(self):
        self.client = Client()


    def sign_in(self, username: str, password: str):
        msg = { "op": "login",
                "username": username,
                "password": password}
        return self.client.send_msg(msg)
        
    
    def sign_up(self, username: str, password: str):
        msg = { "op": "cadastro",
                "username": username,
                "password": password}
        return self.client.send_msg(msg)
