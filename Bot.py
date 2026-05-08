from random import randint
from Player import Player
from Ship import Ship

class Bot(Player):

    def __init__(self, name, board):
        super().__init__(name, board)
        self.shoted = set() # це множина, куди бот записує клітинки(координати), в які вже стріляв
        self.possible_opt = [] # список для того, аби записувати сусідні клітинки для тих, куди стріляли і там був корабель

    def get_move(self):
        # 1.Якщо є варіанти для добивання корабля (коли не пустий список)
        if self.possible_opt:
            move = self.possible_opt.pop(0)
            while move in self.shoted and self.possible_opt:
                move = self.possible_opt.pop(0)
            if move not in self.shoted:
                self.shoted.add(move)
                return move

        # 2. Постріли випадково
        while True:
            row = random.randint(0, 9)
            col = random.randint(0, 9)
            if (row, col) not in self.shoted:
                self.shoted.add((row, col))
                return (row, col)