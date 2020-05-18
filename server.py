import os
import cherrypy
import cherrypy_cors
import time
import random
import json

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
            cherrypy.session.acquire_lock()

            # find game with that ID
            data = cherrypy.request.json
            room_code = data["roomCode"]

            # does this room code exist?
            if room_code not in self.game_by_room_code:
                return {
                    "gameExists": False
                }

            # room code exists, return the game ID and player2 ID
            game = self.game_by_room_code[room_code]
            self.save_session_data(game.game_id, game.player2_id)

            cherrypy.session.release_lock()
            return game.join_two_player_game()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def has_player_joined(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            cherrypy.session.acquire_lock()

            # WAIT JSON object
            data = cherrypy.request.json
            gid = data["gameID"]
            pid = data["playerID"]

            # save game and player ID in the current session
            self.save_session_data(gid, pid)

            # returns a JOINED JSON object
            ret = self.game_by_game_id[gid].has_player_joined(pid)

            cherrypy.session.release_lock()
            return ret

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def has_game_started(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            cherrypy.session.acquire_lock()

            # WAIT JSON object
            data = cherrypy.request.json
            gid = data["gameID"]
            pid = data["playerID"]

            # save game and player ID in the current session
            self.save_session_data(gid, pid)

            # returns a GAME STATE JSON object
            ret = self.game_by_game_id[gid].has_game_started(pid)

            cherrypy.session.release_lock()
            return ret

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def start_two_player_game(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            cherrypy.session.acquire_lock()

            # WAIT JSON object
            data = cherrypy.request.json
            gid = data["gameID"]
            pid = data["playerID"]

            # save game and player ID in the current session
            self.save_session_data(gid, pid)

            # returns a GAME STATE JSON object
            self.game_by_game_id[gid].start_two_player_game(pid)
            ret = self.game_by_game_id[gid].to_JSON()

            cherrypy.session.release_lock()
            return ret

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def leave_two_player_game(self):
        log("LEAVE GAME CALLED")
        if cherrypy.request.method == 'OPTIONS':
            log("LEAVE GAME OPTIONS REQUEST RECEIVED")
            cherrypy_cors.preflight(allowed_methods=['POST'])
        elif cherrypy.request.method == 'POST':
            cherrypy.session.acquire_lock()

            log("LEAVE GAME POST REQUEST RECEIVED")
            # WAIT JSON object
            data = cherrypy.request.json
            gid = data["gameID"]
            player_id = data["playerID"]

            # if no player is left, remove from memory
            pnum = self.game_by_game_id[gid].get_player_number_from_id(player_id)
            log(f"Disconnecting Player: {pnum} PID: {player_id} from GID: {gid}")
            self.game_by_game_id[gid].disconnect(player_id)
            if not self.game_by_game_id[gid].any_connected():
                log("No players connected, removing game from server.")
                room_code = self.game_by_game_id[gid].room_code
                game = self.game_by_game_id.pop(gid)
                self.game_by_room_code.pop(room_code)
                game.stop()

            cherrypy.session.release_lock()
        else:
            log(f"LEAVE GAME {cherrypy.request.method} REQUEST RECEIVED")

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def make_move(self):
        # makes a move. returns new board state
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            cherrypy.session.acquire_lock()

            data = cherrypy.request.json
            gid = data["gameID"]
            pid = data["playerID"]
            move_from = data["moveFrom"]
            move_to = data["moveTo"]

            self.save_session_data(gid, pid)

            # TODO: check if game exists
            self.game_by_game_id[gid].make_move(pid, move_from, move_to)

            ret = self.game_by_game_id[gid].to_JSON()

            cherrypy.session.release_lock()
            return ret

    @cherrypy.expose
    def wait_for_move(self):
        cherrypy.session.acquire_lock()

        cherrypy.response.headers['Content-Type'] = 'text/event-stream;charset=utf-8'
        cherrypy.response.headers['Cache-Control'] = 'no-cache'

        # get data saved in session
        gid = cherrypy.session.get("gameID")
        pid = cherrypy.session.get("playerID")
        game = self.game_by_game_id[gid]
        pnum = game.get_player_number_from_id(pid)
        log(f"Player {pnum} waiting for move. GID: {gid}, PID: {pid}, SID: {cherrypy.session.id}")

        def SSE():
            cherrypy.session.acquire_lock()
            game.lock.acquire()
            while game.turn != pnum:
                yield 'data: ' + json.dumps(game.to_JSON()) + '\n\n'
                log(f"Thread from player: {pnum} sleeping. zzz")
                cherrypy.session.release_lock()
                game.lock.wait(timeout=25)
                cherrypy.session.acquire_lock()
                log(f"Thread from player: {pnum} woke up!")
                if game.stopped:
                    log(f"Game ended, stopping wait for move from player: {pnum}")
                    break
            yield 'data: ' + json.dumps(game.to_JSON()) + '\n\n'
            yield 'event: close\n'
            yield 'data: connection closed\n\n'
            game.lock.notify()
            game.lock.release()
            cherrypy.session.release_lock()

        cherrypy.session.release_lock()

        return SSE()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def get_two_player_game_data(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
            cherrypy.session.acquire_lock()

            # WAIT JSON object
            data = cherrypy.request.json
            gid = data["gameID"]
            pid = data["playerID"]

            # save game and player ID in the current session
            game = self.game_by_game_id[gid]
            self.save_session_data(gid, pid)

            # returns a GAME STATE JSON object
            ret = game.to_JSON()

            cherrypy.session.release_lock()
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
    def leave_single_player_game(self):
        if cherrypy.request.method == 'OPTIONS':
            cherrypy_cors.preflight(allowed_methods=['POST'])
        if cherrypy.request.method == 'POST':
        # json input should have game_id
            data = cherrypy.request.json
            gid = data["gameID"]

            if gid in self.game_by_game_id:
                log(f"Leaving single player game with GID: {gid} from server.")
                self.game_by_game_id.pop(gid)
            else:
                log(f"ERROR: GID: {gid} not found when trying to leave single player game.")

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

    def save_session_data(self, gid, pid):
        pnum = self.game_by_game_id[gid].get_player_number_from_id(pid)
        log(f"Saving IDs for player {pnum} with sid: {cherrypy.session.id}")
        cherrypy.session["gameID"] = gid
        cherrypy.session["playerID"] = pid

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
        "tools.sessions.on": True,
        "tools.sessions.locking": "explicit",
        "tools.response_headers.on": True,
        "tools.response_headers.headers": [
            ("Access-Control-Allow-Origin", "http://localhost:3000,https://badgames-xyz.github.io/badchess"),
            ("Access-Control-Allow-Credentials", "true"),
        ],
    })
    print("Starting Bad Chess Server...")
    cherrypy.quickstart(server)
