class InvalidLengthShipError(Exception):
    pass

shiplength = (1, 2, 3, 4)

class Ship:
    def __init__(self, length, orientation):
        if length not in shiplength:
            raise InvalidLengthShipError (f"Недопустима довжина корабля: {length}")

        self.length = length
        self.orientation = orientation
        self.lives = length
        self.coordinates = []

    def hit(self):
        if self.lives > 0:
            self.lives -= 1

    def defeated(self):
        return self.lives == 0

    def set_coordinates(self, x, y):
        self.coordinates = []
        for i in range(self.length):
            if self.orientation == "h":
                self.coordinates.append((x + i, y))
            elif self.orientation == "v":
                self.coordinates.append((x, y + i))