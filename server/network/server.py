import socket
import json
import threading
import sqlite3
import logging
from Controller.ControllerLoginCadastrar import *
from Controller.ControllerJogar import *
from Controller.ControllerPartida import *

class Server():
    def __init__(self, all_cards):
        self.server = ""
        self.controller_log_cad = ControllerLoginCadastrar()
        self.controller_jogar = ControllerJogar()
        self.controller_partida = ControllerPartida(all_cards)
        

    def verify_identifier(self, conn: socket.socket):
              
        # Recebe a mensagem
        msg = conn.recv(1024)
        # Converte a mensagem para dicionário
        msg_dict = json.loads(msg.decode("utf8"))
        
        #editar para aceitar outras mensagens alem de logar e cadastrar
        identifier = msg_dict['op']
        
        logging.basicConfig(level=logging.DEBUG)
        logger = logging.getLogger(__name__)

        logger.debug(f"{identifier}")

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
        
        elif identifier == 'define_deck':
            self.controller_jogar.set_user_ready()
            if self.controller_jogar.qt_users_ready == 1:
                self.controller_partida.jogador1 = conn
                self.controller_partida.deck1 = random.sample(msg_dict['deck'], len(msg_dict['deck']))
                conn.sendall(f"{self.controller_jogar.qt_users_ready}".encode("utf8"))
                
                
            elif self.controller_jogar.qt_users_ready == 2:
                self.controller_partida.jogador2 = conn
                self.controller_partida.deck2 = random.sample(msg_dict['deck'], len(msg_dict['deck']))
                conn.sendall(f"{self.controller_jogar.qt_users_ready}".encode("utf8"))
                
            elif self.controller_jogar.qt_users_ready == 3:
                self.controller_partida.jogador3 = conn
                self.controller_partida.deck3 = random.sample(msg_dict['deck'], len(msg_dict['deck']))   
                conn.sendall(f"{self.controller_jogar.qt_users_ready}".encode("utf8"))

                self.controller_jogar.set_game_ready()        

                self.controller_partida.jogador1.sendall("Game Ready".encode("utf8"))
                self.controller_partida.jogador2.sendall("Game Ready".encode("utf8"))
                self.controller_partida.jogador3.sendall("Game Ready".encode("utf8"))

                self.controller_partida.game_start(self.controller_partida.jogador1, self.controller_partida.jogador2, self.controller_partida.jogador3)
                
        
            
           
        



    def listen(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", 4242))
            s.listen()
            while True:
                conn, addr = s.accept()
                print(f"Connected with {addr}")
                thread = threading.Thread(target=self.verify_identifier, args=(conn,))
                thread.start()
        
            
