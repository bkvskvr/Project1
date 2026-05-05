import random
from Player import Player
from Ship import Ship

class Bot(player):

    def __init__(self, name, board):
        super().__init__(name, board)
        self.shoted = set() # це множина, куди бот записує клітинки(координати), в які вже стріляв
        self.possible_opt = [] # список для того, аби записувати сусідні клітинки для тих, куди стріляли і там був корабель

    def get_move(self):
        x, y = self.possible_opt.pop(0)
        while (x, y) in self.shoted and self.possible_opt:
            x, y = self.possible_opt.pop(0)
