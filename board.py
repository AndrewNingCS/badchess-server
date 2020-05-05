from pieces import *
from utility import Coord

class Board():
    def __init__(self):
        # starting new game when init is called
        self.white_pieces = [
            Pawn(Coord(0, 6), True),
            Pawn(Coord(1, 6), True),
            Pawn(Coord(2, 6), True),
            Pawn(Coord(3, 6), True),
            Pawn(Coord(4, 6), True),
            Pawn(Coord(5, 6), True),
            Pawn(Coord(6, 6), True),
            Pawn(Coord(7, 6), True),
            Rook(Coord(0, 7), True),
            Horse(Coord(1, 7), True),
            Bishop(Coord(2, 7), True),
            Queen(Coord(3, 7), True),
            King(Coord(4, 7), True),
            Bishop(Coord(5, 7), True),
            Horse(Coord(6, 7), True),
            Rook(Coord(7, 7), True)
        ]
        self.black_pieces = [
            Pawn(Coord(0, 1), False),
            Pawn(Coord(1, 1), False),
            Pawn(Coord(2, 1), False),
            Pawn(Coord(3, 1), False),
            Pawn(Coord(4, 1), False),
            Pawn(Coord(5, 1), False),
            Pawn(Coord(6, 1), False),
            Pawn(Coord(7, 1), False),
            Rook(Coord(0, 0), False),
            Horse(Coord(1, 0), False),
            Bishop(Coord(2, 0), False),
            Queen(Coord(3, 0), False),
            King(Coord(4, 0), False),
            Bishop(Coord(5, 0), False),
            Horse(Coord(6, 0), False),
            Rook(Coord(7, 0), False)
        ]

        self.white_dead = []
        self.black_dead = []

    def compute_occupied(self):
        occupied = [
            [E, E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E, E],
            [E, E, E, E, E, E, E, E]
        ]
        for p in self.white_pieces:
            occupied[p.y][p.x] = W

        for p in self.black_pieces:
            occupied[p.y][p.x] = B

        return occupied

    def set_occupied_grid(self):
        self.occupied = self.compute_occupied()

    # given a 
    def validate_move(self, player, move):
        piece = None
        if player == 1:
            to_check = self.white_pieces
        else:
            to_check = self.black_pieces

        for p in to_check:
            if p.pos == move.f:
                piece = p
                break

        # does the player and piece colour match up?
        if piece is None:
            return False

        # get all possible moves of piece
        moves = piece.possible_moves(self.compute_occupied())

        if move in moves: # valid move
            return True
        
        return False


    def make_move(self, player, move):
        # assume the move has been validated
        # if there is a piece in the to_position, remove it
        if player == 1:
            to_change = self.white_pieces
            to_remove = self.black_pieces
            dead_pile = self.black_dead
        else:
            to_change = self.black_pieces
            to_remove = self.white_pieces
            dead_pile = self.white_dead

        for i, p in enumerate(to_remove):
            if p.pos == move.t:
                dead_pile.append(to_remove.pop(i)) # piece is eaten
                break
        for p in to_change:
            if p.pos == move.f:
                p.update_pos(move.t)
                if p.name == "Pawn":
                    if player == 1 and p.y == 0:
                        p = Queen(p.pos, True)
                    elif player == 2 and p.y == 7:
                        p = Queen(p.pos, False)


    def to_JSON(self):
        json = []
        for y in range(8):
            row = []
            for x in range(8):
                row.append(["N", False])
            json.append(row)

        for p in self.white_pieces + self.black_pieces:
            json[p.y][p.x] = p.to_JSON()

        return json
