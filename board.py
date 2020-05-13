from pieces import *
from utility import Coord

class Board():
    def __init__(self):
        # starting new game when init is called
        self.create_standard_board()

        self.white_dead = []
        self.black_dead = []

    def create_standard_board(self):
        self.width = 8
        self.height = 8
        self.board = [
        [
            Rook(Coord(0, 0), False),
            Horse(Coord(1, 0), False),
            Bishop(Coord(2, 0), False),
            Queen(Coord(3, 0), False),
            King(Coord(4, 0), False),
            Bishop(Coord(5, 0), False),
            Horse(Coord(6, 0), False),
            Rook(Coord(7, 0), False)
        ],
        [
            Pawn(Coord(0, 1), False),
            Pawn(Coord(1, 1), False),
            Pawn(Coord(2, 1), False),
            Pawn(Coord(3, 1), False),
            Pawn(Coord(4, 1), False),
            Pawn(Coord(5, 1), False),
            Pawn(Coord(6, 1), False),
            Pawn(Coord(7, 1), False)
        ],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [
            Pawn(Coord(0, 6), True),
            Pawn(Coord(1, 6), True),
            Pawn(Coord(2, 6), True),
            Pawn(Coord(3, 6), True),
            Pawn(Coord(4, 6), True),
            Pawn(Coord(5, 6), True),
            Pawn(Coord(6, 6), True),
            Pawn(Coord(7, 6), True)
        ],
        [
            Rook(Coord(0, 7), True),
            Horse(Coord(1, 7), True),
            Bishop(Coord(2, 7), True),
            Queen(Coord(3, 7), True),
            King(Coord(4, 7), True),
            Bishop(Coord(5, 7), True),
            Horse(Coord(6, 7), True),
            Rook(Coord(7, 7), True)
        ]]

    # given a move, return if the move is valid. Will also check if the move
    # is a castle move.
    def validate_move(self, player_number, move):
        piece = self.board[move.f.y][move.f.x]

        # is there a piece there?
        if piece is None:
            return False

        # special case: check if the move is the king rook castling
        if isinstance(piece, King):
            piece.is_castle(self.board, move)

        # does the player and piece colour match up?
        if (piece.is_white and player_number == 2) or (not piece.is_white and player_number == 1):
            return False
        
        # get all possible moves of piece
        moves = piece.possible_moves(self.board)

        if move in moves: # valid move
            return True
        
        return False


    def make_move(self, player, move):
        # assume the move has been validated

        # if the move is the king rook castling, do it first
        if move.is_castle:
            if player == 1:
                h = self.height-1
            else:
                h = 0
            self.board[h][self.width-4] = None # set the old king to none
            self.board[h][self.width-1] = None # set the old rook to none
            new_king = King(Coord(self.width-2, h), player == 1) # create new king
            new_king.has_moved = True
            new_rook = Rook(Coord(self.width-3, h), player == 1) # create new rook
            new_rook.has_moved = True
            self.board[h][self.width-2] = King(Coord(self.width-2, h), player == 1)
            self.board[h][self.width-3] = Rook(Coord(self.width-3, h), player == 1)
            return

        # if a piece is being eaten, add to correct dead pile
        if self.board[move.t.y][move.t.x] is not None:
            if player == 1:
                self.black_dead.append(self.board[move.t.y][move.t.x])
            else:
                self.white_dead.append(self.board[move.t.y][move.t.x])

        # move the piece
        self.board[move.t.y][move.t.x] = self.board[move.f.y][move.f.x]
        self.board[move.f.y][move.f.x] = None

        # update the piece's new position
        self.board[move.t.y][move.t.x].update_pos(move.t)

        # if the piece is a pawn and it hit the other end, it becomes a Queen
        # TODO: Real rules say the player gets to choose the piece it becomes
        if isinstance(self.board[move.t.y][move.t.x], Pawn):
            if player == 1 and move.t.y == 0:
                self.board[move.t.y][move.t.x] = Queen(move.t, True)
            elif player == 2 and move.t.y == self.height - 1:
                self.board[move.t.y][move.t.x] = Queen(move.t, False)

    # Returns true if player one is in checkmate (loses)
    def player_one_in_checkmate(self):
        pass

    # Returns true if player two is in checkmate (loses)
    def player_two_in_checkmate(self):
        pass

    # Returns true if player one is in check (king under attack)
    def player_one_in_check(self):
        
        pass

    # Returns true if player two is in check (king under attack)
    def player_two_in_check(self):
        pass

    def game_over(self):
        for p in self.white_dead:
            if p.name == "King":
                return True
        for p in self.black_dead:
            if p.name == "King":
                return True
        return False

    def possible_moves_JSON(self):
        json = []
        for row in self.board:
            t = []
            for piece in row:
                e = []
                if piece is not None:
                    moves = piece.possible_moves(self.board)
                    for m in moves:
                        e.append([m.t.x, m.t.y])
                t.append(e)
            json.append(t)

        return json

    def dead_pieces_JSON(self):
        json = {
            "white": [p.to_JSON() for p in self.white_dead],
            "black": [p.to_JSON() for p in self.black_dead]
        }

        return json


    def to_JSON(self):
        json = [[p.to_JSON() if p is not None else ["N", False] for p in row] for row in self.board]

        return json
