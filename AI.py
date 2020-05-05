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

    # Beginner level: Returns a random move from all possible moves
    def beginner_move(self, board):
        board.set_occupied_grid()
        all_moves = []
        for p in board.black_pieces:
            all_moves += p.possible_moves(board.occupied)

        return random.choice(all_moves)

    def intermediate_move(self, board):
        pass

    def hard_move(self, board):
        pass


        