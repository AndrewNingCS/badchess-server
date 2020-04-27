import os
import cherrypy

class Server():
    @cherrypy.expose
    def index(self):
        return "Server is up and running"

if __name__ == "__main__":
    server = Server()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Bad Chess Server...")
    cherrypy.quickstart(server)
