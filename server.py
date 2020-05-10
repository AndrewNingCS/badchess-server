import os
import cherrypy
import cherrypy_cors
import time
import random

from game import Game
from log import log

class Server():
    def __init__(self):
        test_game = Game(0, "TEST")
        self.game_by_game_id = {
            "test": test_game
        }
        self.game_by_room_code = {
            "TEST": test_game
        }

    @cherrypy.expose
    def index(self):
        return "Server is up and running"

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def create_two_player_game(self):
        gid = self.create_game_id()
        room_code = self.create_room_code()
        game = Game(gid, room_code)
        self.game_by_game_id[gid] = game
        self.game_by_room_code[room_code] = game

        # return a json object with
        # - game ID
        # - player 1 ID
        # - room code

        # store the game by room code so that player 2 can join later
        ret = self.game_by_game_id[gid].create_two_player_game()

        return ret

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def join_two_player_game(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            # find game with that ID
            data = cherrypy.request.json
            room_code = data["roomCode"]

            # does this room code exist?
            if room_code not in self.game_by_room_code:
                return {
                    "gameExists": False
                }

            #

            # room code exists, return the game ID and player2 ID
            game = self.game_by_room_code[room_code]
            return game.join_two_player_game()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def has_player_joined(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            # WAIT JSON object
            data = cherrypy.request.json
            gid = data["gameID"]
            player_id = data["playerID"]

            # returns a JOINED JSON object
            ret = self.game_by_game_id[gid].has_player_joined(player_id)
            return ret

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def has_game_started(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            # WAIT JSON object
            data = cherrypy.request.json
            gid = data["gameID"]
            player_id = data["playerID"]

            # returns a GAME STATE JSON object
            ret = self.game_by_game_id[gid].to_JSON()
            return ret

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start_two_player_game(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            # WAIT JSON object
            data = cherrypy.request.json
            gid = data["gameID"]
            player_id = data["playerID"]

            # returns a GAME STATE JSON object
            self.game_by_game_id[gid].start_two_player_game(player_id)
            ret = self.game_by_game_id[gid].to_JSON()
            return ret

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def leave_two_player_game(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            # WAIT JSON object
            data = cherrypy.request.json
            gid = data["gameID"]
            player_id = data["playerID"]

            # if no player is left, remove from memory
            self.game_by_game_id[gid].disconnect(player_id)
            if not self.game_by_game_id[gid].any_connected():
                room_code = self.game_by_game_id[gid].room_code
                self.game_by_game_id.pop(gid)
                self.game_by_room_code.pop(room_code)

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def make_move(self):
        # makes a move. returns new board state
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            data = cherrypy.request.json
            gid = data["gameID"]
            player_id = data["playerID"]
            move_from = data["moveFrom"]
            move_to = data["moveTo"]

            # TODO: check if game exists
            self.game_by_game_id[gid].make_move(player_id, move_from, move_to)

            ret = self.game_by_game_id[gid].to_JSON()
            return ret

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def wait_for_move(self):
        # waits for other player to make a move. blocks until a move is made
        # returns new board state
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            data = cherrypy.request.json
            gid = data["gameID"]
            player_id = data["playerID"]

            # TODO: check if game exists
            self.game_by_game_id[gid].wait_for_move(player_id) # this should block for at most 2 mins

            ret = self.game_by_game_id[gid].to_JSON()
            return ret

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def create_single_player_game(self):
        # create unique game ID (maybe based off time?)
        gid = self.create_game_id()
        room_code = self.create_room_code()
        game = Game(gid, room_code)
        self.game_by_game_id[gid] = game
        self.game_by_room_code[room_code] = game

        game.start_single_player_game()

        return self.game_by_game_id[gid].to_JSON()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def single_player_move(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
        # json input should have game_id, move_from, and move_to fields
            data = cherrypy.request.json
            gid = data["gameID"]
            move_from = data["moveFrom"]
            move_to = data["moveTo"]
            self.game_by_game_id[gid].single_player_move(move_from, move_to)
            
            ret = self.game_by_game_id[gid].to_JSON()
            return ret


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def game_exists(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            data = cherrypy.request.json
            if data["gameID"] in self.game_by_game_id:
                data["gameExists"] = "True"
            else:
                data["gameExists"] = "False"
            return data

    @cherrypy.expose
    def stream(self):
        cherrypy.response.headers['Content-Type'] = 'text/event-stream'

        # def streamer():
        for i in range(3):
            time.sleep(1)
            yield 'data:hello\n'

        time.sleep(1)
        yield 'data:done!\n\n'

        # return streamer()
        

    # Returns a unique int to use as a game_id
    def create_game_id(self):
        gid = int(time.time())
        return gid

    # Returns a random 4 uppercase letter sequence thats not already in use
    def create_room_code(self):
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        seq = ""
        for i in range(4):
            seq += (random.choice(letters))
        while seq in self.game_by_room_code:
            seq = ""
            for i in range(4):
                seq += (random.choice(letters))
        return seq


if __name__ == "__main__":
    cherrypy_cors.install()
    server = Server()
    cherrypy.config.update({
        "server.socket_host": "0.0.0.0",
        "server.socket_port": int(os.environ.get("PORT", "8080")),
        "cors.expose.on": True,
        "response.stream": True,
    })
    print("Starting Bad Chess Server...")
    cherrypy.quickstart(server)
