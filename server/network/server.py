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
            
            if identifier == 'login':
                username, password = msg_dict['username'], msg_dict['password']
                if self.controller_log_cad.sign_in_bd(username, password) == 0:
                    cards = self.controller_log_cad.return_colection(username)
                    msg_rtn = {"op": "colecao", "colecao": cards}
                    msg_json = json.dumps(msg_rtn)
                    conn.sendall(bytes(msg_json, encoding="utf-8"))
                else:
                    conn.sendall(f"Failed".encode("utf8"))

            elif identifier == 'cadastro':
                username, password = msg_dict['username'], msg_dict['password']
                if self.controller_log_cad.sign_up_bd(username, password) == 0:
                    conn.sendall(f"Success".encode("utf8"))
                else:
                    conn.sendall(f"Failed".encode("utf8"))

            elif identifier == 'salvaDeck':
                pass

                
    def listen(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", 4242))
            s.listen()
            while True:
                conn, addr = s.accept()
                print(f"Connected with {addr}")
                thread = threading.Thread(target=self.verify_identifier, args=(conn,))
                thread.start()
