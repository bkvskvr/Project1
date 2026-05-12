class Player:
    def __init__(self, name, board, enemy_board):
        self.name = name
        self.board = board
        self.enemy_board = enemy_board

    def make_shot(self, x, y):
        # Гравець робить постріл по дошці противника
        return self.enemy_board.shot(x, y)

    def is_defeated(self):
        # Перевіряємо, чи всі власні кораблі знищені( Якщо кораблів ще немає на полі, то ми ще не програли)
        if len(self.board.ships) == 0:
            return False
        return all(ship.defeated() for ship in self.board.ships)