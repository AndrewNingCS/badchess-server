import random

from board import Board

BEGINNER = 0
INTERMEDIATE = 1
HARD = 2

class AI():
    def __init__(self, level):
        self.level = min(max(level, BEGINNER), HARD)

    @classmethod
    def beginner(cls):
        return cls(BEGINNER)

    @classmethod
    def intermediate(cls):
        return cls(INTERMEDIATE)

    @classmethod
    def hard(cls):
        return cls(HARD)

    def make_move(self, board):
        if self.level == BEGINNER:
            return self.beginner_move(board)
        if self.level == INTERMEDIATE:
            return self.intermediate_move(board)
        if self.level == HARD:
            return self.hard_move(board)

    # Beginner level: Returns a move that will eat another piece.
    # if no such move exists, will return a random move
    def beginner_move(self, board):
        all_moves = []

        # get all moves
        for row in board:
            for piece in row:
                if piece is not None and not piece.is_white:
                    all_moves += piece.possible_moves(board)

        # keep the moves that can kill something
        kill_moves = [m for m in all_moves if m.eating_move]

        # if there is at least one such move, return a random one
        if kill_moves:
            return random.choice(kill_moves)

        # no kill moves, return random move
        return random.choice(all_moves)

    def intermediate_move(self, board):
        pass

    def hard_move(self, board):
        pass


        