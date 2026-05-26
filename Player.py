class Player:
    def __init__(self, name, board, enemy_board):
        self.name = name
        self.board = board
        self.enemy_board = enemy_board

    def make_shot(self, x, y):
        return self.enemy_board.shot(x, y)

    def is_defeated(self):
        if not self.board.ships:
            return False
        return all(ship.defeated() for ship in self.board.ships)