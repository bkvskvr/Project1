from random import randint
from Player import Player

class Bot(Player):

    def __init__(self, name, board, enemy_board):
        super().__init__(name, board, enemy_board)
        self.shoted = set()
        self.possible_opt = set()

    def get_move(self):
        # 1. Добиваємо кораблі
        while self.possible_opt:
            move = self.possible_opt.pop() # pop() без індексу для множини
            if move not in self.shoted:
                self.shoted.add(move)
                return move

        # 2. Якщо немає цілей, стріляємо випадково
        while True:
            row = randint(0, 9)
            col = randint(0, 9)
            if (row, col) not in self.shoted:
                self.shoted.add((row, col))
                return (row, col)

    def register_hit(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d_row, d_col in directions:
            n_row, n_col = row + d_row, col + d_col
            if 0 <= n_row < 10 and 0 <= n_col < 10:
                if (n_row, n_col) not in self.shoted:
                    self.possible_opt.add((n_row, n_col))

    def make_turn(self, player_board, destroyed_ships):
        bot_hit_flag = False

        while True:
            b_row, b_col = self.get_move()
            b_res = self.make_shot(b_col, b_row)

            if b_res:
                self.register_hit(b_row, b_col)
                bot_hit_flag = True

                for ship in player_board.ships:
                    if (b_col, b_row) in ship.coordinates:
                        ship.hit()

                        if ship.defeated():
                            player_board.mark_destroyed_perimeter(ship, bot_brain=self)
                            destroyed_ships.append(list(ship.coordinates))
                        break
            else:
                break

        return " Бот влучив у твій корабель! Твій хід." if bot_hit_flag else " Бот промахнувся. Твій хід."