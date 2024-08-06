"""
O cliente envia seu nome e mostra a resposta do servidor.
Essa não é necessariamente a melhor implementação de como lidar com as comunicações
com o servidor, serve apenas para ilustrar que isso é possível.
Inclusive, não é necessário usar as mesmas bibliotecas.

Referências:
- [Biblioteca de sockets](https://docs.python.org/3/library/socket.html)
- [Biblioteca arcade](https://api.arcade.academy/en/latest/)
"""

from sys import argv
import arcade
import arcade.gui
import threading
import socket

class Client():
    
    def __init__(self):
        self.username = ""


    def sign_in(self, username: str, password: str):
        msg = f"login-{username}-{password}"
        server_msg = self.send_to_server(msg)
                  
        if server_msg.decode('utf8') == "Success":
            return 0
        else:
            return 1
    
    def sign_up(self, username: str, password: str):
        msg = f"cadastro-{username}-{password}"
        server_msg = self.send_to_server(msg)
                  
        if server_msg.decode('utf8') == "Success":
            return 0
        else:
            return 1


    def send_to_server(self, msg: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("0.0.0.0", 4242))
            self.current_message = "..."
            s.sendall(msg.encode("utf8"))
            return s.recv(1024)

