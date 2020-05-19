from utility import Coord, Move
from log import log

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
        # default, should never be called
        return []

    # Returns all moves from current position in all 4 straight directions
    def possible_straight_moves(self, board):
        w = len(board[0])
        h = len(board)
        moves = []

        # go in all 4 directions until you hit the wall, enemy, or your own team
        # go left
        cur = self.pos.left()
        while cur.in_grid(w, h):
            has_piece = board[cur.y][cur.x] is not None
            if has_piece and board[cur.y][cur.x].is_white != self.is_white: # hit enemy piece
                moves.append(Move(self.pos.copy(), cur, board[cur.y][cur.x]))
                break
            if has_piece and board[cur.y][cur.x].is_white == self.is_white: # hit own piece
                break
            moves.append(Move(self.pos.copy(), cur))
            cur = cur.left()

        # go right
        cur = self.pos.right()
        while cur.in_grid(w, h):
            has_piece = board[cur.y][cur.x] is not None
            if has_piece and board[cur.y][cur.x].is_white != self.is_white:
                moves.append(Move(self.pos.copy(), cur, board[cur.y][cur.x]))
                break
            if has_piece and board[cur.y][cur.x].is_white == self.is_white:
                break
            moves.append(Move(self.pos.copy(), cur))
            cur = cur.right()

        # go up
        cur = self.pos.up()
        while cur.in_grid(w, h):
            has_piece = board[cur.y][cur.x] is not None
            if has_piece and board[cur.y][cur.x].is_white != self.is_white:
                moves.append(Move(self.pos.copy(), cur, board[cur.y][cur.x]))
                break
            if has_piece and board[cur.y][cur.x].is_white == self.is_white:
                break
            moves.append(Move(self.pos.copy(), cur))
            cur = cur.up()

        # down
        cur = self.pos.down()
        while cur.in_grid(w, h):
            has_piece = board[cur.y][cur.x] is not None
            if has_piece and board[cur.y][cur.x].is_white != self.is_white:
                moves.append(Move(self.pos.copy(), cur, board[cur.y][cur.x]))
                break
            if has_piece and board[cur.y][cur.x].is_white == self.is_white:
                break
            moves.append(Move(self.pos.copy(), cur))
            cur = cur.down()

        return moves

    # Returns all moves from the current position in all 4 diagonal directions
    def possible_diagonal_moves(self, board):
        w = len(board[0])
        h = len(board)
        moves = []

        # go in all 4 diagonals until you hit the wall, enemy, or your own team
        # left up diagonal
        cur = self.pos.left().up()
        while cur.in_grid(w, h):
            has_piece = board[cur.y][cur.x] is not None
            if has_piece and board[cur.y][cur.x].is_white != self.is_white:
                moves.append(Move(self.pos.copy(), cur, board[cur.y][cur.x]))
                break
            if has_piece and board[cur.y][cur.x].is_white == self.is_white:
                break
            moves.append(Move(self.pos.copy(), cur))
            cur = cur.left().up()

        # left down diagonal
        cur = self.pos.left().down()
        while cur.in_grid(w, h):
            has_piece = board[cur.y][cur.x] is not None
            if has_piece and board[cur.y][cur.x].is_white != self.is_white:
                moves.append(Move(self.pos.copy(), cur, board[cur.y][cur.x]))
                break
            if has_piece and board[cur.y][cur.x].is_white == self.is_white:
                break
            moves.append(Move(self.pos.copy(), cur))
            cur = cur.left().down()

        # right up diagonal
        cur = self.pos.right().up()
        while cur.in_grid(w, h):
            has_piece = board[cur.y][cur.x] is not None
            if has_piece and board[cur.y][cur.x].is_white != self.is_white:
                moves.append(Move(self.pos.copy(), cur, board[cur.y][cur.x]))
                break
            if has_piece and board[cur.y][cur.x].is_white == self.is_white:
                break
            moves.append(Move(self.pos.copy(), cur))
            cur = cur.right().up()

        # right down diagonal
        cur = self.pos.right().down()
        while cur.in_grid(w, h):
            has_piece = board[cur.y][cur.x] is not None
            if has_piece and board[cur.y][cur.x].is_white != self.is_white:
                moves.append(Move(self.pos.copy(), cur, board[cur.y][cur.x]))
                break
            if has_piece and board[cur.y][cur.x].is_white == self.is_white:
                break
            moves.append(Move(self.pos.copy(), cur))
            cur = cur.right().down()

        return moves

    def to_JSON(self):
        return [self.piece, self.is_white]


class Pawn(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "Pawn"
        self.initial_pos = pos

    def possible_moves(self, board):
        w = len(board[0])
        h = len(board)
        moves = []
        
        if self.is_white:
            move_one = self.pos.up()
            move_two = move_one.up()
        else:
            move_one = self.pos.down()
            move_two = move_one.down()
        dl = move_one.left()  # diagonal left
        dr = move_one.right() # diagonal right

        # check if anything is in front of the pawn
        if move_one.in_grid(w, h) and board[move_one.y][move_one.x] is None:
            moves.append(Move(self.pos.copy(), move_one))
            if self.pos == self.initial_pos:
                # if pawn is in inital position, and nothing in front, we check two spaces forward
                if move_two.in_grid(w, h) and board[move_two.y][move_two.x] is None:
                    moves.append(Move(self.pos.copy(), move_two))

        # check the left diagonal. Must be occupied by enemy piece
        if dl.in_grid(w, h) and board[dl.y][dl.x] is not None:
            diag_left_enemy = not board[dl.y][dl.x].is_white == self.is_white
            if diag_left_enemy:
                moves.append(Move(self.pos.copy(), dl, board[dl.y][dl.x]))
        
        # check the right diagonal. Must be occupied by enemy piece
        if dr.in_grid(w, h) and board[dr.y][dr.x] is not None:
            diag_right_enemy = not board[dr.y][dr.x].is_white == self.is_white
            if diag_right_enemy:
                moves.append(Move(self.pos.copy(), dr, board[dr.y][dr.x]))

        return moves
        

    def log(self):
        colour = "White" if self.is_white else "Black"
        log(f"{colour} {self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["P", self.is_white]


class Rook(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "Rook"
        self.has_moved = False

    def update_pos(self, pos):
        super().update_pos(pos)
        self.has_moved = True

    def possible_moves(self, board):
        return super().possible_straight_moves(board)

    def log(self):
        colour = "White" if self.is_white else "Black"
        log(f"{colour} {self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["R", self.is_white]


class Horse(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "Horse"

    def possible_moves(self, board):
        w = len(board[0])
        h = len(board)
        moves = []

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
                if board[m.y][m.x] is None:
                    moves.append(Move(self.pos.copy(), m))
                elif board[m.y][m.x].is_white != self.is_white:
                    moves.append(Move(self.pos.copy(), m, board[m.y][m.x]))

        return moves


    def log(self):
        colour = "White" if self.is_white else "Black"
        log(f"{colour} {self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["H", self.is_white]


class Bishop(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "Bishop"

    def possible_moves(self, occupied):
        return super().possible_diagonal_moves(occupied)

    def log(self):
        colour = "White" if self.is_white else "Black"
        log(f"{colour} {self.name} at {self.pos.to_string()}")

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
        colour = "White" if self.is_white else "Black"
        log(f"{colour} {self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["Q", self.is_white]


class King(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.name = "King"
        self.has_moved = False

    def update_pos(self, pos):
        super().update_pos(pos)
        self.has_moved = True

    def possible_moves(self, board):
        w = len(board[0])
        h = len(board)
        moves = []

        # king can move to any adjacent sq (even diags)
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
                if board[m.y][m.x] is None:
                    moves.append(Move(self.pos.copy(), m))
                elif board[m.y][m.x].is_white != self.is_white:
                    moves.append(Move(self.pos.copy(), m, board[m.y][m.x]))

        # king can also castle
        move_castle = Move(self.pos.copy(), self.pos.right().right())
        if self.is_castle(board, move_castle):
            moves.append(move_castle)

        return moves

    # checks if a given move on a given board is a king rook castling move
    # will set the is_castle flag in move to True
    def is_castle(self, board, move):
        h = len(board)
        w = len(board[0])
        if self.is_white:
            row = h - 1
        else:
            row = 0

        # the king must not have moved previously
        if self.has_moved:
            return False

        # rook must exist in corner position
        rook_exists = board[row][w-1] is not None and isinstance(board[row][w-1], Rook)
        if not rook_exists:
            return False

        # if the move is not to the left of the rook, not a castle move
        if move.t != Coord(w-2, row):
            return False

        # needs to be nothing inbetween the king and rook
        nothing_between = board[row][w-2] is None and board[row][w-3] is None
        if not nothing_between:
            return False

        # the rook must not have moved before either
        rook_moved = board[row][w-1].has_moved
        if rook_moved:
            return False

        move.is_castle = True
        return True

    def log(self):
        colour = "White" if self.is_white else "Black"
        log(f"{colour} {self.name} at {self.pos.to_string()}")

    def to_JSON(self):
        return ["K", self.is_white]

