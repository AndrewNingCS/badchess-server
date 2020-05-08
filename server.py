import os
import cherrypy
import cherrypy_cors
import time
import random

from game import Game

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
        return { "data": "Server is up and running" }

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
            room_code = data["room_code"]

            # does this room code exist?
            if room_code not in self.game_by_room_code:
                return {
                    "game_exists": False
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
            gid = data["game_id"]
            player_id = data["player_id"]

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
            gid = data["game_id"]
            player_id = data["player_id"]

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
            gid = data["game_id"]
            player_id = data["player_id"]

            # returns a GAME STATE JSON object
            self.game_by_game_id[gid].start_two_player_game(player_id)
            ret = self.game_by_game_id[gid].to_JSON()
            return ret

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def make_move(self):
        # makes a move. returns new board state
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            data = cherrypy.request.json
            gid = data["game_id"]
            player_id = data["player_id"]
            move_from = data["move_from"]
            move_to = data["move_to"]

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
            gid = data["game_id"]
            player_id = data["player_id"]

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
            gid = data["game_id"]
            move_from = data["move_from"]
            move_to = data["move_to"]
            self.game_by_game_id[gid].single_player_move(move_from, move_to)
            
            ret = self.game_by_game_id[gid].to_JSON()
            time.sleep(10)
            return ret


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def game_exists(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            data = cherrypy.request.json
            if data["game_id"] in self.game_by_game_id:
                data["game_exists"] = "True"
            else:
                data["game_exists"] = "False"
            return data

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
    })
    print("Starting Bad Chess Server...")
    cherrypy.quickstart(server)
