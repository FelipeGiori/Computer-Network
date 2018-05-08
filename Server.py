import pandas as pd
import numpy as np
import random

class Servidor:
    def __init__(self):
        # Como a tabela usa x e y pertencentes ao conjunto dos inteiros e o tabuleiro usa x inteiro e
        # y char, a variável y_map é um dicionário onde uma letra tem um inteiro atrelado a ela. e.g. y_map['a'] = 0 
        FEATURE_LIST = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.y_map = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7, 'i':8, 'j':9}
        self.y_map_reverse = dict([[v,k] for k,v in self.y_map.items()])
        self.server_table = pd.read_table("server_table.txt", delim_whitespace = True, names = (FEATURE_LIST))
        self.server_shot_table = pd.DataFrame(0, index = np.arange(len(self.server_table)), columns = FEATURE_LIST)
        self.x, self.y = 0, 0
        self.hit_status = False


    # Gera um novo ataque
    def get_attack(self):
        # Verifica se acertou na rodada passada
        # Caso positivo procura uma posição adjascente disponível
        # Caso negativo gera uma posição aleatória
        if(self.hit_status):
            if(self.x < 9 and self.check_valid_attack(self.x + 1, self.y)):
                self.x, self.y = self.x + 1, self.y
                return self.y_map_reverse[self.x], self.y
            elif(self.x > 0 and self.check_valid_attack(self.x - 1, self.y)):
                self.x, self.y = self.x - 1, self.y
                return self.y_map_reverse[self.x], self.y
            elif(self.y < 9 and self.check_valid_attack(self.x, self.y + 1)):
                self.x, self.y = self.x, self.y + 1
                return self.y_map_reverse[self.x], self.y
            elif(self.y > 0 and self.check_valid_attack(self.x, self.y - 1)):
                self.x, self.y = self.x, self.y - 1
                return self.y_map_reverse[self.x], self.y
            else:
                self.x, self.y = self.random_attack()
                return self.y_map_reverse[self.x], self.y
        else:
            self.x, self.y = self.random_attack()
            return self.y_map_reverse[self.x], self.y
    

    # Seleciona uma posição aleatória onde ainda não foi feito um disparo
    # O método where da biblioteca numpy faz a busca por essas posições.
    def random_attack(self):
        valid_pos = np.where(self.server_shot_table == 0)
        n = random.randint(0, len(valid_pos[0]) - 1)
        return valid_pos[0][n], valid_pos[1][n]


    # Verifica se já foi feito um disparo nas coord x e y
    def check_valid_attack(self, x, y):
        return self.server_shot_table.iloc[x, y] == 0

    
    def hit(self, x, y):
        print("Target hit")
        self.server_shot_table.iloc[self.y_map[x], y] = 'H'
        self.hit_status = True

    
    def miss(self, x, y):
        print("Target missed")
        self.server_shot_table.iloc[self.y_map[x], y] = 'M'
        self.hit_status = False
        

    # Verifica se o disparo levado acertou ou errou
    def check_hit_taken(self, x, y):
        if(self.server_table.iloc[self.y_map[x], y] == 1):
            print("We've been hit")
            self.server_table.iloc[self.y_map[x], y] = 'H'
            return True
        else:
            print("They missed")
            return False

    
    # Verifica se ainda há algum barco no tabuleiro
    def check_for_boats(self):
        return sum((self.server_table == 1).sum()) > 0