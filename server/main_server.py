from sys import argv
import sqlite3
import time
from Controller.ControllerLoginCadastrar import *
from Controller.ControllerPartida import *
from Controller.ControllerSaveDeck import *
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



    daemon = Pyro5.api.Daemon()
    uri = daemon.register(ControllerLoginCadastrar, objectId="controler-log-cad")

    ns = Pyro5.api.locate_ns()
    ns.register("server.log_cad", uri)

    uri = daemon.register(ControllerPartida(cards_dict), objectId="controler-partida")

    ns = Pyro5.api.locate_ns()
    ns.register("server.partida", uri)

    uri = daemon.register(ControllerSaveDeck, objectId="controler-save-deck")

    ns = Pyro5.api.locate_ns()
    ns.register("server.deck", uri)

    daemon.requestLoop()
        
if __name__ == "__main__":
    main(*argv[1:])
