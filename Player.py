import random
from Ship import Ship

class Player:
    def __init__(self, name, board, enemy_board):
        self.name = name
        self.board = board
        self.enemy_board = enemy_board