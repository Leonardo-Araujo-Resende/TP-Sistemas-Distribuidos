import sqlite3

class ControllerLoginCadastrar():
    def __init__(self):
        self.username = ""
           
    def sign_up_bd(self, username, password):
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
                    

    def sign_in_bd(self, username, password):
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

