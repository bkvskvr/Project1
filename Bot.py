from random import randint
from Player import Player
from Ship import Ship

class Bot(Player):

    def __init__(self, name, board, enemy_board):
        super().__init__(name, board, enemy_board)
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
            row = randint(0, 9)
            col = randint(0, 9)
            if (row, col) not in self.shoted:
                self.shoted.add((row, col))
                return (row, col)

    def register_hit(self, row, col):
    # Цей метод викликається коли бот влучає в клітинку успішно і
    # він додає сусідні клітинки до списку, де можливо буде ще один успішний постріл
        # Напрямки для перевірки: (зміщення_row, зміщення_col)
        # (-1, 0) - вгору, (1, 0) - вниз, (0, -1) - ліворуч, (0, 1) - праворуч
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for d_row, d_col in directions:
            n_row = row + d_row
            n_col = col + d_col

            # Перевіряємо математичні межі поля (від 0 до 9 включно)
            if 0 <= n_row < 10 and 0 <= n_col < 10:
                # Додаємо лише ті координати, куди ще не стріляли
                # і яких ще немає в черзі possible_opt
                if (n_row, n_col) not in self.shoted and (n_row, n_col) not in self.possible_opt:
                    self.possible_opt.append((n_row, n_col))