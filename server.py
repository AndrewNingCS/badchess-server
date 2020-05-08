import os
import cherrypy
import cherrypy_cors
import time

from game import Game

class Server():
    def __init__(self):
        self.games = {
            "test": Game(0)
        }
        self.game_by_room_code = {}

    @cherrypy.expose
    def index(self):
        return { "data": "Server is up and running" }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def create_two_player_game(self):
        gid = int(time.time())
        self.games[gid] = Game(gid)

        # return a json object with
        # - game ID
        # - player 1 ID
        # - room code

        # store the game by room code so that player 2 can join later
        ret = self.games[gid].create_two_player_game()
        self.game_by_room_code[ret["room_code"]] = self.games[gid]

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
    @cherrypy.tools.json_out()
    def create_single_player_game(self):
        # create unique game ID (maybe based off time?)
        gid = int(time.time())
        self.games[gid] = Game(gid)

        return self.games[gid].to_JSON()

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
            self.games[gid].single_player_move(move_from, move_to)
            
            ret = self.games[gid].to_JSON()
            time.sleep(10)
            return ret


    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def game_exists(self):
        data = cherrypy.request.json
        if data["game_id"] in self.games:
            data["game_exists"] = "True"
        else:
            data["game_exists"] = "False"
        return data


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
