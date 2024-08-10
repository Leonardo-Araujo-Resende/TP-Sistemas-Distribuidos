import sqlite3
import random


class ControllerLoginCadastrar():
    def __init__(self):
        self.username = ""
           
    def sign_up_bd(self, username, password):
        bd_conn = sqlite3.connect('corrida_maluca.db')
        c = bd_conn.cursor()
        
        c.execute("SELECT * FROM users WHERE username = (?)", (username,))
        users = c.fetchall()
                
        #se forem unicos, insere no banco
        if len(users) == 0:
            c.execute("INSERT INTO users VALUES (?, ?)", (username, password,))

            #criando e inserindo no banco a colecao de cartas do usuario
            colecao_inicial = random.sample(range(1, 31), 9)
            nomes_cartas = [f"{id}" for id in colecao_inicial]
            for nome_carta in nomes_cartas:
                c.execute("INSERT INTO cards (username, filename) VALUES (?, ?)", (username, nome_carta))
            
            bd_conn.commit()
            bd_conn.close()

            return 0
                
        else:
            bd_conn.commit()
            bd_conn.close()
            return 1
            

    def sign_in_bd(self, username, password):
        #cria o banco e a tabela de usuarios
        bd_conn = sqlite3.connect('corrida_maluca.db')
        c = bd_conn.cursor()
        
        #verifica se o usuario eh unico
        c.execute("SELECT * FROM users WHERE username = (?) AND password = (?)", (username, password,))
        users = c.fetchall()

        bd_conn.commit()
        bd_conn.close()
        
        #se forem unicos, insere no banco
        if len(users) != 0:

            return 0
        else:
        
            return 1

    def return_colection(self, username):

        bd_conn = sqlite3.connect('corrida_maluca.db')
        c = bd_conn.cursor()
        c.execute("SELECT filename FROM cards WHERE username = ?", (username,))
        filenames = c.fetchall()
        filenames = [filename[0] for filename in filenames]

        bd_conn.commit()
        bd_conn.close()
        return filenames
