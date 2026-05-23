import random
from Ship import Ship

class ShotIndexError(Exception):
    pass

class Board:
    def __init__(self):
        self.field = [[0 for _ in range(10)] for _ in range(10)]
        # Якщо 0 - там пусто, 1 - корабель, 2 - не по цілі, 3 - попадання

        self.ships = []

    def display(self):
        symbols = {
            0: "~",
            1: "■",
            2: "*",
            3: "X"
        }

        for i, row in enumerate(self.field):
            row_num = str(i)
            row_str = f"{row_num} "
            for cell in row:
                row_str += symbols[cell] + " "
            print(row_str)

    def add_ship(self, ship):
        if not self.placement(ship):
            return False
        self.ships.append(ship)

        for x, y in ship.coordinates:
            self.field[y][x] = 1

        return True


    def placement(self, ship):
        for x, y in ship.coordinates:
            if x < 0 or x >= 10 or y < 0 or y >= 10:
                return False

            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    check_x = x + dx
                    check_y = y + dy

                    if 0 <= check_x < 10 and 0 <= check_y < 10:
                        if self.field[check_y][check_x] == 1:
                            return False
        return True


    def shot(self, x, y): # вистріл опонента
        try:
            if not (0 <= x < 10 and 0 <= y < 10):
                raise ShotIndexError()

            if self.field[y][x] == 1:
                self.field[y][x] = 3
                return True

            if self.field[y][x] == 0:
                self.field[y][x] = 2
                return False

            return None

        except ShotIndexError:
            return None


    def auto_place_ships(self):
        ship_lengths = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

        for length in ship_lengths:
            while True:
                orientation = random.choice(['h', 'v'])
                x = random.randint(0, 9)
                y = random.randint(0, 9)

                new_ship = Ship(length, orientation)
                new_ship.set_coordinates(x, y)

                if self.add_ship(new_ship):
                    break

    def mark_destroyed_perimeter(self, ship, bot_brain=None):
        for sx, sy in ship.coordinates:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = sx + dx, sy + dy
                    if not (0 <= nx < 10 and 0 <= ny < 10):
                        continue

                    if self.field[ny][nx] != 0:
                        continue

                    self.field[ny][nx] = 2

                    if bot_brain:
                        bot_brain.shoted.add((ny, nx))
                        bot_brain.possible_opt.discard((ny, nx))
