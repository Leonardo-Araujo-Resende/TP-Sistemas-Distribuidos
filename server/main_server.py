from sys import argv
from network.server import Server

def main():
    server = Server()     
    server.listen()
        
if __name__ == "__main__":
    main(*argv[1:])
