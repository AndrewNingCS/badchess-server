from threading import Condition

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
        self.turn = 1
        self.room_code = 'TEST' # TODO: Generate a random code each time
        self.player1_id = 'PLAYER1' # TODO: change these to something more random
        self.player2_id = 'PLAYER2'
        self.setup = False
        self.player1_connected = False
        self.player2_connected = False
        self.started = False
        self.lock = Condition()

    # Sets up the two player game. Returns a json with the necessary info
    def create_two_player_game(self):
        self.setup = True

        return self.room_JSON(1)

    # Returns a json object with game ID and player 2 ID
    # This assumes the game is already created by player 1
    # (that is, setup_two_player_game has been called)
    def join_two_player_game(self):
        return self.room_JSON(2)

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

        # Returns with AI move, so still player 1's turn
        self.turn = 1

    def room_JSON(self, player):
        ret = {}
        ret["game_id"] = self.game_id
        if player == 1:
            ret["player_id"] = self.player1_id
        else:
            ret["player_id"] = self.player2_id
        ret["room_code"] = self.room_code

        return ret

    def to_JSON(self):
        json = {}
        json["game_started"] = self.started
        if not self.started: # if game has not started, return
            return json
        json["game_id"] = self.game_id
        json["invalid_move"] = self.invalid_move
        json["player_turn"] = self.turn
        json["board"] = self.board.to_JSON()
        json["possible_moves"] = self.board.possible_moves_JSON()
        json["dead_pieces"] = self.board.dead_pieces_JSON()

        return json

    def make_move(self, player_id, f, t):
        # check player_id parameters
        self.lock.acquire()
        player_number = 0
        if player_id == self.player1_id:
            player_number = 1
        else:
            player_number = 2
        while self.turn != player_number:
            self.lock.wait()
        move = Move(Coord.from_array(f), Coord.from_array(t))
        self.board.make_move(player_number, move)
        self.turn = self.turn%2 + 1
        self.lock.notify()
        self.lock.release()
    
    def wait_for_move(self, player_id):
        self.lock.acquire()
        player_number = 0
        if player_id == self.player1_id:
            player_number = 1
        else:
            player_number = 2
        while self.turn != player_number:
            self.lock.wait()
        self.lock.release()
