from pieces import Piece
from board import Board
from utility import Coord, Move
from AI import AI


class Game():
    def __init__(self, gid):
        self.game_id = gid
        self.board = Board()
        self.invalid_move = False
        self.undo = []
        self.redo = []
        # TODO: make an AI class
        self.AI = AI.beginner()

    def single_player_move(self, f, t):
        move = Move(Coord.from_array(f), Coord.from_array(t))

        if not self.board.validate_move(1, move):
            # not valid move. Set invalid move flag
            self.invalid_move = True
            return

        # switch if target is empty spot
        self.board.make_move(1, move)
        self.invalid_move = False

        # AI now makes a move
        AI_move = self.AI.make_move(self.board.board) # TODO: what if nothing is returned
        self.board.make_move(2, AI_move)

    def to_JSON(self):
        json = {}
        json["game_id"] = self.game_id
        json["invalid_move"] = self.invalid_move
        json["board"] = self.board.to_JSON()

        return json
                
