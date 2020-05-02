import os
import cherrypy
import cherrypy_cors
import time

class Server():
    def __init__(self):
        self.games = {}

    @cherrypy.expose
    def index(self):
        return { "data": "Server is up and running" }

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def create_single_player_game(self):
        # create unique game ID (maybe based off time?)
        gid = int(time.time())

        # send back game state data with game ID
        game_state = {
            "game_id": gid,
            "board": [
                [["R", False], ["H", False], ["B", False], ["K", False], ["Q", False], ["B", False], ["H", False], ["R", False]],
                [["P", False], ["P", False], ["P", False], ["P", False], ["P", False], ["P", False], ["P", False], ["P", False]],
                [["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True]],
                [["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True]],
                [["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True]],
                [["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True], ["N", True]],
                [["P", True], ["P", True], ["P", True], ["P", True], ["P", True], ["P", True], ["P", True], ["P", True]],
                [["R", True], ["H", True], ["B", True], ["K", True], ["Q", True], ["B", True], ["H", True], ["R", True]]
            ]
        }

        return game_state

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
