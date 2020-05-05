from utility import Coord, Move
from log import log

E = 0 # empty
W = 1 # white
B = 2 # black

class Piece():
    def __init__(self, pos, is_white):
        self.pos = pos
        self.x = pos.x
        self.y = pos.y
        self.is_white = is_white

    def update_pos(self, pos):
        self.pos = pos
        self.x = pos.x
        self.y = pos.y

    def possible_moves(self, occupied):
        # return all moves
        ret = []
        for x in range(len(occupied[0])):
            for y in range(len(occupied)):
                ret.append(Move(Coord(self.x, self.y), Coord(x, y)))
        return ret

    def possible_straight_moves(self, occupied):
        w = len(occupied[0])
        h = len(occupied)
        moves = []

        your_team = B
        enemy = W
        if self.is_white:
            your_team = W
            enemy = B

        # go in all 4 directions until you hit the wall, enemy, or your own team
        # left
        cur = self.pos.left()
        while cur.in_grid(w, h):
            if occupied[cur.y][cur.x] == enemy:
                moves.append(Move(self.pos, cur))
                break
            if occupied[cur.y][cur.x] == your_team:
                break
            moves.append(Move(self.pos, cur))
            cur = cur.left()

        # right
        cur = self.pos.right()
        while cur.in_grid(w, h):
            if occupied[cur.y][cur.x] == enemy:
                moves.append(Move(self.pos, cur))
                break
            if occupied[cur.y][cur.x] == your_team:
                break
            moves.append(Move(self.pos, cur))
            cur = cur.right()

        # up
        cur = self.pos.up()
        while cur.in_grid(w, h):
            if occupied[cur.y][cur.x] == enemy:
                moves.append(Move(self.pos, cur))
                break
            if occupied[cur.y][cur.x] == your_team:
                break
            moves.append(Move(self.pos, cur))
            cur = cur.up()

        # down
        cur = self.pos.down()
        while cur.in_grid(w, h):
            if occupied[cur.y][cur.x] == enemy:
                moves.append(Move(self.pos, cur))
                break
            if occupied[cur.y][cur.x] == your_team:
                break
            moves.append(Move(self.pos, cur))
            cur = cur.down()

        return moves

    def possible_diagonal_moves(self, occupied):
        w = len(occupied[0])
        h = len(occupied)
        moves = []

        your_team = B
        enemy = W
        if self.is_white:
            your_team = W
            enemy = B

        # go in all 4 diagonals until you hit the wall, enemy, or your own team
        # left up diagonal
        cur = self.pos.left().up()
        while cur.in_grid(w, h):
            if occupied[cur.y][cur.x] == enemy:
                moves.append(Move(self.pos, cur))
                break
            if occupied[cur.y][cur.x] == your_team:
                break
            moves.append(Move(self.pos, cur))
            cur = cur.left().up()

        # left down diagonal
        cur = self.pos.left().down()
        while cur.in_grid(w, h):
            if occupied[cur.y][cur.x] == enemy:
                moves.append(Move(self.pos, cur))
                break
            if occupied[cur.y][cur.x] == your_team:
                break
            moves.append(Move(self.pos, cur))
            cur = cur.left().down()

        # right up diagonal
        cur = self.pos.right().up()
        while cur.in_grid(w, h):
            if occupied[cur.y][cur.x] == enemy:
                moves.append(Move(self.pos, cur))
                break
            if occupied[cur.y][cur.x] == your_team:
                break
            moves.append(Move(self.pos, cur))
            cur = cur.right().up()

        # right down diagonal
        cur = self.pos.right().down()
        while cur.in_grid(w, h):
            if occupied[cur.y][cur.x] == enemy:
                moves.append(Move(self.pos, cur))
                break
            if occupied[cur.y][cur.x] == your_team:
                break
            moves.append(Move(self.pos, cur))
            cur = cur.right().down()

        return moves

    def to_JSON(self):
        return [self.piece, self.is_white]


class Pawn(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "Pawn"
        self.initial_pos = pos

    def possible_moves(self, occupied):
        w = len(occupied[0])
        h = len(occupied)
        moves = []
        
        if self.is_white:
            up_one = self.pos.up()
            up_two = up_one.up()
            diag_left = up_one.left()
            diag_right = up_one.right()

            if up_one.in_grid(w, h) and occupied[up_one.y][up_one.x] == E:
                moves.append(Move(self.pos, up_one))
                if self.pos == self.initial_pos:
                    if up_two.in_grid(w, h) and occupied[up_two.y][up_two.x] == E:
                        moves.append(Move(self.pos, up_two))
            if diag_left.in_grid(w, h) and occupied[diag_left.y][diag_left.x] == B:
                moves.append(Move(self.pos, diag_left))
            if diag_right.in_grid(w, h) and occupied[diag_right.y][diag_right.x] == B:
                moves.append(Move(self.pos, diag_right))
        else:
            down_one = self.pos.down()
            down_two = down_one.down()
            diag_left = down_one.left()
            diag_right = down_one.right()

            if down_one.in_grid(w, h) and occupied[down_one.y][down_one.x] == E:
                moves.append(Move(self.pos, down_one))
            if down_two.in_grid(w, h) and occupied[down_two.y][down_two.x] == E:
                moves.append(Move(self.pos, down_two))
            if diag_left.in_grid(w, h) and occupied[diag_left.y][diag_left.x] == W:
                moves.append(Move(self.pos, diag_left))
            if diag_right.in_grid(w, h) and occupied[diag_right.y][diag_right.x] == W:
                moves.append(Move(self.pos, diag_right)) 

        return moves
        

    def log(self):
        log(f"{self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["P", self.is_white]


class Rook(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "Rook"

    def possible_moves(self, occupied):
        return super().possible_straight_moves(occupied)

    def log(self):
        log(f"{self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["R", self.is_white]


class Horse(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "Horse"

    def possible_moves(self, occupied):
        w = len(occupied[0])
        h = len(occupied)
        moves = []

        enemy = W
        if self.is_white:
            enemy = B

        possible = [
            self.pos.left().left().up(),
            self.pos.left().left().down(),
            self.pos.right().right().up(),
            self.pos.right().right().down(),
            self.pos.up().up().left(),
            self.pos.up().up().right(),
            self.pos.down().down().left(),
            self.pos.down().down().right()
        ]

        for m in possible:
            if m.in_grid(w, h):
                if occupied[m.y][m.x] == enemy or occupied[m.y][m.x] == E:
                    moves.append(Move(self.pos, m))

        return moves


    def log(self):
        log(f"{self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["H", self.is_white]


class Bishop(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "Bishop"

    def possible_moves(self, occupied):
        return super().possible_diagonal_moves(occupied)

    def log(self):
        log(f"{self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["B", self.is_white]


class Queen(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "Queen"

    def possible_moves(self, occupied):
        diag_moves = super().possible_diagonal_moves(occupied)
        straight_moves = super().possible_straight_moves(occupied)
        return diag_moves + straight_moves
    
    def log(self):
        log(f"{self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["Q", self.is_white]


class King(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "King"

    def possible_moves(self, occupied):
        w = len(occupied[0])
        h = len(occupied)
        moves = []

        enemy = W
        if self.is_white:
            enemy = B

        # king can move to any adjacent sq (even diags)
        # TODO: Castling with the Rook
        possible = [
            self.pos.left(),
            self.pos.right(),
            self.pos.up(),
            self.pos.down(),
            self.pos.left().up(),
            self.pos.left().down(),
            self.pos.right().up(),
            self.pos.right().down()
        ]

        for m in possible:
            if m.in_grid(w, h):
                valid_dest = occupied[m.y][m.x] == enemy or occupied[m.y][m.x] == E
                if valid_dest:
                    moves.append(Move(self.pos, m))

        return moves

    def log(self):
        log(f"{self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["K", self.is_white]

