import pandas as pd
import numpy as np

class Cliente:
    def __init__(self):
        # Como a tabela usa x e y pertencentes ao conjunto dos inteiros e o tabuleiro usa x inteiro e
        # y char, a variável y_map é um dicionário onde uma letra tem um inteiro atrelado a ela. e.g. y_map['a'] = 0 
        FEATURE_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.y_map = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9}
        self.y_map_reverse = dict([[v,k] for k,v in self.y_map.items()])
        self.client_table = pd.read_table("table_cliente.txt", delim_whitespace = True, names = (FEATURE_LIST))
        self.client_shot_table = pd.DataFrame(0, index = np.arange(len(self.client_table)), columns = FEATURE_LIST)
        self.TABLE_DIMM = 10


    # Apresenta o tabuleiro com seus navios
    def print_your_table(self):
        print("Your table:")
        print(self.client_table)

    
    # Apresenta o tabuleiro dos seus disparos
    def print_shot_table(self):
        print("Shots table:\n"
               "H: hit \n"
               "M: miss")
        print(self.client_shot_table)

    
    def print_tables(self):
        self.print_shot_table()
        self.print_your_table()
    

    def hit(self, x, y):
        print("Target hit")
        self.client_shot_table.iloc[self.y_map[x], y] = 'H'

    
    def miss(self, x, y):
        print("Target missed")
        self.client_shot_table.iloc[self.y_map[x], y] = 'M'
        

    # Verifica se o disparo levado acertou ou errou
    def check_hit_taken(self, x, y):
        if(self.client_table.iloc[self.y_map[x], y] == 1):
            print("We've been hit")
            self.client_table.iloc[self.y_map[x], y] = 'H'
            return True
        else:
            print("They missed")
            return False
    

    # Verifica se ainda há barcos no tabuleiro
    def check_for_boats(self):
        return sum((self.client_table == 1).sum()) > 0

    
    # Faz algumas validações para saber se o input dado pelo cliente é valido
    def check_valid_play(self, std_in):
        if(len(std_in) > 2):
            print("Too many values. Please type only the x and y coordinates or p for the table")
            return False
        elif(len(std_in) == 1):
            if(std_in[0] != 'p' and std_in[0] != 'P'):
                print("This is not a valid input")
                return False
            else:
                return True
        elif(len(std_in) == 2):
            try:
                if(int(self.y_map[std_in[0]]) >= self.TABLE_DIMM or int(std_in[1]) >= self.TABLE_DIMM):
                    print("Invalid input. Coordinates must be between a ... j and 0 ... 9")
                    return False
                else:
                    return True
            except:
                print("Invalid input. Coordinates must be between a ... j and 0 ... 9")
                return False
        else:
            return True