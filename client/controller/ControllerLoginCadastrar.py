from sys import argv
from network.Client import *
import json

class ControllerLoginCadastrar():
    
    def __init__(self):
        self.client = Client()


    def sign_in(self, username: str, password: str):
        msg = { "op": "login",
                "username": username,
                "password": password}
        
        response = self.client.send_msg(msg)
        try:
            # Tenta carregar a mensagem como JSON
            dados = json.loads(response)
            return dados['colecao']
            
            
        except json.JSONDecodeError:
            # Se falhar, significa que a mensagem não é um JSON 
            return 1

        
    
    def sign_up(self, username: str, password: str):
        msg = { "op": "cadastro",
                "username": username,
                "password": password}
        
        if self.client.send_msg(msg) == "Success":
            return 0
        else:
            return 1

        
        
