from threading import Condition
from random import choice
from json import dumps

from pieces import Piece
from board import Board
from utility import Coord, Move
from AI import AI
from log import log


class Game():
    def __init__(self, gid, room_code):
        self.game_id = gid
        self.room_code = room_code
        self.board = Board()
        self.invalid_move = False
        self.undo = []
        self.redo = []
        self.AI = AI.beginner()
        self.turn = 1
        self.setup = False
        self.started = False
        self.stopped = False
        self.lock = Condition()
        self.player1_connected = False
        self.player2_connected = False
        self.game_over = False
        self.winner = 0

        self.player_ids = [] # used so that players do not have the same IDs
        self.player1_id = self.create_player_id()
        self.player2_id = self.create_player_id()

    def get_player_number_from_id(self, id):
        if id == self.player1_id:
            return 1
        elif id == self.player2_id:
            return 2
        log("Player Number Error")

    # Sets up the two player game. Returns a json with the necessary info
    def create_two_player_game(self):
        self.setup = True
        self.player1_connected = True

        return self.room_JSON(1)

    # Returns a json object with game ID and player 2 ID
    # This assumes the game is already created by player 1
    # (that is, setup_two_player_game has been called)
    def join_two_player_game(self):
        self.player2_connected = True
        return self.room_JSON(2)

    # Starts the game
    def start_two_player_game(self, player_id):
        # TODO: should only player 1 be able to start?
        self.started = True

    # returns a JOINED JSON object
    def has_player_joined(self, player_id):
        if player_id == self.player1_id:
            has_joined = self.player2_connected
        else:
            has_joined = self.player1_connected
        return {
            "joined": has_joined
        }

    # Disconnects a player given by the ID. 
    def disconnect(self, player_id):
        if player_id == self.player1_id:
            log("Disconnecting Player 1")
            self.player1_connected = False
            with self.lock:
                self.lock.notifyAll()
        elif player_id == self.player2_id:
            log("Disconnecting Player 2")
            self.player2_connected = False
            with self.lock:
                self.lock.notifyAll()
        else:
            log("Disconnect Error: Player ID not found")

    def any_connected(self):
        return self.player1_connected or self.player2_connected

    def stop(self):
        self.stopped = True
        log(f"Stopping game with GID: {self.game_id}")
        with self.lock:
            self.lock.notifyAll()

    # Starts the game in single player mode
    def start_single_player_game(self):
        self.started = True

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

    def make_move(self, player_id, f, t):
        # check player_id parameters
        self.lock.acquire()
        player_number = self.get_player_number_from_id(player_id)
        while self.turn != player_number:
            self.lock.wait()
            if self.stopped:
                break
        move = Move(Coord.from_array(f), Coord.from_array(t))
        if self.board.validate_move(player_number, move):
            self.board.make_move(player_number, move)
            if self.board.game_over():
                self.game_over = True
                self.winner = self.turn
            self.turn = self.turn%2 + 1
        self.lock.notify()
        self.lock.release()
    
    # generator function
    def wait_for_move(self, player_id):
        self.lock.acquire()
        player_number = self.get_player_number_from_id(player_id)
        while self.turn != player_number:
            yield 'data: ' + dumps(self.to_JSON()) + '\n\n'
            self.lock.wait(timeout=25)
            if self.stopped:
                log(f"Game ended, stopping wait for move from player: {player_number}")
                break
        yield 'data: ' + dumps(self.to_JSON()) + '\n\n'
        self.lock.notify()
        self.lock.release()

    def room_JSON(self, player):
        ret = {}
        ret["gameID"] = self.game_id
        if player == 1:
            ret["playerID"] = self.player1_id
        else:
            ret["playerID"] = self.player2_id
        ret["roomCode"] = self.room_code

        return ret

    def to_JSON(self):
        json = {}
        json["gameStarted"] = self.started
        if not self.started: # if game has not started, return
            return json
        json["gameID"] = self.game_id
        json["invalidMove"] = self.invalid_move
        json["playerTurn"] = self.turn
        json["board"] = self.board.to_JSON()
        json["possibleMoves"] = self.board.possible_moves_JSON()
        json["deadPieces"] = self.board.dead_pieces_JSON()
        json["winner"] = self.winner if self.game_over else 0

        return json

    # Returns a random 8 uppercase letter sequence thats not already in use
    def create_player_id(self, length=8):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        seq = ""
        for i in range(length):
            seq += (choice(letters))
        while seq in self.player_ids:
            seq = ""
            for i in range(length):
                seq += (choice(letters))
        self.player_ids.append(seq)
        return seq
