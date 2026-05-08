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
            0: "🌊",
            1: "🚢",
            2: "⚪",
            3: "💥"
        }

        for i, row in enumerate(self.field):
            row_num = str(i)
            row_str = f"{row_num} "
            for cell in row:
                row_str += symbols[cell] + " "
            print(row_str)

    def add_ship(self, ship): #перевірка, додавання кораблів
        if not self.placement(ship):
            return False
        self.ships.append(ship)

        for x, y in ship.coordinates:
            self.field[y][x] = 1

        return True


    def placement(self, ship):
        for x, y in ship.coordinates:
            if x < 0 or x >= 10 or y < 0 or y >= 10: #
                return False

            for dy in [-1, 0, 1]: #
                for dx in [-1, 0, 1]:
                    check_x = x + dx
                    check_y = y + dy

                    if 0 <= check_x < 10 and 0 <= check_y < 10: #
                        if self.field[check_y][check_x] == 1: #
                            return False
        return True


    def shot(self, x, y): # вистріл опонента
        try:
            if x < 0 or x >= 10 or y < 0 or y >= 10:  # Перевіряємо чи постріл в межах поля, якщо ні, то викликаємо власну помилку
                raise ShotIndexError()

            if self.field[y][x] == 1:  # якщо там корабель - 1, то замінюємо на влучено
                self.field[y][x] = 3
                return True  # Опонент попав отже має додатковий хід
            elif self.field[y][x] == 0:
                self.field[y][x] = 2
                return False
            elif self.field[y][x] == 2 or self.field[y][x] == 3:
                return None
        except ShotIndexError:
            return None

    def auto_place_ships(self):
        # Стандартний набір кораблів: один на 4, два на 3, три на 2, чотири на 1
        ship_lengths = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

        for length in ship_lengths:
            placed = False
            while not placed:
                # Випадково обираємо орієнтацію: 'h' - горизонтальна, 'v' - вертикальна
                orientation = random.choice(['h', 'v'])
                # Випадкові координати початку корабля
                x = random.randint(0, 9)
                y = random.randint(0, 9)

                # Створюємо тимчасовий об'єкт корабля
                new_ship = Ship(length, orientation)
                new_ship.set_coordinate(x, y) # Генеруємо його координати

                # Намагаємося додати його на поле
                # add_ship сам перевірить, чи не виходить він за межі і чи не стоїть поруч з іншими
                if self.add_ship(new_ship):
                    placed = True