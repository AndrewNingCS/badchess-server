from log import log

class Coord():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def from_array(cls, arr):
        return cls(arr[0], arr[1])

    def up(self):
        return Coord(self.x, self.y-1)

    def down(self):
        return Coord(self.x, self.y+1)

    def left(self):
        return Coord(self.x-1, self.y)

    def right(self):
        return Coord(self.x+1, self.y)

    def in_grid(self, width, height):
        if self.x >= 0 and self.x < width and self.y >= 0 and self.y < height:
            return True
        return False

    def log(self):
        log(self.to_string())

    def to_string(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, p):
        if p is None:
            return False
        return self.x == p.x and self.y == p.y

    def __ne__(self, p):
        return not self.__eq__(p)


class Move():
    def __init__(self, f, t, ate=None):
        self.f = f
        self.t = t
        self.eating_move = ate is not None
        self.eating_piece = ate
        self.is_castle = False # is this move castling?

    def set_eating_piece(self, p):
        self.eating_move = p is not None
        self.eating_piece = p

    def log(self):
        print(f"{self.f.to_string()} to {self.t.to_string()}")

    def __eq__(self, m):
        if m is None:
            return False
        return self.f == m.f and self.t == m.t

    def __ne__(self, m):
        return not self.__eq__(m)

    