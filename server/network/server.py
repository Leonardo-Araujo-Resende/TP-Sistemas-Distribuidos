import socket
import json
import threading
import sqlite3
from Controller.ControllerLoginCadastrar import *

class Server():
    def __init__(self,):
        self.server = ""
        self.controller_log_cad = ControllerLoginCadastrar()
        

    def verify_identifier(self, conn: socket.socket):
        with conn:
            # Recebe a mensagem
            msg = conn.recv(1024)
            # Converte a mensagem para dicionário
            msg_dict = json.loads(msg.decode("utf8"))
            
            #editar para aceitar outras mensagens alem de logar e cadastrar
            identifier = msg_dict['op']
            if identifier == "login":
                username, password = msg_dict['username'], msg_dict['password']
                if self.controller_log_cad.sign_in_bd(username, password) == 0:
                    conn.sendall(f"Success".encode("utf8"))
                else:
                    conn.sendall(f"Failed".encode("utf8"))
            # elif identifier == "SaveDeck":
                #implementar salvamento de deck no banco
            else:
                username, password = msg_dict['username'], msg_dict['password']
                if self.controller_log_cad.sign_up_bd(username, password) == 0:
                    conn.sendall(f"Success".encode("utf8"))
                else:
                    conn.sendall(f"Failed".encode("utf8"))

    def listen(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", 4242))
            s.listen()
            while True:
                conn, addr = s.accept()
                print(f"Connected with {addr}")
                thread = threading.Thread(target=self.verify_identifier, args=(conn,))
                thread.start()
