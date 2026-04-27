class Board:
    def __init__(self):
        self.field = [[0 for _ in range(10)] for _ in range(10)]
        # Якщо 0 - там пусто, 1 - корабель, 2 - не по цілі, 3 - попадання

        self.ships = []

    def display(self):
        for row in self.field:
            print(row)

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
        pass
