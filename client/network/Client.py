from sys import argv
import socket
import json

class Client():
    
    def __init__(self):
        self.username = ""


    def sign_in(self, msg):
        
        msg_json = json.dumps(msg)
        server_msg = self.send_to_server(msg_json)
                  
        if server_msg.decode('utf8') == "Success":
            return 0
        else:
            return 1
    
    def sign_up(self, msg):
        
        msg_json = json.dumps(msg)
        server_msg = self.send_to_server(msg_json)
                  
        if server_msg.decode('utf8') == "Success":
            return 0
        else:
            return 1

    def save_deck(self,msg):
        msg_json = json.dumps(msg)
        server_msg = self.send_to_server(msg_json)
                  
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

