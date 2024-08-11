from sys import argv
from network.server import Server
import sqlite3

def main():
    server = Server()
    server.listen()
        
if __name__ == "__main__":
    main(*argv[1:])
