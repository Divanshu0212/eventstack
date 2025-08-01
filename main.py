
import os
import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.log
from handlers.auth import LoginHandler, GitHubAuthHandler, LogoutHandler
from handlers.events import (
    DashboardHandler, EventCreateHandler, EventViewHandler,
    EventVoteHandler, EventEditHandler
)
from handlers.info import AboutHandler, PrivacyHandler, SupportHandler, ContactHandler
from handlers.websocket import VoteWebSocketHandler
from models.db import init_db

def make_app():
    settings = {
        "cookie_secret": os.environ.get("COOKIE_SECRET", "super-secret-key"),
        "login_url": "/login",
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "xsrf_cookies": True,
        "debug": True,
    }

    return tornado.web.Application([
        (r"/", LoginHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/auth/github", GitHubAuthHandler),
        (r"/dashboard", DashboardHandler),
        (r"/create", EventCreateHandler),
        (r"/event/([a-zA-Z0-9\-]+)", EventViewHandler),
        (r"/vote", EventVoteHandler),
        (r"/event/([a-zA-Z0-9\-]+)/edit", EventEditHandler),

        # Informational Pages
        (r"/about", AboutHandler),
        (r"/privacy", PrivacyHandler),
        (r"/support", SupportHandler),

        # Contact Page
        (r"/contact", ContactHandler),

        # WebSocket route
        (r"/ws/vote/([a-zA-Z0-9\-]+)", VoteWebSocketHandler),
    ], **settings)

if __name__ == "__main__":
    # Initialize the database
    init_db()
    
    port = int(os.environ.get("PORT", 8888))
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(port)
    print(f"Server running at http://localhost:{port}")
    tornado.ioloop.IOLoop.current().start()
