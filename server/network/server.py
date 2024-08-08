import socket
import json
import threading
import sqlite3
from Controller.ControllerLoginCadastrar import *

class Server():
    def __init__(self,):
        self.server = ""

    def verify_identifier(self, conn: socket.socket, controller):
        with conn:
            # Recebe a mensagem
            msg = conn.recv(1024)
            # Converte a mensagem para dicionário
            msg_dict = json.loads(msg.decode("utf8"))
            identifier, username, password = msg_dict['op'], msg_dict['username'], msg_dict['password']
            if identifier == "login":
                if controller.sign_in_bd(username, password) == 0:
                    conn.sendall(f"Success".encode("utf8"))
                else:
                    conn.sendall(f"Failed".encode("utf8"))
            else:
                if controller.sign_up_bd(username, password) == 0:
                    conn.sendall(f"Success".encode("utf8"))
                else:
                    conn.sendall(f"Failed".encode("utf8"))

    def listen(self):
        controller = ControllerLoginCadastrar()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", 4242))
            s.listen()
            while True:
                conn, addr = s.accept()
                print(f"Connected with {addr}")
                thread_login = threading.Thread(target=self.verify_identifier, args=(conn, controller,))
                thread_login.start()

