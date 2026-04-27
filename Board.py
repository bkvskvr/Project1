class Board:
    def __init__(self):
        self.field = [[0 for _ in range(10)] for _ in range(10)]

        self.ships = []

    def display(self):
        for row in self.field:
            print(row)

