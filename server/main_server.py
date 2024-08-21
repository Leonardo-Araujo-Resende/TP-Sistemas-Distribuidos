from sys import argv
import sqlite3
import time
from Controller.ControllerLoginCadastrar import *
import Pyro5.api

def main():
    bd_conn = sqlite3.connect('corrida_maluca.db')
    c = bd_conn.cursor()

    c.execute("SELECT * FROM card_list")
    cards = c.fetchall()

    cards_dict = {}
    for card in cards:
        card_name = card[0]
        cards_dict[card_name] = {
            "gimmick": card[1],
            "speed": card[2],
            "accel": card[3],
            "weight": card[4],
            "capacity": card[5],
            "resistance": card[6]
        }


    bd_conn.commit()
    bd_conn.close()    

    # server = Server(cards_dict)
    # server.listen()



    daemon = Pyro5.api.Daemon(host="0.0.0.0", port=9090)
    uri = daemon.register(ControllerLoginCadastrar, objectId="controler-log-cad")
    print("Registrou no daemon: ", uri, flush= True)
    # ns = Pyro5.api.locate_ns()
    # print("Criou o ns", flush= True)
    # ns.register("server.log_cad", uri)
    # registrations = ns.list()

    # for name, uri in registrations.items():
    #     print(f"{name}: {uri}",flush = True)
    daemon.requestLoop()
        
if __name__ == "__main__":
    main(*argv[1:])
