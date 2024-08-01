"""
O servidor recebe o nome do client e o cumprimenta.
A biblioteca `tqdm` foi usada única e exclusivamente para mostrar
que é possível colocar dependências diferentes no requirements.txt
de cada parte do sistema, ela não cumpre nenhum propósito funcional aqui.

Referências:
- [Biblioteca de sockets](https://docs.python.org/3/library/socket.html)
"""
from random import randint
from sys import argv
import socket
import threading
import sqlite3

#funcao para separar username e senha da mensagem
def extract_fields(msg: str):
    identifier, username, password = msg.split("-")
    return identifier, username, password

def sign_up_bd(username: str, password: str):
            #cria o banco e a tabela de usuarios
            bd_conn = sqlite3.connect('corrida_maluca.db')
            c = bd_conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS users (
                    username TEXT,
                    password TEXT
                    )""")
                  
            #verifica se o usuario eh unico
            c.execute("SELECT * FROM users WHERE username = (?)", (username,))
            users = c.fetchall()
            print(f"Users selected to verify: {users}")

            
            #se forem unicos, insere no banco
            if len(users) == 0:
                c.execute("INSERT INTO users VALUES (?, ?)", (username, password,))
                
                #mostra a insercao  
                c.execute("SELECT * FROM users")
                query = c.fetchall()
                print(f"All users and passwords: {query}")
                bd_conn.commit()
                return 0
                
            else:
                bd_conn.commit()
                return 1
            

def sign_in_bd(username: str, password: str):
            #cria o banco e a tabela de usuarios
            bd_conn = sqlite3.connect('corrida_maluca.db')
            c = bd_conn.cursor()
            
            #verifica se o usuario eh unico
            c.execute("SELECT * FROM users WHERE username = (?) AND password = (?)", (username, password,))
            users = c.fetchall()
            print(f"Users selected to verify: {users}")

            
            #se forem unicos, insere no banco
            if len(users) != 0:
                bd_conn.commit()
                return 0
            else:
                bd_conn.commit()
                return 1


def verify_identifier(conn: socket.socket):
    with conn:
         #recebe a mensagem 
        msg = conn.recv(1024)
        identifier, username, password = extract_fields(msg.decode("utf8"))
        if identifier == "login":
            if sign_in_bd(username, password) == 0:
                conn.sendall(f"Success".encode("utf8"))
            else:
                conn.sendall(f"Failed".encode("utf8"))
        else:
            if sign_up_bd(username, password) == 0:
                conn.sendall(f"Success".encode("utf8"))
            else:
                conn.sendall(f"Failed".encode("utf8"))
            
def main():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 4242))
        s.listen()
        while True:
            conn, addr = s.accept()
            print(f"Connected with {addr}")
            thread_login = threading.Thread(target=verify_identifier, args=(conn,))
            thread_login.start()
        


if __name__ == "__main__":
    main(*argv[1:])
