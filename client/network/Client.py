from sys import argv
import socket
import json

class Client():
    
    def __init__(self):
        self.username = ""


    def send_msg(self, msg):
        msg_json = json.dumps(msg)
        server_msg = self.send_to_server(msg_json)
        return server_msg.decode('utf8')


    def send_to_server(self, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("0.0.0.0", 4242))
            self.current_message = "..."
            s.sendall(bytes(msg, encoding= "utf-8"))
            return s.recv(1024)

