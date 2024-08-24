import sqlite3
import random
import Pyro5.api

@Pyro5.api.expose
class ControllerSaveDeck(object):
           
    def save_deck_on_db(self, username, deck, deck_index):
        bd_conn = sqlite3.connect('corrida_maluca.db')
        c = bd_conn.cursor()

        c.execute("""DELETE FROM decks WHERE username = ? AND deck_id = ?""", (username, deck_index))

        for card in deck:
            c.execute("""INSERT INTO decks (username, deck_id, card_filename) VALUES (?, ?, ?)""", (username, deck_index, str(card))) 

        bd_conn.commit()
        bd_conn.close()  
    
    def search_deck_on_db(self, username, deck_index):
        bd_conn = sqlite3.connect('corrida_maluca.db')
        c = bd_conn.cursor()

        c.execute("""SELECT card_filename FROM decks WHERE username = ? AND deck_id = ?""", (username, deck_index))
        
        cards = c.fetchall()
        
        bd_conn.close()

        deck = [int(card[0]) for card in cards]

        return deck

