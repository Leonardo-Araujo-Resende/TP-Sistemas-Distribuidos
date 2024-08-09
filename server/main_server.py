from sys import argv
from network.server import Server
import sqlite3

def main():
    server = Server()
    bd_conn = sqlite3.connect('corrida_maluca.db')
    c = bd_conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
                )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                filename TEXT NOT NULL,
                FOREIGN KEY(username) REFERENCES users(username)
                )""")
    
    c.execute("""CREATE TABLE IF NOT EXISTS decks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                deck_id INTEGER NOT NULL,
                card_filename TEXT NOT NULL,
                FOREIGN KEY(username) REFERENCES users(username)
                )""")
    bd_conn.commit()
    bd_conn.close()
    server.listen()
        
if __name__ == "__main__":
    main(*argv[1:])
