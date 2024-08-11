from sys import argv
import socket
import json

class Client():
    
    def __init__(self):
        self.username = ""
        self.socket = None


    def send_msg(self, msg):
        msg_json = json.dumps(msg)
        server_msg = self.send_to_server(msg_json)
        return server_msg.decode('utf8')


    def send_to_server(self, msg):
        if self.socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(("0.0.0.0", 4242))
        
        self.socket.sendall(bytes(msg, encoding= "utf-8"))
        return self.socket.recv(1024)

    def listen_for_server_msg(self):
        # if self.socket is None:
        #     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     self.socket.connect(("0.0.0.0", 4242))
        return self.socket.recv(1024).decode('utf8')

